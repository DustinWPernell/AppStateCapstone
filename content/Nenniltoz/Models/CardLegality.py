from django.db import models

from Models.Card import Card


class CardLegalityManager(models.Manager):
    def get_card_set(self, card_id):
        return CardLegality.objects.get(card_obj__card_id=card_id)

    def legal_or_not(self, legal_term):
        if legal_term == "legal":
            return "legalTableField"
        elif legal_term == "banned":
            return "bannedTableField"
        else:
            return "notLegalTableField"

    def legality_create(self, card, standard, future, historic, gladiator, modern, legacy, pauper, vintage, penny, commander,
               brawl, duel, oldschool, premodern):
        return CardLegality.objects.create(
            card_obj=card,
            standard=self.legal_or_not(standard),
            future=self.legal_or_not(future),
            historic=self.legal_or_not(historic),
            gladiator=self.legal_or_not(gladiator),
            modern=self.legal_or_not(modern),
            legacy=self.legal_or_not(legacy),
            pauper=self.legal_or_not(pauper),
            vintage=self.legal_or_not(vintage),
            penny=self.legal_or_not(penny),
            commander=self.legal_or_not(commander),
            brawl=self.legal_or_not(brawl),
            duel=self.legal_or_not(duel),
            old_school=self.legal_or_not(oldschool),
            premodern=self.legal_or_not(premodern),
        )

    def legality_update(self, card_id, standard, future, historic, gladiator, modern, legacy, pauper, vintage, penny, commander,
               brawl, duel, oldschool, premodern):
        return CardLegality.objects.filter(card_obj__card_id=card_id).update(
            standard=self.legal_or_not(standard),
            future=self.legal_or_not(future),
            historic=self.legal_or_not(historic),
            gladiator=self.legal_or_not(gladiator),
            modern=self.legal_or_not(modern),
            legacy=self.legal_or_not(legacy),
            pauper=self.legal_or_not(pauper),
            vintage=self.legal_or_not(vintage),
            penny=self.legal_or_not(penny),
            commander=self.legal_or_not(commander),
            brawl=self.legal_or_not(brawl),
            duel=self.legal_or_not(duel),
            old_school=self.legal_or_not(oldschool),
            premodern=self.legal_or_not(premodern),
        )

class CardLegality(models.Model):
    """
        Stores legality for specific card
            * standard - Game type standard
            * future - Game type future
            * historic - Game type historic
            * gladiator - Game type gladiator
            * modern - Game type modern
            * legacy - Game type legacy
            * pauper - Game type pauper
            * vintage - Game type vintage
            * penny - Game type penny
            * commander - Game type commander
            * brawl - Game type brawl
            * duel - Game type duel
            * oldSchool - Game type oldSchool
            * premodern - Game type premodern
            * card_id - ID for the card (specific to printing)
    """
    standard = models.CharField(max_length=30)
    future = models.CharField(max_length=30)
    historic = models.CharField(max_length=30)
    gladiator = models.CharField(max_length=30)
    modern = models.CharField(max_length=30)
    legacy = models.CharField(max_length=30)
    pauper = models.CharField(max_length=30)
    vintage = models.CharField(max_length=30)
    penny = models.CharField(max_length=30)
    commander = models.CharField(max_length=30)
    brawl = models.CharField(max_length=30)
    duel = models.CharField(max_length=30)
    old_school = models.CharField(max_length=30)
    premodern = models.CharField(max_length=30)
    card_obj = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='legal_card')

    objects = CardLegalityManager()


    class Meta:
        app_label = "Management"

    def __int__(self):
        return self.id