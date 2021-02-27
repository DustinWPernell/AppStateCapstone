from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login_page', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('player_profile', views.player_profile, name='player_profile'),
    path('send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('process_friend', views.process_friend, name='process_friend'),
    path('remove_friend', views.remove_friend, name='remove_friend'),
    path('add_follower', views.add_follower, name='add_follower'),
    path('remove_follower', views.remove_follower, name='remove_follower'),
]
