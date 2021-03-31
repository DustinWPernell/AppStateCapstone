import json
import logging

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Collection.models import CardFace, Symbol, CardIDList, Rule, Deck, DeckCards
from Users.models import UserCards, UserProfile

logger = logging.getLogger(__name__)


# Create your views here.
def card_display(request, oracle_id):
    """Display individual cards.

    Retrieves card information from the database based on what 'card_id' is in request. Then displays the card data.

    @param request:
    @param oracle_id: Oracle ID for current card

    :todo: Touch up data display/layout
    """
    logger.info("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    try:
        card_obj = CardIDList.get_card_by_oracle(oracle_id)

        card_faces = CardFace.get_face_by_card(card_obj.card_id)

        card_set_list = CardFace.get_card_sets(oracle_id)
        card_set_list.sort(key=lambda item: item.get("set_name"))

        rulings_list = Rule.objects.filter(oracle_id=oracle_id).order_by('-pub_date')

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        if request.user.is_authenticated:
            try:
                user_card = UserCards.get_user_card_by_oracle(oracle_id, request.user)
                notes = user_card.notes
                has_notes = notes != ""
                context = {'font_family': font_family, 'should_translate': should_translate, 'card': card_faces,
                           'faces': card_faces, 'set_info': card_set_list,
                           'has_card': True, 'user_card': user_card, 'has_notes': has_notes,
                           'rulings': rulings_list, 'has_rules': len(rulings_list) > 0,
                           'auth': request.user.is_authenticated}
            except UserCards.DoesNotExist:
                context = {'font_family': font_family, 'should_translate': should_translate, 'card': card_faces,
                           'faces': card_faces, 'set_info': card_set_list,
                           'has_card': False,
                           'rulings': rulings_list, 'has_rules': len(rulings_list) > 0,
                           'auth': request.user.is_authenticated}


        else:
            context = {'font_family': font_family, 'should_translate': should_translate, 'card': card_faces,
                       'faces': card_faces, 'set_info': card_set_list,
                       'rulings': rulings_list, 'has_rules': len(rulings_list) > 0,
                       'auth': request.user.is_authenticated}

        return render(request, 'Collection/card_display.html', context)

    except CardIDList.DoesNotExist:
        message = "Oracle ID incorrect.\nPlease check ID."
        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'message': message}
        return render(request, 'error.html', context)


def collection_display(request):
    """Display entire card database.

    Retrieves all cards from database in alphabetical order and displays them based on what 'page' is in request.

    @param request:

    :todo: Loading image for long searches
    """
    logger.info("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
    init_mana_list = Symbol.get_base_symbols()
    card_id_list_full = CardIDList.get_card_ids()
    full_card_list_all = []
    for card_list_obj in card_id_list_full:
        full_card_list_all.append(card_list_obj.card_id)

    selected_mana = []
    search_term = 'Search'
    if request.method == 'POST':
        if 'clearSearch' in request.POST:
            del request.session['search']
            del request.session['searchTerm']
            del request.session['selected_mana']
            del request.session['card_id_list']
        else:
            text = request.POST.get('SearchTerm')
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
                card_id_list = []
                colorless = ['{C}', '', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                             '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                             '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}']

                has_colorless = any(item in selected_mana for item in colorless)
                if has_colorless:
                    filtered_card_list = CardFace.card_face_filter_by_card_color_term_colorless(
                        full_card_list_all, selected_mana, search_term
                    )
                else:
                    filtered_card_list = CardFace.card_face_filter_by_card_color_term(
                        full_card_list_all, selected_mana, search_term
                    )

                for card_list_obj in filtered_card_list:
                    if card_list_obj.legal.card_obj.card_id not in card_id_list:
                        card_id_list.append(card_list_obj.legal.card_obj.card_id)
            else:
                filtered_card_list = CardFace.card_face_filter_by_card_term(
                    full_card_list_all, search_term
                )

                card_id_list = []
                for card_list_obj in filtered_card_list:
                    if card_list_obj.legal.card_obj.card_id not in card_id_list:
                        card_id_list.append(card_list_obj.legal.card_obj.card_id)

            request.session['search'] = True
            request.session['searchTerm'] = search_term
            request.session['selected_mana'] = selected_mana
            request.session['card_id_list'] = card_id_list
        return redirect('card_database')
    else:
        try:
            search_term = request.session['searchTerm']
            selected_mana = request.session['selected_mana']
            card_id_list = request.session['card_id_list']
            clear_search = True
        except KeyError:
            card_id_list = full_card_list_all
            clear_search = False

    mana_list = []
    for init_mana in init_mana_list:
        if init_mana.symbol in selected_mana:
            mana_list.append(
                {'symbol': init_mana.symbol, 'checked': True, 'image_url': init_mana.image_url, 'id': init_mana.id})
        else:
            mana_list.append(
                {'symbol': init_mana.symbol, 'checked': False, 'image_url': init_mana.image_url, 'id': init_mana.id})

    card_list = CardFace.get_face_list_by_card(card_id_list)

    page = request.GET.get('page', 1)

    paginator = Paginator(card_list, 20)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards,
               'SearchTerm': search_term, 'mana_list': mana_list, 'clearSearch': clear_search}
    return render(request, 'Collection/collection_display.html', context)


