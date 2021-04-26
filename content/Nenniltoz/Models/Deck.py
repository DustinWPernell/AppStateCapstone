import json
import operator
from functools import reduce
from random import randint

from django.db import models
from django.db.models import Q, Count

from Models.DeckCard import DeckCard
from Models.DeckType import DeckType
from Users.models import UserProfile

class DeckManager(models.Manager):
    def deck_filter_by_color_term(self, current_username, mana, term, is_colorless, has_color):
        if is_colorless:
            list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                              '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                              '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                              '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                              '{G}', '{2/G}', '{G/P}', '{HG}']
            mana_filter = (
                    reduce(
                        operator.or_, (
                            Q(color_id__contains=item) for item in mana
                        )
                    ) &
                    reduce(
                        operator.and_, (
                            ~Q(color_id__contains=item) for item in list_of_colors
                        )
                    )
            )
        elif has_color :
            mana_filter = reduce(
                operator.or_, (
                    Q(color_id__contains=item) for item in mana
                )
            )
        else:
            mana_filter = Q(id__gt=0)

        filter = (
                Q(is_private=False) |
                Q(deck_user=current_username)
        ) & mana_filter & (
                Q(name__icontains=term) |
                Q(description__icontains='{' + term + '}')
        )

        return self.run_query(filter, True)

    def get_deck_by_user_term(self, current_username, show_private, term):
        if show_private:
            filter = Q(deck_user=current_username) & (
                            Q(name__icontains=term) |
                            Q(description__icontains='{' + term + '}')
                     )
        else:
            filter = Q(is_private=False) & \
                     Q(deck_user=current_username) & (
                             Q(name__icontains=term) |
                             Q(description__icontains='{' + term + '}')
                     )

        return self.run_query(filter, False)

    def get_deck_list(self, current_username):
        filter = Q(is_private=False) | \
                 Q(deck_user=current_username)

        return self.run_query(filter, True)

    def get_deck(self, current_username, deck_id):
        return self.select_related().get(
            (
                    Q(is_private=False) |
                    Q(deck_user=current_username)
            ) &
            Q(id=deck_id)
        )

    def get_deck_type(self, deck_id):
        return DeckType.objects.get_deck_type_by_type(
            self.get(
                Q(id=int(deck_id))
            ).deck_type.id
        )

    def get_card_list(self, deck_id, side):
        if side:
            return self.get(id=deck_id).side_list
        else:
            return self.get(id=deck_id).card_list

    def set_card_list(self, deck_id, side, newVal):
        if side:
            self.filter(id=deck_id).update(
                side_list=newVal
            )
        else:
            self.filter(id=deck_id).update(
                card_list=newVal
            )

    def set_color_list(self, deck_id, color):
        self.filter(id=deck_id).update(
            color_id=color
        )

    def deck_create(self, deck_name_field, deck_type_field, deck_privacy_field, deck_description_field,
                    color_id, creator, username):
        return self.create(
            name=deck_name_field,
            deck_type=DeckType.objects.get(id=deck_type_field),
            is_private=deck_privacy_field == 'True',
            description=deck_description_field,
            color_id=color_id,
            created_by=creator,
            deck_user=username,
            is_pre_con=(username == "Preconstructed")
        )

    def deck_update(self, deck_id, deck_name_field, deck_type_field, deck_privacy_field, deck_description_field):
        self.filter(id=deck_id).update(
            name=deck_name_field,
            deck_type=deck_type_field,
            is_private=deck_privacy_field,
            description=deck_description_field
        )

    def run_query(self, filter, limit):
        if limit:
            count = self.filter(filter).aggregate(count=Count('id'))['count']
            if count <= 500:
                start_index = 0
            else:
                start_index = randint(0, count - 1)
            return self.build_json(self.select_related().filter(
                filter
            ).order_by('name')[start_index:start_index+500])
        else:
            return self.build_json(self.select_related().filter(
                filter
            ).order_by('name'))

    def build_json(self, deck_list):
        deck_json_list = ""
        i = 0
        for deck in deck_list:
            deck_json_list = deck_json_list + deck.__str__()
            if len(deck_list) > 1 and i + 1 < len(deck_list):
                deck_json_list = deck_json_list + '},'
                i += 1
        return deck_json_list.__str__()

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
    card_list = models.CharField(max_length=2000)
    side_list = models.CharField(max_length=1000)

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
            color_id=self.color_id,
            created_by=self.created_by,
            deck_user=user.username,
            is_pre_con=False,
            card_list=self.card_list,
            side_list=self.side_list
        )
        # endregion

        # region Copy Cards
        deck_cards = DeckCard.objects.deck_card_by_deck(self.id)
        deck_cards_list = list(deck_cards.split("},"))
        if deck_cards_list[0] == '':
            deck_cards_list = []

        for card in deck_cards_list:
            card_json = json.loads(card)
            DeckCard.objects.create(
                deck=new_deck.id,
                card_oracle=card_json['oracle_id'],
                quantity=card_json['quantity'],
                sideboard=card_json['sideboard'],
                commander=card_json['commander'],
            )
        # endregion
        return new_deck

