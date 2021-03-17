from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.urls import reverse


# Create your models here.
class Preference:
    """
        Stores choices for settings
            * SNIPPET_EXPOSURE_PUBLIC - Setting for a public profile
            * SNIPPET_EXPOSURE_UNLIST - Setting for a unlisted profile
            * SNIPPET_EXPOSURE_PRIVATE - Setting for a private profile
    """
    SNIPPET_EXPOSURE_PUBLIC = 'public'
    SNIPPET_EXPOSURE_UNLIST = 'unlisted'
    SNIPPET_EXPOSURE_PRIVATE = 'private'

    exposure_choices = (
        (SNIPPET_EXPOSURE_PUBLIC, 'Public'),
        (SNIPPET_EXPOSURE_UNLIST, 'Unlisted'),
        (SNIPPET_EXPOSURE_PRIVATE, 'Private'),
    )


class PendingFriends(models.Model):
    """
        Stores pending friends in a 2 way relationship
            * user_one - Foreign key for linking to a User object
            * user_one - Foreign key for linking to a User object
            * created_on - Date object was created
            * rejected - Rejected status of the request
    """
    user_one = models.ForeignKey(User, related_name='pend_friend_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='pend_friend_two', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    rejected = models.BooleanField(default=False)


class Friends(models.Model):
    """
        Stores friends in a 2 way relationship
            * user_one - Foreign key for linking to a User object
            * user_one - Foreign key for linking to a User object
            * created_on - Date object was created
    """
    user_one = models.ForeignKey(User, related_name='friend_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='friend_two', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class Followers(models.Model):
    """
        Stores followers in a 2 way relationship
            * user_one - Foreign key for linking to a User object
            * user_one - Foreign key for linking to a User object
            * created_on - Date object was created
    """
    user_one = models.ForeignKey(User, related_name='follower_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='follower_two', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    """
        Stores user profiles
            * user - Foreign key for linking to a User object
            * default_exposure - Setting for privacy of a profile
    """
    user = models.ForeignKey(User, related_name='user_profile', on_delete=models.CASCADE)
    cardView = models.BooleanField(default=False)
    deckView = models.BooleanField(default=True)
    profileView = models.BooleanField(default=True)
    avatarImg = models.CharField(max_length=200)

    def __int__(self):
        return self.user.id


class UserCards(models.Model):
    """
        Stores user card relationship
            * user - Foreign key for linking to a User object
            * cardID - String containing cardID
            * quantity - number of cards owned. If 0 on wish list
    """
    user = models.ForeignKey(User, related_name='user_card', on_delete=models.CASCADE)
    cardID = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)


class News(models.Model):
    """
        Stores news object
            * headline - Heading to display on the page
            * imageURL - image URL to display on the page
    """
    headline = models.CharField(max_length=200)
    imageURL = models.CharField(max_length=200)
    eventDate = models.DateField(default=datetime.now)

    def __str__(self):
        return self.headline
