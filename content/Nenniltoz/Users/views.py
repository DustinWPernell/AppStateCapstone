import json
import logging
from datetime import datetime

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from Collection.models import CardFace, CardIDList
from .forms import CreateUserForm
from .models import News, UserProfile, Friends, PendingFriends, Followers, UserCards

logger = logging.getLogger(__name__)


@login_required
def add_follower(request, user_id):
    """Adds a followed user to the user.

    Add the followed user to the database.  Error checks for
        * Already following
        * If the user being followed exist

    @param request:
    @param user_id: User id of displayed profile.

    :todo: None
    """
    follower = request.POST['newFollower']
    user_obj = User.objects.get(id=user_id)
    follower_obj = User.objects.get(username=follower)
    follower_obj_exist = User.objects.filter(username=follower).exists()

    follower_exist = Followers.objects.filter(user_one=user_obj, user_two=follower_obj).exists()

    if follower_exist:
        messages.error(request, 'Already following.')
    elif not follower_obj_exist:
        messages.error(request, 'Username does not exist.')
    else:
        Followers.objects.create(
            user_one=user_obj,
            user_two=follower_obj,
            created_on=datetime.now()
        )
        messages.success(request, 'Follower Added.')

    return redirect('user_profile', user_id=str(request.user.id))


@login_required
def add_friend(request, user_id):
    """Creates friend relationship.

    Creates the 2 way friend relationship in the database. Removes the pending friend request from the database

    @param request:
    @param user_id: User id of displayed profile.

    :todo: None
    """
    friend = request.POST['newFriend']
    user_obj = User.objects.get(id=user_id)
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
    return redirect('user_profile', user_id=str(request.user.id))


def index(request):
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


def login_page(request):
    """Login page.

    Shows a login form. On POST, redirects to the user profile if credentials are good.

    @param request:

    :todo: Update display/layout
    """
    logger.info("Run: login_page; Params: " + json.dumps(request.GET.dict()))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('user_profile', user_id=str(request.user.id))

        else:
            messages.error(request, 'Error wrong username/password')

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate}
    return render(request, 'Users/login.html', context)


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
    return render(request, 'Users/logout.html', context)

@login_required
def new_deck(request):
    """Displays new deck page

    Redirects to new deck page

    @param request:

    :todo: Finish new deck page
    """

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate}
    return render(request, 'Users/Profile/newDeck.html', context)


@login_required
def process_friend(request, user_id):
    """Processes button click for friend request on receivers profile.

    Determines if the user selected to accept or reject the friend request.

    @param request:
    @param user_id: User id of displayed profile.

    :todo: None

    """
    user = request.POST['curUser']
    friend = request.POST['newFriend']
    user_obj = User.objects.get(username=user)
    friend_obj = User.objects.get(username=friend)

    if 'userRedirect' not in request.POST:
        if 'pendAcceptBtn' not in request.POST:
            PendingFriends.objects.filter(user_one=friend_obj, user_two=user_obj).update(rejected=True)
            messages.error(request, 'Friend request rejected. Send new request to add as friend.')
        else:
            messages.success(request, 'Friend request accepted.')
            add_friend(request, user_id)
        return redirect('user_profile', user_id=str(request.user.id))
    else:
        return redirect('user_profile', user_id=str(friend_obj.id))


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
            return redirect('login_page')

    else:
        f = UserCreationForm()

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate, 'form': f}
    return render(request, 'Users/register.html', context)


@login_required
def remove_follower(request, user_id):
    """Removes a followed user

    Removes the followed user from the relationship with the current user.

    @param request:
    @param user_id: User id of displayed profile.

    :todo: None
    """
    follower_id = request.POST['newFollowerID']
    user_obj = User.objects.get(id=user_id).id
    follower_obj = User.objects.get(id=follower_id)

    if 'followerRejectBtn' in request.POST:
        Followers.objects.get(user_one=user_obj, user_two=follower_obj).delete()
        messages.error(request, 'Removed follower.')
        return redirect('user_profile', user_id=str(user_id))
    else:
        return redirect('user_profile', user_id=str(follower_id))


