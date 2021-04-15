import json
import logging
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from Collection.models import CardFace
from Models.Deck import Deck
from Users.models import UserProfile, UserCards
from static.python.session_manager import SessionManager

logger = logging.getLogger(__name__)


class SettingsUpdate(View):
    user = User

    @login_required
    def post(self, request, user_id):
        """Updated setting

        Updates user settings in database

        @param request:
        @param user_id: Current user ID

        :todo: None
        """
        logger.info("Run: update_settings; Params: " + json.dumps(request.GET.dict()))
        user_obj = User.objects.get(id=user_id).id

        setting = request.GET['setting']
        value = request.GET['value']
        if value == 'false':
            value = False
        elif value == 'true':
            value = True

        custom_user_profile = NenniUserProfile.objects.get(user=user_obj)
        setattr(custom_user_profile, setting, value)
        custom_user_profile.save()
        messages.success(request, 'Updated Settings.')
        return HttpResponse("Finished")


class NenniUserProfile(View):
    user = User

    @login_required
    def post(self, request, user_id):
        logger.info("Run: user_profile; Params: " + json.dumps(request.GET.dict()))

        # region Page numbers
        try:
            deck_page = request.GET.get('deck_page', -1)
            if deck_page == -1:
                deck_page = request.session['deck_page']
        except KeyError:
            deck_page = request.GET.get('deck_page', 1)
            request.session['deck_page'] = deck_page

        try:
            card_page = request.GET.get('card_page', -1)
            if card_page == -1:
                card_page = request.session['card_page']
        except KeyError:
            card_page = request.GET.get('card_page', 1)
            request.session['card_page'] = card_page

        try:
            wish_page = request.GET.get('wish_page', -1)
            if wish_page == -1:
                wish_page = request.session['wish_page']
        except KeyError:
            wish_page = request.GET.get('wish_page', 1)
            request.session['wish_page'] = wish_page
        # endregion

        if 'user_clear_deck_search' in request.POST:
             request.session['user_search_deck_term'] = ""
             request.session['user_search_deck_cards'] = Deck.objects.get_deck_by_user_term(request.user.username, "")
             request.session['user_clear_deck_search'] = False
        elif 'user_search_deck' in request.POST:
            search_term = request.POST.get('user_search_deck_term')
            request.session['user_search_deck_term'] = search_term
            request.session['user_search_deck_cards'] = Deck.objects.get_deck_by_user_term(request.user.username, search_term)
            request.session['user_clear_deck_search'] = True
        elif 'user_clear_card_search' in request.POST:
             request.session['user_search_card_term'] = ""
             request.session['user_search_card_cards'] = UserCards.get_user_card_term(user_id, "", False)
             request.session['user_clear_card_search'] = False
        elif 'user_search_card' in request.POST:
            search_term = request.POST.get('user_search_card_term')
            request.session['user_search_card_term'] = search_term
            request.session['user_search_card_cards'] = UserCards.get_user_card_term(user_id, search_term, False)
            request.session['user_clear_card_search'] = True
        elif 'user_clear_wish_search' in request.POST:
            request.session['user_search_wish_term'] = ""
            request.session['user_search_wish_cards'] = UserCards.get_user_card_term(user_id, "", True)
            request.session['user_clear_wish_search'] = False
        elif 'user_search_wish' in request.POST:
            search_term = request.POST.get('user_search_wish_term')
            request.session['user_search_wish_term'] = search_term
            request.session['user_search_wish_cards'] = UserCards.get_user_card_term(user_id, search_term, True)
            request.session['user_clear_wish_search'] = True

        return redirect('../' + str(user_id) + '?deck_page=' + str(deck_page) + '&card_page=' +
                        str(card_page) + '&wish_page=' + str(wish_page))

    @login_required
    def get(self, request, user_id):
        """Display the profile of a user.

        Uses the GET data from request to display user data.

        @param request:
        @param user_id: User id of displayed profile.

        :todo: None
        """
        logger.info("Run: user_profile; Params: " + json.dumps(request.GET.dict()))
        user_profile_obj = UserProfile.get_profile_by_user(user_id)

        try:
            session_user = request.session['user_view']
            if session_user != user_id:
                SessionManager.clear_other_session_data(request, SessionManager.All)
                request.session['user_view'] = user_id
        except KeyError:
            SessionManager.clear_other_session_data(request, SessionManager.All)
            request.session['user_view'] = user_id

        user_profile = UserProfile.get_profile_by_user(user_id)

        # region Page numbers
        try:
            deck_page = request.GET.get('deck_page', -1)
            if deck_page == -1:
                deck_page = request.session['deck_page']
        except KeyError:
            deck_page = request.GET.get('deck_page', 1)
            request.session['deck_page'] = deck_page

        try:
            card_page = request.GET.get('card_page', -1)
            if card_page == -1:
                card_page = request.session['card_page']
        except KeyError:
            card_page = request.GET.get('card_page', 1)
            request.session['card_page'] = card_page

        try:
            wish_page = request.GET.get('wish_page', -1)
            if wish_page == -1:
                wish_page = request.session['wish_page']
        except KeyError:
            wish_page = request.GET.get('wish_page', 1)
            request.session['wish_page'] = wish_page
        # endregion

        # region Cards from session
        try:
            user_search_deck_term = request.session['user_search_deck_term']
            user_search_deck_cards = request.session['user_search_deck_cards']
            user_clear_deck_search = request.session['user_clear_deck_search']
        except KeyError:
            user_search_deck_term = request.session['user_search_deck_term'] = ""
            user_search_deck_cards = request.session['user_search_deck_cards'] = Deck.objects.get_deck_by_user_term(user_profile.user.username, "")
            user_clear_deck_search = request.session['user_clear_deck_search'] = False

        try:
            user_search_card_term = request.session['user_search_card_term']
            user_search_card_cards = request.session['user_search_card_cards']
            user_clear_card_search = request.session['user_clear_card_search']
        except KeyError:
            user_search_card_term = request.session['user_search_card_term'] = ""
            user_search_card_cards = request.session['user_search_card_cards'] = UserCards.get_user_card_term(user_id, "", False)
            user_clear_card_search = request.session['user_clear_card_search'] = False

        try:
            user_search_wish_term = request.session['user_search_wish_term']
            user_search_wish_cards = request.session['user_search_wish_cards']
            user_clear_wish_search = request.session['user_clear_wish_search']
        except KeyError:
            user_search_wish_term = request.session['user_search_wish_term'] = ""
            user_search_wish_cards = request.session['user_search_wish_cards'] = UserCards.get_user_card_term(user_id, "", True)
            user_clear_wish_search = request.session['user_clear_wish_search'] = False
        # endregion

        # region Paginators
        user_deck_list_split = list(user_search_deck_cards.split("},"))
        if user_deck_list_split[0] == '':
            user_deck_list_split = []
        deck_show = len(user_deck_list_split) > 0 or user_clear_deck_search
        deck_paginator = Paginator(user_deck_list_split, 10)
        try:
            deck_list = deck_paginator.page(deck_page)
        except PageNotAnInteger:
            deck_list = deck_paginator.page(1)
        except EmptyPage:
            deck_list = deck_paginator.page(deck_paginator.num_pages)

        user_card_list_split = list(user_search_card_cards.split("},"))
        if user_card_list_split[0] == '':
            user_card_list_split = []
        card_show = len(user_card_list_split) > 0 or user_clear_card_search
        card_paginator = Paginator(user_card_list_split, 5)
        try:
            card_list = card_paginator.page(card_page)
        except PageNotAnInteger:
            card_list = card_paginator.page(1)
        except EmptyPage:
            card_list = card_paginator.page(card_paginator.num_pages)

        user_wish_card_list_split = list(user_search_wish_cards.split("},"))
        if user_wish_card_list_split[0] == '':
            user_wish_card_list_split = []
        wish_show = user_wish_card_list_split.__len__() > 0 or user_clear_wish_search
        wish_paginator = Paginator(user_wish_card_list_split, 5)
        try:
            wish_list = wish_paginator.page(wish_page)
        except PageNotAnInteger:
            wish_list = wish_paginator.page(1)
        except EmptyPage:
            wish_list = wish_paginator.page(wish_paginator.num_pages)
        o_player = not str(request.user.id) == user_id
        # endregion

        friend_obj = user_profile_obj.get_user_friends()
        pending_obj = user_profile_obj.get_user_pending()
        follower_obj = user_profile_obj.get_user_followers()

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {
            'font_family': font_family, 'should_translate': should_translate,
            'user_profile_obj': user_profile_obj,
            'has_friend': len(friend_obj) > 0, 'friend_obj': friend_obj,
            'has_pending': len(pending_obj) > 0, 'pending_obj': pending_obj,
            'has_follower': len(follower_obj) > 0, 'follower_obj': follower_obj,
            'o_player': o_player,
            'deckPage': deck_page, 'deck_list': deck_list, 'user_search_deck_term': user_search_deck_term,
            'clear_deck_search': user_clear_deck_search, 'deckShow': deck_show,
            'cardPage': card_page, 'card_list': card_list, 'user_search_card_term': user_search_card_term,
            'clear_card_search': user_clear_card_search, 'cardShow': card_show,
            'wish_page': wish_page, 'wish_list': wish_list, 'user_search_wish_term': user_search_wish_term,
            'clear_wish_search': user_clear_wish_search, 'wishShow': wish_show,
        }
        return render(request, 'Users/user_profile.html', context)

