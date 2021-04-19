from django.db import models
from django.db.models import Q


class CardSetManager(models.Manager):
    def get_card_set(self, set_id, set_name):
        filter = (
            Q(set_id=set_id) |
            Q(name=set_name)
        )
        return self.run_query(filter)

    def set_create(self, set_id, code, name, released_at, icon_svg_uri):
        CardSet.objects.create(
            set_id=set_id,
            code=code,
            name=name,
            released_at=released_at,
            icon_svg_uri=icon_svg_uri,
        )

    def set_update(self, set_id, code, name, released_at, icon_svg_uri):
        CardSet.objects.filter(set_id=set_id).create(
            code=code,
            name=name,
            released_at=released_at,
            icon_svg_uri=icon_svg_uri,
        )

    def run_query(self, filter):
        return CardSet.objects.select_related().get(
            filter
        )

class CardSet(models.Model):
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

    objects = CardSetManager()

    class Meta:
        app_label = "Management"

    def __str__(self):
        return self.name