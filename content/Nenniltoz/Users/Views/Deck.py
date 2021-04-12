import logging


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render, redirect
from django.views import View

from Collection.models import CardFace, Symbol
from Models.Deck import DeckManager
from Users.models import UserProfile, UserCards

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
    user = User

    def create_copy(self, request, deck_obj):
# region Copy Deck
        new_deck = Deck.objects.create(
            name=deck_obj.name,
            deck_type=deck_obj.deck_type,
            is_private=UserProfile.get_deck_private(request.user),
            image_url=deck_obj.image_url,
            description=deck_obj.description,
            commander_id=deck_obj.commander_id,
            commander_name=deck_obj.commander_name,
            commander_file=deck_obj.commander_file,
            commander_oracle=deck_obj.commander_oracle,
            color_id=deck_obj.color_id,
            created_by=deck_obj.created_by,
            deck_user=request.user.id,
            is_pre_con=False
        )
# endregion

# region Copy Cards
        deck_cards = DeckCards.deck_card_by_deck_user()

        for card in deck_cards:
            DeckCards.objects.create(
                deck=new_deck,
                card_oracle = card.card_oracle,
                card_name = card.card_name,
                card_file = card.card_file,
                card_search = card.card_search,
                quantity = card.quantity,
                sideboard = card.sideboard,
            )
# endregion
        return new_deck

    @login_required
    def get(self, request, user_id, deck_id):
        """Displays new deck page

        Redirects to new deck page

        @param request:

        :todo: Finish new deck page
        """

        try:
            deck_obj = DeckManager.get_deck_by_deck(int(deck_id))

            if deck_obj.deck_user is not user_id:
                deck_obj = self.create_copy(request, deck_obj)
                messages.success(request, "Deck copied to your profile.")

        except DeckManager.DoesNotExist:
            deck_obj = "new"

        deck_types = DeckManager.get_types()

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {
            'font_family': font_family, 'should_translate': should_translate,
            'deck_obj': deck_obj, 'deck_types': deck_types,
        }
        return render(request, 'Users/Profile/ProfileDecks/modify_deck.html', context)


class Save_Deck(View):
    def post(self, request, user_id, deck_id):
        deck_name = request.session['deck_name'] = request.POST.get('deck_name')
        is_private = request.session['is_private'] = request.POST.get('is_private')
        image_url = request.session['image_url'] = request.POST.get('image_url')
        description = request.session['description'] = request.POST.get('description')
        deck_type = request.session['deck_type'] = request.POST.get('deck_type')
        commander = request.session['commander'] = request.POST.get('commander')

        if 'create_deck' in request.POST:
            deck_type_obj = DeckType.get_deck_type_by_type(deck_type)
            color_id = ''
            if deck_type_obj.has_commander:
                try:
                    commander_obj = CardFace.get_face_by_card(commander)
                    commander_id = commander_obj.legal.card_obj.card_id
                    commander_name=commander_obj.name
                    commander_file=commander_obj.image_file
                    commander_oracle=commander_obj.legal.card_obj.oracle_id
                    for sym in Symbol.objects.all():
                        color_id = color_id + sym.symbol
                except CardFace.DoesNotExist:
                    commander_id= None
                    commander_name= None
                    commander_file= None
                    commander_oracle= None
                    messages.error(request, "Commander not found. Leaving blank")
            else:
                commander_id = None
                commander_name = None
                commander_file = None
                commander_oracle = None

            new_deck = Deck.objects.create(
                name=deck_name,
                deck_type=deck_type_obj,
                is_private=is_private == 'True',
                image_url=image_url,
                description=description,
                commander_id=commander_id,
                commander_name=commander_name,
                commander_file=commander_file,
                commander_oracle=commander_oracle,
                color_id=color_id,
                created_by=request.user.id,
                deck_user=request.user.id,
                is_pre_con=(request.user.username == "Preconstructed")
            )
            deck_id = new_deck.id
        elif 'update_deck' in request.POST:
            try:
                deck_obj = Deck.get_deck_by_deck(deck_id)
                deck_type_obj = DeckType.get_deck_type_by_type(deck_type)

                color_id = ''
                if deck_type_obj.has_commander:
                    try:
                        commander_obj = CardFace.get_face_by_card(commander)
                        commander_id = commander_obj.legal.card_obj.card_id
                        commander_name = commander_obj.name
                        commander_file = commander_obj.image_file
                        commander_oracle = commander_obj.legal.card_obj.oracle_id
                        for sym in Symbol.objects.all():
                            color_id = color_id + sym.symbol
                    except CardFace.DoesNotExist:
                        commander_id = None
                        commander_name = None
                        commander_file = None
                        commander_oracle = None
                        messages.error(request, "Commander not found. Leaving blank")
                else:
                    commander_id = None
                    commander_name = None
                    commander_file = None
                    commander_oracle = None

                deck_obj.deck_name = deck_name
                deck_obj.deck_type = deck_type_obj
                deck_obj.is_private = is_private == 'True'
                deck_obj.image_url = image_url
                deck_obj.description = description
                deck_obj.commander_id=commander_id,
                deck_obj.commander_name=commander_name,
                deck_obj.commander_file=commander_file,
                deck_obj.commander_oracle=commander_oracle,
                deck_obj.color_id=color_id,
                deck_obj.save()
            except DeckType.DoesNotExist:
                messages.error(request, "Deck type not defined. Deck not modified.")
            except Deck.DoesNotExist:
                messages.error(request, "Deck not found. Deck not modified.")

        return redirect('Users/user_profile/' + str(user_id) + '/manage_deck/' + str(deck_id) + '/')


class Commander_Picker(View):
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
            card_list = CardFace.card_face_commander_filter_by_name_term(search_term).order_by('name')
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
            card_list = CardFace.card_face_commander_filter_by_name_term(search_term).order_by('name')
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