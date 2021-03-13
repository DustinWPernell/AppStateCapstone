from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login_page', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('user_profile/<userID>/', views.user_profile, name='user_profile'),
    path('user_profile/<userID>/user_profile', views.user_profile, name='user_profile'),
    path('user_profile/<userID>/send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('user_profile/<userID>/add_friend', views.add_friend, name='add_friend'),
    path('user_profile/<userID>/process_friend', views.process_friend, name='process_friend'),
    path('user_profile/<userID>/remove_friend', views.remove_friend, name='remove_friend'),
    path('user_profile/<userID>/add_follower', views.add_follower, name='add_follower'),
    path('user_profile/<userID>/remove_follower', views.remove_follower, name='remove_follower'),
    path('select_avatar', views.select_avatar, name='select_avatar'),
    path('save_avatar', views.save_avatar, name='save_avatar'),
    path('new_deck', views.new_deck, name='new_deck'),

]
