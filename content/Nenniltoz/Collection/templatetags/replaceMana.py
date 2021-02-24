from django import template

from Collection.models import Symbol

register = template.Library()

@register.filter
def replaceMana(val):
    symbols = Symbol.objects.all()
    for sym in symbols:
        val = val.replace(sym.symbol, "<img class=\"singCardSymbol\" src=\"" + sym.imageURL + "\" alt=\""+ sym.symbol +"\">")
    return val