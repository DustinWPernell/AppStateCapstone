from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_index, name='index'),
    path('APIimport', views.api_import, name='APIimport'),
    path('quick_search_update', views.quick_search_update, name='quick_search_update'),
    path('retrieveAPI', views.retrieve_api, name='retrieveAPI'),
    path('cardUpdate', views.card_update, name='cardUpdate'),
    path('ruleUpdate', views.rule_update, name='ruleUpdate'),
    path('symbolUpdate', views.symbol_update, name='symbolUpdate'),
    path('setUpdate', views.set_update, name='setUpdate'),
    path('oracleUpdate', views.oracle_update, name='oracleUpdate'),
    path('oracle_search', views.oracle_search, name='oracle_search'),
]
