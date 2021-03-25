from django import template

from Collection.models import Symbol

register = template.Library()


@register.filter
def replaceMana(val):
    symbols = Symbol.objects.all()
    for sym in symbols:
        val = val.replace(sym.symbol,
                          "<img class=\"manaSymbol\" src=\"" + sym.image_url + "\" alt=\"" + sym.symbol + "\">")
    return val


@register.filter
def replacePeriod(val):
    val = val.replace(". ", ". \\n ")
    val = val.replace(".) ", ".) \\n ")
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
    val = val.replace("{", '<span style="color: lightgreen">')
    val = val.replace("}", '</span>')
    return val