def deck_list(request):
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


def deck_display(request, deck_id):
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


def collection_index(request):
    """Display landing page for collections.

    This page is not currently used by the application.

    @param request:

    :todo: None
    """
    logger.info("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")


def update_user_card_data(request, oracle_id):
    """Updates quantity of card.

    Updates the number of cards owned by user based on POST data

    @param request:
    @param oracle_id: Card ID for current card

    :todo: None
    """
    if 'addCards' in request.POST:
        card_quantity = int(request.POST['quantity'])
        user_card_id = request.POST['user_card_id']
        card_notes = request.POST['notes']
        if card_quantity <= 0:
            card_quantity = 1
        if user_card_id == '':
            UserCards.objects.create(
                id=str(request.user.id) + ':' + str(oracle_id),
                card=CardFace.get_face_by_card(CardIDList.get_card_by_oracle(oracle_id).card_id)[0],
                user=request.user,
                oracle_id=oracle_id,
                wish=False,
                quantity=card_quantity,
                notes=card_notes
            )
        else:
            user_card = UserCards.objects.get(id=str(user_card_id))
            user_card.wish = False
            user_card.quantity = card_quantity
            user_card.notes = card_notes
            user_card.save()

        messages.success(request, 'Added ' + str(card_quantity) + ' card(s) to your collection.')
    elif 'wishCards' in request.POST:
        card_quantity = int(request.POST['quantity'])
        user_card_id = request.POST['user_card_id']
        card_notes = request.POST['notes']
        if card_quantity <= 0:
            card_quantity = 1
        if user_card_id == '':
            UserCards.objects.create(
                id=str(request.user.id) + ':' + str(oracle_id),
                card=CardFace.get_face_by_card(CardIDList.get_card_by_oracle(oracle_id).card_id)[0],
                user=request.user,
                oracle_id=oracle_id,
                wish=True,
                quantity=card_quantity,
                notes=card_notes
            )
        else:
            user_card = UserCards.objects.get(id=str(user_card_id))
            user_card.wish = True
            user_card.quantity = card_quantity
            user_card.notes = card_notes
            user_card.save()

        messages.success(request, 'Added card to wish list.')
    elif 'remove' in request.POST:
        user_card_id = request.POST['user_card_id']
        user_card = UserCards.objects.get(id=str(user_card_id))
        user_card.quantity = 0
        user_card.wish = False
        user_card.save()

        messages.error(request, 'Removed card(s) from collection.')
    elif 'update' in request.POST:
        user_card_id = request.POST['user_card_id']
        card_quantity = request.POST['quantity']
        user_card = UserCards.objects.get(id=str(user_card_id))
        user_card.quantity = card_quantity
        user_card.save()

        messages.success(request, 'Updated quantity of cards.')
    elif 'notes_button' in request.POST:
        user_card_id = request.POST['user_card_id']
        card_notes = request.POST['notes']
        user_card = UserCards.objects.get(id=str(user_card_id))
        user_card.notes = card_notes
        user_card.save()

        messages.success(request, 'Updated notes for cards.')
    return redirect('../' + oracle_id)
