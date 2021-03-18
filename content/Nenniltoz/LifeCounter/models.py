import hashlib

from django.contrib.auth.models import User
from django.db import models
import json
from datetime import datetime

# Create your models here.
from django.db.models import Q

from Users.models import UserProfile


class GameType(models.Model):
    GAME_TYPES = (
        ('standard', 'Standard'),
        ('future', 'Future'),
        ('historic', 'Historic'),
        ('gladiator', 'Gladiator'),
        ('modern', 'Modern'),
        ('legacy', 'Legacy'),
        ('pauper', 'Pauper'),
        ('vintage', 'Vintage'),
        ('penny', 'Penny'),
        ('commander', 'Commander'),
        ('brawl', 'Brawl'),
        ('duel', 'Duel'),
        ('oldSchool', 'Old School'),
        ('premodern', 'Premodern'),
    )

    type = models.CharField(choices=GAME_TYPES,
                              max_length=25,
                              default='Standard')
    num_players = models.IntegerField(default=2) # 0 is any number
    starting_life = models.IntegerField(default=20)
    min_deck_size = models.IntegerField(default=60)
    max_deck_size = models.IntegerField(default=0) # 0 for none
    side_board_size = models.IntegerField(default=15)
    card_copy_limit = models.IntegerField(default=4)
    has_commander = models.BooleanField(default=False)



class Game(models.Model):
    """
    Represents a game of Obstruction between two players.
    Initial values when created will just be a creator
    who is also the current_turn and the cols and rows
    """
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    game_code = models.CharField(max_length=200)
    game_type = models.ForeignKey(GameType, related_name='game_type', on_delete=models.CASCADE)
    started = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Game #{0}'.format(self.pk)

    @staticmethod
    def get_available_games():
        return Game.objects.filter(started=None)

    @staticmethod
    def created_count(user):
        return Game.objects.filter(creator=user).count()

    @staticmethod
    def get_by_id(id):
        try:
            return Game.objects.get(pk=id)
        except Game.DoesNotExist:
            # TODO: Handle this Exception
            pass

    @staticmethod
    def get_by_code(code):
        try:
            return Game.objects.get(game_code=code)
        except Game.DoesNotExist:
            # TODO: Handle this Exception
            pass

    @staticmethod
    def create_new(user, type):
        """
        Create a new game and game squares
        :param user: the user that created the game
        :return: a new game object
        """
        # make the game's name from the username and the number of
        # games they've created
        game_type = GameType.objects.get(type=type)
        hash = hashlib.sha1(('U' + str(user.id) + 'T' + str(game_type.id) + 'D' + str(datetime.now())).encode("UTF-8")).hexdigest()
        game_code = str(hash[:10]).upper()
        new_game = Game(creator=user, game_type=game_type, game_code=game_code)
        new_game.save()
        user_profile = UserProfile.objects.get(user=user)



        new_player = GamePlayer(
            game=new_game,
            player=user,
            life=new_game.game_type.starting_life,
            avatar_img=user_profile.avatarImg

        )

        new_player.save()
        # put first log into the GameLog
        new_game.add_log('Game created by {0}'.format(new_game.creator.username))

        return new_game

    def add_log(self, text, user=None):
        """
        Adds a text log associated with this game.
        """
        entry = GameLog(game=self, text=text, player=user).save()
        return entry

    def get_all_game_players(self):
        """
        Gets all of the players for this Game
        """
        return GamePlayer.objects.filter(game=self)

    def get_all_game_players_but_indicated(self, user):
        """
        Gets all of the players for this Game
        """
        return GamePlayer.objects.filter(Q(game=self) & ~Q(player=user))

    def get_game_player_stats(self, user):
        """
        Gets a square for a game by it's row and col pos
        """
        try:
            return GamePlayer.objects.get(game=self, player=user)
        except GamePlayer.DoesNotExist:
            return None

    def set_game_player_stats(self, user_id, stats):
        """
        Gets a square for a game by it's row and col pos
        """
        user = User.objects.get(id=user_id)

        try:
            player = GamePlayer.objects.get(game=self, player=user)
            if stats != {}:
                player.status = stats["status"]
                player.life = stats["life"]
                player.acorn = stats["acorn"]
                player.energy = stats["energy"]
                player.poison = stats["poison"]
                player.experience = stats["exp"]
                player.storm = stats["storm"]
                player.clues = stats["clues"]
                player.food = stats["food"]
                player.treasure = stats["treasure"]
                player.commander_cost = stats["commander_cost"]
                player.commander_damage = stats["commander_damage"]
                player.monarch = stats["monarch"]
                player.citys_blessing = stats["citys_blessing"]
                player.save()
        except GamePlayer.DoesNotExist:
            user_profile = UserProfile.objects.get(user=user)
            new_player = GamePlayer(
                game=self,
                player=user,
                life=self.game_type.starting_life,
                avatar_img=user_profile.avatarImg
            )
            new_player.save()


    def get_game_log(self):
        """
        Gets the entire log for the game
        """
        return GameLog.objects.filter(game=self)

    def send_game_update(self):
        """
        Send the updated game information and squares to the game's channel group
        """
        # imported here to avoid circular import
        from serializers import GamePlayerSerializer, GameLogSerializer, GameSerializer

        players = self.get_all_game_players()
        player_serializer = GamePlayerSerializer(players, many=True)

        # get game log
        log = self.get_game_log()
        log_serializer = GameLogSerializer(log, many=True)

        game_serilizer = GameSerializer(self)

        message = {'game': game_serilizer.data,
                   'log': log_serializer.data,
                   'players': player_serializer.data}

        return message


    def mark_started(self):
        """
        Sets a game to completed status and records the winner
        """
        self.started = datetime.now()
        self.save()


class GamePlayer(models.Model):
    STATUS_TYPES = (
        ('Forfeit', 'Forfeit'),
        ('Playing', 'Playing'),
        ('Dead', 'Dead')
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_TYPES,
                              max_length=25,
                              default='Playing')
    avatar_img = models.CharField(max_length=200)
    life = models.IntegerField()
    acorn = models.IntegerField(default=0)
    energy = models.IntegerField(default=0)
    poison = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    storm = models.IntegerField(default=0)
    clues = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    treasure = models.IntegerField(default=0)
    commander_cost = models.CharField(max_length=200, default="{{},}") # { {'commander_id': string,'added_cost': int}, }  cost increments by 2
    commander_damage = models.CharField(max_length=200, default="{{},}") # { {'user_id': int,'commander_id': string,'damage': int}, }
    monarch = models.BooleanField(default=False)
    citys_blessing = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0} - ({1}, {2})'.format(self.game, self.player, self.status)

    @staticmethod
    def get_by_id(id):
        try:
            return GamePlayer.objects.get(pk=id)
        except GamePlayer.DoesNotExist:
            # TODO: Handle exception for GamePlayer
            return None


class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    player = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Game #{0} Log'.format(self.game.id)