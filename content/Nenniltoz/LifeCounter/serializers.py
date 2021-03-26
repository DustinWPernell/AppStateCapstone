from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Game, GamePlayer, GameLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'creator', 'game_code', 'game_type',
                  'started', 'created', 'modified')
        depth = 1


class GamePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayer
        fields = ('id', 'game', 'player', 'status', 'life', 'acorn', 'energy', 'poison', 'experience', 'storm',
                  'clues', 'food', 'treasure', 'commander_cost', 'commander_damage', 'monarch', 'citys_blessing')


class GameLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameLog
        fields = ('id', 'text', 'player', 'created')
        depth = 1
