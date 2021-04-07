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
from Users.models import UserProfile, UserCards

logger = logging.getLogger(__name__)


class Settings_Update(View):
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

        custom_user_profile = UserProfile.objects.get(user=user_obj)
        setattr(custom_user_profile, setting, value)
        custom_user_profile.save()
        messages.success(request, 'Updated Settings.')
        return HttpResponse("Finished")


class User_Profile(View):
    user = User
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

        # region Page numbers

        try:
            deck_page = request.GET.get('deckPage', -1)
            if deck_page == -1:
                deck_page = request.session['deckPage']
        except KeyError:
            deck_page = request.GET.get('deckPage', 1)
            request.session['deckPage'] = deck_page

        try:
            card_page = request.GET.get('cardPage', -1)
            if card_page == -1:
                card_page = request.session['cardPage']
        except KeyError:
            card_page = request.GET.get('cardPage', 1)
            request.session['cardPage'] = card_page

        try:
            card_wish_page = request.GET.get('cardWishPage', -1)
            if card_wish_page == -1:
                card_wish_page = request.session['cardWishPage']
        except KeyError:
            card_wish_page = request.GET.get('cardWishPage', 1)
            request.session['cardWishPage'] = card_wish_page

        # endregion

        # region Cards from session

        try:
            search_deck_term = request.session['user_search_deck_term']
            # user_deck_obj_list = request.session['user_decks']
            # user_decks = CardFace.objects.filter(Q(id__in=user_deck_obj_list)).order_by('name'))
            user_clear_deck_search = request.session['user_clear_deck_search']
        except KeyError:
            # user_deck_obj_list = []
            user_decks = []
            search_deck_term = "Search"
            user_clear_deck_search = False
            request.session['user_clear_deck_search'] = False

        try:
            search_card_term = request.session['user_search_card_term']
            user_card_obj_list = request.session['user_cards']
            user_cards = UserCards.get_user_card_by_oracle_list(user_card_obj_list, user_profile_obj.user)
            user_clear_card_search = request.session['user_clear_card_search']
        except KeyError:
            user_cards = UserCards.get_user_card_term(user_profile_obj.user, "", False)
            search_card_term = "Search"
            user_clear_card_search = request.session['user_clear_card_search'] = False

        try:
            search_wish_term = request.session['user_search_wish_term']
            user_wish_card_obj_list = request.session['user_wish_cards']
            user_wish_cards = UserCards.get_user_card_by_oracle_list(user_wish_card_obj_list, user_profile_obj.user)
            user_clear_wish_search = request.session['user_clear_wish_search']
        except KeyError:
            user_wish_cards = UserCards.get_user_card_term(user_profile_obj.user, "", True)
            search_wish_term = "Search"
            user_clear_wish_search = request.session['user_clear_wish_search'] = False

        # endregion

        # region Paginators

        deck_paginator = Paginator(user_decks, 10)
        try:
            decks = deck_paginator.page(deck_page)
        except PageNotAnInteger:
            decks = deck_paginator.page(1)
        except EmptyPage:
            decks = deck_paginator.page(deck_paginator.num_pages)

        card_paginator = Paginator(user_cards, 5)
        try:
            cards = card_paginator.page(card_page)
        except PageNotAnInteger:
            cards = card_paginator.page(1)
        except EmptyPage:
            cards = card_paginator.page(card_paginator.num_pages)

        wish_paginator = Paginator(user_wish_cards, 5)
        try:
            wish_cards = wish_paginator.page(card_wish_page)
        except PageNotAnInteger:
            wish_cards = wish_paginator.page(1)
        except EmptyPage:
            wish_cards = wish_paginator.page(wish_paginator.num_pages)
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
            'deckPage': deck_page, 'deckPager': decks, 'search_deck_term': search_deck_term,
            'clear_deck_search': user_clear_deck_search, 'deckShow': (deck_paginator.count > 0 or user_clear_deck_search),
            'cardPage': card_page, 'cardPager': cards, 'search_card_term': search_card_term,
            'clear_card_search': user_clear_card_search, 'cardShow': (card_paginator.count > 0 or user_clear_card_search),
            'cardWishPage': card_wish_page, 'cardWishPager': wish_cards, 'search_wish_term': search_wish_term,
            'clear_wish_search': user_clear_wish_search, 'wishShow': (wish_paginator.count > 0 or user_clear_wish_search),
        }
        return render(request, 'Users/user_profile.html', context)


