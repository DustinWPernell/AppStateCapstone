import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Nenniltoz.settings'

import django

django.setup()

from itertools import islice

import logging
from datetime import datetime
from urllib.request import urlopen

import ijson
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from Collection.models import Symbol, Rule, CardIDList, IgnoreCards
from Management.models import Settings
from Models import Card, CardFace, CardLayout, CardLegality, CardSet

logger = logging.getLogger("logger")


def build_comma_list(field, obj):
    array = get_from_json(field, obj)
    obj_list = ""
    for obj in array:
        obj_list = obj_list + ", " + obj

    obj_list = obj_list.strip()
    obj_list = obj_list.strip(",")
    return obj_list


def get_from_json(field, obj):
    if field in obj:
        return obj[field]
    else:
        return ""


def symbol_import_job(param):
    """Performs API call for symbols.

    Calls Scryfall API for retrieval of symbols. Parses symbols Json file. Creates symbols objects for each symbol.
    """
    logger.info("Param: " + param)
    Settings.objects.update_or_create(
        id=1,
        defaults={'lastSymbolImport': datetime.now().date()},
    )

    api_symbol = Settings.get_api_symbol()

    f = urlopen(api_symbol)
    objects = list(ijson.items(f, 'data.item'))
    for obj in objects:
        if 'symbol' in obj:
            symbol = obj['symbol']
        else:
            symbol = ""

        try:
            Symbol.objects.get(symbol=symbol)
        except Symbol.DoesNotExist:
            if 'english' in obj:
                english = obj['english']
            else:
                english = ""

            if 'svg_uri' in obj:
                svg_uri = obj['svg_uri']
            else:
                svg_uri = ""

            if 'represents_mana' in obj:
                represents_mana = obj['represents_mana']
            else:
                represents_mana = ""

            if 'cmc' in obj:
                cmc = obj['cmc']
            else:
                cmc = ""

            color_id = build_comma_list('colors', obj)

            Symbol.objects.create(
                symbol=symbol,
                text=english,
                image_url=svg_uri,
                is_mana=represents_mana,
                mana_cost=cmc,
                color_id=color_id,
            )
    return HttpResponse("Finished")


def set_import_job(param):
    """Performs API call for sets.

    Calls Scryfall API for retrieval of sets. Parses sets Json file. Creates sets objects for each set.
    """
    logger.info("Param: " + param)

    api_set = Settings.get_api_set()

    f = urlopen(api_set)
    objects = list(ijson.items(f, 'data.item'))
    for obj in objects:
        if 'id' in obj:
            set_id = obj['id']
        else:
            set_id = ""

        try:
            CardSet.objects.get_card_set(set_id, '')
        except ObjectDoesNotExist:
            if 'code' in obj:
                code = obj['code']
            else:
                code = ""
            if 'name' in obj:
                name = obj['name']
            else:
                name = ""
            if 'released_at' in obj:
                released_at = obj['released_at']
            else:
                released_at = ""
            if 'icon_svg_uri' in obj:
                icon_svg_uri = obj['icon_svg_uri']
            else:
                icon_svg_uri = ""

            CardSet.objects.set_create(set_id, code, name, released_at, icon_svg_uri)
    return HttpResponse("Finished")


def rule_import_job(param):
    """Performs API call for rules.

    Calls Scryfall API for retrieval of bulk rules. Parses bulk rule Json file. Creates a Rule object for each rule.
    """
    logger.info("Param: " + param)
    Settings.objects.update_or_create(
        id=1,
        defaults={'lastRuleImport': datetime.now().date()},
    )

    api_rule = Settings.get_api_rule()

    Rule.objects.all().delete()

    objects = list(ijson.items(urlopen(api_rule), 'item'))

    batch_size = 100
    rule_obj = (Rule(oracle_id='%s' % i['oracle_id'],
                     pub_date='%s' % i['published_at'],
                     comment='%s' % i['comment']
                     ) for i in objects)
    while True:
        batch = list(islice(rule_obj, batch_size))
        if not batch:
            break
        Rule.objects.bulk_create(batch, batch_size)

    # for obj in objects:
    #   if 'oracle_id' in obj:
    #        oracle_id = obj['oracle_id']
    #    else:
    #        oracle_id = ""
    #    if 'published_at' in obj:
    #        published_at = obj['published_at']
    #    else:
    #        published_at = ""
    #    if 'comment' in obj:
    #        comment = obj['comment']
    #    else:
    #        comment = ""

    #    Rule.objects.create(
    #        oracle_id=oracle_id,
    #        pub_date=published_at,
    #        comment=comment,
    #    )
    return HttpResponse("Finished")

def build_color_list(list):
    color_list = ''
    for color in list:
        color = color.replace("\"", "")
        color_list = color_list + "{" + color + "}"
    return color_list

