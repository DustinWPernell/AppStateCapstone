import json
import logging
import os
from json import JSONDecodeError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from Collection.models import Symbol, CardIDList
from Models.CardFace import CardFace
from Models.Deck import Deck
from Models.UserCard import UserCard
from Users.models import UserProfile
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


class UserBulkAdd(View):
    user = User
    card = 'user_card_save_list'
    list = 'user_card_list'
    clear = 'user_card_clear'

    def add_to_user(self, request, user_id, card_list, wish):
        formatted_list = ''

        card_list = list(card_list.split("\n"))
        if card_list[0] == '':
            card_list = []
        for card_item in card_list:
            card_item = card_item.replace('\r', '')
            try:
                if card_item != '':
                    card_values = card_item.split(" ", 1)
                    if card_values[0] != '':
                        card_quantity = int(card_values[0])
                        card_name = card_values[1]
                        card_id_info = CardIDList.get_card_by_name(card_name)
                        user_card = UserCard.objects.get_user_card_oracle(user_id, card_id_info.oracle_id, True, wish)
                        if len(user_card) > 0:
                            user_json = json.loads(user_card)
                            UserCard.objects.user_card_update(
                                user_id,
                                card_id_info.oracle_id,
                                card_quantity + int(user_json['quantity']),
                                wish,
                                user_json['notes']
                            )
                        else:
                            UserCard.objects.user_card_create(
                                user_id,
                                card_id_info.oracle_id,
                                card_id_info.card_name,
                                card_id_info.color_id,
                                card_quantity,
                                wish,
                                ''
                            )
                        #formatted_list = formatted_list + str(card_quantity) + " " + str(card_name) + '\n'
            except:
                messages.error(request, "List in incorrect format. " + str(card_item) + " not added to collection.")
                formatted_list = formatted_list + str(card_item) + '\n'
        return formatted_list

    def post(self, request):
        user_id = request.GET.get('user_id', -1)
        wish = False
        if request.GET.get('wish', 'False') == 'True':
            wish = True

        if str(self.card) in request.POST:
            card_list = request.POST[str(self.list)]
            request.session[str(self.list)] = self.add_to_user(request, user_id, card_list, wish)
        elif str(self.clear):
            request.session[str(self.list)] = ''
        elif 'return' in request.POST:
            return HttpResponseRedirect(reverse('user_profile') + '?user_id='+str(request.user.id))
        return HttpResponseRedirect(reverse('user_card_bulk') + '?user_id=' + str(user_id) + '&wish=' + str(wish))

    @login_required
    def get(self, request):
        """Displays list for selecting new avatar

        Displays full list of card art with search by name feature.

        @param request:

        :todo: None
        """
        SessionManager.clear_other_session_data(request, SessionManager.BulkCard)

        user_id = request.GET.get('user_id', -1)
        wish = False
        title = " collection "
        if request.GET.get('wish', 'False') == 'True':
            wish = True
            title = " wish List "

        try:
            user_card_list = request.session[str(self.list)]
        except KeyError:
            user_card_list = ''

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate,
                   str(self.list): user_card_list,
                   'user_id': user_id, 'wish': wish, 'title': title}
        return render(request, 'Users/Profile/ProfileCards/bulk_add_card.html', context)


