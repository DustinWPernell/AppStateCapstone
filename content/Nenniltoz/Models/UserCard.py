
from django.db import models
from django.db.models import Q

from Collection.models import CardIDList
from Models import CardFace
from static.python.data_helpers import data_helpers


class UserCardManager(models.Manager):
    def get_user_card(self, user_id, wish, color, is_colorless, has_color, term):
        if len(color) > 0:
            oracle_list = CardFace.objects.card_filter_by_color_term(color, term, is_colorless, has_color)
            oracles = []
            for card in oracle_list.iterator():
                if card.oracle_id not in oracles:
                    oracles.append(card.oracle_id)

            mana_filter = data_helpers.mana_filter(is_colorless, has_color, color)
            oracle_filter = (
                        Q(card_oracle__in=oracles) | (
                            Q(notes__icontains='{' + term + '}') &
                            mana_filter
                        )
                  )
        else:
            oracle_filter = data_helpers.mana_filter(is_colorless, has_color, color)

        filter = Q(user=user_id) & Q(wish=wish) & oracle_filter
        return self.run_query(filter)

    def get_user_card_oracle(self, user_id, oracle_id, check_wish, wish):
        if check_wish:
            filter = Q(user=user_id) & Q(card_oracle=oracle_id) & Q(wish=wish)
        else:
            filter = Q(user=user_id) & Q(card_oracle=oracle_id)
        return self.run_query(filter)

    def user_card_create(self, user_id, card_oracle, card_name, color_id, quantity, wish, notes):
        self.create(
            user=user_id,
            card_oracle=card_oracle,
            card_name=card_name,
            color_id=color_id,
            quantity=quantity,
            wish=wish,
            notes=notes
        )

    def user_card_update(self, user_id, card_oracle, quantity, wish, notes):
        return self.filter(user=user_id, card_oracle=card_oracle, wish=wish).update(
            quantity=quantity,
            notes=notes
        )

    def user_card_delete(self, user_id, card_oracle, wish):
        self.filter(user=user_id,
                    card_oracle=card_oracle,
                    wish=wish,
                    ).delete()

    def run_query(self, filter):
        return self.build_json(self.select_related().filter(
            filter
        ))

    def build_json(self, card_list):
        card_json_list = ""
        i = 0
        for card in card_list:
            card_json_list = card_json_list + card.__str__()
            if len(card_list) > 1 and i + 1 < len(card_list):
                card_json_list = card_json_list + '},'
                i += 1
        return card_json_list.__str__()

class UserCard(models.Model):
    user = models.IntegerField()
    card_name = models.CharField(max_length=100)
    card_oracle = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    wish = models.BooleanField(default=False)
    notes = models.CharField(max_length=1000, default="")
    color_id = models.CharField(max_length=50)

    objects = UserCardManager()

    class Meta:
        app_label = "Management"

    def __str__(self):
        card_id_obj = CardIDList.get_card_face_by_oracle(self.card_oracle)
        card = CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id=card_id_obj.card_id)
        )[0]

        return '{' \
               '"user_id": "' + str(self.user) + \
               '", "oracle_id": "' + str(self.card_oracle) + \
               '", "quantity": "' + str(self.quantity) + \
               '", "wish": "' + str(self.wish) + \
               '", "notes": "' + str(self.notes) + \
               '", "card_name": "' + str(self.card_name) + \
               '", "card_image": "' + str(card.image_url) + \
               '", "avatar_img": "' + str(card.avatar_img) + \
               '", "color_id": "' + str(self.color_id) + \
               '"}'