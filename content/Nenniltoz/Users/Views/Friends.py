import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View

from Users.models import Friends, PendingFriends, Followers

logger = logging.getLogger(__name__)

class Add_Follower(View):
    user = User
    @login_required
    def post(self, request, user_id):
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

class Add_Friend(View):
    user = User
    @login_required
    def post(self, request, user_id):
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

class Remove_Follower(View):
    user = User
    @login_required
    def post(self, request, user_id):
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

class Remove_Friend(View):
    user = User
    @login_required
    def post(self, request, user_id):
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

class Send_Friend_Request(View):
    user = User

    def add_friend(self, request, user_id):
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

    @login_required
    def post(self, request, user_id):
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
            self.add_friend(request, friend_obj.id)
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

class Process_Friend(View):
    user = User

    def add_friend(self, request, user_id):
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

    @login_required
    def post(self, request, user_id):
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
                self.add_friend(request, user_id)
            return redirect('user_profile', user_id=str(request.user.id))
        else:
            return redirect('user_profile', user_id=str(friend_obj.id))