import html
import json

from django import template
from django.utils.safestring import mark_safe
import bleach

from Collection.models import Symbol

register = template.Library()

@register.filter
def convert_to_json(data):
    if isinstance(data, dict):
        return data
    else:
        data = json.loads(data)
        return data


@register.filter
def replaceMana(val):
    symbols = Symbol.objects.all()
    for sym in symbols:
        val = val.replace(sym.symbol,
                          "<img class=\"manaSymbol\" src=\"" + sym.image_url + "\" alt=\"" + sym.symbol + "\">")
    return val


@register.filter
def replacePeriod(val):
    val = val.replace(". ", ". <br> ")
    val = val.replace(".) ", ".) <br> ")
    return val


@register.filter
def replaceTextMana(val):
    symbols = Symbol.objects.all()
    for sym in symbols:
        val = val.replace(sym.symbol,
                          "<img class=\"smallManaSymbol\" src=\"" + sym.image_url + "\" alt=\"" + sym.symbol + "\">")
    return val


@register.filter
def remove_bracket(val):
    val = val.replace("{", '<span class="searchable">')
    val = val.replace("}", '</span>')
    return val


_ALLOWED_ATTRIBUTES = {
        'span': ['class'],
}
_ALLOWED_TAGS = ['span']

@register.filter()
def check_safe(text):
    return mark_safe(bleach.clean(text, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRIBUTES))