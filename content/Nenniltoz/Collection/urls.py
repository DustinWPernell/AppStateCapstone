from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('collectionAll', views.collection_display, name='collectionAll'),
    path('Card/<cardID>/', views.card_display, name='Card'),
    path('Card/<cardID>/add_card', views.add_card, name='add_card'),
    path('Card/<cardID>/update_quantity', views.update_quantity, name='update_quantity'),
]
