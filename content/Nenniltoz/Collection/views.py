import json
import logging

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Collection.models import CardFace, Symbol, CardIDList, Rule, Deck, DeckCards
from Users.models import UserCards, UserProfile

logger = logging.getLogger(__name__)

def collection_index(request):
    """Display landing page for collections.

    This page is not currently used by the application.

    @param request:

    :todo: None
    """
    logger.info("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")

