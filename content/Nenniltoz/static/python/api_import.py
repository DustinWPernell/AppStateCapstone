import os
from itertools import islice

import boto3
from decouple import config
import requests

os.environ['DJANGO_SETTINGS_MODULE'] = 'Nenniltoz.settings'

import django

django.setup()

import logging
from datetime import datetime
from urllib.request import urlopen

import ijson
from django.http import HttpResponse

from Collection.models import Symbol, CardSets, Rule, CardIDList, Card, Legality, CardFace, IgnoreCards, CardLayout
from Management.models import Settings

logger = logging.getLogger("logger")


def build_comma_list(array_obj):
    list = ""
    for obj in array_obj:
        list = list + ", " + obj

    list = list.strip()
    list = list.strip(",")
    return list


def symbol_import_job(param):
    """Performs API call for symbols.

    Calls Scryfall API for retrieval of symbols. Parses symbols Json file. Creates symbols objects for each symbol.

    @param request:

    :todo: Set to process in background
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

            color_id = build_comma_list(obj['colors'])

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

    @param request:

    :todo: Set to process in background
    """
    logger.info("Param: " + param)

    api_set = Settings.get_api_set()

    f = urlopen(api_set)
    objects = list(ijson.items(f, 'data.item'))
    cur_order = 0
    for obj in objects:
        if 'id' in obj:
            set_id = obj['id']
        else:
            set_id = ""

        try:
            CardSets.objects.get(set_id=set_id)
        except CardSets.DoesNotExist:
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

            CardSets.objects.create(
                set_id=set_id,
                code=code,
                name=name,
                released_at=released_at,
                icon_svg_uri=icon_svg_uri,
                order=cur_order,
            )
        cur_order = cur_order + 1
    return HttpResponse("Finished")


