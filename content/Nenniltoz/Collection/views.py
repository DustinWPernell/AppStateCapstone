import json
import logging

from django.http import HttpResponse


logger = logging.getLogger(__name__)

def collection_index(request):
    """Display landing page for collections.

    This page is not currently used by the application.

    @param request:

    :todo: None
    """
    logger.info("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")

