from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('collectionAll', views.collection_display, name='collectionAll'),
    path('Card/<card_id>/', views.card_display, name='Card'),
    path('Card/<card_id>/add_card', views.add_card, name='add_card'),
    path('Card/<card_id>/update_quantity', views.update_quantity, name='update_quantity'),
]
