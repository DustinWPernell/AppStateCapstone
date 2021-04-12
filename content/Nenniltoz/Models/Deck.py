import operator
from functools import reduce
from random import randint

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Count

from Users.models import UserProfile


class DeckManager(models.Manager):
    @staticmethod
    def get_types():
        type_list = DeckType.objects.all()
        type_json_list = ""
        i = 0
        for type_obj in type_list:
            type_json_list = type_json_list + type_obj.__str__()
            if len(type_list) > 1 and i + 1 < len(type_list):
                type_json_list = type_json_list + '}, '
                i += 1
        return type_json_list.__str__()

    @staticmethod
    def get_deck_type_by_type(type_id):
        return DeckType.objects.filter(id=type_id)

    @staticmethod
    def deck_filter_by_color_term_colorless(user, mana, term):
        count = DeckManager.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)

        list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                          '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                          '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                          '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                          '{G}', '{2/G}', '{G/P}', '{HG}']
        return Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=user)
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
        ).order_by('name')[random_index:random_index+500]

    @staticmethod
    def deck_filter_by_color_term(user, mana, term):
        # Retrieve all decks that are not private and colorId contains the selected colors,
        # or name contains the search term
        return Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=user)
            ) &
            reduce(
                operator.or_, (
                    Q(mana_cost__contains=item) for item in mana
                )
            ) &
            Q(colorId__contains=mana) & (
                    Q(name__icontains=term) |
                    Q(decsription__icontains='{' + term + '}')
            )
        ).order_by('name')

    @staticmethod
    def get_deck_by_user_term(user, term):
        # Retrieve all decks that are not private and colorId contains the selected colors,
        # or name contains the search term
        filtered_deck_list = Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=user)
            ) & (
                    Q(name__icontains=term) |
                    Q(description__icontains='{' + term + '}')
            )
        ).order_by('name')

        deck_json_list = ""
        for deck in filtered_deck_list:
            deck_json_list = deck_json_list + deck.__str__()
            if len(filtered_deck_list) > 1:
                deck_json_list = deck_json_list + '}, '

        return deck_json_list.__str__()

    @staticmethod
    def get_deck_by_deck_list(deck_ids):
        return Deck.objects.select_related().filter(
            Q(id__in=deck_ids)
        ).order_by('name')

    @staticmethod
    def get_deck_by_deck(deck_id):
        return Deck.objects.select_related().get(
            Q(id=deck_id)
        )

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
    def deck_card_by_deck(deck_id):
        return DeckCards.objects.filter(
            Q(deck__id=deck_id)
        )

    @staticmethod
    def build_json_by_deck_user(deck_id, user_id, side):
        json_obj = []
        deck_cards = DeckManager.deck_card_by_deck_user(deck_id, user_id, side)
        for card in deck_cards:
            card_obj = {}
            card_obj["card_oracle"] = card.card_oracle
            card_obj["name"] = card.card_name
            card_obj["quantity"] = str(card.quantity)
            card_obj["card_file"] = card.card_file
            json_obj.append(card_obj)

        return json_obj

    @staticmethod
    def deck_create(deck_name_field, deck_type_obj, deck_privacy_field, deck_description_field,
                    color_id, user_id, username):
        new_deck = Deck.objects.create(
            name=deck_name_field,
            deck_type=deck_type_obj,
            is_private=deck_privacy_field == 'True',
            description=deck_description_field,
            color_id=color_id,
            created_by=user_id,
            deck_user=user_id,
            is_pre_con=(username == "Preconstructed")
        )
        return new_deck.id


class DeckType(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    min_deck_size = models.IntegerField(default=60)
    max_deck_size = models.IntegerField(default=0)  # 0 for none
    side_board_size = models.IntegerField(default=15)
    card_copy_limit = models.IntegerField(default=4)
    has_commander = models.BooleanField(default=False)

    class Meta:
        app_label = "Management"

    def __str__(self):
        return '{"type_id": "' + str(self.id) + '", "type_name": "' + str(self.name) + '", "desc": "' + \
               str(self.desc) + '", "min_deck_size": "' + str(self.min_deck_size) + '", "max_deck_size": "' + \
               str(self.max_deck_size) + '", "side_board_size": "' + str(self.side_board_size) + \
               '", "card_copy_limit": "' + str(self.card_copy_limit) + '", "has_commander": "' + \
               str(self.has_commander) + '"}'


class Deck(models.Model):
    name = models.CharField(max_length=200)
    color_id = models.CharField(max_length=20)
    created_by = models.CharField(max_length=50)
    created_by.null = True
    deck_user = models.CharField(max_length=50)
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

    class Meta:
        app_label = "Management"

    def __str__(self):
        return '{"deck_id": "' + str(self.id) + '", "deck_name": "' + \
                str(self.name).replace('"', '&#34;').replace('\'', '&#39;') + '", "color_id": "' + \
                str(self.color_id) + '", "created_by": "' + str(self.created_by) + '", "deck_user": "' + \
                str(self.deck_user) + '", "is_pre_con": "' + str(self.is_pre_con) + '", "is_private": "' + \
                str(self.is_private) + '", "description": "' + str(self.description) + '", "deck_type": "' + \
                str(self.deck_type.__str__()) + '"}'

    def get_created_by(self):
        return User.objects.get(id=self.created_by)

    def get_deck_user_by(self):
        return User.objects.get(id=self.deck_user)

    def create_copy(self, user):
        # region Copy Deck
        new_deck = Deck.objects.create(
            name=self.name,
            deck_type=self.deck_type,
            is_private=UserProfile.get_deck_private(user),
            image_url=self.image_url,
            description=self.description,
            commander_id=self.commander_id,
            commander_name=self.commander_name,
            commander_file=self.commander_file,
            commander_oracle=self.commander_oracle,
            color_id=self.color_id,
            created_by=self.created_by,
            deck_user=user.id,
            is_pre_con=False
        )
        # endregion

        # region Copy Cards
        deck_cards = DeckManager.deck_card_by_deck(self.id)

        for card in deck_cards:
            DeckCards.objects.create(
                deck=new_deck,
                card_oracle=card.card_oracle,
                card_name=card.card_name,
                card_file=card.card_file,
                card_search=card.card_search,
                quantity=card.quantity,
                sideboard=card.sideboard,
            )
        # endregion
        return new_deck


class DeckCards(models.Model):
    deck = models.ForeignKey(Deck, related_name='deck_cards', on_delete=models.CASCADE)
    card_oracle = models.CharField(max_length=200)
    card_name = models.CharField(max_length=200)
    card_file = models.CharField(max_length=200)
    card_file.null = True
    card_search = models.CharField(max_length=2000)
    quantity = models.IntegerField(default=0)
    sideboard = models.BooleanField(default=False)

    class Meta:
        app_label = "Management"
