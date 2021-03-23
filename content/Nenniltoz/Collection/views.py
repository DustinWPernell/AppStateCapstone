import json
import logging
import operator
from functools import reduce

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from google_trans_new import google_translator

from Collection.models import Card, CardFace, Symbol, CardSets, CardLayout, CardIDList, Rule, Legality, Deck
from Users.models import UserCards, UserProfile

logger = logging.getLogger(__name__)


# Create your views here.
def add_card(request, card_id):
    """Add cards to user collection

    Adds a card to either the users collection or wish list

    @param request:
    @param card_id: Card ID for current card

    :todo: None
    """
    user = request.user

    if 'addCards' in request.POST:
        card_quantity = int(request.POST['quantity'])
        if card_quantity == 0:
            card_quantity = 1
        UserCards.objects.create(
            cardID=card_id,
            user=user,
            quantity=card_quantity,
        )
    else:
        UserCards.objects.create(
            cardID=card_id,
            user=user,
            quantity=0,
        )
    return redirect('../' + card_id)


def card_display(request, card_id):
    """Display individual cards.

    Retrieves card information from the database based on what 'cardID' is in request. Then displays the card data.

    @param request:
    @param card_id: Card ID for current card

    :todo: Touch up data display/layout
    """
    logger.debug("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    card_obj = Card.objects.get(cardID=card_id)
    face_obj = CardFace.objects.filter(cardID_id=card_id)

    set_info = []
    card_sets = CardFace.objects.filter(name=face_obj[0].name)

    layouts = CardLayout.objects.filter(sides=2)
    layout_strings = []
    for lay in layouts:
        layout_strings.append(lay.layout)

    card_set_list = []
    for card_set_obj in card_sets:
        set_card_obj = Card.objects.get(cardID=card_set_obj.cardID_id)
        face_obj = CardFace.objects.filter(cardID_id=card_set_obj.cardID_id)
        card_set = CardSets.objects.get(order=card_set_obj.setOrder)

        if card_set.name not in card_set_list:
            card_set_list.append(card_set.name)

        if set_card_obj.layout in layout_strings:
            set_info.append(
                {'set_name': card_set.name, 'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].imageURL,
                 'card_image_two': face_obj[1].imageURL})
        else:
            set_info.append(
                {'set_name': card_set.name, 'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].imageURL,
                 'card_image_two': 'NONE'})

    rulings_list = Rule.objects.filter(oracleID=card_obj.oracleID).order_by('-pub_date')

    legalities = Legality.objects.get(cardID_id=card_obj.cardID)

    quantity = 0
    card_count = -1

    if request.user.is_authenticated:
        user_card = UserCards.objects.values('quantity').filter(
            Q(user=request.user) &
            Q(cardID=card_id)
        )

        if user_card.count() > 0:
            quantity = user_card[0]['quantity']
            card_count = quantity
    set_info.sort(key=lambda item: item.get("set_name"))

    font_family = UserProfile.get_font(request.user.id)
    should_translate = UserProfile.get_translate(request.user.id)
    context = {'font_family': font_family, 'should_translate': should_translate, 'card': card_obj, 'faces': face_obj, 'set_info': set_info, 'set_list': card_set_list,
               'rulings': rulings_list, 'has_rules': len(rulings_list) > 0, 'legal': legalities,
               'quantity': quantity, 'cardCount': card_count, 'auth': request.user.is_authenticated}
    return render(request, 'Collection/CardDisplay.html', context)


def collection_display(request):
    """Display entire card database.

    Retrieves all cards from database in alphabetical order and displays them based on what 'page' is in request.

    @param request:

    :todo: Loading image for long searches
    """
    logger.debug("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
    init_mana_list = Symbol.objects.filter(symbol__in=['{W}', '{U}', '{B}', '{R}', '{G}', '{C}', '{S}'])
    card_id_list_full = CardIDList.objects.all()
    full_card_list_all = []
    for card_list_obj in card_id_list_full:
        full_card_list_all.append(card_list_obj.cardID)

    selected_mana = []
    search_term = 'Search'
    if request.method == 'POST':
        if 'clearSearch' in request.POST:
            del request.session['search']
            del request.session['searchTerm']
            del request.session['selected_mana']
            del request.session['card_id_list']
        else:
            translator = google_translator()
            text = request.POST.get('SearchTerm')
            search_term = translator.translate(text, lang_tgt='en')
            selected_mana = []
            list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                              '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                              '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                              '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                              '{G}', '{2/G}', '{G/P}', '{HG}']
            for selected in init_mana_list:
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
                card_mana_id_list = []
                for mana_color in selected_mana:
                    if mana_color in ['{C}', '', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                                      '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                                      '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}']:
                        mana_match = CardFace.objects.values('cardID_id').filter(Q(cardID_id__in=full_card_list_all) &
                                                                                 Q(manaCost__contains=mana_color) &
                                                                                 reduce(operator.and_, (
                                                                                     ~Q(manaCost__contains=item) for
                                                                                     item in list_of_colors)))
                    else:
                        mana_match = CardFace.objects.values('cardID_id').filter(cardID_id__in=full_card_list_all,
                                                                                 manaCost__contains=mana_color)
                    for match in mana_match:
                        if match['cardID_id'] not in card_mana_id_list:
                            card_mana_id_list.append(match['cardID_id'])
            else:
                card_mana_id_list = []
                for card_obj in full_card_list_all:
                    if card_obj not in card_mana_id_list:
                        card_mana_id_list.append(card_obj)

            card_key_id_list = []
            key_match = Card.objects.values('cardID').filter(
                Q(cardID__in=card_mana_id_list) & Q(keywords__icontains=search_term))
            for match in key_match:
                if match['cardID'] not in card_key_id_list:
                    card_key_id_list.append(match['cardID'])

            filtered_card_list = CardFace.objects.values('cardID_id').filter(
                Q(cardID_id__in=card_key_id_list)
                | (Q(cardID_id__in=card_mana_id_list)
                   & (Q(name__icontains=search_term)
                      | Q(text__icontains=search_term)
                      | Q(typeLine__icontains=search_term)
                      | Q(flavorText__icontains=search_term))
                   )
            )

            card_id_list = []
            for card_list_obj in filtered_card_list:
                if card_list_obj['cardID_id'] not in card_id_list:
                    card_id_list.append(card_list_obj['cardID_id'])

            request.session['search'] = True
            request.session['searchTerm'] = search_term
            request.session['selected_mana'] = selected_mana
            request.session['card_id_list'] = card_id_list
        return redirect('collectionAll')
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
                {'symbol': init_mana.symbol, 'checked': True, 'imageURL': init_mana.imageURL, 'id': init_mana.id})
        else:
            mana_list.append(
                {'symbol': init_mana.symbol, 'checked': False, 'imageURL': init_mana.imageURL, 'id': init_mana.id})

    card_list = CardFace.objects.filter(Q(cardID_id__in=card_id_list)).order_by('name')

    page = request.GET.get('page', 1)

    paginator = Paginator(card_list, 50)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)

    font_family = UserProfile.get_font(request.user.id)
    should_translate = UserProfile.get_translate(request.user.id)
    context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards, 'SearchTerm': search_term, 'mana_list': mana_list, 'clearSearch': clear_search}
    return render(request, 'Collection/CollectionDisplay.html', context)


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
            list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                              '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                              '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                              '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                              '{G}', '{2/G}', '{G/P}', '{HG}']
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
                # If any many color is selected, loop through selected list and filter by cards containing those colors
                for mana_color in selected_mana:
                    # Retrieve all decks that are not private and colorId contains the selected color,
                    # or name contains the search term, display the deck.

                    # If colorless is selected, do not show colored cards that also cost colorless mana.
                    if mana_color in ['{C}', '', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                                      '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                                      '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}']:
                        mana_match = Deck.objects.values('id').filter(Q(isPrivate=False) &
                                                                                 Q(name__icontains=search_term) &
                                                                                 Q(colorId__contains=mana_color) &
                                                                                 reduce(operator.and_, (
                                                                                     ~Q(colorId__contains=item) for
                                                                                     item in list_of_colors)))
                    else:
                        mana_match = Deck.objects.values('id').filter(Q(isPrivate=False) &
                                                                                 Q(colorId__contains=mana_color) &
                                                                                 Q(name__icontains=search_term))
                    # Pulls the id's of the matched mana list and ensures it isn't already searched.
                    for match in mana_match:
                        if match['id'] not in deck_id_list:
                            deck_id_list.append(match['id'])
            else:
                mana_match = Deck.objects.values('id').filter(Q(isPrivate=False) &
                                                              Q(name__icontains=search_term))
                # Pulls the id's of the matched mana list and ensures it isn't already searched.
                for match in mana_match:
                    if match['id'] not in deck_id_list:
                        deck_id_list.append(match['id'])

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
            deck_list_obj = Deck.objects.filter(Q(id__in=deck_id_list)).order_by('name')
        except KeyError:
            deck_list_obj = Deck.objects.filter(isPrivate=False).order_by('name')
            clear_search = False

    mana_list = []
    for init_mana in init_mana_list:
        # Goes through the mana symbols and checks to see what is selected. If selected, it checks it. If not, it doesn't.
        if init_mana.symbol in selected_mana:
            mana_list.append(
                {'symbol': init_mana.symbol, 'checked': True, 'imageURL': init_mana.imageURL, 'id': init_mana.id})
        else:
            mana_list.append(
                {'symbol': init_mana.symbol, 'checked': False, 'imageURL': init_mana.imageURL, 'id': init_mana.id})

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

    font_family = UserProfile.get_font(request.user.id)
    should_translate = UserProfile.get_translate(request.user.id)
    # Left is variable name, right is variable data.
    context = {'font_family': font_family, 'should_translate': should_translate, 'pages': deck,
               'SearchTerm': search_term, 'mana_list': mana_list, 'clearSearch': clear_search}
    return render(request, 'Collection/CollectionDisplay.html', context)


def deck_display(request):
    logger.debug("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    deck = request.GET.get('deckID')
    deck_obj = Deck.objects.filter(id=deck)

    context = {'deck': deck_obj}
    return render(request, 'Collection/DeckDisplay.html', context)


def collection_index(request):
    """Display landing page for collections.

    This page is not currently used by the application.

    @param request:

    :todo: None
    """
    logger.debug("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")


def update_quantity(request, card_id):
    """Updates quantity of card.

    Updates the number of cards owned by user based on POST data

    @param request:
    @param card_id: Card ID for current card

    :todo: None
    """
    user = request.user

    if 'remove' in request.POST:
        UserCards.objects.filter(Q(cardID=card_id) & Q(user=user)).delete()
    else:
        card_quantity = request.POST['quantity']
        UserCards.objects.filter(Q(cardID=card_id) & Q(user=user)).update(quantity=card_quantity)
    return redirect('../' + card_id)
