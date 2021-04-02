import operator
from datetime import datetime
from functools import reduce

import boto3
import requests
from decouple import config
from django.contrib.auth.models import User

from django.db import models
from django.db.models import Q


# Create your models here.


class IgnoreCards(models.Model):
    """
        Stores cards that should be ignored during import
            * type - Type of field that should be searched (name/set)
            * value - Value that should be looked for
    """
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value


#region Cards

class CardIDList(models.Model):
    """
        Stores Unique card named objects
            * card_id - ID for the card (specific to printing)
            * name - Name of the card
    """
    card_id = models.CharField(max_length=200)
    oracle_id = models.CharField(max_length=200)
    card_name = models.CharField(max_length=200)
    card_name.null = True

    @staticmethod
    def get_card_ids():
        return CardIDList.objects.all()

    @staticmethod
    def get_card_by_oracle(oracle_id):
        return CardIDList.objects.get(oracle_id=oracle_id)
        # .get(oracle_id=oracle_id)


class CardLayout(models.Model):
    """
        Stores different kinds of layouts for card
            * layout - Type of layout
            * sides - number of sides a layout has
            * multiFace - number of faces a layout has
    """
    layout = models.CharField(max_length=30)
    sides = models.IntegerField()
    multi_face = models.IntegerField()

    def __int__(self):
        return self.id


class CardSets(models.Model):
    """
        Stores rule objects
            * set_id - ID for the set
            * code - Short string to identify set
            * name - Full name of set
            * released_at - Data the set was released
            * icon_svg_uri - Set icon
            * order - Order in which the set will appear (newest first)
    """
    set_id = models.CharField(max_length=200, primary_key=True)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    released_at = models.DateField(default=datetime.now)
    icon_svg_uri = models.CharField(max_length=200)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Card(models.Model):
    """
        Stores a card object
            * card_id - ID for the card (specific to printing)
            * oracleID - ID for the card (specific to name)
            * keywords - Keywords that appear on all faces of the card
            * rarity - How rare the card is
            * setName - Set of the card
            * layout - Layout of the card
            * setOrder - Order in which set occurs
            * color - Stores color identity of card
    """
    card_id = models.CharField(max_length=200)
    oracle_id = models.CharField(max_length=200)
    keywords = models.CharField(max_length=500)
    rarity = models.CharField(max_length=20)
    set_name = models.CharField(max_length=100)
    layout = models.ForeignKey(CardLayout, on_delete=models.DO_NOTHING, related_name='card_layout')
    color = models.CharField(max_length=30)
    set_obj = models.ForeignKey(CardSets, on_delete=models.DO_NOTHING, related_name='card_set')

    def __str__(self):
        return self.card_id


class Legality(models.Model):
    """
        Stores legality for specific card
            * standard - Game type standard
            * future - Game type future
            * historic - Game type historic
            * gladiator - Game type gladiator
            * modern - Game type modern
            * legacy - Game type legacy
            * pauper - Game type pauper
            * vintage - Game type vintage
            * penny - Game type penny
            * commander - Game type commander
            * brawl - Game type brawl
            * duel - Game type duel
            * oldSchool - Game type oldSchool
            * premodern - Game type premodern
            * card_id - ID for the card (specific to printing)
    """
    standard = models.CharField(max_length=30)
    future = models.CharField(max_length=30)
    historic = models.CharField(max_length=30)
    gladiator = models.CharField(max_length=30)
    modern = models.CharField(max_length=30)
    legacy = models.CharField(max_length=30)
    pauper = models.CharField(max_length=30)
    vintage = models.CharField(max_length=30)
    penny = models.CharField(max_length=30)
    commander = models.CharField(max_length=30)
    brawl = models.CharField(max_length=30)
    duel = models.CharField(max_length=30)
    old_school = models.CharField(max_length=30)
    premodern = models.CharField(max_length=30)
    card_obj = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='legal_card')

    def __int__(self):
        return self.id


