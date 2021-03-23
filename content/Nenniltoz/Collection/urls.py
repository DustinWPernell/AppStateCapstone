from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('card_database', views.collection_display, name='card_database'),
    path('Card/<oracle_id>/', views.card_display, name='Card'),
    path('Card/<oracle_id>/update_user_card_data', views.update_user_card_data, name='update_user_card_data'),
]
