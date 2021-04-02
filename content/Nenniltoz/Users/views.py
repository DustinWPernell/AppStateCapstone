import json
import logging
import os
from datetime import datetime

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, BadHeaderError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Collection.models import CardFace, Deck, DeckType, DeckCards
from static.python.mailers import send_password_reset
from .forms import CreateUserForm
from .models import News, UserProfile, Friends, PendingFriends, Followers, UserCards

logger = logging.getLogger(__name__)


def index(request):
    latest_news_list = News.objects.order_by('eventDate', 'headline')[:5]
    context = {'latest_news_list': latest_news_list, }
    """Display the home page.

    Retrieves the most recent news articles from the database and displays them on the page

    @param request:

    :todo: Set up expiration dates for news items
    """
    logger.info("Run: index; Params: " + json.dumps(request.GET.dict()))

    latest_news_list = News.get_next_5()

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate, 'latest_news_list': latest_news_list, }
    return render(request, 'Users/index.html', context)


@login_required
def logout_page(request):
    """Logout page.

    Logs the user out.

    @param request:
    
    :todo: Update display/layout
    """
    logger.info("Run: logout_page; Params: " + json.dumps(request.GET.dict()))

    auth.logout(request)
    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate}
    return render(request, 'logout.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_password_reset(subject,  [user.email])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})



def register(request):
    """Registration Page.

    Displays registration form. On POST creates User and UserProfile object with data provided by POST.

    @param request:
    
    :todo: Update display/layout
    """
    logger.info("Run: register; Params: " + json.dumps(request.GET.dict()))

    if request.user.is_authenticated:
        return redirect('user_profile', user_id=str(request.user.id))

    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save(request)

            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Account not created')
    else:
        f = UserCreationForm()

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate, 'form': f}
    return render(request, 'Users/register.html', context)