class CardFace(models.Model):
    """
        Stores card face object (could be many for one card object)
            * name - Name of the card face
            * image_url - URL for the card face image
            * mana_cost - Mana cost for the card face
            * loyalty - Starting loyalty for the card (may be empty)
            * power - Base power for the card (may be empty)
            * toughness - Base toughness for the card (may be empty)
            * type_line - The type line for the card (Creature/Enchantment/...)
            * color_id - The color id of the card
            * text - The text displayed in the main area of the card
            * flavor_text - The fun text normally display at the bottom of the card (may be empty)
            * card_id - ID for the card (specific to printing)
            * avatar_img - Image URL for profile avatars
            * set_order - Order in which set occurs
            * firstFace - Boolean used in displaying cards with multiple faces
    """
    name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    image_file = models.CharField(max_length=200)
    image_file.null = True
    mana_cost = models.CharField(max_length=100)
    loyalty = models.CharField(max_length=10)
    power = models.CharField(max_length=10)
    toughness = models.CharField(max_length=10)
    type_line = models.CharField(max_length=500)
    color_id = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    flavor_text = models.CharField(max_length=500)
    avatar_img = models.CharField(max_length=200)
    avatar_file = models.CharField(max_length=200)
    avatar_file.null = True
    first_face = models.BooleanField()
    legal = models.ForeignKey(Legality, on_delete=models.CASCADE, related_name='face_legal')
    card_search = models.CharField(max_length=2000)

    def __int__(self):
        return self.id

    def get_remote_image(self):
        session = boto3.Session(
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        )
        s3 = session.client('s3')

        if self.image_url and not self.image_file:
            filename = "cards/image_%s" % self.legal.card_obj.card_id + '.png'
            image_data = requests.get(self.image_url, stream=True)
            try:
                s3.upload_fileobj(image_data.raw, config('AWS_STORAGE_BUCKET_NAME'), filename)
                self.image_file = filename
                self.save()
            except Exception as e:
                return e

        return config('AWS_S3_CUSTOM_DOMAIN') + '/' + self.image_file

    def get_remote_avatar(self):
        session = boto3.Session(
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        )
        s3 = session.client('s3')

        if self.avatar_img and not self.avatar_file:
            filename = "cards/avatar_%s" % self.legal.card_obj.card_id + '.png'
            image_data = requests.get(self.avatar_img, stream=True)
            try:
                s3.upload_fileobj(image_data.raw, config('AWS_STORAGE_BUCKET_NAME'), filename)
                self.avatar_file = filename
                self.save()
            except Exception as e:
                return e

        return config('AWS_S3_CUSTOM_DOMAIN') + '/' + self.avatar_file

    @staticmethod
    def get_face_by_card(card_id):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id=card_id)
        ).order_by('name')

    @staticmethod
    def get_face_list_by_card(card_id_list):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_id_list)
        ).order_by('name')

    @staticmethod
    def card_face_by_card_and_oracle(card_id, oracle_id):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_id) &
            Q(legal__card_obj__oracle_id__in=oracle_id)
        ).order_by('name')

    @staticmethod
    def card_face_by_card(card_id):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_id)
        ).order_by('name')

    @staticmethod
    def card_face_filter_by_card_oracle_term(card_id, oracle_id, term):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_id) &
            Q(legal__card_obj__oracle_id__in=oracle_id) &
            Q(card_search__icontains=term)
        ).order_by('name')

    @staticmethod
    def card_face_filter_by_card_oracle_term_notes(card_id, oracle_id, notes_terms, term):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_id) &
            Q(legal__card_obj__oracle_id__in=oracle_id) & (
                    Q(card_search__icontains=term) |
                    Q(legal__card_obj__oracle_id__in=notes_terms)
            )
        ).order_by('name')

    @staticmethod
    def card_face_filter_by_card_color_term_colorless(card_ids, mana_color, term):
        list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                          '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                          '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                          '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                          '{G}', '{2/G}', '{G/P}', '{HG}']
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_ids) & (
                    reduce(
                        operator.or_, (
                            Q(mana_cost__contains=item) for item in mana_color
                        )
                    ) &
                    reduce(
                        operator.and_, (
                            ~Q(mana_cost__contains=item) for item in list_of_colors
                        )
                    )
            ) &
            Q(card_search__icontains=term)
        ).order_by('name')

    @staticmethod
    def card_face_filter_by_card_color_term(card_ids, mana_color, term):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_ids) &
            reduce(
                operator.or_, (
                    Q(mana_cost__contains=item) for item in mana_color
                )
            ) &
            Q(card_searchs__icontains=term)
        ).order_by('name')

    @staticmethod
    def card_face_filter_by_card_term(card_ids, term):
        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_ids) &
            Q(card_search__icontains=term)
        ).order_by('name')

    @staticmethod
    def card_face_filter_by_name_term(term):
        return CardFace.objects.select_related().filter(
            Q(name__icontains=term)
        ).order_by('name')

    @staticmethod
    def get_card_sets(oracle_id):
        set_info = []
        face_list = CardFace.objects.select_related().filter(
            Q(legal__card_obj__oracle_id=oracle_id)
        ).order_by('legal__card_obj__set_obj__name')

        card_set_list = []
        for card_set_obj in face_list:

            if card_set_obj.legal.card_obj.set_obj.name not in card_set_list:
                card_set_list.append(card_set_obj.legal.card_obj.set_obj.name)
                if card_set_obj.legal.card_obj.layout.sides == 2:
                    set_info.append(
                        {'set_name': card_set_obj.legal.card_obj.set_obj.name,
                         'set_image': card_set_obj.legal.card_obj.set_obj.icon_svg_uri,
                         'card_image_one': card_set_obj.get_remote_image(),
                         'card_image_two': card_set_obj.legal.face_legal.all()[1].get_remote_image()})
                else:
                    set_info.append(
                        {'set_name': card_set_obj.legal.card_obj.set_obj.name,
                         'set_image': card_set_obj.legal.card_obj.set_obj.icon_svg_uri,
                         'card_image_one': card_set_obj.get_remote_image(),
                         'card_image_two': 'NONE'})

        return set_info


