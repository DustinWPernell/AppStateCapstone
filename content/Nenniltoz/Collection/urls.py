from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('collectionAll', views.collection_display, name='collectionAll'),
    path('Card/<cardID>/', views.card_display, name='Card'),
]
