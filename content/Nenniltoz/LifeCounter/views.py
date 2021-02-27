from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    """Display landing page for life counter.

    This page is not currently used by the application.

    :param request: Does not utilize any portions of this param.

    :returns: "Hello World From LifeCounter"

    :todo: None
    """
    return HttpResponse("Hello World From LifeCounter")