from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_index, name='index'),
    path('APIimport', views.api_import, name='APIimport'),
    path('retrieveAPI', views.retrieve_api, name='retrieveAPI'),
    path('cardUpdate', views.card_update, name='cardUpdate'),
    path('ruleUpdate', views.rule_update, name='ruleUpdate'),
    path('symbolUpdate', views.symbol_update, name='symbolUpdate'),
    path('setUpdate', views.set_update, name='setUpdate'),
]
