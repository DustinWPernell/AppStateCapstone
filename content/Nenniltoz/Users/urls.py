from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login_page', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('user_profile/<user_id>/', views.user_profile, name='user_profile'),
    path('user_profile/<user_id>/user_profile', views.user_profile, name='user_profile'),
    path('user_profile/<user_id>/send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('user_profile/<user_id>/add_friend', views.add_friend, name='add_friend'),
    path('user_profile/<user_id>/process_friend', views.process_friend, name='process_friend'),
    path('user_profile/<user_id>/remove_friend', views.remove_friend, name='remove_friend'),
    path('user_profile/<user_id>/add_follower', views.add_follower, name='add_follower'),
    path('user_profile/<user_id>/remove_follower', views.remove_follower, name='remove_follower'),
    path('user_profile/<user_id>/update_settings/', views.update_settings, name='update_settings'),
    path('select_avatar', views.select_avatar, name='select_avatar'),
    path('save_avatar', views.save_avatar, name='save_avatar'),
    path('modify_deck', views.modify_deck, name='modify_deck'),

]
