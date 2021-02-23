import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# Create your views here.
from Management.models import Settings

logger = logging.getLogger(__name__)


@staff_member_required
def admin_index(request):
    logger.debug("Run: admin_index; Params: " + json.dumps(request.GET.dict()))
    return render(request, 'Management/adminLand.html')


@staff_member_required
def api_import(request):
    logger.debug("Run: api_import; Params: " + json.dumps(request.GET.dict()))
    settings_list = Settings.objects
    context = {'settings_list': settings_list, }
    return render(request, 'Management/APIimport.html', context)
