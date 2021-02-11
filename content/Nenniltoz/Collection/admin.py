from django.contrib import admin

# Register your models here.
from .models import Card
from .models import Rule
from .models import Lagality
from .models import Symbol

admin.site.register(Card)
admin.site.register(Rule)
admin.site.register(Lagality)
admin.site.register(Symbol)
