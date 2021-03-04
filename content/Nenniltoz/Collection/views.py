import json
import logging
import operator
from functools import reduce

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from Collection.models import Card, CardFace, Symbol, CardSets, CardLayout, CardIDList

logger = logging.getLogger(__name__)


# Create your views here.
def collection_index(request):
    """Display landing page for collections.

    This page is not currently used by the application.

    :param request: Does not utilize any portions of this param.

    :returns: "Hello World From Collections"

    :todo: None
    """
    logger.debug("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")


def collection_display(request):
    """Display entire card database.

    Retrieves all cards from database in alphabetical order and displays them based on what 'page' is in request.

    :param request: GET data: 'page' - page number for paginator

    :returns: HTML rendering of all cards contained in the database.

    :todo: Loading image for long searches
            Colorless pulls all cards with any mana color
    """
    logger.debug("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
    init_mana_list = Symbol.objects.filter(symbol__in=['{W}', '{U}', '{B}', '{R}', '{G}', '{C}', '{S}'])
    card_id_list_full = CardIDList.objects.all()
    full_card_list_all = []
    for card_list_obj in card_id_list_full:
        full_card_list_all.append(card_list_obj.cardID)

    selected_mana = []
    SearchTerm = 'Search'
    if request.method == 'POST':
        if 'clearSearch' in request.POST:
            del request.session['search']
            del request.session['searchTerm']
            del request.session['selected_mana']
            del request.session['card_id_list']
        else:
            SearchTerm = request.POST.get('SearchTerm')
            selected_mana = []
            list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}','{HW}',
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
                            symbol__in=['', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}','{2}','{3}','{4}','{5}','{6}','{7}',
                                            '{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}',
                                            '{20}','{100}','{1000000}','{P}'])
                    else:
                        alt_mana= []

                    for am in alt_mana:
                        if am.symbol not in selected_mana:
                            selected_mana.append(am.symbol)

            if len(selected_mana) > 0:
                card_mana_id_list = []
                for mana_color in selected_mana:
                    if mana_color in ['{C}','', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}','{2}','{3}','{4}','{5}','{6}','{7}',
                                            '{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}',
                                            '{20}','{100}','{1000000}','{P}']:
                        mana_match = CardFace.objects.values('cardID_id').filter(Q(cardID_id__in=full_card_list_all) &
                                                                                 Q(manaCost__contains=mana_color) &
                                                                                 reduce(operator.and_, (
                                                                                     ~Q(manaCost__contains = item) for item in list_of_colors)))
                    else:
                        mana_match = CardFace.objects.values('cardID_id').filter(cardID_id__in=full_card_list_all, manaCost__contains=mana_color)
                    for match in mana_match:
                        if match['cardID_id'] not in card_mana_id_list:
                            card_mana_id_list.append(match['cardID_id'])
            else:
                card_mana_id_list = []
                for card_obj in full_card_list_all:
                    if card_obj not in card_mana_id_list:
                        card_mana_id_list.append(card_obj)

            card_key_id_list = []
            key_match = Card.objects.values('cardID').filter(Q(cardID__in=card_mana_id_list) & Q(keywords__icontains=SearchTerm))
            for match in key_match:
                if match['cardID'] not in card_key_id_list:
                    card_key_id_list.append(match['cardID'])

            filtered_card_list = CardFace.objects.values('cardID_id').filter(
                Q(cardID_id__in=card_key_id_list)
                | (Q(cardID_id__in=card_mana_id_list)
                    & (Q(name__icontains=SearchTerm)
                    | Q(text__icontains=SearchTerm)
                    | Q(typeLine__icontains=SearchTerm)
                    | Q(flavorText__icontains=SearchTerm))
                    )
            )

            card_id_list = []
            for card_list_obj in filtered_card_list:
                if card_list_obj['cardID_id'] not in card_id_list:
                    card_id_list.append(card_list_obj['cardID_id'])

            request.session['search'] = True
            request.session['searchTerm'] = SearchTerm
            request.session['selected_mana'] = selected_mana
            request.session['card_id_list'] = card_id_list
        return redirect('collectionAll')
    else:
        try:
            SearchTerm = request.session['searchTerm']
            selected_mana = request.session['selected_mana']
            card_id_list = request.session['card_id_list']
            clear_search = True
        except KeyError:
            card_id_list = full_card_list_all
            clear_search = False

    mana_list = []
    for init_mana in init_mana_list:
        if init_mana.symbol in selected_mana:
            mana_list.append({'symbol': init_mana.symbol, 'checked': True, 'imageURL': init_mana.imageURL, 'id': init_mana.id})
        else:
            mana_list.append({'symbol': init_mana.symbol, 'checked': False, 'imageURL': init_mana.imageURL, 'id': init_mana.id})

    card_list = CardFace.objects.filter(Q(cardID_id__in=card_id_list)).order_by('name')

    page = request.GET.get('page', 1)

    paginator = Paginator(card_list, 50)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)


    context = {'pages': cards, 'SearchTerm': SearchTerm, 'mana_list': mana_list, 'clearSearch': clear_search}
    return render(request, 'Collection/CollectionDisplay.html', context)


def card_display(request, cardID):
    """Display individual cards.

    Retrieves card information from the database based on what 'cardID' is in request. Then displays the card data.

    :param request: GET data: 'cardID' - card id for retrieving data from database

    :returns: HTML rendering of single card.

    :todo: Touch up data display/layout, Add ruling/legalities to the page
    """
    logger.debug("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    card_obj = Card.objects.filter(cardID=cardID)
    face_obj = CardFace.objects.filter(cardID_id=cardID)

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
            set_info.append({'set_name': card_set.name,'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].imageURL, 'card_image_two': face_obj[1].imageURL})
        else:
            set_info.append({'set_name': card_set.name,'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].imageURL, 'card_image_two': 'NONE'})

    context = {'card': card_obj, 'faces': face_obj, 'set_info': set_info, 'set_list': card_set_list}
    return render(request, 'Collection/CardDisplay.html', context)