class Rule(models.Model):
    """
        Stores rule objects
            * oracleID - ID for the card (specific to name)
            * pub_date - Data the ruling was made
            * comment - The text about the ruling
    """
    oracle_id = models.CharField(max_length=200)
    pub_date = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.oracle_id

#endregion

#region Decks

class DeckType(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    min_deck_size = models.IntegerField(default=60)
    max_deck_size = models.IntegerField(default=0)  # 0 for none
    side_board_size = models.IntegerField(default=15)
    card_copy_limit = models.IntegerField(default=4)
    has_commander = models.BooleanField(default=False)

    @staticmethod
    def get_deck_type_by_type(type):
        return DeckType.objects.get(name__icontains=type)


class Deck(models.Model):
    name = models.CharField(max_length=200)
    color_id = models.CharField(max_length=20)
    created_by = models.CharField(max_length=50)
    created_by.null = True
    deck_user = models.CharField(max_length=50)
    created_by.null = True
    is_pre_con = models.BooleanField()
    is_private = models.BooleanField()
    image_url = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    deck_type = models.ForeignKey(DeckType, related_name='type_deck', on_delete=models.CASCADE)
    commander_oracle = models.CharField(max_length=200)
    commander_id = models.CharField(max_length=200)
    commander_name = models.CharField(max_length=200)
    commander_file = models.CharField(max_length=200)
    commander_id.null = True
    commander_name.null = True
    commander_file.null = True
    commander_oracle.null = True

    def get_created_by(self):
        return User.objects.get(id=self.created_by)

    @staticmethod
    def deck_filter_by_color_term_colorless(user, mana, term):
        # Retrieve all decks that are not private and colorId contains the selected colors,
        # or name contains the search term
        list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                          '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                          '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                          '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                          '{G}', '{2/G}', '{G/P}', '{HG}']
        return Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=user.id)
            ) &
            Q(name__icontains=term) & (
                    reduce(
                        operator.or_, (
                            Q(mana_cost__contains=item) for item in mana
                        )
                    ) &
                    reduce(
                        operator.and_, (
                            ~Q(mana_cost__contains=item) for item in list_of_colors
                        )
                    )
            )
        ).order_by('name')

    @staticmethod
    def deck_filter_by_color_term(user, mana, term):
        # Retrieve all decks that are not private and colorId contains the selected colors,
        # or name contains the search term
        return Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=user.id)
            ) &
            reduce(
                operator.or_, (
                    Q(mana_cost__contains=item) for item in mana
                )
            ) &
            Q(colorId__contains=mana) &
            Q(name__icontains=term)
        ).order_by('name')

    @staticmethod
    def deck_filter_by_term(user, term):
        # Retrieve all decks that are not private and colorId contains the selected colors,
        # or name contains the search term
        return Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=user.id)
            ) &
            Q(name__icontains=term)
        ).order_by('name')

    @staticmethod
    def get_deck_by_deck_list(deck_ids):
        return Deck.objects.select_related().filter(
            Q(id__in=deck_ids)
        ).order_by('name')

    @staticmethod
    def get_deck_by_deck(deck_id):
        return Deck.objects.select_related().get(
            Q(id__in=deck_id)
        )


