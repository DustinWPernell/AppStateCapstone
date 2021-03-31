from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('register', views.register, name='register'),
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
    path('user_profile/<user_id>/modify_deck/<deck_id>/', views.modify_deck, name='modify_deck'),
    # path("password_reset", views.password_reset_request, name="password_reset")
]
