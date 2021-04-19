from django.db import models
from django.db.models import Q

from Models.CardLayout import CardLayout
from Models.CardSet import CardSet


class CardManager(models.Manager):
    def get_card(self, card_id):
        return Card.objects.get(card_id=card_id)

    def card_create(self, card_id, ori_id, key_words, set_name, rarity, layout_obj, set_obj, color_list):
        return Card.objects.create(
            card_id=card_id,
            oracle_id=ori_id,
            keywords=key_words,
            set_name=set_name,
            rarity=rarity,
            layout=layout_obj,
            set_obj=set_obj,
            color=color_list
        )

    def card_update(self, card_id, ori_id, key_words, set_name, rarity, layout_obj, set_obj, color_list):
        return Card.objects.filter(card_id=card_id).create(
            card_id=card_id,
            oracle_id=ori_id,
            keywords=key_words,
            set_name=set_name,
            rarity=rarity,
            layout=layout_obj,
            set_obj=set_obj,
            color=color_list
        )

    def run_query(self, filter):
        return Card.objects.select_related().filter(
            filter
        ).order_by('name')

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
    set_obj = models.ForeignKey(CardSet, on_delete=models.DO_NOTHING, related_name='card_set')

    objects = CardManager()

    class Meta:
        app_label = "Management"

    def __str__(self):
        return self.card_id


