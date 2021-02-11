from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import News


# Create your views here.
def index(request):
    latest_news_list = News.objects.order_by('-headline')[:5]
    template = loader.get_template('Users/index.html')
    context = {
        'latest_news_list': latest_news_list,
    }
    return HttpResponse(template.render(context, request))
