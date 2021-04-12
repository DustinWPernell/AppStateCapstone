import logging
import operator
import datetime
from functools import reduce

import boto3
import requests
from decouple import config
from django.core import serializers

from django.db import models
from django.db.models import Q

logger = logging.getLogger("logger")
# Create your models here.
#region Cards
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
    card_url = models.CharField(max_length=200)
    card_url.null = True

    @staticmethod
    def get_cards():
        return CardIDList.objects.all().order_by('card_name')

    @staticmethod
    def get_card_face():
        card_id_list_full = CardIDList.get_cards()
        full_card_list_all = []

        for card_list_obj in card_id_list_full:
            full_card_list_all.append(card_list_obj.card_id)

        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=full_card_list_all)
        ).order_by('name')

    @staticmethod
    def get_card_by_oracle(oracle_id):
        return CardIDList.objects.get(oracle_id=oracle_id)
        # .get(oracle_id=oracle_id)

    @staticmethod
    def convert_to(obj_list):
        return serializers.serialize('xml', obj_list)

    @staticmethod
    def get_json(limit):
        if (limit):
            return QuickResult.get_oracles(limit)
        else:
            return QuickResult.run_oracles(limit)


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
    released_at = models.DateField()
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

    def __str__(self):
        return '{"oracle_id": "' + str(self.legal.card_obj.oracle_id) + '", "card_name": "' + str(self.name).replace('"', '&#34;').replace('\'', '&#39;') + \
               '", "card_url": "' + str(self.image_url) + '", "card_id": "' + str(self.legal.card_obj.card_id) + '"}'

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
        return CardFace.objects.filter(
            Q(legal__card_obj__card_id=card_id)
        ).order_by('name')

    @staticmethod
    def card_face_filter_by_card_color_term_colorless(card_ids, mana_color, term):
        list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                          '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                          '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                          '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                          '{G}', '{2/G}', '{G/P}', '{HG}']
        filtered_card_list =  CardFace.objects.select_related().filter(
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

        card_json_list = ""
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1:
                card_json_list = card_json_list + '}, '
        return card_json_list.__str__()

    @staticmethod
    def card_face_filter_by_card_term(card_ids, mana_color, term):
        list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                          '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                          '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                          '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                          '{G}', '{2/G}', '{G/P}', '{HG}',
                          '{C}', '', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                          '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                          '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}']
        keywords = ["living weapon","jump-start","basic landcycling","commander ninjutsu","legendary landwalk",
                    "nonbasic landwalk","totem armor","megamorph","haunt","forecast","graft","fortify","frenzy",
                    "gravestorm","hideaway","level Up","infect","protection","reach","rampage","phasing","multikicker",
                    "morph","provoke","modular","offering","ninjutsu","replicate","recover","poisonous","prowl","reinforce",
                    "persist","retrace","rebound","miracle","overload","outlast","prowess","renown","myriad","shroud",
                    "trample","vigilance","shadow","storm","soulshift","splice","transmute","ripple","suspend","vanishing",
                    "transfigure","wither","unearth","undying","soulbond","unleash","ascend","assist","afterlife",
                    "companion","fabricate","embalm","escape","fuse","menace","ingest","melee","improvise","mentor",
                    "partner","mutate","scavenge","tribute","surge","skulk","undaunted","riot","spectacle","forestwalk",
                    "islandwalk","mountainwalk","double strike","cumulative upkeep","first strike","encore","sunburst",
                    "deathtouch","defender","foretell","amplify","affinity","bushido","convoke","bloodthirst","absorb",
                    "aura swap","changeling","conspire","cascade","annihilator","battle Cry","cipher","bestow","dash","awaken",
                    "crew","aftermath","afflict","equip","flanking","echo","fading","fear","eternalize","entwine","epic","dredge",
                    "delve","evoke","exalted","evolve","extort","dethrone","exploit","devoid","emerge","escalate","flying",
                    "haste","hexproof","indestructible","intimidate","lifelink","horsemanship","kicker","madness","hidden agenda",
                    "swampwalk","desertwalk","wizardcycling","slivercycling","cycling","landwalk","plainswalk","champion","enchant",
                    "plainscycling","islandcycling","swampcycling","mountaincycling","forestcycling","landcycling","yypecycling",
                    "split second","flash","flashback","banding","augment","double agenda","partner with","hexproof from",
                    "boast","devour","buyback","ward","meld","bolster","clash","fateseal","investigate","manifest","monstrosity",
                    "populate","proliferate","scry","support","detain","explore","fight","amass","adapt","assemble","abandon",
                    "activate","attach","exert","cast","counter","create","destroy","discard","double","exchange","exile",
                    "play","regenerate","reveal","sacrifice","set in motion","shuffle","tap","untap","vote","transform","surveil",
                    "goad","planeswalk","mill","learn"
                    ]
        if mana_color == list_of_colors and term.lower() in keywords:
            return QuickResult.get_keyword(card_ids, term.lower())
        elif len(mana_color) > 0 and term == "":
            return QuickResult.get_color(card_ids, mana_color)
        else:
            filtered_card_list = CardFace.objects.select_related().filter(
                Q(legal__card_obj__card_id__in=card_ids) &
                Q(card_search__icontains=term) &
                reduce(
                    operator.or_, (
                        Q(mana_cost__contains=item) for item in mana_color
                    )
                )
            ).order_by('name')

            card_json_list = ""
            for card in filtered_card_list:
                card_json_list = card_json_list + card.__str__()
                if len(filtered_card_list) > 1:
                    card_json_list = card_json_list + '}, '

            return card_json_list.__str__()

    @staticmethod
    def card_face_commander_filter_by_card_term(card_ids, mana_color, term):
        filtered_card_list = CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=card_ids) &
            Q(card_search__icontains=term) &
            Q(type_line__icontains="legendary") & (
                Q(type_line__icontains="creature") | (
                    Q(type_line__icontains="planeswalker") &
                    Q(text__icontains="can be your commander")
                )
            ) &
            reduce(
                operator.or_, (
                    Q(mana_cost__contains=item) for item in mana_color
                )
            )
        ).order_by('name')

        card_json_list = ""
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1:
                card_json_list = card_json_list + '}, '
        return card_json_list.__str__()

    @staticmethod
    def card_face_filter_by_name_term(term):
        filtered_card_list = CardFace.objects.select_related().filter(
            Q(name__icontains=term)
        ).order_by('name')

        card_json_list = ""
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1:
                card_json_list = card_json_list + '}, '
        return card_json_list.__str__()

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
                         'card_image_one': card_set_obj.image_url,
                         'card_image_two': card_set_obj.legal.face_legal.all()[1].image_url})
                else:
                    set_info.append(
                        {'set_name': card_set_obj.legal.card_obj.set_obj.name,
                         'set_image': card_set_obj.legal.card_obj.set_obj.icon_svg_uri,
                         'card_image_one': card_set_obj.image_url,
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

class QuickResult(models.Model):
    search = models.CharField(max_length=500)
    last_update = models.DateField(default=datetime.datetime.now())
    result = models.TextField(default='{}')

    def __str__(self):
        return self.search

    @staticmethod
    def get_oracles(limit):
        date = datetime.datetime.now() - datetime.timedelta(days=7)
        obj = QuickResult.objects.get(search='oracles')
        if obj.last_update < date.date():
            QuickResult.run_oracles(limit)
            obj = QuickResult.objects.get(search='oracles')
        return obj.result

    @staticmethod
    def run_oracles(limit):
        if limit:
            card_id_list_full = CardIDList.get_cards()[0:5000]
        else:
            card_id_list_full = CardIDList.get_cards()

        full_card_list_all = []
        for card_list_obj in card_id_list_full:
            full_card_list_all.append(card_list_obj.card_id)

        filtered_card_list = CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=full_card_list_all)
        ).order_by('name')

        card_json_list = ""
        i = 0
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1 and i + 1 < len(filtered_card_list):
                card_json_list = card_json_list + '}, '
                i += 1

        if limit:
            obj, created = QuickResult.objects.get_or_create(
                search='oracles',
            )
            obj.last_update = datetime.datetime.now()
            obj.result = card_json_list.__str__()
            obj.save()
        else:
            return card_json_list

    @staticmethod
    def get_keyword(card_ids, keyword):
        try:
            date = datetime.datetime.now() - datetime.timedelta(days=7)
            obj = QuickResult.objects.get(search=keyword)
            if obj.last_update < date.date():
                QuickResult.run_keyword(card_ids, keyword)
                obj = QuickResult.objects.get(search=keyword)
        except QuickResult.DoesNotExist:
            QuickResult.run_keyword(card_ids, keyword)
            obj = QuickResult.objects.get(search=keyword)
        return obj.result

    @staticmethod
    def run_keyword(card_ids, keyword):
        filtered_card_list = CardFace.objects.select_related().filter(
                Q(legal__card_obj__card_id__in=card_ids) &
                Q(card_search__icontains=keyword)
            ).order_by('name')

        card_json_list = ""
        i = 0
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1 and i + 1 < len(filtered_card_list):
                card_json_list = card_json_list + '}, '
                i += 1

        obj, created = QuickResult.objects.get_or_create(
            search=keyword,
        )
        obj.last_update = datetime.datetime.now()
        obj.result = card_json_list.__str__()
        obj.save()

    @staticmethod
    def get_color(card_ids, color):
        color_term = ""

        for col in color:
            color_term = color_term + col

        try:
            date = datetime.datetime.now() - datetime.timedelta(days=7)
            obj = QuickResult.objects.get(search=color_term)
            if obj.last_update < date.date():
                QuickResult.run_color(card_ids, color, color_term)
                obj = QuickResult.objects.get(search=color_term)
        except QuickResult.DoesNotExist:
            QuickResult.run_color(card_ids, color, color_term)
            obj = QuickResult.objects.get(search=color_term)
        return obj.result

    @staticmethod
    def run_color(card_ids, color, color_term):
        filtered_card_list = CardFace.objects.select_related().filter(
                Q(legal__card_obj__card_id__in=card_ids) &
                reduce(
                    operator.or_, (
                        Q(mana_cost__icontains=item) for item in color
                    )
                )
            ).order_by('name')

        card_json_list = ""
        i = 0
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1 and i + 1 < len(filtered_card_list):
                card_json_list = card_json_list + '}, '
                i += 1

        obj, created = QuickResult.objects.get_or_create(
            search=color_term,
        )
        obj.last_update = datetime.datetime.now()
        obj.result = card_json_list.__str__()
        obj.save()