@login_required
def remove_friend(request, user_id):
    """Removes a friend

    Removes the 2 way relationship for friends.

    @param request:
    @param user_id: User id of displayed profile.

    :todo: None
    """
    friend_id = request.POST['newFriendID']
    user_obj = User.objects.get(id=user_id)
    friend_obj = User.objects.get(id=friend_id)
    if 'friendRejectBtn' in request.POST:
        Friends.objects.get(user_one=user_obj, user_two=friend_obj).delete()
        Friends.objects.get(user_one=friend_obj, user_two=user_obj).delete()

        messages.error(request, 'Removed friend. Send new request to add as friend.')

        return redirect('user_profile', user_id=str(user_id))
    else:
        return redirect('user_profile', user_id=str(friend_id))


def save_avatar(request):
    """Saves new avatar to user

    Sets new avatar image to selected URL returned by POST.

    @param request:

    :todo: None
    """

    avatar = request.POST['newAvatar']
    user_obj = User.objects.get(id=request.user.id)

    custom_user_profile = UserProfile.objects.get(user=user_obj)
    custom_user_profile.avatar_img = avatar
    custom_user_profile.save()

    return redirect('user_profile', user_id=str(request.user.id))


@login_required
def select_avatar(request):
    """Displays list for selecting new avatar

    Displays full list of card art with search by name feature.

    @param request:

    :todo: None
    """
    search_term = 'Search'
    if request.method == 'POST':
        if 'clearSearch' in request.POST:
            del request.session['avatar_search_term']
            del request.session['avatar_clear_search']
            card_list = CardFace.objects.all().order_by('name')
            search_term = ''
            clear_search = False
        else:
            search_term = request.POST.get('avatarSearchTerm')

            card_list = CardFace.card_face_filter_by_name_term(search_term).order_by('name')

            request.session['avatar_search_term'] = search_term
            request.session['avatar_clear_search'] = clear_search = True
    else:
        try:
            search_term = request.session['avatar_search_term']
            card_list = CardFace.card_face_filter_by_name_term(search_term).order_by('name')
            clear_search = True
        except KeyError:
            card_list = CardFace.objects.all().order_by('name')
            clear_search = False

    page = request.GET.get('page', 1)

    paginator = Paginator(card_list, 50)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)


    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards, 'SearchTerm': search_term, 'clearSearch': clear_search}
    return render(request, 'Users/Profile/select_avatar.html', context)


@login_required
def send_friend_request(request, user_id):
    """Sends friend request

    Uses POST data to send friend request to user. Error checks for
        * Already sent request
        * Already friends
        * If friend request was to to the current user and accepts it
        * If the user being sent the request exist

    @param request:

    :todo: None
    """
    user = request.POST['curUser']
    friend = request.POST['newFriend']
    user_obj = User.objects.get(id=user_id)
    friend_obj = User.objects.get(username=friend)
    friend_obj_exist = User.objects.filter(username=friend).exists()
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
    elif not friend_obj_exist:
        messages.success(request, 'Username does not exist.')
    else:
        PendingFriends.objects.create(
            user_one=user_obj,
            user_two=friend_obj,
            created_on=datetime.now()
        )
        messages.success(request, 'Friend request sent.')

    return redirect('user_profile', user_id=str(request.user.id))


@login_required
def update_settings(request, user_id):
    """Updated setting

    Updates user settings in database

    @param request:
    @param user_id: Current user ID
    @param setting: Setting to be changed
    @param value: Value to be set

    :todo: None
    """
    logger.info("Run: update_settings; Params: " + json.dumps(request.GET.dict()))
    user_obj = User.objects.get(id=user_id).id

    setting = request.GET['setting']
    value = request.GET['value']
    if value == 'false':
        value = False
    elif value == 'true':
        value = True

    custom_user_profile = UserProfile.objects.get(user=user_obj)
    setattr(custom_user_profile, setting, value)
    custom_user_profile.save()
    messages.success(request, 'Updated Settings.')
    return HttpResponse("Finished")