class DeckCards(models.Model):
    deck = models.ForeignKey(Deck, related_name='deck_cards', on_delete=models.CASCADE)
    card_oracle = models.CharField(max_length=200)
    card_name = models.CharField(max_length=200)
    card_file = models.CharField(max_length=200)
    card_file.null = True
    card_search = models.CharField(max_length=2000)
    quantity = models.IntegerField(default=0)
    sideboard = models.BooleanField(default=False)

    @staticmethod
    def deck_card_by_deck_user(deck_id, user_id, side):
        return DeckCards.objects.select_related().filter(
            Q(deck__id=deck_id) & (
                    Q(deck__is_private=False) |
                    Q(deck__deck_user=user_id)
            ) &
            Q(sideboard=side)
        )

    @staticmethod
    def build_json_by_deck_user(deck_id, user_id, side):
        json_obj = []
        deck_cards = DeckCards.deck_card_by_deck_user(deck_id, user_id, side)
        for card in deck_cards:
            card_obj = {}
            card_obj["card_oracle"] = card.card_oracle
            card_obj["name"] = card.card_name
            card_obj["quantity"] = str(card.quantity)
            card_obj["card_file"] = card.card_file
            json_obj.append(card_obj)

        return json_obj

#endregion

class Symbol(models.Model):
    """
        Stores symbols
            * symbol - Symbol key example: {B}
            * text -
            * imageURL - URL for the symbol image
            * isMana - Boolean stating if the symbol is mana
            * manaCost - Mana cost for the symbol
            * colorID - Color id for the symbol
    """
    symbol = models.CharField(max_length=20)
    text = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)
    is_mana = models.CharField(max_length=20)
    mana_cost = models.CharField(max_length=20)
    mana_cost.null = True
    color_id = models.CharField(max_length=200)

    def __str__(self):
        return self.symbol

    @staticmethod
    def get_base_symbols():
        return Symbol.objects.filter(symbol__in=['{W}', '{U}', '{B}', '{R}', '{G}', '{C}', '{S}'])

    @staticmethod
    def get_colorless():
        return Symbol.objects.filter(
            symbol__in=['', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                        '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                        '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}'])

    @staticmethod
    def get_green():
        return Symbol.objects.filter(
            symbol__in=['{B/G}', '{R/G}', '{G/W}', '{G/U}', '{2/G}', '{G/P}', '{HG}'])

    @staticmethod
    def get_red():
        return Symbol.objects.filter(
            symbol__in=['{B/R}', '{U/R}', '{R/G}', '{R/W}', '{2/R}', '{R/P}', '{HR}'])

    @staticmethod
    def get_black():
        return Symbol.objects.filter(
            symbol__in=['{W/B}', '{B/R}', '{B/G}', '{U/B}', '{2/B}', '{B/P}', '{HB}'])

    @staticmethod
    def get_blue():
        return Symbol.objects.filter(
            symbol__in=['{W/U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}'])

    @staticmethod
    def get_white():
        return Symbol.objects.filter(
            symbol__in=['{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}'])



