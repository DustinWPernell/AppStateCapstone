from django.contrib import admin

# Register your models here.
from Models import Deck
from .models import IgnoreCards, CardLayout, Card, Rule, Legality, Symbol

admin.site.register(CardLayout)
admin.site.register(IgnoreCards)
admin.site.register(Card)
admin.site.register(Rule)
admin.site.register(Legality)
admin.site.register(Symbol)
