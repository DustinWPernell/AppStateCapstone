from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('card_database', views.collection_display, name='card_database'),
    path('Card/<oracle_id>/', views.card_display, name='Card'),
    path('Card/<oracle_id>/add_card', views.add_card, name='add_card'),
    path('Card/<oracle_id>/update_quantity', views.update_quantity, name='update_quantity'),
    path('deck_list', views.deck_list, name='deck_list')
]
