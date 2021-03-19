import json
import logging
import operator
from functools import reduce

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from google_trans_new import google_translator

from Collection.models import Card, CardFace, Symbol, CardSets, CardLayout, CardIDList, Rule, Legality
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
            card_id=card_id,
            user=user,
            quantity=card_quantity,
        )
    else:
        UserCards.objects.create(
            card_id=card_id,
            user=user,
            quantity=0,
        )
    return redirect('../' + card_id)


def card_display(request, card_id):
    """Display individual cards.

    Retrieves card information from the database based on what 'card_id' is in request. Then displays the card data.

    @param request:
    @param card_id: Card ID for current card

    :todo: Touch up data display/layout
    """
    logger.debug("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    card_obj = Card.objects.get(card_id=card_id)
    face_obj = CardFace.objects.filter(card_id=card_id)

    set_info = []
    card_sets = CardFace.objects.filter(name=face_obj[0].name)

    layouts = CardLayout.objects.filter(sides=2)
    layout_strings = []
    for lay in layouts:
        layout_strings.append(lay.layout)

    card_set_list = []
    for card_set_obj in card_sets:
        set_card_obj = Card.objects.get(card_id=card_set_obj.card_id)
        face_obj = CardFace.objects.filter(card_id_id=card_set_obj.card_id)
        card_set = CardSets.objects.get(order=card_set_obj.set_order)

        if card_set.name not in card_set_list:
            card_set_list.append(card_set.name)

        if set_card_obj.layout in layout_strings:
            set_info.append(
                {'set_name': card_set.name, 'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].image_url,
                 'card_image_two': face_obj[1].image_url})
        else:
            set_info.append(
                {'set_name': card_set.name, 'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].image_url,
                 'card_image_two': 'NONE'})

    rulings_list = Rule.objects.filter(oracle_id=card_obj.oracle_id).order_by('-pub_date')

    legalities = Legality.objects.get(card_id=card_obj.card_id)

    quantity = 0
    card_count = -1

    if request.user.is_authenticated:
        user_card = UserCards.objects.values('quantity').filter(
            Q(user=request.user) &
            Q(card_id=card_id)
        )

        if user_card.count() > 0:
            quantity = user_card[0]['quantity']
            card_count = quantity
    set_info.sort(key=lambda item: item.get("set_name"))

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate, 'card': card_obj, 'faces': face_obj, 'set_info': set_info, 'set_list': card_set_list,
               'rulings': rulings_list, 'has_rules': len(rulings_list) > 0, 'legal': legalities,
               'quantity': quantity, 'card_count': card_count, 'auth': request.user.is_authenticated}
    return render(request, 'Collection/card_display.html', context)


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
                        mana_match = CardFace.objects.values('card_id').filter(Q(card_id__in=full_card_list_all) &
                                                                                 Q(manaCost__contains=mana_color) &
                                                                                 reduce(operator.and_, (
                                                                                     ~Q(manaCost__contains=item) for
                                                                                     item in list_of_colors)))
                    else:
                        mana_match = CardFace.objects.values('card_id').filter(card_id__in=full_card_list_all,
                                                                                 manaCost__contains=mana_color)
                    for match in mana_match:
                        if match['card_id'] not in card_mana_id_list:
                            card_mana_id_list.append(match['card_id'])
            else:
                card_mana_id_list = []
                for card_obj in full_card_list_all:
                    if card_obj not in card_mana_id_list:
                        card_mana_id_list.append(card_obj)

            card_key_id_list = []
            key_match = Card.objects.values('card_id').filter(
                Q(card_id__in=card_mana_id_list) & Q(keywords__icontains=search_term))
            for match in key_match:
                if match['card_id'] not in card_key_id_list:
                    card_key_id_list.append(match['card_id'])

            filtered_card_list = CardFace.objects.values('card_id').filter(
                Q(card_id__in=card_key_id_list)
                | (Q(card_id__in=card_mana_id_list)
                   & (Q(name__icontains=search_term)
                      | Q(text__icontains=search_term)
                      | Q(typeLine__icontains=search_term)
                      | Q(flavorText__icontains=search_term))
                   )
            )

            card_id_list = []
            for card_list_obj in filtered_card_list:
                if card_list_obj['card_id'] not in card_id_list:
                    card_id_list.append(card_list_obj['card_id'])

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

    card_list = CardFace.objects.filter(Q(card_id__in=card_id_list)).order_by('name')

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
    context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards, 'SearchTerm': search_term, 'mana_list': mana_list, 'clearSearch': clear_search}
    return render(request, 'Collection/collection_display.html', context)


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
        UserCards.objects.filter(Q(card_id=card_id) & Q(user=user)).delete()
    else:
        card_quantity = request.POST['quantity']
        UserCards.objects.filter(Q(card_id=card_id) & Q(user=user)).update(quantity=card_quantity)
    return redirect('../' + card_id)
