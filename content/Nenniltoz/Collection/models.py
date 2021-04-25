import logging
import operator
import datetime
from functools import reduce

from django.core import serializers

from django.db import models
from django.db.models import Q

from static.python.api_access import APIAccess

logger = logging.getLogger("logger")

#region Cards
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


class CardIDList(models.Model):
    """
        Stores Unique card named objects
            * card_id - ID for the card (specific to printing)
            * name - Name of the card
    """
    card_id = models.CharField(max_length=200)
    oracle_id = models.CharField(max_length=200)
    card_name = models.CharField(max_length=200)
    card_name.null = True
    card_url = models.CharField(max_length=200)
    card_url.null = True
    color_id = models.CharField(max_length=50)
    tcg_price = models.CharField(max_length=1000)
    tcg_set = models.BooleanField(default=False)
    tcg_price_date = models.DateField(default=datetime.datetime.now())

    @staticmethod
    def get_tcg_price(oracle_id):
        card = CardIDList.objects.get(
            Q(oracle_id=oracle_id)
        )
        date = datetime.datetime.now() - datetime.timedelta(days=3)
        tcg_pricing = ""
        tcg_set = False
        if not card.tcg_set or card.tcg_price_date < date.date():
            tcg_card_list = APIAccess.run_post(
                APIAccess.Relevance,
                [{"value": [card.card_name], "name": "ProductName"}],
                1,
                0
            ).json()
            if int(tcg_card_list["totalItems"]) > 0:
                tcg_pricing = ""
                te = tcg_card_list["results"]
                for price in APIAccess.run_pricing(te).json()["results"]:
                    tcg_pricing = tcg_pricing + \
                        '{' + \
                            '"market_price":"' + str(price["marketPrice"]).replace(",","&#44;") + \
                            '","type_name":"' + price["subTypeName"] + \
                            '","url":"' + APIAccess.build_url(tcg_card_list["results"]) + \
                        '"} ,}'
                    tcg_set = True
                tcg_pricing = tcg_pricing.strip(",}").strip(" ")
            card.tcg_set = tcg_set
            card.tcg_price = tcg_pricing
            card.tcg_price_date = datetime.datetime.now()
            card.save()

        if card.tcg_set:
            return card.tcg_price.split(",}")
        else:
            return "Not listed"

    @staticmethod
    def get_cards():
        return CardIDList.objects.all().order_by('card_name')

    @staticmethod
    def get_card_by_name(name):
        return CardIDList.objects.get(card_name=name)

    @staticmethod
    def get_card_face():
        card_id_list_full = CardIDList.get_cards()
        full_card_list_all = []

        for card_list_obj in card_id_list_full:
            full_card_list_all.append(card_list_obj.card_id)

        return CardFace.objects.select_related().filter(
            Q(legal__card_obj__card_id__in=full_card_list_all)
        ).order_by('name')

    @staticmethod
    def get_card_by_oracle(oracle_id):
        return CardIDList.objects.get(oracle_id=oracle_id)
        # .get(oracle_id=oracle_id)

    @staticmethod
    def get_card_face_by_oracle(oracle_id):
        return  CardIDList.objects.get(oracle_id=oracle_id)

    @staticmethod
    def convert_to(obj_list):
        return serializers.serialize('xml', obj_list)

    @staticmethod
    def get_json(limit):
        if (limit):
            return QuickResult.get_oracles(limit)
        else:
            return QuickResult.run_oracles(limit)


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

    @staticmethod
    def get_base_symbols():
        return Symbol.objects.filter(symbol__in=['{W}', '{U}', '{B}', '{R}', '{G}', '{C}', '{S}'])

    @staticmethod
    def get_colorless():
        return Symbol.objects.filter(
            symbol__in=['', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                        '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                        '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}'])

    @staticmethod
    def get_green():
        return Symbol.objects.filter(
            symbol__in=['{B/G}', '{R/G}', '{G/W}', '{G/U}', '{2/G}', '{G/P}', '{HG}'])

    @staticmethod
    def get_red():
        return Symbol.objects.filter(
            symbol__in=['{B/R}', '{U/R}', '{R/G}', '{R/W}', '{2/R}', '{R/P}', '{HR}'])

    @staticmethod
    def get_black():
        return Symbol.objects.filter(
            symbol__in=['{W/B}', '{B/R}', '{B/G}', '{U/B}', '{2/B}', '{B/P}', '{HB}'])

    @staticmethod
    def get_blue():
        return Symbol.objects.filter(
            symbol__in=['{W/U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}'])

    @staticmethod
    def get_white():
        return Symbol.objects.filter(
            symbol__in=['{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}'])

class QuickResult(models.Model):
    search = models.CharField(max_length=500)
    last_update = models.DateField(default=datetime.datetime.now())
    result = models.TextField(default='{}')

    def __str__(self):
        return self.search

    @staticmethod
    def get_oracles(card_manager, limit):
        date = datetime.datetime.now() - datetime.timedelta(days=7)
        obj = QuickResult.objects.get(search='oracles')
        if obj.last_update < date.date():
            QuickResult.run_oracles(card_manager, limit)
            obj = QuickResult.objects.get(search='oracles')
        return obj.result

    @staticmethod
    def run_oracles(card_manager, limit):
        if limit:
            card_id_list_full = CardIDList.get_cards()[0:5000]
        else:
            card_id_list_full = CardIDList.get_cards()

        full_card_list_all = []
        for card_list_obj in card_id_list_full:
            full_card_list_all.append(card_list_obj.card_id)

        filtered_card_list = card_manager.select_related().filter(
            Q(legal__card_obj__card_id__in=full_card_list_all)
        ).order_by('name')

        card_json_list = ""
        i = 0
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1 and i + 1 < len(filtered_card_list):
                card_json_list = card_json_list + '}, '
                i += 1

        if limit:
            obj, created = QuickResult.objects.get_or_create(
                search='oracles',
            )
            obj.last_update = datetime.datetime.now()
            obj.result = card_json_list.__str__()
            obj.save()
        else:
            return card_json_list

    @staticmethod
    def get_keyword(card_manager, keyword):
        try:
            date = datetime.datetime.now() - datetime.timedelta(days=7)
            obj = QuickResult.objects.get(search=keyword)
            if obj.last_update < date.date():
                QuickResult.run_keyword(card_manager, keyword)
                obj = QuickResult.objects.get(search=keyword)
        except QuickResult.DoesNotExist:
            QuickResult.run_keyword(card_manager, keyword)
            obj = QuickResult.objects.get(search=keyword)
        return obj.result

    @staticmethod
    def run_keyword(card_manager, keyword):
        filtered_card_list = card_manager.select_related().filter(
            Q(legal__card_obj__card_id__in=CardIDList.objects.values("card_id").all()) &
            Q(card_search__icontains=keyword)
            ).order_by('name')

        card_json_list = ""
        i = 0
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1 and i + 1 < len(filtered_card_list):
                card_json_list = card_json_list + '}, '
                i += 1

        obj, created = QuickResult.objects.get_or_create(
            search=keyword,
        )
        obj.last_update = datetime.datetime.now()
        obj.result = card_json_list.__str__()
        obj.save()

    @staticmethod
    def get_color(card_manager, color):
        color_term = ""

        for col in color:
            color_term = color_term + col

        try:
            date = datetime.datetime.now() - datetime.timedelta(days=7)
            obj = QuickResult.objects.get(search=color_term)
            if obj.last_update < date.date():
                QuickResult.run_color(card_manager, color, color_term)
                obj = QuickResult.objects.get(search=color_term)
        except QuickResult.DoesNotExist:
            QuickResult.run_color(card_manager, color, color_term)
            obj = QuickResult.objects.get(search=color_term)
        return obj.result

    @staticmethod
    def run_color(card_manager, color, color_term):
        filtered_card_list = card_manager.select_related().filter(
            Q(legal__card_obj__card_id__in=CardIDList.objects.values("card_id").all()) &
            reduce(
                    operator.or_, (
                        Q(mana_cost__icontains=item) for item in color
                    )
                )
            ).order_by('name')

        card_json_list = ""
        i = 0
        for card in filtered_card_list:
            card_json_list = card_json_list + card.__str__()
            if len(filtered_card_list) > 1 and i + 1 < len(filtered_card_list):
                card_json_list = card_json_list + '}, '
                i += 1

        obj, created = QuickResult.objects.get_or_create(
            search=color_term,
        )
        obj.last_update = datetime.datetime.now()
        obj.result = card_json_list.__str__()
        obj.save()
