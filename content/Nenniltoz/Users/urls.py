from django.urls import path

from . import views
from .Views.Deck import Manage_Deck
from .Views.Friends import Send_Friend_Request, Add_Friend, Process_Friend, Remove_Friend, Add_Follower, Remove_Follower
from .Views.Profile import User_Profile, Settings_Update, Avatar_Picker, Save_Avatar, User_Profile_Search

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('register', views.register, name='register'),
    path('user_profile/<user_id>/', User_Profile.as_view(), name='user_profile'),
    path('user_profile/<user_id>/user_profile_search', User_Profile_Search.as_view(), name='user_profile_search'),
    path('user_profile/<user_id>/user_profile', User_Profile.as_view(), name='user_profile'),
    path('user_profile/<user_id>/send_friend_request', Send_Friend_Request.as_view(), name='send_friend_request'),
    path('user_profile/<user_id>/add_friend', Add_Friend.as_view(), name='add_friend'),
    path('user_profile/<user_id>/process_friend', Process_Friend.as_view(), name='process_friend'),
    path('user_profile/<user_id>/remove_friend', Remove_Friend.as_view(), name='remove_friend'),
    path('user_profile/<user_id>/add_follower', Add_Follower.as_view(), name='add_follower'),
    path('user_profile/<user_id>/remove_follower', Remove_Follower.as_view(), name='remove_follower'),
    path('user_profile/<user_id>/update_settings/', Settings_Update.as_view(), name='update_settings'),
    path('select_avatar', Avatar_Picker.as_view(), name='select_avatar'),
    path('save_avatar', Save_Avatar.as_view(), name='save_avatar'),
    path('user_profile/<user_id>/modify_deck/<deck_id>/', Manage_Deck.as_view(), name='modify_deck'),
    # path("password_reset", views.password_reset_request, name="password_reset")
]
