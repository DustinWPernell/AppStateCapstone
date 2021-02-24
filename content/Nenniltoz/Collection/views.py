import json
import logging
from datetime import datetime
from urllib.request import urlopen

import ijson
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from Collection.models import Card, CardFace, Legality, Symbol, Rule, IgnoreCards
from Management.models import Settings

logger = logging.getLogger(__name__)
APIapi = "https://api.scryfall.com/bulk-data"
APIcard = ""
APIrule = ""
APIsymbol = "https://api.scryfall.com/symbology"


# Create your views here.
def collection_index(request):
    logger.debug("Run: collection_index; Params: " + json.dumps(request.GET.dict()))
    return HttpResponse("Hello World From Collections")


def collection_display(request):
    logger.debug("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
    card_list = CardFace.objects.filter(firstFace=1).order_by('name')
    page = request.GET.get('page', 1)

    paginator = Paginator(card_list, 50)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)

    context = {'pages': cards, }
    return render(request, 'Collection/CollectionDisplay.html', context)


def card_display(request):
    logger.debug("Run: card_display; Params: " + json.dumps(request.GET.dict()))
    card = request.GET.get('cardID')
    card_obj = Card.objects.filter(cardID=card)
    face_obj = CardFace.objects.filter(cardID=card)

    context = {'card': card_obj, 'faces': face_obj}
    return render(request, 'Collection/CardDisplay.html', context)


@staff_member_required
def card_update(request):
    logger.debug("Run: card_update; Params: " + json.dumps(request.GET.dict()))
    settings_obj = Settings.objects.update_or_create(
        id=1,
        defaults={'lastCardImport': datetime.now().date()}
    )

    Card.objects.all().delete()

    global APIcard

    f = urlopen(APIcard)
    objects = list(ijson.items(f, 'item'))
    for obj in objects:
        if check_card_obj(obj):
            card_id = obj['id']
            ori_id = obj['oracle_id']
            set_name=obj['set_name']
            rarity=obj['rarity']
            layout=obj['layout']
            key_words = ""
            keyword_array = obj['keywords']
            for new_keyword in keyword_array:
                key_words = key_words + ", " + new_keyword

            key_words = key_words.strip()
            key_words = key_words.strip(",")

            newCard = Card.objects.create(
                cardID=card_id,
                oracleID=ori_id,
                keywords=key_words,
                setName=set_name,
                rarity=rarity,
                layout=layout,
            )

            newCard.save()

            if 'card_faces' not in obj:
                if 'name' in obj:
                    name = obj['name']
                else:
                    name = ""
                if 'image_uris' in obj:
                    image_url = obj['image_uris']['png']
                else:
                    image_url = ""
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
                color_id = ""
                for newColor in colors_array:
                    color_id = color_id + ", " + newColor

                color_id = color_id.strip()
                color_id = color_id.strip(",")

                CardFace.objects.create(
                    name=name,
                    imageURL=image_url,
                    manaCost=mana_cost,
                    loyalty=loyalty,
                    power=power,
                    toughness=toughness,
                    typeLine=type_line,
                    colorId=color_id,
                    text=text,
                    flavorText=flavor_text,
                    cardID=newCard,
                    firstFace=True,
                )
            else:
                firstFace = True
                for face in obj['card_faces']:
                    if 'name' in face:
                        name = face['name']
                    else:
                        name = ""
                    if 'image_uris' in face:
                        image_url = face['image_uris']['png']
                    else:
                        if 'image_uris' in obj:
                            image_url = obj['image_uris']['png']
                        else:
                            image_url = ""
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
                    color_id = ""
                    for newColor in colors_array:
                        color_id = color_id + ", " + newColor

                    color_id = color_id.strip()
                    color_id = color_id.strip(",")

                    CardFace.objects.create(
                        name=name,
                        imageURL=image_url,
                        manaCost=mana_cost,
                        loyalty=loyalty,
                        power=power,
                        toughness=toughness,
                        typeLine=type_line,
                        colorId=color_id,
                        text=text,
                        flavorText=flavor_text,
                        cardID=newCard,
                        firstFace=firstFace,
                    )
                    firstFace = False

            Legality.objects.create(
                cardID=newCard,
                standard=obj['legalities']['standard'],
                future=obj['legalities']['future'],
                historic=obj['legalities']['historic'],
                gladiator=obj['legalities']['gladiator'],
                modern=obj['legalities']['modern'],
                legacy=obj['legalities']['legacy'],
                pauper=obj['legalities']['pauper'],
                vintage=obj['legalities']['vintage'],
                penny=obj['legalities']['penny'],
                commander=obj['legalities']['commander'],
                brawl=obj['legalities']['brawl'],
                duel=obj['legalities']['duel'],
                oldSchool=obj['legalities']['oldschool'],
                premodern=obj['legalities']['premodern'],
            )
    return HttpResponse("Finished")


def check_card_obj(obj):
    setIgnore = IgnoreCards.objects.filter(type="set")
    for set in setIgnore:
        if obj['set_name'] == set.value:
            return False

    nameIgnore = IgnoreCards.objects.filter(type="name")
    if 'card_faces' not in obj:
        nameVal = obj['name']
    else:
        nameVal = ""

    for name in nameIgnore:
        if name.value in nameVal:
            return False
    return True


@staff_member_required
def symbol_update(request):
    logger.debug("Run: symbol_update; Params: " + json.dumps(request.GET.dict()))
    settings_obj = Settings.objects.update_or_create(
        id=1,
        defaults={'lastSymbolImport': datetime.now().date()},
    )

    Symbol.objects.all().delete()
    global APIsymbol

    f = urlopen(APIsymbol)
    objects = list(ijson.items(f, 'data.item'))
    for obj in objects:
        colors_array = obj['colors']
        color_id = ""
        for new_color in colors_array:
            color_id = color_id + ", " + new_color

        color_id = color_id.strip()
        color_id = color_id.strip(",")

        if 'symbol' in obj:
            symbol = obj['symbol']
        else:
            symbol = ""
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

        Symbol.objects.create(
            symbol=symbol,
            text=english,
            imageURL=svg_uri,
            isMana=represents_mana,
            manaCost=cmc,
            colorID=color_id,
        )
    return HttpResponse("Finished")


@staff_member_required
def rule_update(request):
    logger.debug("Run: rule_update; Params: " + json.dumps(request.GET.dict()))
    settings_obj = Settings.objects.update_or_create(
        id=1,
        defaults={'lastRuleImport': datetime.now().date()},
    )

    Rule.objects.all().delete()
    global APIrule
    global APIcard

    f = urlopen(APIrule)
    objects = list(ijson.items(f, 'item'))
    for obj in objects:
        if 'oracle_id' in obj:
            oracle_id = obj['oracle_id']
        else:
            oracle_id = ""
        if 'published_at' in obj:
            published_at = obj['published_at']
        else:
            published_at = ""
        if 'comment' in obj:
            comment = obj['comment']
        else:
            comment = ""

        Rule.objects.create(
            oracleID=oracle_id,
            pub_date=published_at,
            comment=comment,
        )
    return HttpResponse("Finished")


@staff_member_required
def retrieve_api(request):
    logger.debug("Run: retrieve_api; Params: " + json.dumps(request.GET.dict()))
    global APIapi
    global APIcard
    global APIrule

    f = urlopen(APIapi)
    objects = list(ijson.items(f, 'data'))[0]
    for obj in objects:
        if obj['type'] == "oracle_cards":
            APIcard = obj['download_uri']
        elif obj['type'] == "rulings":
            APIrule = obj['download_uri']
    return HttpResponse("Finished")
