from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from .forms import SignUpForm
from .models import News


# Create your views here.
def index(request):
    latest_news_list = News.objects.order_by('-headline')[:5]
    context = { 'latest_news_list': latest_news_list, }
    return render(request, 'Users/index.html', context)

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../Users/home')
    else:
        form = SignUpForm()
    return render(request, 'Users/register.html', {'form': form})