import operator
from functools import reduce

from django.db import models
from django.db.models import Q

from Collection.models import QuickResult, CardIDList
from Models.CardLegality import CardLegality


class CardFaceManager(models.Manager):
    def card_filter_by_color_term(self, mana, term, is_colorless, has_color):
        keywords = ["living weapon", "jump-start", "basic landcycling", "commander ninjutsu", "legendary landwalk","nonbasic landwalk", "totem armor", "megamorph", "haunt", "forecast", "graft", "fortify", "frenzy","gravestorm", "hideaway", "level Up", "infect", "protection", "reach", "rampage", "phasing","multikicker", "morph", "provoke", "modular", "offering", "ninjutsu", "replicate", "recover", "poisonous", "prowl","reinforce", "persist", "retrace", "rebound", "miracle", "overload", "outlast", "prowess", "renown", "myriad","shroud", "trample", "vigilance", "shadow", "storm", "soulshift", "splice", "transmute", "ripple", "suspend","vanishing", "transfigure", "wither", "unearth", "undying", "soulbond", "unleash", "ascend", "assist","afterlife", "companion", "fabricate", "embalm", "escape", "fuse", "menace", "ingest", "melee", "improvise","mentor", "partner", "mutate", "scavenge", "tribute", "surge", "skulk", "undaunted", "riot", "spectacle","forestwalk", "islandwalk", "mountainwalk", "double strike", "cumulative upkeep", "first strike", "encore","sunburst", "deathtouch", "defender", "foretell", "amplify", "affinity", "bushido", "convoke", "bloodthirst","absorb", "aura swap", "changeling", "conspire", "cascade", "annihilator", "battle Cry", "cipher", "bestow","dash", "awaken", "crew", "aftermath", "afflict", "equip", "flanking", "echo", "fading", "fear", "eternalize","entwine", "epic", "dredge","delve", "evoke", "exalted", "evolve", "extort", "dethrone", "exploit", "devoid", "emerge","escalate", "flying","haste", "hexproof", "indestructible", "intimidate", "lifelink", "horsemanship", "kicker","madness", "hidden agenda","swampwalk", "desertwalk", "wizardcycling", "slivercycling", "cycling", "landwalk", "plainswalk","champion", "enchant","plainscycling", "islandcycling", "swampcycling", "mountaincycling", "forestcycling", "landcycling","yypecycling","split second", "flash", "flashback", "banding", "augment", "double agenda", "partner with","hexproof from","boast", "devour", "buyback", "ward", "meld", "bolster", "clash", "fateseal", "investigate","manifest", "monstrosity","populate", "proliferate", "scry", "support", "detain", "explore", "fight", "amass", "adapt","assemble", "abandon","activate", "attach", "exert", "cast", "counter", "create", "destroy", "discard", "double","exchange", "exile","play", "regenerate", "reveal", "sacrifice", "set in motion", "shuffle", "tap", "untap", "vote","transform", "surveil","goad", "planeswalk", "mill", "learn"]
        if not has_color and term.lower() in keywords:
            return QuickResult.get_keyword(self, term.lower())
        elif has_color and term == "":
            return QuickResult.get_color(self, mana)
        else:
            if is_colorless:
                list_of_colors = ['{W}', '{W/U}', '{W/B}', '{R/W}', '{G/W}', '{2/W}', '{W/P}', '{HW}',
                                  '{U}', '{U/B}', '{U/R}', '{G/U}', '{2/U}', '{U/P}', '{HU}',
                                  '{B}', '{B/R}', '{B/G}', '{2/B}', '{B/P}', '{HB}',
                                  '{R}', '{R/G}', '{2/R}', '{R/P}', '{HR}',
                                  '{G}', '{2/G}', '{G/P}', '{HG}']
                mana_filter = (
                        reduce(
                            operator.or_, (
                                Q(color_id__contains=item) for item in mana
                            )
                        ) &
                        reduce(
                            operator.and_, (
                                ~Q(color_id__contains=item) for item in list_of_colors
                            )
                        )
                )
            elif has_color :
                mana_filter = reduce(
                    operator.or_, (
                        Q(color_id__contains=item) for item in mana
                    )
                )
            else:
                mana_filter = Q(id__gt=-1)

            filter = mana_filter & Q(card_search__icontains=term)

            return self.run_query(filter)

    def get_face_by_card(self, card_id):
        return CardFace.objects.filter(Q(legal__card_obj__card_id=card_id)).order_by('name')

    def card_face_commander_filter(self, term):
        filter = ( Q(legal__card_obj__card_id__in=CardIDList.objects.values("card_id").all()) &
                    (
                            Q(legal__commander='legalTableField') |
                            Q(legal__brawl='legalTableField') |
                            Q(legal__duel='legalTableField')
                    ) &
                    Q(card_search__icontains=term) &
                    Q(type_line__icontains="legendary") & (
                            Q(type_line__icontains="creature") | (
                                Q(type_line__icontains="planeswalker") &
                                Q(text__icontains="can be your commander")
                            )
                    )
                )

        return self.run_query(filter)

    def card_face_avatar_filter(self, term):
        filter = Q(name__icontains=term)& (
                Q(type_line__icontains="creature") |
                Q(type_line__icontains="planeswalker")
        )

        return self.run_query(filter)

    def get_card_sets(self, oracle_id):
        set_info = []
        face_list = CardFace.objects.select_related().filter(
            Q(legal__card_obj__oracle_id=oracle_id)
        ).order_by('legal__card_obj__set_obj__name')

        card_set_list = []
        for card_set_obj in face_list:

            if card_set_obj.legal.card_obj.set_obj.name not in card_set_list:
                card_set_list.append(card_set_obj.legal.card_obj.set_obj.name)
                if card_set_obj.legal.card_obj.layout.sides == 2:
                    set_info.append(
                        {'set_name': card_set_obj.legal.card_obj.set_obj.name,
                         'set_image': card_set_obj.legal.card_obj.set_obj.icon_svg_uri,
                         'card_image_one': card_set_obj.image_url,
                         'card_image_two': card_set_obj.legal.face_legal.all()[1].image_url})
                else:
                    set_info.append(
                        {'set_name': card_set_obj.legal.card_obj.set_obj.name,
                         'set_image': card_set_obj.legal.card_obj.set_obj.icon_svg_uri,
                         'card_image_one': card_set_obj.image_url,
                         'card_image_two': 'NONE'})

        return set_info

    def card_face_create(self, name, image_url, mana_cost, loyalty, power, toughness, type_line, color_id, text,
                         flavor_text, avatar_img, first_face, legal, card_search):
        return CardFace.objects.create(
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
            legal=legal,
            card_search=card_search,
        )

    def card_face_update(self, card_id, name, image_url, mana_cost, loyalty, power, toughness, type_line, color_id, text,
                         flavor_text, avatar_img, card_search):
        return CardFace.objects.filter(
            Q(legal__card_obj__card_id=card_id) &
            Q(name=name)
        ).update(
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
            card_search=card_search,
        )

    def get_card_face(self, limit):
        if (limit):
            return QuickResult.get_oracles(self, limit)
        else:
            return QuickResult.run_oracles(self, limit)

    def run_query(self, filter):
        return self.build_json(CardFace.objects.select_related().filter(
            filter
        ).order_by('name'))

    def build_json(self, card_list):
        card_json_list = ""
        i = 0
        for card in card_list:
            card_json_list = card_json_list + card.__str__()
            if len(card_list) > 1 and i + 1 < len(card_list):
                card_json_list = card_json_list + '},'
                i += 1
        return card_json_list.__str__()


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
    avatar_img = models.CharField(max_length=200)
    first_face = models.BooleanField()
    legal = models.ForeignKey(CardLegality, on_delete=models.CASCADE, related_name='face_legal')
    card_search = models.CharField(max_length=2000)

    objects = CardFaceManager()

    class Meta:
        app_label = "Management"

    def __str__(self):
        return '{"oracle_id": "' + str(self.legal.card_obj.oracle_id) + '", "card_name": "' + str(self.name).replace('"', '&#34;').replace('\'', '&#39;') + \
               '", "card_url": "' + str(self.image_url) + '", "avatar_img": "' + str(self.avatar_img) + '", "card_id": "' + str(self.legal.card_obj.card_id) + '"}'