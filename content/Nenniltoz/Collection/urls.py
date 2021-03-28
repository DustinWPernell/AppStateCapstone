from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('card_database', views.collection_display, name='card_database'),
    path('Card/<oracle_id>/', views.card_display, name='Card'),
    path('deck_list', views.deck_list, name='deck_list'),
    path('Card/<oracle_id>/update_user_card_data', views.update_user_card_data, name='update_user_card_data'),
    path('Deck/<deck_id>/', views.deck_display, name='Deck'),
]
