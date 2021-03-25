from django.db import models


# Create your models here.
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