class AvatarPicker(View):
    user = User

    def post(self, request):
        if 'clearSearch' in request.POST:
            del request.session['avatar_search_term']
            del request.session['avatar_clear_search']
            search_term = ''
            card_list = CardFace.objects.all().order_by('name')
            clear_search = False
        else:
            search_term = request.POST.get('avatarSearchTerm')
            card_list = CardFace.card_face_filter_by_name_term(search_term).order_by('name')
            clear_search = True

        request.session['avatar_search_term'] = search_term
        request.session['avatar_card_list'] = card_list
        request.session['avatar_clear_search'] = clear_search

    @login_required
    def get(self, request):
        """Displays list for selecting new avatar

        Displays full list of card art with search by name feature.

        @param request:

        :todo: None
        """
        search_term = 'Search'
        try:
            search_term = request.session['avatar_search_term']
            card_list = CardFace.card_face_filter_by_name_term(search_term).order_by('name')
            clear_search = True
        except KeyError:
            card_list = CardFace.objects.all().order_by('name')
            clear_search = False

        page = request.GET.get('page', 1)

        paginator = Paginator(card_list, 50)
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)

        font_family = NenniUserProfile.get_font(request.user)
        should_translate = NenniUserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards,
                   'SearchTerm': search_term, 'clearSearch': clear_search}
        return render(request, 'Users/Profile/select_avatar.html', context)


class SaveAvatar(View):
    user = User
    @login_required
    def post(self, request):
        """Saves new avatar to user

        Sets new avatar image to selected URL returned by POST.

        @param request:

        :todo: None
        """

        avatar = request.POST['newAvatar']
        user_obj = User.objects.get(id=request.user.id)

        custom_user_profile = NenniUserProfile.objects.get(user=user_obj)

        try:
            os.remove(custom_user_profile.avatar_file.name)
        except OSError as e:
            print("Error: %s : %s" % (custom_user_profile.avatar_file, e.strerror))

        custom_user_profile.avatar_img = avatar
        custom_user_profile.avatar_file = None
        custom_user_profile.save()



        return redirect('user_profile', user_id=str(request.user.id))