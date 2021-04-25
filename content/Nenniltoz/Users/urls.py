from django.urls import path

from . import views
from .Views.Deck import Manage_Deck, Commander_Picker, Image_Picker, Manage_Cards
from .Views.Friends import Send_Friend_Request, Add_Friend, Process_Friend, Remove_Friend, Add_Follower, Remove_Follower
from .Views.Profile import NenniUserProfile, SettingsUpdate, AvatarPicker, UserCardList, UserBulkAdd

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('register', views.register, name='register'),
    path('user_profile', NenniUserProfile.as_view(), name='user_profile'),
    path('user_card_bulk', UserBulkAdd.as_view(), name='user_card_bulk'),
    path('user_card_list', UserCardList.as_view(), name='user_card_list'),
    path('send_friend_request', Send_Friend_Request.as_view(), name='send_friend_request'),
    path('add_friend', Add_Friend.as_view(), name='add_friend'),
    path('process_friend', Process_Friend.as_view(), name='process_friend'),
    path('remove_friend', Remove_Friend.as_view(), name='remove_friend'),
    path('add_follower', Add_Follower.as_view(), name='add_follower'),
    path('remove_follower', Remove_Follower.as_view(), name='remove_follower'),
    path('update_settings', SettingsUpdate.as_view(), name='update_settings'),
    path('select_avatar', AvatarPicker.as_view(), name='select_avatar'),
    path('modify_deck/select_commander', Commander_Picker.as_view(), name='select_commander'),
    path('modify_deck/select_deck_image', Image_Picker.as_view(), name='select_deck_image'),
    path('modify_deck', Manage_Deck.as_view(), name='modify_deck'),
    path('modify_cards', Manage_Cards.as_view(), name='modify_cards'),
    # path("password_reset", views.password_reset_request, name="password_reset")
]