class UserCardList(View):
    search = 'user_card_list_search'
    term = 'user_card_list_search_Term'
    mana = 'user_card_list_selected_mana'
    cards = 'user_card_list_card_list'
    clear = 'user_card_list_clear'
    
    def post(self, request):
        logger.info("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
        user_id = request.GET.get('user_id', -1)
        wish = False
        if request.GET.get('wish', 'False') == 'True':
            wish = True

        if 'return' in request.POST:
            return HttpResponseRedirect(reverse('user_profile') + '?user_id=' + str(user_id))

        init_mana_list = Symbol.get_base_symbols()

        if str(self.clear) in request.POST:
            request.session[str(self.term)] = ""
            request.session[str(self.mana)] = []
            request.session[str(self.cards)] = UserCard.objects.get_user_card(user_id, wish, [], False, False,"")
            request.session[str(self.clear)] = False
        elif str(self.search) in request.POST:
            text = request.POST.get(str(self.term))
            search_term = text
            selected_mana = []
            has_colorless = False
            has_color = False
            for selected in init_mana_list:
                mana_ele = request.POST.get("mana-" + str(selected.id))
                if mana_ele == '':
                    selected_mana.append(selected.symbol)
                    if selected.symbol == '{W}':
                        alt_mana = Symbol.get_white()
                    elif selected.symbol == '{U}':
                        alt_mana = Symbol.get_blue()
                    elif selected.symbol == '{B}':
                        alt_mana = Symbol.get_black()
                    elif selected.symbol == '{R}':
                        alt_mana = Symbol.get_red()
                    elif selected.symbol == '{G}':
                        alt_mana = Symbol.get_green()
                    elif selected.symbol == '{C}':
                        alt_mana = Symbol.get_colorless()
                    else:
                        alt_mana = []

                    for am in alt_mana:
                        if am.symbol not in selected_mana:
                            selected_mana.append(am.symbol)

            if len(selected_mana) > 0:
                colorless = ['{C}', '', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                             '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                             '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}']

                has_colorless = any(item in selected_mana for item in colorless)
                has_color = True


            filtered_card_list = UserCard.objects.get_user_card(
                user_id,
                wish,
                selected_mana,
                has_colorless,
                has_color,
                search_term)
            CardFace.objects.card_filter_by_color_term(
                selected_mana, search_term, has_colorless, has_color
            )

            request.session[str(self.term)] = search_term
            request.session[str(self.mana)] = selected_mana
            request.session[str(self.cards)] = filtered_card_list
            request.session[str(self.clear)] = True
        return redirect('/user_card_list?user_id='+str(request.user.id)+'&wish='+str(wish))

    def get(self, request):
        SessionManager.clear_other_session_data(request, SessionManager.UserCard)
        user_id = request.GET.get('user_id', -1)
        wish = False
        if request.GET.get('wish', 'False') == 'True':
            wish = True

        init_mana_list = Symbol.get_base_symbols()
        try:
            search_term = request.session[str(self.term)]
            selected_mana = request.session[str(self.mana)]
            card_list = request.session[str(self.cards)]
            clear_search = request.session[str(self.clear)]
        except KeyError:
            search_term = request.session[str(self.term)] = ""
            selected_mana = request.session[str(self.mana)] = []
            card_list = request.session[str(self.cards)] = UserCard.objects.get_user_card(user_id, wish, [], False, False,"")
            clear_search = request.session[str(self.clear)] = False

        mana_list = []
        for init_mana in init_mana_list:
            if init_mana.symbol in selected_mana:
                mana_list.append(
                    {'symbol': init_mana.symbol, 'checked': True, 'image_url': init_mana.image_url,
                     'id': init_mana.id})
            else:
                mana_list.append(
                    {'symbol': init_mana.symbol, 'checked': False, 'image_url': init_mana.image_url,
                     'id': init_mana.id})

        card_list_split = list(card_list.split("},"))
        if card_list_split[0] == '':
            card_list_split = []
        page = request.GET.get('page', 1)
        paginator = Paginator(card_list_split, 20)
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards,
                   'search_Term': search_term, 'mana_list': mana_list, 'user_card_list_clear': clear_search,
                   'user_id': str(user_id), 'wish': str(wish)}
        return render(request, 'Users/Profile/ProfileCards/user_card_list.html', context)


