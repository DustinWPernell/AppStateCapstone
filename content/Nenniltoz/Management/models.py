import json
import datetime

import requests
from dateutil.parser import parse
from django.db import models


# Create your models here.
from Nenniltoz.settings import TCG_PUBLIC, TCG_PRIVATE


class Settings(models.Model):
    """
        Stores general settings for the app
            * lastCardImport - Date of last card import
            * lastRuleImport - Date of last rule import
            * lastSymbolImport - Dat of last symbol import
    """
    last_card_import = models.CharField(max_length=200)
    last_rule_import = models.CharField(max_length=200)
    last_symbol_import = models.CharField(max_length=200)
    api_bulk_data = models.CharField(max_length=200)
    api_card = models.CharField(max_length=200)
    api_symbol = models.CharField(max_length=200)
    api_rule = models.CharField(max_length=200)
    api_sing_card = models.CharField(max_length=200)
    api_set = models.CharField(max_length=200)
    bearer = models.CharField(max_length=500)
    bearer_exp = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return self.id

    @staticmethod
    def get_settings():
        return Settings.objects.get(id=1)

    @staticmethod
    def get_api_bulk_data():
        return Settings.objects.get(id=1).api_bulk_data

    @staticmethod
    def get_api_card():
        return Settings.objects.get(id=1).api_card

    @staticmethod
    def get_api_symbol():
        return Settings.objects.get(id=1).api_symbol

    @staticmethod
    def get_api_rule():
        return Settings.objects.get(id=1).api_rule

    @staticmethod
    def get_api_sing_card():
        return Settings.objects.get(id=1).api_sing_card

    @staticmethod
    def get_api_set():
        return Settings.objects.get(id=1).api_set

    @staticmethod
    def get_tcg_bearer():
        setting = Settings.objects.get(id=1)
        bearer_exp = setting.bearer_exp
        date = datetime.datetime.now() + datetime.timedelta(days=3)
        if bearer_exp < date.date():
            response = requests.post("https://api.tcgplayer.com/token",
                                    headers={
                                        "Content-Type": "application/json",
                                        "Accept": "application/json",
                                        "User-Agent": "Nenniltoz"
                                    },
                                    data=(f"grant_type=client_credentials"
                                          f"&client_id={TCG_PUBLIC}"
                                          f"&client_secret={TCG_PRIVATE}"))
            setting.bearer = response.json()['access_token']
            setting.bearer_exp = parse(response.json()['.expires'], fuzzy=True)
            setting.save()
        return setting.bearer
