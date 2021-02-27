from django.db import models


# Create your models here.
class Settings(models.Model):
    """
        Stores general settings for the app
            * lastCardImport - Date of last card import
            * lastRuleImport - Date of last rule import
            * lastSymbolImport - Dat of last symbol import
    """
    lastCardImport = models.CharField(max_length=200)
    lastRuleImport = models.CharField(max_length=200)
    lastSymbolImport = models.CharField(max_length=200)

    def __str__(self):
        return self.id
