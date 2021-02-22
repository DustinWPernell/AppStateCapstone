from django.db import models


# Create your models here.
class Card(models.Model):
    cardID = models.CharField(max_length=200, primary_key=True)
    oracleID = models.CharField(max_length=200)
    keywords = models.CharField(max_length=500)
    rarity = models.CharField(max_length=20)
    setName = models.CharField(max_length=100)

    def __str__(self):
        return self.cardID


class CardFace(models.Model):
    name = models.CharField(max_length=200)
    imageURL = models.CharField(max_length=200)
    manaCost = models.CharField(max_length=100)
    loyalty = models.CharField(max_length=10)
    power = models.CharField(max_length=10)
    toughness = models.CharField(max_length=10)
    typeLine = models.CharField(max_length=500)
    colorId = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    flavorText = models.CharField(max_length=500)
    cardID = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.cardID


class Legality(models.Model):
    standard = models.CharField(max_length=15)
    future = models.CharField(max_length=15)
    historic = models.CharField(max_length=15)
    gladiator = models.CharField(max_length=15)
    modern = models.CharField(max_length=15)
    legacy = models.CharField(max_length=15)
    pauper = models.CharField(max_length=15)
    vintage = models.CharField(max_length=15)
    penny = models.CharField(max_length=15)
    commander = models.CharField(max_length=15)
    brawl = models.CharField(max_length=15)
    duel = models.CharField(max_length=15)
    oldSchool = models.CharField(max_length=15)
    premodern = models.CharField(max_length=15)
    cardID = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.cardID


class Symbol(models.Model):
    symbol = models.CharField(max_length=20)
    text = models.CharField(max_length=50)
    imageURL = models.CharField(max_length=200)
    isMana = models.CharField(max_length=20)
    manaCost = models.CharField(max_length=20)
    manaCost.null = True
    colorID = models.CharField(max_length=200)

    def __str__(self):
        return self.symbol


class Rule(models.Model):
    oracleID = models.CharField(max_length=200)
    pub_date = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.oracleID
