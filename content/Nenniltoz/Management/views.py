import json
import logging
from urllib.request import urlopen

import ijson
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from rq import Queue

from Management.models import Settings
from Users.models import UserProfile
from static.python.api_import import card_import_job, oracle_import_job, rule_import_job, set_import_job, \
    symbol_import_job
from worker import conn

logger = logging.getLogger("logger")


@staff_member_required
def admin_index(request):
    """Display landing page for management.

    This page is not currently used by the application.

    @param request:

    :todo: None
    """
    logger.info("Params: " + json.dumps(request.GET.dict()))

    font_family = UserProfile.get_font(request.user)
    context = {'font_family': font_family}
    return render(request, 'Management/admin_land.html', context)


@staff_member_required
def api_import(request):
    """Displays API import options.

    Shows the Scryfall import option implemented. As import processes data, updates display progress.
    Warning: Processing takes a long time when importing cards an rules.

    @param request:

    :todo: None
    """
    logger.info("Params: " + json.dumps(request.GET.dict()))
    settings_list = Settings.objects.all()

    font_family = UserProfile.get_font(request.user)
    context = {'font_family': font_family, 'settings_list': settings_list, }
    return render(request, 'Management/api_import.html', context)


@staff_member_required
def card_update(request):
    logger.info("Params: " + json.dumps(request.GET.dict()))
    global api_card
    q = Queue(connection=conn)
    q.enqueue(card_import_job, 'http://heroku.com', job_timeout=20000)
    return HttpResponse("Added to queue")


@staff_member_required
def oracle_update(request):
    logger.info("Params: " + json.dumps(request.GET.dict()))
    global api_sing_card
    q = Queue(connection=conn)
    q.enqueue(oracle_import_job, 'http://heroku.com', job_timeout=20000)
    return HttpResponse("Added to queue")


@staff_member_required
def retrieve_api(request):
    """Performs API call for bulk data urls.

    Calls Scryfall API for retrieval of bulk data urls. Parses bulk data url Json file. Stores URLs for cards and rules.

    @param request:

    :todo: Set to process in background
    """
    logger.info("Run: retrieve_api; Params: " + json.dumps(request.GET.dict()))
    settings = Settings.get_settings()

    objects = list(ijson.items(urlopen(settings.api_bulk_data), 'data'))[0]
    for obj in objects:
        if obj['type'] == "default_cards":
            settings.api_card = obj['download_uri']
        elif obj['type'] == "rulings":
            settings.api_rule = obj['download_uri']
        elif obj['type'] == "oracle_cards":
            settings.api_sing_card = obj['download_uri']
            logger.info("site =" + obj['download_uri'])

    settings.save()
    return HttpResponse("Finished")


@staff_member_required
def rule_update(request):
    logger.info("Params: " + json.dumps(request.GET.dict()))
    global api_rule
    q = Queue(connection=conn)
    q.enqueue(rule_import_job, 'http://heroku.com', job_timeout=20000)
    return HttpResponse("Added to queue")


@staff_member_required
def set_update(request):
    logger.info("Params: " + json.dumps(request.GET.dict()))
    global api_set
    q = Queue(connection=conn)
    q.enqueue(set_import_job, 'http://heroku.com', job_timeout=20000)
    return HttpResponse("Added to queue")


@staff_member_required
def symbol_update(request):
    logger.info("Params: " + json.dumps(request.GET.dict()))
    global api_symbol
    q = Queue(connection=conn)
    q.enqueue(symbol_import_job, 'http://heroku.com', job_timeout=20000)
    return HttpResponse("Added to queue")
