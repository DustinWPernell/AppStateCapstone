import operator
from functools import reduce
from random import randint

from django.db import models
from django.db.models import Q, Count

from Models.DeckCard import DeckCard
from Models.DeckType import DeckType
from Users.models import UserProfile

class DeckManager(models.Manager):
    def deck_filter_by_color_term_colorless(self, current_username, mana, term):
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
                    Q(deck_user=current_username)
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

    def deck_filter_by_color_term(self, current_username, mana, term):
        # Retrieve all decks that are not private and colorId contains the selected colors,
        # or name contains the search term
        return Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=current_username)
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

    def get_deck_by_user_term(self, current_username, term):
        filtered_deck_list = Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=current_username)
            ) & (
                    Q(name__icontains=term) |
                    Q(description__icontains='{' + term + '}')
            )
        ).order_by('name')

        deck_json_list = ""
        i = 0
        for deck in filtered_deck_list:
            deck_json_list = deck_json_list + deck.__str__()
            if len(filtered_deck_list) > 1 and i + 1 < len(filtered_deck_list):
                deck_json_list = deck_json_list + '},'
                i += 1
        return deck_json_list.__str__()

    def get_deck_list(self, current_username):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        filtered_deck_list = Deck.objects.select_related().filter(
            (
                    Q(is_private=False) |
                    Q(deck_user=current_username)
            )
        ).order_by('name')[random_index:random_index+500]

        deck_json_list = ""
        i = 0
        for deck in filtered_deck_list:
            deck_json_list = deck_json_list + deck.__str__()
            if len(filtered_deck_list) > 1 and i + 1 < len(filtered_deck_list):
                deck_json_list = deck_json_list + '},'
                i += 1
        return deck_json_list.__str__()

    def get_deck(self, current_username, deck_id):
        return Deck.objects.select_related().get(
            (
                    Q(is_private=False) |
                    Q(deck_user=current_username)
            ) &
            Q(id=deck_id)
        )

    def get_deck_type(self, deck_id):
        return DeckType.objects.get_deck_type_by_type(
            Deck.objects.get(
                Q(id=int(deck_id))
            ).deck_type.id
        )

    def deck_create(self, deck_name_field, deck_type_obj, deck_privacy_field, deck_description_field,
                    color_id, username):
        new_deck = Deck.objects.create(
            name=deck_name_field,
            deck_type=deck_type_obj,
            is_private=deck_privacy_field == 'True',
            description=deck_description_field,
            color_id=color_id,
            created_by=username,
            deck_user=username,
            is_pre_con=(username == "Preconstructed")
        )
        return new_deck.id

class Deck(models.Model):
    name = models.CharField(max_length=200)
    color_id = models.CharField(max_length=20)
    created_by = models.CharField(max_length=50)
    created_by.null = True
    deck_user = models.CharField(max_length=50)
    is_pre_con = models.BooleanField()
    is_private = models.BooleanField()
    image_url = models.CharField(max_length=200, default="static/img/generic_box.png")
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

    objects = DeckManager()

    class Meta:
        app_label = "Management"

    def __str__(self):
        return '{"deck_id": "' + str(self.id) + \
               '", "deck_name": "' + str(self.name) + \
               '", "color_id": "' + str(self.color_id) + \
               '", "created_by": "' + str(self.created_by) + \
               '", "deck_user": "' + str(self.deck_user) + \
               '", "is_pre_con": "' + str(self.is_pre_con) + \
               '", "is_private": "' + str(self.is_private) + \
               '", "description": "' + str(self.description) + \
               '", "deck_type": "' + str(self.deck_type.desc) + \
               '", "image_url": "' + str(self.image_url) + \
               '"}'

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
            deck_user=user.username,
            is_pre_con=False
        )
        # endregion

        # region Copy Cards
        deck_cards = DeckCard.objects.deck_card_by_deck(self.id)

        for card in deck_cards:
            DeckCard.objects.create(
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

