import json
import logging
from datetime import datetime

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm
from .models import News, UserProfile, Friends, PendingFriends, Followers

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    logger.debug("Run: index; Params: " + json.dumps(request.GET.dict()))

    latest_news_list = News.objects.order_by('-headline')[:5]
    context = {'latest_news_list': latest_news_list, }
    return render(request, 'Users/index.html', context)


def login_page(request):
    logger.debug("Run: login_page; Params: " + json.dumps(request.GET.dict()))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('user_profile')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'Users/login.html')

@login_required
def logout_page(request):
    logger.debug("Run: logout_page; Params: " + json.dumps(request.GET.dict()))

    auth.logout(request)
    return render(request, 'Users/logout.html')


def register(request):
    logger.debug("Run: register; Params: " + json.dumps(request.GET.dict()))

    if request.user.is_authenticated:
        return redirect('user_profile', username=request.user.username)

    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save(request)

            messages.success(request, 'Account created successfully')
            return redirect('user_profile')

    else:
        f = UserCreationForm()

    return render(request, 'Users/register.html', {'form': f})


def build_pending_list(user):
    pending_list = PendingFriends.objects.filter(user_two=user, rejected=False)
    pending_user_list = []
    for pending in pending_list:
        pending_user_list.append(pending.user_one)

    return pending_user_list


def build_friend_list(user):
    friend_list = Friends.objects.filter(user_one=user)
    friend_user_list = []
    for friend in friend_list:
        friend_user_list.append(friend.user_two)

    return friend_user_list

def build_follower_list(user):
    follower_list = Followers.objects.filter(user_one=user)
    follower_user_list = []
    for follower in follower_list:
        follower_user_list.append(follower.user_two)

    return follower_user_list


def player_profile(request):
    logger.debug("Run: player_profile; Params: " + json.dumps(request.GET.dict()))
    user = get_object_or_404(User, id=request.user.id)
    user_profile_obj = UserProfile.objects.get(user=user)
    friend_obj = build_friend_list(user)
    pending_obj = build_pending_list(user)
    follower_obj = build_follower_list(user)

    return render(request, 'Users/UserProfile.html', {'user_profile_obj': user_profile_obj, 'user': user,
                                                      'friend_obj': friend_obj, 'pending_obj': pending_obj, 'follower_obj':follower_obj})


@login_required
def user_profile(request):
    logger.debug("Run: user_profile; Params: " + json.dumps(request.GET.dict()))
    user = get_object_or_404(User, id=request.user.id)
    user_profile_obj = UserProfile.objects.get(user=user)
    friend_obj = build_friend_list(user)
    pending_obj = build_pending_list(user)
    follower_obj = build_follower_list(user)

    return render(request, 'Users/UserProfile.html', {'user_profile_obj': user_profile_obj, 'user': user,
                                                      'friend_obj': friend_obj, 'pending_obj': pending_obj, 'follower_obj':follower_obj})


@login_required
def send_friend_request(request):
    user = request.POST['curUser']
    friend=request.POST['newFriend']
    user_obj = User.objects.get(username=user)
    friend_obj = User.objects.get(username=friend)
    pending_friends_exist = PendingFriends.objects.filter(user_one=user_obj, user_two=friend_obj).exists()
    friends_exist = Friends.objects.filter(user_one=user_obj, user_two=friend_obj).exists()
    pending_sent_exist = PendingFriends.objects.filter(user_one=friend_obj, user_two=user_obj).exists()

    if pending_friends_exist:
        messages.error(request, 'Friend already sent.')
    elif friends_exist:
        messages.error(request, 'Already friends.')
    elif pending_sent_exist:
        messages.success(request, 'Friend request accepted.')
        add_friend(request)
    else:
        try:
            PendingFriends.objects.create(
                user_one=user_obj,
                user_two=friend_obj,
                created_on=datetime.now()
            )
            messages.success(request, 'Friend request sent.')
        except ValueError:
            messages.error(request, 'Username does not exist.')

    return redirect('user_profile')


@login_required
def add_friend(request):
    user = request.POST['curUser']
    friend=request.POST['newFriend']
    user_obj = User.objects.get(username=user)
    friend_obj = User.objects.get(username=friend)
    Friends.objects.create(
        user_one=user_obj,
        user_two=friend_obj,
        created_on=datetime.now()
    )
    Friends.objects.create(
        user_one=friend_obj,
        user_two=user_obj,
        created_on=datetime.now()
    )
    try:
        PendingFriends.objects.get(user_one=friend_obj, user_two=user_obj).delete()
    except:
        PendingFriends.objects.get(user_one=user_obj, user_two=friend_obj).delete()
    return redirect('user_profile')


@login_required
def process_friend(request):
    user = request.POST['curUser']
    friend=request.POST['newFriend']
    user_obj = User.objects.get(username=user)
    friend_obj = User.objects.get(username=friend)

    if 'pendAcceptBtn' not in request.POST:
        PendingFriends.objects.filter(user_one=friend_obj, user_two=user_obj).update(rejected=True)
        messages.error(request, 'Friend request rejected. Send new request to add as friend.')
    else:
        messages.success(request, 'Friend request accepted.')
        add_friend(request)
    return redirect('user_profile')


@login_required
def remove_friend(request):
    user = request.POST['curUser']
    friend=request.POST['newFriend']
    user_obj = User.objects.get(username=user).id
    friend_obj = User.objects.get(username=friend).id

    Friends.objects.get(user_one=user_obj, user_two=friend_obj).delete()
    Friends.objects.get(user_one=friend_obj, user_two=user_obj).delete()

    messages.error(request, 'Removed friend. Send new request to add as friend.')

    return redirect('user_profile')

@login_required
def add_follower(request):
    user = request.POST['curUser']
    follower=request.POST['newFollower']
    user_obj = User.objects.get(username=user)
    follower_obj = User.objects.get(username=follower)

    follower_exist = Followers.objects.filter(user_one=user_obj, user_two=follower_obj).exists()

    if follower_exist:
        messages.error(request, 'Already following.')
    else:
        try:
            Followers.objects.create(
                user_one=user_obj,
                user_two=follower_obj,
                created_on=datetime.now()
            )
            messages.success(request, 'Follower Added.')
        except ValueError:
            messages.error(request, 'Username does not exist.')


    return redirect('user_profile')

@login_required
def remove_follower(request):
    user = request.POST['curUser']
    follower = request.POST['newFollower']
    user_obj = User.objects.get(username=user).id
    follower_obj = User.objects.get(username=follower).id

    Followers.objects.get(user_one=user_obj, user_two=follower_obj).delete()

    messages.error(request, 'Removed follower.')

    return redirect('user_profile')
