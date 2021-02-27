import json
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from Collection.models import Card, CardFace

logger = logging.getLogger(__name__)


# Create your views here.
def collection_index(request):
    logger.debug("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")


def collection_display(request):
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
    logger.debug("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    card = request.GET.get('cardID')
    card_obj = Card.objects.filter(cardID=card)
    face_obj = CardFace.objects.filter(cardID=card)

    context = {'card': card_obj, 'faces': face_obj}
    return render(request, 'Collection/CardDisplay.html', context)
