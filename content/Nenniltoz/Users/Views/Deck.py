import logging


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render, redirect
from django.views import View

from Collection.models import CardFace, Deck, DeckType, DeckCards
from Users.models import UserProfile, UserCards

logger = logging.getLogger(__name__)

class Manage_Cards(View):
    @login_required
    def get(self, request, user_id):

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

        if request.method == 'POST':
            deck_name = request.session['deck_name'] = request.POST.get('deck_name')
            is_private = request.session['is_private'] = request.POST.get('is_private')
            image_url = request.session['image_url'] = request.POST.get('image_url')
            description = request.session['description'] = request.POST.get('description')
            deck_type = request.session['deck_type'] = request.POST.get('deck_type')
            commander = request.session['commander'] = request.POST.get('commander')

            if 'user_clear_user_card_search' in request.POST:
                del request.session['user_search_card_term']
                del request.session['user_cards']
                request.session['user_clear_card_search'] = False

            elif 'user_search_user_card' in request.POST:
                search_term = request.POST.get('user_search_card_term')
                user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, False)
                card_id_list = []
                for card_list_obj in user_card_obj_term:
                    if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                        card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)

                request.session['user_search_card_term'] = search_term
                request.session['user_cards'] = card_id_list
                request.session['user_clear_card_search'] = True

            elif 'user_clear_all_card_search' in request.POST:
                del request.session['user_search_all_term']
                del request.session['user_all_cards']
                request.session['user_clear_all_search'] = False

            elif 'user_search_all_card' in request.POST:
                search_term = request.POST.get('user_search_all_term')
                user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, True)
                card_id_list = []
                for card_list_obj in user_card_obj_term:
                    if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                        card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)

                request.session['user_search_all_term'] = search_term
                request.session['user_all_cards'] = card_id_list
                request.session['user_clear_all_search'] = True

            elif 'user_clear_wish_card_search' in request.POST:
                del request.session['user_search_wish_term']
                del request.session['user_wish_cards']
                request.session['user_clear_wish_search'] = False

            elif 'user_search_wish_card' in request.POST:
                search_term = request.POST.get('user_search_wish_term')
                user_card_obj_term = UserCards.get_user_card_term(user_profile_obj.user, search_term, True)
                card_id_list = []
                for card_list_obj in user_card_obj_term:
                    if card_list_obj.card.legal.card_obj.card_id not in card_id_list:
                        card_id_list.append(card_list_obj.card.legal.card_obj.oracle_id)

                request.session['user_search_wish_term'] = search_term
                request.session['user_wish_cards'] = card_id_list
                request.session['user_clear_wish_search'] = True

            elif 'save_cards' in request.POST:
                card_list = request.SESSION['deck_card_list'] = request.POST.get('hid_deck_card_list')



            return redirect('../' + str(user_id) + '?user_card_page=' +
                            str(card_page) + '&all_card_page=' + str(all_card_page) + '&wish_card_page=' + str(
                wish_card_page))

        # region Cards from sessions

        try:
            card_list = request.SESSION['deck_card_list']
        except KeyError:
            card_list = DeckCards.build_json_by_deck_user()

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
    @login_required
    def get(self, request, user_id, deck_id):
        """Displays new deck page

        Redirects to new deck page

        @param request:

        :todo: Finish new deck page
        """
        user_profile_obj = UserProfile.get_profile_by_user(user_id)

        if request.method == 'POST':
            deck_name = request.session['deck_name'] = request.POST.get('deck_name')
            is_private = request.session['is_private'] = request.POST.get('is_private')
            image_url = request.session['image_url'] = request.POST.get('image_url')
            description = request.session['description'] = request.POST.get('description')
            deck_type = request.session['deck_type'] = request.POST.get('deck_type')
            commander = request.session['commander'] = request.POST.get('commander')

            if 'create_deck' in request.POST:
                # todo make deck
                # js to load selected cards into deck / sideboard

                deck_type_obj = DeckType.get_deck_type_by_type(deck_type)

                if deck_type_obj.has_commander:
                    try:
                        commander_obj = CardFace.get_face_by_card(commander)
                    except CardFace.DoesNotExist:
                        commander_obj = None
                        messages.error(request, "Commander not found. Leaving blank")
                else:
                    commander_obj = None

                Deck.objects.create(
                    deck_name=deck_name,
                    deck_type=deck_type_obj,
                    is_private=is_private == 'True',
                    image_url=image_url,
                    description=description,
                    commander=commander_obj,
                    color_id="",
                    created_by=request.user.id,
                    is_pre_con=request.user.username == "Preconstructed"
                )

            elif 'update_deck' in request.POST:
                # todo make deck
                # js to load selected cards into deck / sideboard

                try:
                    deck_id = request.POST.get('deck_id')
                    deck_obj = Deck.get_deck_by_deck(deck_id)
                    deck_type_obj = DeckType.get_deck_type_by_type(deck_type)

                    if deck_type_obj.has_commander:
                        try:
                            commander_obj = CardFace.get_face_by_card(commander)
                        except CardFace.DoesNotExist:
                            commander_obj = None
                            messages.error(request, "Commander not found. Leaving blank")
                    else:
                        commander_obj = None

                    deck_obj.deck_name = deck_name
                    deck_obj.deck_type = deck_type_obj
                    deck_obj.is_private = is_private == 'True'
                    deck_obj.image_url = image_url
                    deck_obj.description = description
                    deck_obj.commander = commander_obj
                    deck_obj.save()
                except DeckType.DoesNotExist:
                    messages.error(request, "Deck type not defined. Deck not modified.")
                except Deck.DoesNotExist:
                    messages.error(request, "Deck not found. Deck not modified.")

            return redirect('../' + str(user_id))

        if int(deck_id) > -1:
            deck_obj = Deck.get_deck_by_deck(deck_id)
        else:
            deck_obj = "new"

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {
            'font_family': font_family, 'should_translate': should_translate,
            'deck_obj': deck_obj,
        }
        return render(request, 'Users/Profile/ProfileDecks/modify_deck.html', context)