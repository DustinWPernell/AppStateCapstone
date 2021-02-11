from django.shortcuts import get_object_or_404, render

from .models import News


# Create your views here.
def index(request):
    latest_news_list = News.objects.order_by('-headline')[:5]
    context = { 'latest_news_list': latest_news_list, }
    return render(request, 'Users/index.html', context)


def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    return render(request, 'Users/detail.html', {'news': news})
