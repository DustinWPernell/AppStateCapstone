from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q

from Collection.models import CardIDList

from Models import CardFace

class DeckCardManager(models.Manager):
    def deck_card_by_deck_side(self, deck_id, side, commander):
        filter = Q(deck=deck_id) & Q(sideboard=side) & Q(commander=commander)
        return self.run_query(filter)

    def empty_deck(self, deck_id, side, commander):
        filter = Q(deck=deck_id) & Q(sideboard=side) & Q(commander=commander)
        return self.select_related().filter(
            filter
        ).delete()

    def deck_card_by_deck(self, deck_id):
        filter = Q(deck=deck_id)
        return self.run_query(filter)

    def deck_card_create(self, deck_id, card_oracle, quantity, side, commander):
        self.create(
            deck=deck_id,
            card_oracle=card_oracle,
            quantity=quantity,
            sideboard=side,
            commander=commander
        )

    def deck_card_update(self, deck_id, card_oracle, quantity, side, commander):
        return self.filter(deck=deck_id, card_oracle=card_oracle).update(
            quantity=quantity,
            sideboard=side,
            commander=commander
        )

    def deck_card_delete(self, deck_id, card_oracle, side, commander):
        self.filter(deck=deck_id,
                    card_oracle=card_oracle,
                    sideboard=side,
                    commander=commander
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

class DeckCard(models.Model):
    deck = models.IntegerField()
    card_oracle = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    sideboard = models.BooleanField(default=False)
    commander = models.BooleanField(default=False)

    objects = DeckCardManager()

    class Meta:
        app_label = "Management"

    def __str__(self):
        card_id_obj = CardIDList.get_card_face_by_oracle(self.card_oracle)
        card = CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id=card_id_obj.card_id)
        )[0]

        return '{' \
               '"deck_id": "' + str(self.deck) + \
               '", "oracle_id": "' + str(self.card_oracle) + \
               '", "quantity": "' + str(self.quantity) + \
               '", "sideboard": "' + str(self.sideboard) + \
               '", "commander": "' + str(self.commander) + \
               '", "card_name": "' + str(card.name) + \
               '", "card_image": "' + str(card.image_url) + \
               '", "color_id": "' + str(card.color_id) + \
               '"}'