from django.db import models
from django.db.models import Q

from Models import Deck


class DeckCardManager(models.Manager):
    @staticmethod
    def deck_card_by_deck_side(deck_id, side, commander):
        return DeckCard.objects.filter(
            Q(deck=deck_id) &
            Q(sideboard=side) &
            Q(commander=commander)
        )

    @staticmethod
    def deck_card_by_deck(deck_id):
        return DeckCard.objects.filter(
            Q(deck=deck_id)
        )

class DeckCard(models.Model):
    deck = models.IntegerField()
    card_oracle = models.CharField(max_length=200)
    card_name = models.CharField(max_length=200)
    card_img = models.CharField(max_length=200)
    card_img.null = True
    card_search = models.CharField(max_length=2000)
    quantity = models.IntegerField(default=0)
    sideboard = models.BooleanField(default=False)
    commander = models.BooleanField(default=False)

    objects = DeckCardManager()

    class Meta:
        app_label = "Management"