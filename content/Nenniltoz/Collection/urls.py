from django.urls import path

from . import views
from Collection.Views.Cards import Card_Display, Card_Database
from Collection.Views.Decks import Deck_Database, Deck_Display

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('card_database', Card_Database.as_view(), name='card_database'),
    path('card/<oracle_id>/', Card_Display.as_view(), name='card'),
    path('card/<oracle_id>/card', Card_Display.as_view(), name='card'),
    path('deck_database', Deck_Database.as_view(), name='deck_database'),
    path('deck', Deck_Display.as_view(), name='deck'),
]
