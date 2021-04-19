import logging

from django.db import models
from django.db.models import Q

logger = logging.getLogger("logger")


class CardLayoutManager(models.Manager):
    def get_card_layout(self, layout, sides, multi_face):
        filter = (
            Q(layout=layout) |
            Q(sides=sides) |
            Q(multi_face=multi_face)
        )
        return self.run_query(filter)

    def run_query(self, filter):
        return CardLayout.objects.get(
            filter
        )

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

    objects = CardLayoutManager()

    class Meta:
        app_label = "Management"

    def __int__(self):
        return self.id