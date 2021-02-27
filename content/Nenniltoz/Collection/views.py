import json
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from Collection.models import Card, CardFace

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

    :todo: Add search/filter feature
    """
    logger.debug("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
    card_list = CardFace.objects.filter(firstFace=1).order_by('name')
    page = request.GET.get('page', 1)

    paginator = Paginator(card_list, 50)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)

    context = {'pages': cards, }
    return render(request, 'Collection/CollectionDisplay.html', context)


def card_display(request):
    """Display individual cards.

    Retrieves card information from the database based on what 'cardID' is in request. Then displays the card data.

    :param request: GET data: 'cardID' - card id for retrieving data from database

    :returns: HTML rendering of single card.

    :todo: Touch up data display/layout, Add ruling/legalities to the page
    """
    logger.debug("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    card = request.GET.get('cardID')
    card_obj = Card.objects.filter(cardID=card)
    face_obj = CardFace.objects.filter(cardID=card)

    context = {'card': card_obj, 'faces': face_obj}
    return render(request, 'Collection/CardDisplay.html', context)
