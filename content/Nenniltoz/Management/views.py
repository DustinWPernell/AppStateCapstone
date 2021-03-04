import json
import logging
from datetime import datetime
from urllib.request import urlopen

import ijson
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Collection.models import Card, CardFace, Legality, IgnoreCards, Symbol, Rule, CardSets, CardIDList
from Management.models import Settings

logger = logging.getLogger(__name__)
api_bulk_data = "https://api.scryfall.com/bulk-data"
api_card = ""
api_rule = ""
api_symbol = "https://api.scryfall.com/symbology"
api_set = "https://api.scryfall.com/sets"


@staff_member_required
def admin_index(request):
    """Display landing page for management.

    This page is not currently used by the application.

    :param request: Does not utilize any portions of this param.

    :todo: None
    """
    logger.debug("Run: admin_index; Params: " + json.dumps(request.GET.dict()))
    return render(request, 'Management/adminLand.html')


@staff_member_required
def api_import(request):
    """Displays API import options.

    Shows the Scryfall import option implemented. As import processes data, updates display progress.
    Warning: Processing takes a long time when importing cards an rules.

    :param request: Does not utilize any portions of this param.

    :todo: None
    """
    logger.debug("Run: api_import; Params: " + json.dumps(request.GET.dict()))
    settings_list = Settings.objects
    context = {'settings_list': settings_list, }
    return render(request, 'Management/APIimport.html', context)


@staff_member_required
def card_update(request):
    """Performs API call for cards.

    Calls Scryfall API for retrieval of bulk cards. Parses bulk card Json file. Creates Card, Card faces, and legalities objects for each card.

    :param request: Does not utilize any portions of this param.

    :todo: Set to process in background
    """
    logger.debug("Run: card_update; Params: " + json.dumps(request.GET.dict()))
    Settings.objects.update_or_create(
        id=1,
        defaults={'lastCardImport': datetime.now().date()}
    )

    Card.objects.all().delete()

    global api_card

    f = urlopen(api_card)
    objects = list(ijson.items(f, 'item'))
    for obj in objects:
        if check_card_obj(obj):
            card_id = obj['id']
            ori_id = obj['oracle_id']
            set_name = obj['set_name']
            rarity = obj['rarity']
            layout = obj['layout']
            key_words = ""
            keyword_array = obj['keywords']
            for new_keyword in keyword_array:
                key_words = key_words + ", " + new_keyword

            key_words = key_words.strip()
            key_words = key_words.strip(",")

            set_order = CardSets.objects.get(name=set_name).order

            new_card = Card.objects.create(
                cardID=card_id,
                oracleID=ori_id,
                keywords=key_words,
                setName=set_name,
                rarity=rarity,
                layout=layout,
                setOrder=set_order,
            )

            new_card.save()

            if 'card_faces' not in obj:
                if 'name' in obj:
                    name = obj['name']
                else:
                    name = ""
                if 'image_uris' in obj:
                    image_url = obj['image_uris']['png']
                    if 'art_crop' in obj['image_uris']:
                        avatarImg = obj['image_uris']['art_crop']
                    else:
                        avatarImg = ""
                else:
                    image_url = ""
                    avatarImg = ""
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
                    cardID=new_card,
                    firstFace=True,
                    avatarImg=avatarImg,
                    setOrder=set_order,
                )
            else:
                first_face = True
                for face in obj['card_faces']:
                    if 'image_uris' in face:
                        image_url = face['image_uris']['png']
                        if 'art_crop' in face['image_uris']:
                            avatarImg = face['image_uris']['art_crop']
                    else:
                        if 'image_uris' in obj:
                            image_url = obj['image_uris']['png']
                            if 'art_crop' in obj['image_uris']:
                                avatarImg = obj['image_uris']['art_crop']
                            else:
                                avatarImg = ""
                        else:
                            image_url = ""
                            avatarImg = ""

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
                        cardID=new_card,
                        firstFace=first_face,
                        avatarImg=avatarImg,
                        setOrder=set_order,
                    )
                    first_face = False

            Legality.objects.create(
                cardID=new_card,
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

    full_card_list_all = CardFace.objects.raw("SELECT * FROM main.Collection_cardface GROUP BY name ORDER BY name")
    full_card_id_list_all = []
    for card_obj in full_card_list_all:
        if card_obj.cardID.cardID not in full_card_id_list_all:
            CardIDList.objects.create(
                cardID=card_obj.cardID.cardID,
                cardName=card_obj.cardID.name
            )

    return HttpResponse("Finished")


def check_card_obj(obj):
    """Checks for certain issues with cards.

    Loops through values in the database to determine if passed card data should be ignored.

    :param obj: Unprocessed card object in Json format

    :returns:
    :returns: * True: Card is good
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


@staff_member_required
def set_update(request):
    """Performs API call for sets.

    Calls Scryfall API for retrieval of sets. Parses sets Json file. Creates sets objects for each set.

    :param request: Does not utilize any portions of this param.

    :todo: Set to process in background
    """
    logger.debug("Run: set_update; Params: " + json.dumps(request.GET.dict()))

    CardSets.objects.all().delete()
    global api_set

    f = urlopen(api_set)
    objects = list(ijson.items(f, 'data.item'))
    cur_order = 0
    for obj in objects:
        if 'id' in obj:
            set_id = obj['id']
        else:
            set_id = ""
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


@staff_member_required
def symbol_update(request):
    """Performs API call for symbols.

    Calls Scryfall API for retrieval of symbols. Parses symbols Json file. Creates symbols objects for each symbol.

    :param request: Does not utilize any portions of this param.

    :todo: Set to process in background
    """
    logger.debug("Run: symbol_update; Params: " + json.dumps(request.GET.dict()))
    Settings.objects.update_or_create(
        id=1,
        defaults={'lastSymbolImport': datetime.now().date()},
    )

    Symbol.objects.all().delete()
    global api_symbol

    f = urlopen(api_symbol)
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
    """Performs API call for rules.

    Calls Scryfall API for retrieval of bulk rules. Parses bulk rule Json file. Creates a Rule object for each rule.

    :param request: Does not utilize any portions of this param.

    :todo: Set to process in background
    """
    logger.debug("Run: rule_update; Params: " + json.dumps(request.GET.dict()))
    Settings.objects.update_or_create(
        id=1,
        defaults={'lastRuleImport': datetime.now().date()},
    )

    Rule.objects.all().delete()
    global api_rule
    global api_card

    f = urlopen(api_rule)
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
    """Performs API call for bulk data urls.

    Calls Scryfall API for retrieval of bulk data urls. Parses bulk data url Json file. Stores URLs for cards and rules.

    :param request: Does not utilize any portions of this param.

    :todo: Set to process in background
    """
    logger.debug("Run: retrieve_api; Params: " + json.dumps(request.GET.dict()))
    global api_bulk_data
    global api_card
    global api_rule

    f = urlopen(api_bulk_data)
    objects = list(ijson.items(f, 'data'))[0]
    for obj in objects:
        if obj['type'] == "default_cards":
            api_card = obj['download_uri']
        elif obj['type'] == "rulings":
            api_rule = obj['download_uri']
    return HttpResponse("Finished")
