from datetime import datetime

from django.db import models


# Create your models here.
class CardLayout(models.Model):
    """
        Stores different kinds of layouts for card
            * layout - Type of layout
            * sides - number of sides a layout has
            * multiFace - number of faces a layout has
    """
    layout = models.CharField(max_length=30)
    sides = models.IntegerField()
    multi_face = models.IntegerField()

    def __int__(self):
        return self.id


class IgnoreCards(models.Model):
    """
        Stores cards that should be ignored during import
            * type - Type of field that should be searched (name/set)
            * value - Value that should be looked for
    """
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value


class Card(models.Model):
    """
        Stores a card object
            * card_id - ID for the card (specific to printing)
            * oracleID - ID for the card (specific to name)
            * keywords - Keywords that appear on all faces of the card
            * rarity - How rare the card is
            * setName - Set of the card
            * layout - Layout of the card
            * setOrder - Order in which set occurs
            * color - Stores color identity of card
    """
    card_id = models.CharField(max_length=200, primary_key=True)
    oracle_id = models.CharField(max_length=200)
    keywords = models.CharField(max_length=500)
    rarity = models.CharField(max_length=20)
    set_name = models.CharField(max_length=100)
    layout = models.CharField(max_length=30)
    set_order = models.IntegerField()
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.card_id


class CardIDList(models.Model):
    """
        Stores Unique card named objects
            * card_id - ID for the card (specific to printing)
            * name - Name of the card
    """
    card_id = models.CharField(max_length=200, primary_key=True)
    card_name = models.CharField(max_length=200)
    card_name.null = True


class CardFace(models.Model):
    """
        Stores card face object (could be many for one card object)
            * name - Name of the card face
            * image_url - URL for the card face image
            * mana_cost - Mana cost for the card face
            * loyalty - Starting loyalty for the card (may be empty)
            * power - Base power for the card (may be empty)
            * toughness - Base toughness for the card (may be empty)
            * type_line - The type line for the card (Creature/Enchantment/...)
            * color_id - The color id of the card
            * text - The text displayed in the main area of the card
            * flavor_text - The fun text normally display at the bottom of the card (may be empty)
            * card_id - ID for the card (specific to printing)
            * avatar_img - Image URL for profile avatars
            * set_order - Order in which set occurs
            * firstFace - Boolean used in displaying cards with multiple faces
    """
    name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    mana_cost = models.CharField(max_length=100)
    loyalty = models.CharField(max_length=10)
    power = models.CharField(max_length=10)
    toughness = models.CharField(max_length=10)
    type_line = models.CharField(max_length=500)
    color_id = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    flavor_text = models.CharField(max_length=500)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    avatar_img = models.CharField(max_length=200)
    set_order = models.IntegerField()
    first_face = models.BooleanField()

    def __int__(self):
        return self.id


class Legality(models.Model):
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
    old_school = models.CharField(max_length=15)
    premodern = models.CharField(max_length=15)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.card_id


class Symbol(models.Model):
    """
        Stores symbols
            * symbol - Symbol key example: {B}
            * text -
            * imageURL - URL for the symbol image
            * isMana - Boolean stating if the symbol is mana
            * manaCost - Mana cost for the symbol
            * colorID - Color id for the symbol
    """
    symbol = models.CharField(max_length=20)
    text = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)
    is_mana = models.CharField(max_length=20)
    mana_cost = models.CharField(max_length=20)
    mana_cost.null = True
    color_id = models.CharField(max_length=200)

    def __str__(self):
        return self.symbol


class Rule(models.Model):
    """
        Stores rule objects
            * oracleID - ID for the card (specific to name)
            * pub_date - Data the ruling was made
            * comment - The text about the ruling
    """
    oracle_id = models.CharField(max_length=200)
    pub_date = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.oracle_id


class CardSets(models.Model):
    """
        Stores rule objects
            * set_id - ID for the set
            * code - Short string to identify set
            * name - Full name of set
            * released_at - Data the set was released
            * icon_svg_uri - Set icon
            * order - Order in which the set will appear (newest first)
    """
    set_id = models.CharField(max_length=200, primary_key=True)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    released_at = models.DateField(default=datetime.now)
    icon_svg_uri = models.CharField(max_length=200)
    order = models.IntegerField()

    def __str__(self):
        return self.name
