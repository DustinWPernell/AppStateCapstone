import json
import logging

from asgiref.sync import sync_to_async
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Collection.models import Card, CardFace, Symbol, CardIDList, Rule, Legality
from Users.models import UserCards, UserProfile

logger = logging.getLogger(__name__)


# Create your views here.
def add_card(request, oracle_id):
    """Add cards to user collection

    Adds a card to either the users collection or wish list

    @param request:
    @param oracle_id: Card ID for current card

    :todo: None
    """
    user = request.user

    if 'addCards' in request.POST:
        card_quantity = int(request.POST['quantity'])
        if card_quantity == 0:
            card_quantity = 1
        messages.success(request, 'Added ' + str(card_quantity) + ' card(s) to your collection.')
    else:
        card_quantity = 0
        messages.success(request, 'Added card to wish list.')

    UserCards.objects.create(
        oracle_id=oracle_id,
        user=user,
        quantity=card_quantity,
    )
    return redirect('../' + oracle_id)


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

        quantity = 0
        card_count = -1

        if request.user.is_authenticated:
            user_card = UserCards.get_user_card_by_oracle(oracle_id, request.user).values('quantity')
            if user_card.count() > 0:
                quantity = user_card[0]['quantity']
                card_count = quantity

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'card': card_faces,
                   'faces': card_faces, 'set_info': card_set_list,
                   'rulings': rulings_list, 'has_rules': len(rulings_list) > 0,
                   'quantity': quantity, 'card_count': card_count, 'auth': request.user.is_authenticated}
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
               'SearchTerm': search_term, 'mana_list': mana_list, 'clearSearch': clear_search}
    return render(request, 'Collection/collection_display.html', context)


def collection_index(request):
    """Display landing page for collections.

    This page is not currently used by the application.

    @param request:

    :todo: None
    """
    logger.info("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")


def update_quantity(request, oracle_id):
    """Updates quantity of card.

    Updates the number of cards owned by user based on POST data

    @param request:
    @param oracle_id: Card ID for current card

    :todo: None
    """
    user = request.user

    if 'remove' in request.POST:
        UserCards.get_user_card_by_oracle(oracle_id, user).delete()
        messages.error(request, 'Removed card(s) from collection.')
    else:
        card_quantity = request.POST['quantity']
        UserCards.get_user_card_by_oracle(oracle_id, user).update(quantity=card_quantity)
        messages.success(request, 'Updated quantity of cards.')
    return redirect('../' + oracle_id)
