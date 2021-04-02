import json
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View

from Collection.models import Symbol, Deck, DeckCards
from Users.models import UserProfile

logger = logging.getLogger(__name__)

class Deck_Database(View):
    def get(self, request):
        """Display entire card database.

            Retrieves all cards from database in alphabetical order and displays them based on what 'page' is in request.

            @param request:

            :todo: Loading image for long searches
            """
        logger.debug("Run: deck_display; Params: " + json.dumps(request.GET.dict()))
        init_mana_list = Symbol.objects.filter(symbol__in=['{W}', '{U}', '{B}', '{R}', '{G}', '{C}', '{S}'])
        deck_list_obj = []
        selected_mana = []
        deck_id_list = []
        search_term = 'Search'
        if request.method == 'POST':
            if 'clearSearch' in request.POST:
                del request.session['deck_search']
                del request.session['deck_search_term']
                del request.session['deck_selected_mana']
                del request.session['deck_id_list']
            else:
                text = request.POST.get('SearchTerm')
                search_term = text
                selected_mana = []
                for selected in init_mana_list:
                    # Compiles a list of all selected mana color symbols
                    mana_ele = request.POST.get("mana-" + str(selected.id))
                    if mana_ele == '':
                        selected_mana.append(selected.symbol)
                        if selected.symbol == '{W}':
                            alt_mana = Symbol.objects.filter(
                                symbol__in=['{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}'])
                        elif selected.symbol == '{U}':
                            alt_mana = Symbol.objects.filter(
                                symbol__in=['{W/U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}'])
                        elif selected.symbol == '{B}':
                            alt_mana = Symbol.objects.filter(
                                symbol__in=['{W/B}', '{B/R}', '{B/G}', '{U/B}', '{2/B}', '{B/P}', '{HB}'])
                        elif selected.symbol == '{R}':
                            alt_mana = Symbol.objects.filter(
                                symbol__in=['{B/R}', '{U/R}', '{R/G}', '{R/W}', '{2/R}', '{R/P}', '{HR}'])
                        elif selected.symbol == '{G}':
                            alt_mana = Symbol.objects.filter(
                                symbol__in=['{B/G}', '{R/G}', '{G/W}', '{G/U}', '{2/G}', '{G/P}', '{HG}'])
                        elif selected.symbol == '{C}':
                            alt_mana = Symbol.objects.filter(
                                symbol__in=['', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                                            '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                                            '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}'])
                        else:
                            alt_mana = []

                        for am in alt_mana:
                            if am.symbol not in selected_mana:
                                selected_mana.append(am.symbol)
                if len(selected_mana) > 0:
                    # If any many color is selected, loop through selected list and filter by decks containing those colors
                    deck_id_list = []
                    colorless = ['{C}', '', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                                 '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                                 '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}']

                    # Retrieve all decks that are not private and colorId contains the selected colors,
                    # or name contains the search term, display the deck.
                    has_colorless = any(item in selected_mana for item in colorless)
                    # If colorless is selected, do not show colored decks that are also colorless.
                    if has_colorless:
                        filtered_deck_list = Deck.deck_filter_by_color_term_colorless(
                            request.user, selected_mana, search_term
                        )
                    else:
                        filtered_deck_list = Deck.deck_filter_by_color_term(
                            request.user, selected_mana, search_term
                        )
                    # Pulls the id's of the matched mana list and ensures it isn't already searched.
                    for deck_list_obj in filtered_deck_list:
                        if deck_list_obj.id not in deck_id_list:
                            deck_id_list.append(deck_list_obj.id)
                else:
                    filtered_deck_list = Deck.deck_filter_by_term(
                        request.user, search_term
                    )
                    # Pulls the id's of the matched mana list and ensures it isn't already searched.
                    for deck_list_obj in filtered_deck_list:
                        if deck_list_obj.id not in deck_id_list:
                            deck_id_list.append(deck_list_obj.id)

                # Stores search parameters for quicker reloads
                request.session['deck_search'] = True
                request.session['deck_search_term'] = search_term
                request.session['deck_selected_mana'] = selected_mana
                request.session['deck_id_list'] = deck_id_list
            return redirect('deck_list')
        else:
            try:
                search_term = request.session['deck_search_term']
                selected_mana = request.session['deck_selected_mana']
                deck_id_list = request.session['deck_id_list']
                clear_search = True
                deck_list_obj = Deck.get_deck_by_deck_list(deck_id_list)
            except KeyError:
                deck_list_obj = Deck.deck_filter_by_term(request.user, '')
                clear_search = False

        mana_list = []
        for init_mana in init_mana_list:
            # Goes through the mana symbols and checks to see what is selected. If selected, it checks it. If not, it doesn't.
            if init_mana.symbol in selected_mana:
                mana_list.append(
                    {'symbol': init_mana.symbol, 'checked': True, 'imageURL': init_mana.image_url, 'id': init_mana.id})
            else:
                mana_list.append(
                    {'symbol': init_mana.symbol, 'checked': False, 'imageURL': init_mana.image_url, 'id': init_mana.id})

        page = request.GET.get('page', 1)

        paginator = Paginator(deck_list_obj, 100)
        try:
            # Sets the paginator page to the page pulled from the url or 1.
            deck = paginator.page(page)
        except PageNotAnInteger:
            # If you enter something that isnt a number, you'll be taken back to the first page.
            deck = paginator.page(1)
        except EmptyPage:
            # If you enter a number that's too high, you be taken to the last page.
            deck = paginator.page(paginator.num_pages)

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        # Left is variable name, right is variable data.
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': deck,
                   'SearchTerm': search_term, 'mana_list': mana_list, 'clearSearch': clear_search}
        return render(request, 'Collection/deck_list.html', context)

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