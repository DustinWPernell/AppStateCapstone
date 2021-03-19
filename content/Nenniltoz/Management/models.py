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

    def __str__(self):
        return self.id
