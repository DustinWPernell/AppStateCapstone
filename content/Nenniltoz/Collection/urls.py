from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection_index, name='index'),
    path('retrieveAPI', views.retrieve_api, name='retrieveAPI'),
    path('cardUpdate', views.card_update, name='cardUpdate'),
    path('ruleUpdate', views.rule_update, name='ruleUpdate'),
    path('symbolUpdate', views.symbol_update, name='symbolUpdate'),
]
