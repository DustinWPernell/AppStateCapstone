import json
import logging
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from Models.CardFace import CardFace
from Models.Deck import Deck
from Users.models import UserProfile, UserCards
from static.python.session_manager import SessionManager

logger = logging.getLogger(__name__)


class SettingsUpdate(View):
    user = User

    @login_required
    def post(self, request):
        """Updated setting

        Updates user settings in database

        @param request:
        @param user_id: Current user ID

        :todo: None
        """
        logger.info("Run: update_settings; Params: " + json.dumps(request.GET.dict()))
        user_id = request.GET.get('user_id', -1)

        user_obj = User.objects.get(id=user_id)

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
    def post(self, request):
        logger.info("Run: user_profile; Params: " + json.dumps(request.GET.dict()))
        user_id = request.GET.get('user_id', -1)

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

        show_private = int(user_id) == request.user.id

        if 'user_clear_deck_search' in request.POST:
             request.session['user_search_deck_term'] = ""
             request.session['user_search_deck_cards'] = Deck.objects.get_deck_by_user_term(request.user.username, show_private, "")
             request.session['user_clear_deck_search'] = False
        elif 'user_search_deck' in request.POST:
            search_term = request.POST.get('user_search_deck_term')
            request.session['user_search_deck_term'] = search_term
            request.session['user_search_deck_cards'] = Deck.objects.get_deck_by_user_term(request.user.username, show_private, search_term)
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
    def get(self, request):
        """Display the profile of a user.

        Uses the GET data from request to display user data.

        @param request:
        @param user_id: User id of displayed profile.

        :todo: None
        """
        logger.info("Run: user_profile; Params: " + json.dumps(request.GET.dict()))
        user_id = request.GET.get('user_id', -1)

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

        show_private = int(user_id) == request.user.id

        # region Cards from session
        try:
            user_search_deck_term = request.session['user_search_deck_term']
            user_search_deck_cards = request.session['user_search_deck_cards']
            user_clear_deck_search = request.session['user_clear_deck_search']
        except KeyError:
            user_search_deck_term = request.session['user_search_deck_term'] = ""
            user_search_deck_cards = request.session['user_search_deck_cards'] = Deck.objects.get_deck_by_user_term(user_profile.user.username, show_private, "")
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
        deck_paginator = Paginator(user_deck_list_split, 5)
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
            'o_player': o_player, 'user_id': user_id,
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
    term = 'avatar_search_term'
    cards = 'avatar_card_list'
    clear = 'avatar_clear_search'

    def post(self, request):
        user_id = request.GET.get('user_id', -1)

        if self.clear in request.POST:
            request.session[self.term] = ""
            request.session[self.cards] = CardFace.objects.card_face_avatar_filter('')
            request.session[self.clear] = False
        if self.term in request.POST:
            avatar_search_term = request.session[self.term] = request.POST.get(self.term)
            request.session[self.cards] = CardFace.objects.card_face_avatar_filter(avatar_search_term)
            request.session[self.clear] = True
        else:
            user_selected_avatar = request.POST.get('user_selected_avatar')
            user_prof = UserProfile.get_profile_by_user(user_id)
            user_prof.avatar_img = user_selected_avatar
            user_prof.save()

            return HttpResponseRedirect(reverse('user_profile') + '?user_id=' + str(user_id))

        return HttpResponseRedirect(reverse('select_avatar') + '?user_id=' + str(user_id))

    @login_required
    def get(self, request):
        """Displays list for selecting new avatar

        Displays full list of card art with search by name feature.

        @param request:

        :todo: None
        """
        SessionManager.clear_other_session_data(request, SessionManager.avatar_session)
        user_id = request.GET.get('user_id', -1)

        try:
            avatar_search_term = request.session[self.term]
            avatar_card_list = request.session[self.cards]
            avatar_clear_search = request.session[self.clear]
        except KeyError:
            avatar_search_term = request.session[self.term] = ""
            avatar_card_list = request.session[self.cards] = CardFace.objects.card_face_avatar_filter('')
            avatar_clear_search = request.session[self.clear] = False

        avatar_card_list_split = list(avatar_card_list.split("},"))
        if avatar_card_list_split[0] == '':
            avatar_card_list_split = []
        page = request.GET.get('page', 1)
        paginator = Paginator(avatar_card_list_split, 50)
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards,
                   str(self.term): avatar_search_term, str(self.clear): avatar_clear_search, 'user_id': user_id}
        return render(request, 'Users/Profile/select_avatar.html', context)