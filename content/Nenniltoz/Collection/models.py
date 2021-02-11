from django.db import models


# Create your models here.
class Card(models.Model):
    cardID = models.CharField(max_length=200)
    name = models.DateTimeField('date published')
    imageURL = models.CharField(max_length=200)
    manaCost = models.CharField(max_length=100)
    loyalty = models.CharField(max_length=10)
    power = models.CharField(max_length=10)
    toughness = models.CharField(max_length=10)
    typeLine = models.CharField(max_length=500)
    colorId = models.CharField(max_length=200)
    keywords = models.CharField(max_length=500)
    twoFace = models.BooleanField()

    def __str__(self):
        return self.name


class Legality(models.Model):
    cardID = models.ForeignKey(Card, on_delete=models.CASCADE)
    standard = models.BooleanField()
    future = models.BooleanField()
    historic = models.BooleanField()
    gladiator = models.BooleanField()
    modern = models.BooleanField()
    legacy = models.BooleanField()
    pauper = models.BooleanField()
    vintage = models.BooleanField()
    penny = models.BooleanField()
    commander = models.BooleanField()
    brawl = models.BooleanField()
    duel = models.BooleanField()
    oldSchool = models.BooleanField()
    premodern = models.BooleanField()

    def __str__(self):
        return self.cardID


class Rule(models.Model):
    cardID = models.ForeignKey(Card, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.cardID


class Symbol(models.Model):
    symbol = models.CharField(max_length=10)
    text = models.CharField(max_length=50)
    imageURL = models.CharField(max_length=200)
    isMana = models.BooleanField()
    manaCost = models.CharField(max_length=10)
    colorID = models.CharField(max_length=200)

    def __str__(self):
        return self.symbol
