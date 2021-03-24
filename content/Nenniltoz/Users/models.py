from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.db.models import Q

from Collection.models import CardFace
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
            مناهج الحساب
    """
    user = models.ForeignKey(User, related_name='user_profile', on_delete=models.CASCADE)
    card_view = models.BooleanField(default=False)
    deck_view = models.BooleanField(default=True)
    profile_view = models.BooleanField(default=True)
    avatar_img = models.CharField(max_length=200)
    font_family = models.CharField(max_length=200, default='default_font')
    translate = models.CharField(max_length=200, default='')

    def __int__(self):
        return self.user.id

    def get_user_friends(self):
        friend_list = Friends.objects.filter(user_one=self.user)
        friend_user_list = []
        for friend in friend_list:
            friend_user_list.append(friend.user_two)

        return friend_user_list

    def get_user_pending(self):
        pending_list = PendingFriends.objects.filter(user_two=self.user, rejected=False)
        pending_user_list = []
        for pending in pending_list:
            pending_user_list.append(pending.user_one)

        return pending_user_list

    def get_user_followers(self):
        follower_list = Followers.objects.filter(user_one=self.user)
        follower_user_list = []
        for follower in follower_list:
            follower_user_list.append(follower.user_two)

        return follower_user_list

    @staticmethod
    def get_profile_by_user(user_id):
        return UserProfile.objects.select_related().get(user__id=user_id)

    @staticmethod
    def get_font(user):
        if user.is_authenticated:
            up = UserProfile.objects.get(user=user)
            return up.font_family
        else:
            return 'default_font'

    @staticmethod
    def get_translate(user):
        if user.is_authenticated:
            up = UserProfile.objects.get(user=user)
            return up.translate
        else:
            return 'notranslate'


class UserCards(models.Model):
    """
        Stores user card relationship
            * user - Foreign key for linking to a User object
            * card_id - String containing card_id
            * quantity - number of cards owned. If 0 on wish list
    """
    user = models.ForeignKey(User, related_name='user_card', on_delete=models.CASCADE)
    card = models.ForeignKey(CardFace, related_name='card_obj', on_delete=models.CASCADE)
    oracle_id = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    wish = models.BooleanField(default=False)
    notes = models.CharField(max_length=1000, default="")

    @staticmethod
    def get_user_card(user, wish):
        return UserCards.objects.values('oracle_id').filter(
            Q(user=user) &
            Q(wish=wish)
        )

    @staticmethod
    def get_user_card_term(user, term, wish):
        return UserCards.objects.select_related().filter(
            Q(user=user) &
            Q(wish=wish) & (
                (
                    Q(card__name__icontains=term) |
                    Q(card__text__icontains=term) |
                    Q(card__type_line__icontains=term) |
                    Q(card__flavor_text__icontains=term) |
                    Q(card__legal__card_obj__keywords__icontains=term)
                ) | Q(notes__icontains='{'+term+'}')
            )
        ).order_by('card__name')

    @staticmethod
    def get_user_card_by_oracle(oracle_id, user):
        return UserCards.objects.get(
            Q(oracle_id=oracle_id) &
            Q(user=user)
        )

    @staticmethod
    def get_user_card_by_oracle_list(oracle_ids, user):
        return UserCards.objects.select_related().filter(
            Q(oracle_id__in=oracle_ids) &
            Q(user=user)
        )


class News(models.Model):
    """
        Stores news object
            * headline - Heading to display on the page
            * imageURL - image URL to display on the page
    """
    headline = models.CharField(max_length=200)
    eventDate = models.DateField(default=datetime.now)
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.headline

    @staticmethod
    def get_next_5():
        return News.objects.order_by('-headline')[:5]
