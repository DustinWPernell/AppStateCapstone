from django.contrib import admin

# Register your models here.
from .models import IgnoreCards, CardLayout, Card, Rule, Legality, Symbol, Deck, DeckCards

admin.site.register(CardLayout)
admin.site.register(IgnoreCards)
admin.site.register(Card)
admin.site.register(Rule)
admin.site.register(Legality)
admin.site.register(Symbol)
admin.site.register(Deck)
admin.site.register(DeckCards)
