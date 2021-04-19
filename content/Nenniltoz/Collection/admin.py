from django.contrib import admin

# Register your models here.
from Models.CardLayout import CardLayout
from .models import IgnoreCards, Rule, Symbol

admin.site.register(CardLayout)
admin.site.register(IgnoreCards)
admin.site.register(Rule)
admin.site.register(Symbol)
