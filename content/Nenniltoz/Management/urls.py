from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_index, name='index'),
    path('APIimport', views.api_import, name='APIimport'),
]
