from django import template
from django.db.models import Q

from Collection.models import CardLayout

register = template.Library()


@register.filter
def cardDuelSide(val):
    layout = CardLayout.objects.all().filter(
        Q(sides=2)
    )
    for lay in layout:
        if lay.layout == val:
            return True
    return False


@register.filter
def cardMultiFace(val):
    layout = CardLayout.objects.all().filter(
        Q(multi_face=1)
    )
    for lay in layout:
        if lay.layout == val:
            return True
    return False


@register.filter
def cardLandscapeFace(val):
    if "split" == val:
        return True
    return False