def oracle_import_job(param):
    logger.info("Param: " + param)

    api_sing_card = Settings.get_api_sing_card()

    CardIDList.objects.all().delete()

    f = urlopen(api_sing_card)
    objects = list(ijson.items(f, 'item'))

    batch_size = 100
    rule_obj = (Rule(card_id='%s' % i['id'],
                     oracle_id='%s' % i['oracle_id'],
                     card_name='%s' % i['name'],
                     card_file='%s' % i['image_uris']['png'],
                     color_id='%s' % build_color_list(i['color_id'])
                     ) for i in objects)
    while True:
        batch = list(islice(rule_obj, batch_size))
        if not batch:
            break
        Rule.objects.bulk_create(batch, batch_size)

    # for obj in objects:
    #    if check_card_obj(obj):
    #        CardIDList.objects.create(
    #            card_id=obj['id'],
    #            oracle_id=obj['oracle_id'],
    #            card_name=obj['name']
    #        )
    return HttpResponse("Finished")


def card_import_job(param):
    """Performs API call for cards.

    Calls Scryfall API for retrieval of bulk cards. Parses bulk card Json file.
    Creates Card, Card faces, and legalities objects for each card.
    """
    logger.info("Param: " + param)

    Settings.objects.update_or_create(
        id=1,
        defaults={'lastCardImport': datetime.now().date()}
    )

    api_card = Settings.get_api_card()

    objects = list(ijson.items(urlopen(api_card), 'item'))
    for obj in objects:
        if check_card_obj(obj):
            card_id = obj['id']
            ori_id = obj['oracle_id']
            set_name = obj['set_name']
            rarity = obj['rarity']
            layout = obj['layout']
            key_words = build_comma_list('keywords', obj)
            color_list = build_comma_list('color_identity', obj)
            set_obj = CardSet.objects.get_card_set('', set_name)
            layout_obj = CardLayout.objects.get_card_layout(layout=layout, sides=-1, multi_face=-1)

            standard = obj['legalities']['standard']
            future = obj['legalities']['future']
            historic = obj['legalities']['historic']
            gladiator = obj['legalities']['gladiator']
            modern = obj['legalities']['modern']
            legacy = obj['legalities']['legacy']
            pauper = obj['legalities']['pauper']
            vintage = obj['legalities']['vintage']
            penny = obj['legalities']['penny']
            commander = obj['legalities']['commander']
            brawl = obj['legalities']['brawl']
            duel = obj['legalities']['duel']
            old_school = obj['legalities']['oldschool']
            premodern = obj['legalities']['premodern']

            try:
                CardLegality.objects.get_card_set(card_id)

                Card.objects.card_update(
                    card_id, ori_id, key_words, set_name, rarity, layout_obj, set_obj, color_list
                )

                CardLegality.objects.legality_update(
                    card_id, standard, future, historic, gladiator, modern, legacy, pauper, vintage, penny,
                    commander, brawl, duel, old_school, premodern,
                )

                if 'card_faces' not in obj:
                    name = get_from_json('name', obj)
                    if 'image_uris' in obj:
                        image_url = get_from_json('png', obj['image_uris'])
                        avatar_img = get_from_json('art_crop', obj['image_uris'])
                    else:
                        image_url = ""
                        avatar_img = ""
                    mana_cost = get_from_json('mana_cost', obj)
                    loyalty = get_from_json('loyalty', obj)
                    power = get_from_json('power', obj)
                    toughness = get_from_json('toughness', obj)
                    oracle_text = get_from_json('oracle_text', obj)
                    type_line = get_from_json('type_line', obj)
                    flavor_text = get_from_json('flavor_text', obj)
                    color_id = build_comma_list('color_identity', obj)

                    card_search = key_words + ' // ' + set_name + ' // ' + name + ' // ' + oracle_text + ' // ' + type_line

                    CardFace.objects.card_face_update(
                        card_id=card_id,
                        name=name,
                        image_url=image_url,
                        mana_cost=mana_cost,
                        loyalty=loyalty,
                        power=power,
                        toughness=toughness,
                        type_line=type_line,
                        color_id=color_id,
                        text=oracle_text,
                        flavor_text=flavor_text,
                        avatar_img=avatar_img,
                        card_search=card_search,
                    )
                else:
                    for face in obj['card_faces']:
                        name = get_from_json('name', face)
                        if 'image_uris' in face:
                            image_url = get_from_json('png', face['image_uris'])
                            avatar_img = get_from_json('art_crop', face['image_uris'])
                        else:
                            image_url = get_from_json('png', obj['image_uris'])
                            avatar_img = get_from_json('art_crop', obj['image_uris'])
                        mana_cost = get_from_json('mana_cost', face)
                        loyalty = get_from_json('loyalty', face)
                        power = get_from_json('power', face)
                        toughness = get_from_json('toughness', face)
                        oracle_text = get_from_json('oracle_text', face)
                        type_line = get_from_json('type_line', face)
                        flavor_text = get_from_json('flavor_text', face)
                        color_id = build_comma_list('color_identity', face)

                        card_search = key_words + ' // ' + set_name + ' // ' + name + ' // ' + oracle_text + ' // ' + type_line + ' // ' + flavor_text

                        CardFace.objects.card_face_update(
                            card_id=card_id,
                            name=name,
                            image_url=image_url,
                            mana_cost=mana_cost,
                            loyalty=loyalty,
                            power=power,
                            toughness=toughness,
                            type_line=type_line,
                            color_id=color_id,
                            text=oracle_text,
                            flavor_text=flavor_text,
                            avatar_img=avatar_img,
                            card_search=card_search,
                        )
            except ObjectDoesNotExist:

                new_card = Card.objects.card_create(
                    card_id, ori_id, key_words, set_name, rarity, layout_obj, set_obj, color_list
                )

                new_legal = CardLegality.objects.legality_create(
                    new_card, standard, future, historic, gladiator, modern, legacy, pauper, vintage, penny,
                    commander, brawl, duel, old_school, premodern,
                )

                if 'card_faces' not in obj:
                    name = get_from_json('name', obj)
                    if 'image_uris' in obj:
                        image_url = get_from_json('png', obj['image_uris'])
                        avatar_img = get_from_json('art_crop', obj['image_uris'])
                    else:
                        image_url = ""
                        avatar_img = ""
                    mana_cost = get_from_json('mana_cost', obj)
                    loyalty = get_from_json('loyalty', obj)
                    power = get_from_json('power', obj)
                    toughness = get_from_json('toughness', obj)
                    oracle_text = get_from_json('oracle_text', obj)
                    type_line = get_from_json('type_line', obj)
                    flavor_text = get_from_json('flavor_text', obj)
                    color_id = build_comma_list('color_identity', obj)

                    card_search = key_words + ' // ' + set_name + ' // ' + name + ' // ' + oracle_text + ' // ' + type_line + ' // ' + flavor_text

                    CardFace.objects.card_face_create(
                        name=name,
                        image_url=image_url,
                        mana_cost=mana_cost,
                        loyalty=loyalty,
                        power=power,
                        toughness=toughness,
                        type_line=type_line,
                        color_id=color_id,
                        text=oracle_text,
                        flavor_text=flavor_text,
                        avatar_img=avatar_img,
                        first_face=True,
                        legal=new_legal,
                        card_search=card_search,
                    )
                else:
                    first_face = True
                    for face in obj['card_faces']:
                        name = get_from_json('name', face)
                        if 'image_uris' in face:
                            image_url = get_from_json('png', face['image_uris'])
                            avatar_img = get_from_json('art_crop', face['image_uris'])
                        else:
                            image_url = get_from_json('png', obj['image_uris'])
                            avatar_img = get_from_json('art_crop', obj['image_uris'])
                        mana_cost = get_from_json('mana_cost', face)
                        loyalty = get_from_json('loyalty', face)
                        power = get_from_json('power', face)
                        toughness = get_from_json('toughness', face)
                        oracle_text = get_from_json('oracle_text', face)
                        type_line = get_from_json('type_line', face)
                        flavor_text = get_from_json('flavor_text', face)
                        color_id = build_comma_list('color_identity', face)

                        card_search = key_words + ' // ' + set_name + ' // ' + name + ' // ' + oracle_text + ' // ' + type_line + ' // ' + flavor_text

                        CardFace.objects.card_face_create(
                            name=name,
                            image_url=image_url,
                            mana_cost=mana_cost,
                            loyalty=loyalty,
                            power=power,
                            toughness=toughness,
                            type_line=type_line,
                            color_id=color_id,
                            text=oracle_text,
                            flavor_text=flavor_text,
                            avatar_img=avatar_img,
                            first_face=first_face,
                            legal=new_legal,
                            card_search=card_search,
                        )
                        first_face = False
    return HttpResponse("Finished")


def check_card_obj(obj):
    """Checks for certain issues with cards.

    Loops through values in the database to determine if passed card data should be ignored.

    @param obj: Unprocessed card object in Json format

    @returns:
        * True: Card is good
        * False: Card is bad

    """
    set_ignore = IgnoreCards.objects.filter(type="set")
    for set_obj in set_ignore:
        if obj['set_name'] == set_obj.value:
            return False

    name_ignore = IgnoreCards.objects.filter(type="name")
    if 'card_faces' not in obj:
        name_val = obj['name']
    else:
        name_val = ""

    for name in name_ignore:
        if name.value in name_val:
            return False
    return True
