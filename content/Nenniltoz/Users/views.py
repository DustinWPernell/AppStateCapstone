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
    """Display the home page.

    Retrieves the most recent news articles from the database and displays them on the page

    :param request: Does not utilize any portions of this param.

    :todo: Set up expiration dates for news items
    """
    logger.debug("Run: index; Params: " + json.dumps(request.GET.dict()))

    latest_news_list = News.objects.order_by('-headline')[:5]
    context = {'latest_news_list': latest_news_list, }
    return render(request, 'Users/index.html', context)


def login_page(request):
    """Login page.

    Shows a login form. On POST, redirects to the user profile if credentials are good.

    :param request: POST data: * username
        * password

    :todo: Update display/layout
    """
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
    """Logout page.

    Logs the user out.

    :param request: Does not utilize any portions of this param.
    
    :todo: Update display/layout
    """
    logger.debug("Run: logout_page; Params: " + json.dumps(request.GET.dict()))

    auth.logout(request)
    return render(request, 'Users/logout.html')


def register(request):
    """Registration Page.

    Displays registration form. On POST creates User and UserProfile object with data provided by POST.

    :param request: POST data: On form submit POST contains information for creating a user
    
    :todo: Update display/layout
    """
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
    """Build pending friends list.

    Builds a list of pending friend requests pulled from the database. Uses user param to filter for specific user.

    :param user: User who is receiving the friend requests

    :return: Returns list of users that have sent request to current user and that have not been rejected.

    :todo: None
    """
    pending_list = PendingFriends.objects.filter(user_two=user, rejected=False)
    pending_user_list = []
    for pending in pending_list:
        pending_user_list.append(pending.user_one)

    return pending_user_list


def build_friend_list(user):
    """Build friends list.

    Builds a list of friend requests pulled from the database. Uses user param to filter for specific user.

    :param user: User that is requesting the list

    :return: Returns list of users that are friends with the current user.

    :todo: None
    """
    friend_list = Friends.objects.filter(user_one=user)
    friend_user_list = []
    for friend in friend_list:
        friend_user_list.append(friend.user_two)

    return friend_user_list

def build_follower_list(user):
    """Build followers list.

    Builds a list of followers pulled from the database. Uses user param to filter for specific user.

    :param user: User that is doing the following

    :return: Returns list of users that are being followed by the current user.

    :todo: None
    """
    follower_list = Followers.objects.filter(user_one=user)
    follower_user_list = []
    for follower in follower_list:
        follower_user_list.append(follower.user_two)

    return follower_user_list


def player_profile(request):
    """Display the profile of a user that is not logged in.

    Uses the GET data from request to display user data. Displayed user data is not the current user.

    :param request: GET data: User id/username which is being displayed
    
    :todo: Alter to work with non current user
    """
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
    """Display the profile of a user that is logged in.

    Uses the GET data from request to display user data. Displayed user data is the current user.

    :param request: GET data: User id which is being displayed

    :todo: Alter to work with non current user
    """
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
    """Sends friend request

    Uses POST data to send friend request to user. Error checks for
        * Already sent request
        * Already friends
        * If friend request was to to the current user and accepts it
        * If the user being sent the request exist

    :param request: POST data: curUser and newFriend

    :todo: None
    """
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
    """Creates freind relationship.

    Creates the 2 way friend relationship in the database. Removes the pending friend request from the database

    :param request: POST data: curUser and newFriend

    :todo: None
    """
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
    """Processes button click for friend request on receivers profile.

    Determines if the user selected to accept or reject the friend request.

    :param request: POST data: curUser and newFriend

    :todo: None
    """
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
    """Removes a friend

    Removes the 2 way relationship for friends.

    :param request: POST data: curUser and newFriend

    :todo: None
    """
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
    """Adds a followed user to the user.

    Add the followed user to the database.  Error checks for
        * Already following
        * If the user being followed exist

    :param request: POST data: curUser and newFriend

    :todo: None
    """
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
    """Removes a followed user

    Removes the followed user from the relationship with the current user.

    :param request: POST data: curUser and newFriend

    :todo: None
    """
    user = request.POST['curUser']
    follower = request.POST['newFollower']
    user_obj = User.objects.get(username=user).id
    follower_obj = User.objects.get(username=follower).id

    Followers.objects.get(user_one=user_obj, user_two=follower_obj).delete()

    messages.error(request, 'Removed follower.')

    return redirect('user_profile')
