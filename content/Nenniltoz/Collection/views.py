import json
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from Collection.models import Card, CardFace, Symbol, CardSets, CardLayout

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

    :todo: Loading image for long searches \ Filter for keywords
    """
    logger.debug("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
    init_mana_list = Symbol.objects.filter(symbol__in=['{W}', '{U}', '{B}', '{R}', '{G}', '{C}', '{S}'])
    selected_mana = []
    SearchTerm = 'Search'
    if request.method == 'POST':
        if 'clearSearch' in request.POST:
            del request.session['search']
            del request.session['searchTerm']
            del request.session['selected_mana']
            card_list = CardFace.objects.raw(
                "SELECT * FROM main.Collection_cardface Where firstFace = 1 GROUP BY name ORDER BY name ")
            SearchTerm = ''
            clear_search = False
        else:
            selected_mana = []
            for selected in init_mana_list:
                mana_ele = request.POST.get("mana-" + str(selected.id))
                if mana_ele == '':
                    selected_mana.append(selected.symbol)
                    if selected.symbol == '{W}':
                        alt_mana = Symbol.objects.filter(
                            symbol__in=['{W/U}','{W/B}','{R/W}','{G/W}','{2/W}','{W/P}','{HW}'])
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

            SearchTerm = request.POST.get('SearchTerm')
            full_card_id_list = CardFace.objects.raw("SELECT id FROM main.Collection_cardface GROUP BY name ORDER BY name ")
            if len(selected_mana) == 0:
                card_id_list = full_card_id_list
            else:
                card_id_list = []
                for mana_color in selected_mana:
                    mana_match = CardFace.objects.values('id').filter(id__in=full_card_id_list, manaCost__contains=mana_color)
                    for match in mana_match:
                        match_int = int(match['id'])
                        if match_int not in card_id_list:
                            card_id_list.append(match_int)

            card_list = CardFace.objects.filter(Q(id__in=card_id_list) &
                                                (Q(name__icontains=SearchTerm)  | Q(text__icontains=SearchTerm)
                                                | Q(typeLine__icontains=SearchTerm) | Q(flavorText__icontains=SearchTerm))
                                                ).order_by('name')

            request.session['search'] = True
            request.session['searchTerm'] = SearchTerm
            request.session['selected_mana'] = selected_mana
            clear_search = True
    else:
        try:
            SearchTerm = request.session['searchTerm']
            selected_mana = request.session['selected_mana']
            full_card_id_list = CardFace.objects.raw("SELECT id FROM main.Collection_cardface GROUP BY name ORDER BY name ")
            if len(selected_mana) == 0:
                card_id_list = full_card_id_list
            else:
                card_id_list = []
                for mana_color in selected_mana:
                    mana_match = CardFace.objects.values('id').filter(id__in=full_card_id_list, manaCost__contains=mana_color)
                    for match in mana_match:
                        match_int = int(match['id'])
                        if match_int not in card_id_list:
                            card_id_list.append(match_int)

            card_list = CardFace.objects.filter(Q(id__in=card_id_list) & (Q(name__contains=SearchTerm)  | Q(text__contains=SearchTerm) |
                                                Q(typeLine__contains=SearchTerm) | Q(flavorText__contains=SearchTerm))).order_by('name')
            clear_search = True
        except KeyError:
            card_list = CardFace.objects.raw("SELECT * FROM main.Collection_cardface Where firstFace = 1 GROUP BY name ORDER BY name ")
            clear_search = False

    mana_list = []
    for init_mana in init_mana_list:
        if init_mana.symbol in selected_mana:
            mana_list.append({'symbol': init_mana.symbol, 'checked': True, 'imageURL': init_mana.imageURL, 'id': init_mana.id})
        else:
            mana_list.append({'symbol': init_mana.symbol, 'checked': False, 'imageURL': init_mana.imageURL, 'id': init_mana.id})



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

    :todo: Touch up data display/layout, Add ruling/legalities to the page, fix set icons color
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

    for card_set_obj in card_sets:
        set_card_obj = Card.objects.get(cardID=card_set_obj.cardID_id)
        face_obj = CardFace.objects.filter(cardID_id=card_set_obj.cardID_id)
        card_set = CardSets.objects.get(order=card_set_obj.setOrder)


        if set_card_obj.layout in layout_strings:
            set_info.append({'set_name': card_set.name,'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].imageURL, 'card_image_two': face_obj[1].imageURL})
        else:
            set_info.append({'set_name': card_set.name,'set_image': card_set.icon_svg_uri, 'card_image_one': face_obj[0].imageURL, 'card_image_two': 'NONE'})

    context = {'card': card_obj, 'faces': face_obj, 'set_info': set_info}
    return render(request, 'Collection/CardDisplay.html', context)

