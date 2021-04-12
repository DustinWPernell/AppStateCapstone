import json
import logging
from json import JSONDecodeError

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View

from Collection.models import Symbol
from Models.Deck import DeckManager
from Users.models import UserProfile
from static.python.session_manager import SessionManager

logger = logging.getLogger(__name__)

class Deck_Database(View):
    def post(self, request):
        logger.info("POST: collection_display;")
        init_mana_list = Symbol.get_base_symbols()

        if 'collection_deck_clear_search' in request.POST:
            request.session['collection_deck_search_Term'] = ""
            request.session['collection_deck_selected_mana'] = []
            request.session['collection_deck_deck_list'] = DeckManager.get_deck_list()
            request.session['collection_deck_clear'] = False
            request.session['collection_deck_deck_full'] = False
        elif 'collection_deck_full_list' in request.POST:
            request.session['collection_deck_search_Term'] = "Full List"
            request.session['collection_deck_selected_mana'] = []
            request.session['collection_deck_deck_list'] = DeckManager.get_deck_full_list()
            request.session['collection_deck_clear'] = True
            request.session['collection_deck_deck_full'] = True
        else:
            text = request.POST.get('collection_deck_search_Term')
            if text == "Full List":
                text = request.session['collection_deck_search_Term'] = ""
            search_term = text
            selected_mana = []
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
                if has_colorless:
                    filtered_deck_list = DeckManager.deck_filter_by_color_term_colorless(
                        selected_mana, search_term
                    )
                else:
                    filtered_deck_list = DeckManager.deck_filter_by_color_term(
                        selected_mana, search_term
                    )
            else:
                filtered_deck_list = DeckManager.get_deck_by_term(
                    search_term
                )
            request.session['collection_deck_search_Term'] = search_term
            request.session['collection_deck_selected_mana'] = selected_mana
            request.session['collection_deck_deck_list'] = filtered_deck_list
            request.session['collection_deck_clear'] = True
            request.session['collection_deck_deck_full'] = False
        return redirect('deck_database')

    def get(self, request):
        """Display entire card database.

        Retrieves all cards from database in alphabetical order and displays them based on what 'page' is in request.

        @param request:

        :todo: Loading image for long searches
        """
        logger.info("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
        SessionManager.clear_other_session_data(request, SessionManager.Deck_Search)

        init_mana_list = Symbol.get_base_symbols()
        try:
            search_term = request.session['collection_deck_search_Term']
            selected_mana = request.session['collection_deck_selected_mana']
            deck_list = request.session['collection_deck_deck_list']
            clear_search = request.session['collection_deck_clear']
            full_list = request.session['collection_deck_deck_full']
        except KeyError:
            search_term = request.session['collection_deck_search_Term'] = ""
            selected_mana = request.session['collection_deck_selected_mana'] = []
            deck_list = request.session['collection_deck_deck_list'] = DeckManager.get_deck_list()
            clear_search = request.session['collection_deck_clear'] = False
            full_list = request.session['collection_deck_deck_full'] = False


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

        deck_list_split = list(deck_list.split("},"))

        page = request.GET.get('page', 1)
        paginator = Paginator(deck_list_split, 50)
        try:
            decks = paginator.page(page)
        except PageNotAnInteger:
            decks = paginator.page(1)
        except EmptyPage:
            decks = paginator.page(paginator.num_pages)


        try:
            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            context = {'font_family': font_family, 'should_translate': should_translate, 'pages': decks,
                       'search_Term': search_term, 'mana_list': mana_list, 'clearSearch': clear_search,
                       'full_list': full_list}
            return render(request, 'Collection/collection_display.html', context)
        except JSONDecodeError:
            request.session['collection_deck_search_Term'] = ""
            request.session['collection_deck_selected_mana'] = []
            request.session['collection_deck_deck_list'] = DeckManager.get_deck_list()
            request.session['collection_deck_clear'] = False
            request.session['collection_deck_deck_full'] = False
            message = "Invalid search. Please try again."
            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            context = {'font_family': font_family, 'should_translate': should_translate, 'message': message}
            return render(request, 'error.html', context)

class Deck_Display(View):
    def get(self, request, deck_id):
        logger.info("Run: deck_display; Params: " + json.dumps(request.GET.dict()))
        try:
            deck = Deck.get_deck_by_deck(deck_id)
            deck_cards = DeckCards.build_json_by_deck_user(deck_id, request.user.id, False)
            side_cards = DeckCards.build_json_by_deck_user(deck_id, request.user.id, True)
            user_profile = UserProfile.get_profile_by_user(deck.deck_user)
            created_by = UserProfile.get_profile_by_user(deck.created_by)
            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            context = {'font_family': font_family, 'should_translate': should_translate,
                       'auth': request.user.is_authenticated,
                       'deck': deck, 'deck_cards': deck_cards, 'side_cards': side_cards,
                       'user_profile': user_profile, 'created_by': created_by}
            return render(request, 'Collection/deck_display.html', context)

        except DeckCards.DoesNotExist:
            message = "Deck ID incorrect.\nPlease check ID."
            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            context = {'font_family': font_family, 'should_translate': should_translate, 'message': message}
            return render(request, 'error.html', context)