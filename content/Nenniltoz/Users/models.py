import self as self
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.
class Preference:
    SNIPPET_EXPOSURE_PUBLIC = 'public'
    SNIPPET_EXPOSURE_UNLIST = 'unlisted'
    SNIPPET_EXPOSURE_PRIVATE = 'private'

    exposure_choices = (
        (SNIPPET_EXPOSURE_PUBLIC, 'Public'),
        (SNIPPET_EXPOSURE_UNLIST, 'Unlisted'),
        (SNIPPET_EXPOSURE_PRIVATE, 'Private'),
    )


class Snippet(models.Model):
    title = models.CharField(max_length=200, blank=True)
    original_code = models.TextField()
    highlighted_code = models.TextField()
    exposure = models.CharField(max_length=10, choices=Preference.exposure_choices)
    hits = models.IntegerField(default=0)
    slug = models.SlugField()
    created_on = models.DateTimeField(auto_now_add=True)


class PendingFriends(models.Model):
    user_one = models.ForeignKey(User, related_name='pend_friend_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='pend_friend_two', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    rejected = models.BooleanField(default=False)


class Friends(models.Model):
    user_one = models.ForeignKey(User, related_name='friend_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='friend_two', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class Followers(models.Model):
    user_one = models.ForeignKey(User, related_name='follower_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='follower_two', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='user_profile', on_delete=models.CASCADE)
    default_exposure = models.CharField(max_length=10, choices=Preference.exposure_choices,
                                        default=Preference.SNIPPET_EXPOSURE_PUBLIC)

    def __int__(self):
        return self.user.id


class News(models.Model):
    headline = models.CharField(max_length=200)
    imageURL = models.CharField(max_length=200)

    def __str__(self):
        return self.headline