@login_required
def user_profile(request, user_id):
    """Display the profile of a user.

    Uses the GET data from request to display user data.

    @param request:
    @param user_id: User id of displayed profile.

    :todo: None
    """
    logger.info("Run: user_profile; Params: " + json.dumps(request.GET.dict()))
    user_profile_obj = UserProfile.get_profile_by_user(user_id)
    card_id_list_full = CardIDList.objects.values('card_id').all()

    try:
        deck_page = request.GET.get('deckPage', -1)
        if deck_page == -1:
            deck_page = request.session['deckPage']
    except KeyError:
        deck_page = request.GET.get('deckPage', 1)
        request.session['deckPage'] = deck_page

    try:
        card_page = request.GET.get('cardPage', -1)
        if card_page == -1:
            card_page = request.session['cardPage']
    except KeyError:
        card_page = request.GET.get('cardPage', 1)
        request.session['cardPage'] = card_page

    try:
        card_wish_page = request.GET.get('cardWishPage', -1)
        if card_wish_page == -1:
            card_wish_page = request.session['cardWishPage']
    except KeyError:
        card_wish_page = request.GET.get('cardWishPage', 1)
        request.session['cardWishPage'] = card_wish_page

    if request.method == 'POST':
        if 'user_clear_deck_search' in request.POST:
            del request.session['user_search_deck_term']
            del request.session['user_decks']
            request.session['user_clear_deck_search'] = False
        elif 'user_search_deck' in request.POST:
            search_term = request.POST.get('user_search_deck_term')
            filtered_card_list = CardFace.objects.card_face_filter_by_name_term(search_term)

            card_id_list = []
            for card_list_obj in filtered_card_list:
                if card_list_obj['card_id'] not in card_id_list:
                    card_id_list.append(card_list_obj['card_id'])

            request.session['user_search_deck_term'] = search_term
            request.session['user_decks'] = card_id_list
            request.session['user_clear_deck_search'] = True
        elif 'user_clear_card_search' in request.POST:
            del request.session['user_search_card_term']
            del request.session['user_cards']
            request.session['user_clear_card_search'] = False
        elif 'user_search_card' in request.POST:
            search_term = request.POST.get('user_search_card_term')
            user_card_obj_list = UserCards.get_user_card(user_profile_obj.user)
            filtered_card_list = CardFace.card_face_filter_by_card_oracle_term(
                                                    card_id_list_full, user_card_obj_list, search_term)
            card_id_list = []
            for card_list_obj in filtered_card_list:
                if card_list_obj.legal.card_obj.card_id not in card_id_list:
                    card_id_list.append(card_list_obj.legal.card_obj.card_id)

            request.session['user_search_card_term'] = search_term
            request.session['user_cards'] = card_id_list
            request.session['user_clear_card_search'] = True
        elif 'user_clear_wish_search' in request.POST:
            del request.session['user_search_wish_term']
            del request.session['user_wish_cards']
            request.session['user_clear_wish_search'] = False
        elif 'user_search_wish' in request.POST:
            search_term = request.POST.get('user_search_wish_term')
            user_card_obj_list = UserCards.get_user_wish_card(user_profile_obj.user)
            filtered_card_list = CardFace.card_face_filter_by_card_oracle_term(
                                                    card_id_list_full, user_card_obj_list, search_term)
            card_id_list = []
            for card_list_obj in filtered_card_list:
                if card_list_obj.legal.card_obj.card_id not in card_id_list:
                    card_id_list.append(card_list_obj.legal.card_obj.card_id)

            request.session['user_search_wish_term'] = search_term
            request.session['user_wish_cards'] = card_id_list
            request.session['user_clear_wish_search'] = True
        return redirect('../' + str(user_id) + '?deckPage=' + str(deck_page) + '&cardPage=' +
                        str(card_page) + '&cardWishPage=' + str(card_wish_page))
    
    try:
        search_deck_term = request.session['user_search_deck_term']
        # user_deck_obj_list = request.session['user_decks']
        # user_decks = CardFace.objects.filter(Q(id__in=user_deck_obj_list)).order_by('name'))
        user_clear_deck_search = request.session['user_clear_deck_search']
    except KeyError:
        # user_deck_obj_list = []
        user_decks = []
        search_deck_term = "Search"
        user_clear_deck_search = False
        request.session['user_clear_deck_search'] = False

    try:
        search_card_term = request.session['user_search_card_term']
        user_card_obj_list = request.session['user_cards']
        user_cards = CardFace.card_face_by_card(user_card_obj_list)
        user_clear_card_search = request.session['user_clear_card_search']
    except KeyError:
        user_card_obj_list = UserCards.get_user_card(user_profile_obj.user)
        user_cards = CardFace.card_face_by_card_and_oracle(card_id_list_full, user_card_obj_list)
        search_card_term = "Search"
        user_clear_card_search = request.session['user_clear_card_search'] = False

    try:
        search_wish_term = request.session['user_search_wish_term']
        user_wish_card_obj_list = request.session['user_wish_cards']
        user_wish_cards = CardFace.card_face_by_card(user_wish_card_obj_list)
        user_clear_wish_search = request.session['user_clear_wish_search']
    except KeyError:
        user_wish_obj_list = UserCards.get_user_wish_card(user_profile_obj.user)
        user_wish_cards = CardFace.card_face_by_card_and_oracle(card_id_list_full, user_wish_obj_list)
        search_wish_term = "Search"
        user_clear_wish_search = request.session['user_clear_wish_search'] = False

    deck_paginator = Paginator(user_decks, 10)
    try:
        decks = deck_paginator.page(deck_page)
    except PageNotAnInteger:
        decks = deck_paginator.page(1)
    except EmptyPage:
        decks = deck_paginator.page(deck_paginator.num_pages)

    card_paginator = Paginator(user_cards, 10)
    try:
        cards = card_paginator.page(card_page)
    except PageNotAnInteger:
        cards = card_paginator.page(1)
    except EmptyPage:
        cards = card_paginator.page(card_paginator.num_pages)

    wish_paginator = Paginator(user_wish_cards, 10)
    try:
        wish_cards = wish_paginator.page(card_wish_page)
    except PageNotAnInteger:
        wish_cards = wish_paginator.page(1)
    except EmptyPage:
        wish_cards = wish_paginator.page(wish_paginator.num_pages)
    o_player = not str(request.user.id) == user_id

    friend_obj = user_profile_obj.get_user_friends()
    pending_obj = user_profile_obj.get_user_pending()
    follower_obj = user_profile_obj.get_user_followers()

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {
        'font_family': font_family, 'should_translate': should_translate,
        'user_profile_obj': user_profile_obj,
        'has_friend': len(friend_obj) > 0,'friend_obj': friend_obj,
        'has_pending': len(pending_obj) > 0, 'pending_obj': pending_obj,
        'has_follower': len(follower_obj) > 0, 'follower_obj': follower_obj,
        'o_player': o_player,
        'deckPage': deck_page, 'deckPager': decks, 'search_deck_term': search_deck_term,
        'clear_deck_search': user_clear_deck_search, 'deckShow': (deck_paginator.count > 0 or user_clear_deck_search),
        'cardPage': card_page, 'cardPager': cards, 'search_card_term': search_card_term,
        'clear_card_search': user_clear_card_search, 'cardShow': (card_paginator.count > 0 or user_clear_card_search),
        'cardWishPage': card_wish_page, 'cardWishPager': wish_cards, 'search_wish_term': search_wish_term,
        'clear_wish_search': user_clear_wish_search, 'wishShow': (wish_paginator.count > 0 or user_clear_wish_search),
    }
    return render(request, 'Users/user_profile.html', context)