class User_Profile_Search(View):
    user = User
    @login_required
    def post(self, request, user_id):
        logger.info("Run: user_profile; Params: " + json.dumps(request.GET.dict()))
        user_profile_obj = UserProfile.get_profile_by_user(user_id)

        # region Page numbers

        try:
            deck_page = request.GET.get('deckPage', -1)
            if deck_page == -1:
                deck_page = request.session['deckPage']
        except KeyError:
            deck_page = request.GET.get('deckPage', 1)
            request.session['deckPage'] = deck_page

        try:
            card_page = request.GET.get('cardPage', -1)
            if card_page == -1:
                card_page = request.session['cardPage']
        except KeyError:
            card_page = request.GET.get('cardPage', 1)
            request.session['cardPage'] = card_page

        try:
            card_wish_page = request.GET.get('cardWishPage', -1)
            if card_wish_page == -1:
                card_wish_page = request.session['cardWishPage']
        except KeyError:
            card_wish_page = request.GET.get('cardWishPage', 1)
            request.session['cardWishPage'] = card_wish_page

        # endregion

        if request.method == 'POST':
            if 'user_clear_deck_search' in request.POST:
                del request.session['user_search_deck_term']
                del request.session['user_decks']
                request.session['user_clear_deck_search'] = False

            elif 'user_search_deck' in request.POST:
                search_term = request.POST.get('user_search_deck_term')
                filtered_card_list = CardFace.objects.card_face_filter_by_name_term(search_term)

                card_id_list = []
                for card_list_obj in filtered_card_list:
                    if card_list_obj['card_id'] not in card_id_list:
                        card_id_list.append(card_list_obj['card_id'])

                request.session['user_search_deck_term'] = search_term
                request.session['user_decks'] = card_id_list
                request.session['user_clear_deck_search'] = True

            elif 'user_clear_card_search' in request.POST:
                del request.session['user_search_card_term']
                del request.session['user_cards']
                request.session['user_clear_card_search'] = False

            elif 'user_search_card' in request.POST:
                search_term = request.POST.get('user_search_card_term')
                user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, False)
                card_id_list = []
                for card_list_obj in user_card_obj_term:
                    if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                        card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)

                request.session['user_search_card_term'] = search_term
                request.session['user_cards'] = card_id_list
                request.session['user_clear_card_search'] = True

            elif 'user_clear_wish_search' in request.POST:
                del request.session['user_search_wish_term']
                del request.session['user_wish_cards']
                request.session['user_clear_wish_search'] = False

            elif 'user_search_wish' in request.POST:
                search_term = request.POST.get('user_search_wish_term')
                user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, True)
                card_id_list = []
                for card_list_obj in user_card_obj_term:
                    if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                        card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)

                request.session['user_search_wish_term'] = search_term
                request.session['user_wish_cards'] = card_id_list
                request.session['user_clear_wish_search'] = True

            return redirect('../' + str(user_id) + '?deckPage=' + str(deck_page) + '&cardPage=' +
                            str(card_page) + '&cardWishPage=' + str(card_wish_page))


class Avatar_Picker(View):
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

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards,
                   'SearchTerm': search_term, 'clearSearch': clear_search}
        return render(request, 'Users/Profile/select_avatar.html', context)


class Save_Avatar(View):
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

        custom_user_profile = UserProfile.objects.get(user=user_obj)

        try:
            os.remove(custom_user_profile.avatar_file.name)
        except OSError as e:
            print("Error: %s : %s" % (custom_user_profile.avatar_file, e.strerror))

        custom_user_profile.avatar_img = avatar
        custom_user_profile.avatar_file = None
        custom_user_profile.save()



        return redirect('user_profile', user_id=str(request.user.id))