class NenniUserProfile(View):
    user = User

    @login_required
    def post(self, request):
        logger.info("Run: user_profile; Params: " + json.dumps(request.GET.dict()))
        user_id = request.GET.get('user_id', -1)

        if 'view_all_card' in request.POST:
            return HttpResponseRedirect(reverse('user_card_list') + '?user_id='+str(user_id)+'&wish='+str(False))
        elif 'view_all_wish' in request.POST:
            return HttpResponseRedirect(reverse('user_card_list') + '?user_id='+str(user_id)+'&wish='+str(True))
        elif 'bulk_add_card' in request.POST:
            return HttpResponseRedirect(reverse('user_card_bulk') + '?user_id='+str(user_id)+'&wish='+str(False))
        elif 'bulk_add_wish' in request.POST:
            return HttpResponseRedirect(reverse('user_card_bulk') + '?user_id='+str(user_id)+'&wish='+str(True))
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
             request.session['user_search_card_cards'] = UserCard.objects.get_user_card(user_id, False, [], False, False, "")
             request.session['user_clear_card_search'] = False
        elif 'user_search_card' in request.POST:
            search_term = request.POST.get('user_search_card_term')
            request.session['user_search_card_term'] = search_term
            request.session['user_search_card_cards'] = UserCard.objects.get_user_card(user_id, False, [], False, False, search_term)
            request.session['user_clear_card_search'] = True
        elif 'user_clear_wish_search' in request.POST:
            request.session['user_search_wish_term'] = ""
            request.session['user_search_wish_cards'] = UserCard.objects.get_user_card(user_id, True, [], False, False, "")
            request.session['user_clear_wish_search'] = False
        elif 'user_search_wish' in request.POST:
            search_term = request.POST.get('user_search_wish_term')
            request.session['user_search_wish_term'] = search_term
            request.session['user_search_wish_cards'] = UserCard.objects.get_user_card(user_id, True, [], False, False, search_term)
            request.session['user_clear_wish_search'] = True

        return redirect('/user_profile?user_id=' + str(user_id) + '&deck_page=' + str(deck_page) + '&card_page=' +
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
        SessionManager.clear_other_session_data(request, SessionManager.Profile)

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
            deck_page = request.GET.get('deckPage', -1)
            if deck_page == -1:
                deck_page = request.session['deck_page']
        except KeyError:
            deck_page = request.GET.get('deckPage', 1)
            request.session['deck_page'] = deck_page

        try:
            card_page = request.GET.get('cardPage', -1)
            if card_page == -1:
                card_page = request.session['card_page']
        except KeyError:
            card_page = request.GET.get('cardPage', 1)
            request.session['card_page'] = card_page

        try:
            wish_page = request.GET.get('wishPage', -1)
            if wish_page == -1:
                wish_page = request.session['wish_page']
        except KeyError:
            wish_page = request.GET.get('wishPage', 1)
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
            user_search_card_cards = request.session['user_search_card_cards'] = UserCard.objects.get_user_card(user_id, False, [], False, False, "")
            user_clear_card_search = request.session['user_clear_card_search'] = False

        try:
            user_search_wish_term = request.session['user_search_wish_term']
            user_search_wish_cards = request.session['user_search_wish_cards']
            user_clear_wish_search = request.session['user_clear_wish_search']
        except KeyError:
            user_search_wish_term = request.session['user_search_wish_term'] = ""
            user_search_wish_cards = request.session['user_search_wish_cards'] = UserCard.objects.get_user_card(user_id, True, [], False, False, "")
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

        if str(self.clear) in request.POST:
            request.session[str(self.term)] = ""
            request.session[str(self.cards)] = CardFace.objects.card_face_avatar_filter('')
            request.session[str(self.clear)] = False
        if str(self.term) in request.POST:
            avatar_search_term = request.session[str(self.term)] = request.POST.get(str(self.term))
            request.session[str(self.cards)] = CardFace.objects.card_face_avatar_filter(avatar_search_term)
            request.session[str(self.clear)] = True
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
        SessionManager.clear_other_session_data(request, SessionManager.Avatar)
        user_id = request.GET.get('user_id', -1)

        try:
            avatar_search_term = request.session[str(self.term)]
            avatar_card_list = request.session[str(self.cards)]
            avatar_clear_search = request.session[str(self.clear)]
        except KeyError:
            avatar_search_term = request.session[str(self.term)] = ""
            avatar_card_list = request.session[str(self.cards)] = CardFace.objects.card_face_avatar_filter('')
            avatar_clear_search = request.session[str(self.clear)] = False

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