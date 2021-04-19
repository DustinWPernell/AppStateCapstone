import html
import logging


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render, redirect
from django.views import View

from Models import DeckType
from Models.CardFace import CardFace
from Models.Deck import Deck
from Users.models import UserProfile, UserCards
from static.python.session_manager import SessionManager

logger = logging.getLogger(__name__)


class Manage_Cards(View):
    user = User

    def post(self, request, user_id, deck_id):
        user_profile_obj = UserProfile.get_profile_by_user(user_id)

# region Page numbers

        try:
            card_page = request.GET.get('user_card_page', -1)
            if card_page == -1:
                card_page = request.session['user_card_page']
        except KeyError:
            card_page = request.GET.get('user_card_page', 1)
            request.session['user_card_page'] = card_page

        try:
            all_card_page = request.GET.get('all_card_page', -1)
            if all_card_page == -1:
                all_card_page = request.session['all_card_page']
        except KeyError:
            all_card_page = request.GET.get('all_card_page', 1)
            request.session['all_card_page'] = all_card_page

        try:
            wish_card_page = request.GET.get('wish_card_page', -1)
            if wish_card_page == -1:
                wish_card_page = request.session['wish_card_page']
        except KeyError:
            wish_card_page = request.GET.get('wish_card_page', 1)
            request.session['wish_card_page'] = wish_card_page

# endregion

        if 'user_deck_card_clear' in request.POST:
            del request.session['user_deck_card_search_term']
            del request.session['user_deck_card_search_list']
            request.session['user_deck_card_search_clear'] = False
        elif 'user_deck_search_card' in request.POST:
            search_term = request.POST.get('user_deck_card_search_term')
            user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, False)
            card_id_list = []
            for card_list_obj in user_card_obj_term:
                if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                    card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)

            request.session['user_deck_card_search_term'] = search_term
            request.session['user_deck_card_search_list'] = card_id_list
            request.session['user_deck_card_search_clear'] = True
        elif 'user_all_card_clear' in request.POST:
            del request.session['user_all_card_search_term']
            del request.session['user_all_card_search_list']
            request.session['user_all_card_search_clear'] = False
        elif 'user_all_search_card' in request.POST:
            search_term = request.POST.get('user_all_card_search_term')
            user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, True)
            card_id_list = []
            for card_list_obj in user_card_obj_term:
                if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                    card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)
            request.session['user_all_card_search_term'] = search_term
            request.session['user_all_card_search_list'] = card_id_list
            request.session['user_all_card_search_clear'] = True
        elif 'user_wish_card_clear' in request.POST:
            del request.session['user_wish_card_search_term']
            del request.session['user_wish_card_search_list']
            request.session['user_wish_card_search_clear'] = False
        elif 'user_wish_search_card' in request.POST:
            search_term = request.POST.get('user_wish_card_search_term')
            user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, True)
            card_id_list = []
            for card_list_obj in user_card_obj_term:
                if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                    card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)
            request.session['user_wish_card_search_term'] = search_term
            request.session['user_wish_card_search_list'] = card_id_list
            request.session['user_wish_card_search_clear'] = True
        elif 'save_cards' in request.POST:
            card_list = request.SESSION['user_card_selected_list'] = request.POST.get('user_card_selected_list')



        return redirect('../' + str(user_id) + '?user_card_page=' +
                        str(card_page) + '&all_card_page=' + str(all_card_page) + '&wish_card_page=' + str(
            wish_card_page))

    @login_required
    def get(self, request, user_id, deck_id):

        user_profile_obj = UserProfile.get_profile_by_user(user_id)

# region Page numbers

        try:
            card_page = request.GET.get('user_card_page', -1)
            if card_page == -1:
                card_page = request.session['user_card_page']
        except KeyError:
            card_page = request.GET.get('user_card_page', 1)
            request.session['user_card_page'] = card_page

        try:
            all_card_page = request.GET.get('all_card_page', -1)
            if all_card_page == -1:
                all_card_page = request.session['all_card_page']
        except KeyError:
            all_card_page = request.GET.get('all_card_page', 1)
            request.session['all_card_page'] = all_card_page

        try:
            wish_card_page = request.GET.get('wish_card_page', -1)
            if wish_card_page == -1:
                wish_card_page = request.session['wish_card_page']
        except KeyError:
            wish_card_page = request.GET.get('wish_card_page', 1)
            request.session['wish_card_page'] = wish_card_page

# endregion

# region Cards from sessions

        try:
            card_list = request.SESSION['deck_card_list']
        except KeyError:
            card_list = Deck.objects.build_json_by_deck_user()

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
            search_all_term = request.session['user_search_all_card_term']
            user_all_card_obj_list = request.session['user_all_cards']
            user_all_cards = UserCards.get_user_card_by_oracle_list(user_all_card_obj_list, user_profile_obj.user)
            user_clear_all_search = request.session['user_clear_all_search']
        except KeyError:
            user_all_cards = UserCards.get_user_card_term(user_profile_obj.user, "", True)
            search_all_term = "Search"
            user_clear_all_search = request.session['user_clear_all_search'] = False

        try:
            search_wish_term = request.session['user_search_wish_card_term']
            user_wish_card_obj_list = request.session['user_wish_cards']
            user_wish_cards = UserCards.get_user_card_by_oracle_list(user_wish_card_obj_list, user_profile_obj.user)
            user_clear_wish_search = request.session['user_clear_wish_search']
        except KeyError:
            user_wish_cards = UserCards.get_user_card_term(user_profile_obj.user, "", True)
            search_wish_term = "Search"
            user_clear_wish_search = request.session['user_clear_wish_search'] = False

