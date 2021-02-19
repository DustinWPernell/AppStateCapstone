from django.db import models


# Create your models here.
class Settings(models.Model):
    lastCardImport = models.CharField(max_length=200)
    lastRuleImport = models.CharField(max_length=200)
    lastSymbolImport = models.CharField(max_length=200)

    def __str__(self):
        return self.id
