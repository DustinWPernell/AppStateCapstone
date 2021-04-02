from django.urls import path

from . import views
from Collection.Views.Cards import Card_Display, Card_Database, User_Cards
from Collection.Views.Decks import Deck_Database, Deck_Display

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('card_database', Card_Database.as_view(), name='card_database'),
    path('card/<oracle_id>/', Card_Display.as_view(), name='card'),
    path('card/<oracle_id>/update_user_card_data', User_Cards.as_view(), name='update_user_card_data'),
    path('deck_database', Deck_Database.as_view(), name='deck_database'),
    path('deck/<deck_id>/', Deck_Display.as_view(), name='deck'),
]