# endregion

# region Paginators

        card_paginator = Paginator(user_cards, 20)
        try:
            user_cards = card_paginator.page(card_page)
        except PageNotAnInteger:
            user_cards = card_paginator.page(1)
        except EmptyPage:
            user_cards = card_paginator.page(card_paginator.num_pages)

        all_paginator = Paginator(user_all_cards, 20)
        try:
            all_cards = all_paginator.page(all_card_page)
        except PageNotAnInteger:
            all_cards = all_paginator.page(1)
        except EmptyPage:
            all_cards = all_paginator.page(all_paginator.num_pages)

        wish_paginator = Paginator(user_wish_cards, 20)
        try:
            wish_cards = wish_paginator.page(wish_card_page)
        except PageNotAnInteger:
            wish_cards = wish_paginator.page(1)
        except EmptyPage:
            wish_cards = wish_paginator.page(wish_paginator.num_pages)

# endregion

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {
            'font_family': font_family, 'should_translate': should_translate,
        }
        return render(request, 'Users/Profile/ProfileDecks/modify_cards_deck.html', context)


class Manage_Deck(View):
    user = User
    def post(self, request, user_id, deck_id):
        if 'submitDeck' in request.POST:
            deck_name_field = html.escape(request.POST.get('deck_name_field'))
            deck_privacy_field = request.POST.get('deck_privacy_field') == "True"
            deck_description_field = (html.escape(request.POST.get('deck_description_field'))).rstrip().replace(',', '&#44;')
            deck_type_field = request.POST.get('deck_type_field')

            if deck_id == "-1":
                try:
                    color_id = '{C}'
                    Deck.objects.deck_create(
                        deck_name_field,
                        int(deck_type_field),
                        deck_privacy_field,
                        deck_description_field,
                        color_id,
                        request.user.username,
                        request.user.username
                    )
                except ObjectDoesNotExist:
                    messages.error(request, "Object does not exist. Deck not created.")
                except ValueError:
                    messages.error(request, "Value Error. Deck not created.")

            else:
                try:
                    deck_type_obj = DeckType.objects.get(id=int(deck_type_field))

                    Deck.objects.deck_update(
                        deck_id=deck_id,
                        deck_name_field=deck_name_field,
                        deck_type_field=deck_type_obj,
                        deck_privacy_field=deck_privacy_field,
                        deck_description_field=deck_description_field
                    )
                except ObjectDoesNotExist :
                    messages.error(request, "Object does not exist. Deck not modified.")

        return redirect('../' + str(deck_id))
            # 'Users/user_profile/' + str(user_id) + '/manage_deck/' + str(deck_id) + '/')

    @login_required
    def get(self, request, user_id, deck_id):
        """Displays new deck page

        Redirects to new deck page

        @param request:

        :todo: Finish new deck page
        """
        try:
            deck_obj = Deck.objects.get_deck(request.user.username, deck_id)
            deck_type_obj = Deck.objects.get_deck_type(deck_id)
            deck_private = deck_obj.is_private

            if deck_obj.deck_user != request.user.username:
                deck_obj = deck_obj.create_copy(request.user)
                messages.success(request, "Deck copied to your profile.")

        except ObjectDoesNotExist :
            deck_obj = "new"
            deck_type_obj = '{"type_id": "1"}'
            deck_private = UserProfile.get_deck_private(request.user)

        deck_types = DeckType.objects.get_types()
        deck_type_split = list(deck_types.split("},"))

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {
            'font_family': font_family, 'should_translate': should_translate,
            'deck_obj': deck_obj, 'deck_types': deck_type_split, 'deck_id': deck_id,
            'is_private': deck_private, 'deck_type_obj': deck_type_obj
        }
        return render(request, 'Users/Profile/ProfileDecks/modify_deck.html', context)


class Commander_Picker(View):
    user = User

    def post(self, request, user_id, deck_id):
        if 'user_clear_commander_search' in request.POST:
            request.session['user_search_commander_term'] = ""
            request.session['user_search_commander_cards'] = CardFace.objects.card_face_commander_filter("")
            request.session['user_clear_commander_search'] = False
        else:
            search_term = request.POST.get('user_search_commander_term')
            request.session['user_search_commander_term'] = search_term
            request.session['user_search_commander_cards'] = CardFace.objects.card_face_commander_filter(search_term)
            request.session['user_clear_commander_search'] = True

        return redirect('../' + str(deck_id) + "/commander")
    @login_required
    def get(self, request, user_id, deck_id):
        """Displays list for selecting new avatar

        Displays full list of card art with search by name feature.

        @param request:

        :todo: None
        """
        try:
            search_term = request.session['user_search_commander_term']
            commander_list = request.session['user_search_commander_cards']
            clear_commander = request.session['user_clear_commander_search']
        except KeyError:
            search_term = request.session['user_search_commander_term']
            commander_list = request.session['user_search_commander_cards']
            clear_commander = request.session['user_clear_commander_search']

        commander_list_split = list(commander_list.split("},"))
        if commander_list_split[0] == '':
            commander_list_split = []
        page = request.GET.get('page', 1)
        paginator = Paginator(commander_list_split, 20)
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards,
                   'user_search_commander_term': search_term, 'user_clear_commander_search': clear_commander}
        return render(request, 'Users/Profile/ProfileDecks/select_commander.html', context)