def rule_import_job(param):
    """Performs API call for rules.

    Calls Scryfall API for retrieval of bulk rules. Parses bulk rule Json file. Creates a Rule object for each rule.

    @param request:

    :todo: Set to process in background
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


    #for obj in objects:
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
                     ) for i in objects)
    while True:
        batch = list(islice(rule_obj, batch_size))
        if not batch:
            break
        Rule.objects.bulk_create(batch, batch_size)

    #for obj in objects:
    #    if check_card_obj(obj):
    #        CardIDList.objects.create(
    #            card_id=obj['id'],
    #            oracle_id=obj['oracle_id'],
    #            card_name=obj['name']
    #        )
    return (HttpResponse("Finished"))


def card_image_job(param):
    logger.info("Param: " + param)

    session = boto3.Session(
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
    )
    s3 = session.client('s3')

    for card_face in CardFace.objects.select_related().all():
        card_id = card_face.legal.card_obj.card_id
        filename = "cards/image_%s" % card_id + '.png'
        image_data = requests.get(card_face.image_url, stream=True)
        try:
            s3.upload_fileobj(image_data.raw, config('AWS_STORAGE_BUCKET_NAME'), filename)
            card_face.image_file = filename
        except Exception as e:
            return e

        filename = "cards/avatar_%s" % card_id + '.png'
        image_data = requests.get(card_face.avatar_img, stream=True)
        try:
            s3.upload_fileobj(image_data.raw, config('AWS_STORAGE_BUCKET_NAME'), filename)
            card_face.avatar_file = filename
        except Exception as e:
            return e

        card_face.save()


def card_import_job(param):
    """Performs API call for cards.

    Calls Scryfall API for retrieval of bulk cards. Parses bulk card Json file.
    Creates Card, Card faces, and legalities objects for each card.

    @param request:

    :todo: Set to process in background
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
            try:
                legal = Legality.objects.get(card_obj__card_id=card_id)
                legal.standard = legal_or_not(obj['legalities']['standard'])
                legal.future = legal_or_not(obj['legalities']['future'])
                legal.historic = legal_or_not(obj['legalities']['historic'])
                legal.gladiator = legal_or_not(obj['legalities']['gladiator'])
                legal.modern = legal_or_not(obj['legalities']['modern'])
                legal.legacy = legal_or_not(obj['legalities']['legacy'])
                legal.pauper = legal_or_not(obj['legalities']['pauper'])
                legal.vintage = legal_or_not(obj['legalities']['vintage'])
                legal.penny = legal_or_not(obj['legalities']['penny'])
                legal.commander = legal_or_not(obj['legalities']['commander'])
                legal.brawl = legal_or_not(obj['legalities']['brawl'])
                legal.duel = legal_or_not(obj['legalities']['duel'])
                legal.old_school = legal_or_not(obj['legalities']['oldschool'])
                legal.premodern = legal_or_not(obj['legalities']['premodern'])
                legal.save()
            except Legality.DoesNotExist:
                ori_id = obj['oracle_id']
                set_name = obj['set_name']
                rarity = obj['rarity']
                layout = obj['layout']
                key_words = build_comma_list(obj['keywords'])

                color_list = build_comma_list(obj['color_identity'])

                set_obj = CardSets.objects.get(name=set_name)
                layout_obj = CardLayout.objects.get(layout=layout)

                new_card = Card.objects.create(
                    card_id=card_id,
                    oracle_id=ori_id,
                    keywords=key_words,
                    set_name=set_name,
                    rarity=rarity,
                    layout=layout_obj,
                    set_obj=set_obj,
                    color=color_list
                )

                new_legal = Legality.objects.create(
                    card_obj=new_card,
                    standard=legal_or_not(obj['legalities']['standard']),
                    future=legal_or_not(obj['legalities']['future']),
                    historic=legal_or_not(obj['legalities']['historic']),
                    gladiator=legal_or_not(obj['legalities']['gladiator']),
                    modern=legal_or_not(obj['legalities']['modern']),
                    legacy=legal_or_not(obj['legalities']['legacy']),
                    pauper=legal_or_not(obj['legalities']['pauper']),
                    vintage=legal_or_not(obj['legalities']['vintage']),
                    penny=legal_or_not(obj['legalities']['penny']),
                    commander=legal_or_not(obj['legalities']['commander']),
                    brawl=legal_or_not(obj['legalities']['brawl']),
                    duel=legal_or_not(obj['legalities']['duel']),
                    old_school=legal_or_not(obj['legalities']['oldschool']),
                    premodern=legal_or_not(obj['legalities']['premodern']),
                )

                if 'card_faces' not in obj:
                    if 'name' in obj:
                        name = obj['name']
                    else:
                        name = ""

                    if 'image_uris' in obj:
                        image_url = obj['image_uris']['png']
                        if 'art_crop' in obj['image_uris']:
                            avatar_img = obj['image_uris']['art_crop']
                        else:
                            avatar_img = ""
                    else:
                        image_url = ""
                        avatar_img = ""

                    if 'mana_cost' in obj:
                        mana_cost = obj['mana_cost']
                    else:
                        mana_cost = ""

                    if 'loyalty' in obj:
                        loyalty = obj['loyalty']
                    else:
                        loyalty = ""

                    if 'power' in obj:
                        power = obj['power']
                    else:
                        power = ""

                    if 'toughness' in obj:
                        toughness = obj['toughness']
                    else:
                        toughness = ""

                    if 'oracle_text' in obj:
                        text = obj['oracle_text']
                    else:
                        text = ""

                    if 'type_line' in obj:
                        type_line = obj['type_line']
                    else:
                        type_line = ""

                    if 'color_identity' in obj:
                        colors_array = obj['color_identity']
                    else:
                        colors_array = ""

                    if 'flavor_text' in obj:
                        flavor_text = obj['flavor_text']
                    else:
                        flavor_text = ""

                    color_id = build_comma_list(colors_array)


                    card_search = key_words + ' // ' + \
                                  set_name + ' // ' + \
                                  name + ' // ' + \
                                  text + ' // ' + \
                                  type_line + ' // ' + \
                                  flavor_text

                    CardFace.objects.create(
                        name=name,
                        image_url=image_url,
                        mana_cost=mana_cost,
                        loyalty=loyalty,
                        power=power,
                        toughness=toughness,
                        type_line=type_line,
                        color_id=color_id,
                        text=text,
                        flavor_text=flavor_text,
                        avatar_img=avatar_img,
                        first_face=True,
                        legal=new_legal,
                        card_search=card_search,
                    )
                else:
                    first_face = True
                    for face in obj['card_faces']:
                        if 'image_uris' in face:
                            image_url = face['image_uris']['png']
                            if 'art_crop' in face['image_uris']:
                                avatar_img = face['image_uris']['art_crop']
                            else:
                                avatar_img = ""
                        else:
                            if 'image_uris' in obj:
                                image_url = obj['image_uris']['png']
                                if 'art_crop' in obj['image_uris']:
                                    avatar_img = obj['image_uris']['art_crop']
                                else:
                                    avatar_img = ""
                            else:
                                image_url = ""
                                avatar_img = ""

                        if 'name' in face:
                            name = face['name']
                        else:
                            name = ""

                        if 'mana_cost' in face:
                            mana_cost = face['mana_cost']
                        else:
                            mana_cost = ""

                        if 'loyalty' in face:
                            loyalty = face['loyalty']
                        else:
                            loyalty = ""

                        if 'power' in face:
                            power = face['power']
                        else:
                            power = ""

                        if 'toughness' in face:
                            toughness = face['toughness']
                        else:
                            toughness = ""

                        if 'oracle_text' in face:
                            text = face['oracle_text']
                        else:
                            text = ""

                        if 'type_line' in face:
                            type_line = face['type_line']
                        else:
                            type_line = ""

                        if 'color_identity' in face:
                            colors_array = face['color_identity']
                        else:
                            colors_array = ""

                        if 'flavor_text' in face:
                            flavor_text = face['flavor_text']
                        else:
                            flavor_text = ""

                        color_id = build_comma_list(colors_array)

                        card_search = key_words + ' // ' + \
                                      set_name + ' // ' + \
                                      name + ' // ' + \
                                      text + ' // ' + \
                                      type_line + ' // ' + \
                                      flavor_text

                        CardFace.objects.create(
                            name=name,
                            image_url=image_url,
                            mana_cost=mana_cost,
                            loyalty=loyalty,
                            power=power,
                            toughness=toughness,
                            type_line=type_line,
                            color_id=color_id,
                            text=text,
                            flavor_text=flavor_text,
                            avatar_img=avatar_img,
                            first_face=first_face,
                            legal=new_legal,
                            card_search=card_search,
                        )
                        first_face = False
    return HttpResponse("Finished")


def legal_or_not(legal_term):
    if legal_term == "legal":
        return "legalTableField"
    elif legal_term == "banned":
        return "bannedTableField"
    else:
        return "notLegalTableField"


def check_card_obj(obj):
    """Checks for certain issues with cards.

    Loops through values in the database to determine if passed card data should be ignored.

    @param obj: Unprocessed card object in Json format

    @returns:
        * True: Card is good
        * False: Card is bad

    :todo: None
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

