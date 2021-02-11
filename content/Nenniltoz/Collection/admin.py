from django.contrib import admin

# Register your models here.
from .models import Card
from .models import Rule
from .models import Legality
from .models import Symbol

admin.site.register(Card)
admin.site.register(Rule)
admin.site.register(Legality)
admin.site.register(Symbol)
