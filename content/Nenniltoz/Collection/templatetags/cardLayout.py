from django import template

register = template.Library()


@register.filter
def cardDuelSide(val):
    if val == 2:
        return "singCardImagesMulti"
    return "singCardImages"


@register.filter
def cardMultiFace(val):
    if val == 1:
            return "singCardValueMulti"
    return "singCardValue"


@register.filter
def cardLandscapeFace(val):
    if "split" == val:
        return True
    return False
