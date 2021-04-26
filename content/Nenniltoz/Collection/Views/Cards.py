import html
import json
import logging
from json import JSONDecodeError

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View

from Collection.models import Symbol, CardIDList, Rule
from Models import Card, CardFace
from Models.UserCard import UserCard
from Users.models import UserCards, UserProfile
from static.python.session_manager import SessionManager

logger = logging.getLogger(__name__)


class Card_Display(View):
    def post(self, request, oracle_id):
        """Updates quantity of card.

        Updates the number of cards owned by user based on POST data

        @param request:
        @param oracle_id: Card ID for current card

        :todo: None
        """
        if 'collection' in request.POST:
            oracle_id = request.POST['oracle_id']
            user_id = request.user.id

            card_quantity = int(request.POST['card_quantity'])
            card_notes = html.escape(request.POST['card_notes'])
            wish_quantity = int(request.POST['wish_quantity'])
            wish_notes = html.escape(request.POST['wish_notes'])

            if card_quantity != 0:
                card_id_info = CardIDList.get_card_by_oracle(oracle_id)
                user_card = UserCard.objects.get_user_card_oracle(user_id, card_id_info.oracle_id, True, False)
                if len(user_card) > 0:
                    UserCard.objects.user_card_update(
                        user_id,
                        card_id_info.oracle_id,
                        card_quantity,
                        False,
                        card_notes
                    )
                else:
                    UserCard.objects.user_card_create(
                        user_id,
                        card_id_info.oracle_id,
                        card_id_info.card_name,
                        card_id_info.color_id,
                        card_quantity,
                        False,
                        card_notes
                    )
            if wish_quantity != 0:
                card_id_info = CardIDList.get_card_by_oracle(oracle_id)
                card_info = CardFace.objects.get_face_by_card(card_id_info.card_id)[0]
                user_card = UserCard.objects.get_user_card_oracle(user_id, card_id_info.oracle_id, True, True)
                if len(user_card) > 0:
                    UserCard.objects.user_card_update(
                        user_id,
                        card_id_info.oracle_id,
                        wish_quantity,
                        True,
                        wish_notes
                    )
                else:
                    UserCard.objects.user_card_create(
                        user_id,
                        card_id_info.oracle_id,
                        card_id_info.card_name,
                        card_info.mana_cost,
                        wish_quantity,
                        True,
                        wish_notes
                    )
        return redirect('../' + oracle_id)

    def get(self, request, oracle_id):
        """Display individual cards.

        Retrieves card information from the database based on what 'card_id' is in request. Then displays the card data.

        @param request:
        @param oracle_id: Oracle ID for current card

        :todo: Touch up data display/layout
        """
        logger.info("Run: card_display; Params: " + json.dumps(request.GET.dict()))
        SessionManager.clear_other_session_data(request, SessionManager.Card)

        try:
            card_obj = CardIDList.get_card_by_oracle(oracle_id)
            card = Card.objects.get_card(card_obj.card_id)
            card_faces = CardFace.objects.get_face_by_card(card_obj.card_id)

            card_set_list = CardFace.objects.get_card_sets(oracle_id)
            card_set_list.sort(key=lambda item: item.get("set_name"))

            rulings_list = Rule.objects.filter(oracle_id=oracle_id).order_by('-pub_date')

            tcg_pricing = CardIDList.get_tcg_price(oracle_id)

            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            if request.user.is_authenticated:
                try:
                    has_card = True
                    user_card = UserCard.objects.get_user_card_oracle(request.user.id, oracle_id, True, False)
                    if user_card == '':
                        has_card = False
                except ObjectDoesNotExist:
                    has_card = False
                    user_card = ''

                try:
                    has_wish = True
                    user_wish = UserCard.objects.get_user_card_oracle(request.user.id, oracle_id, True, True)
                    if user_wish == '':
                        has_wish = False
                except ObjectDoesNotExist:
                    has_wish = False
                    user_wish = ''
            else:
                has_card = False
                user_card = ''
                has_wish = False
                user_wish = ''

            context = {'font_family': font_family, 'should_translate': should_translate, 'card': card,
                       'faces': card_faces, 'set_info': card_set_list,
                       'rulings': rulings_list, 'has_rules': len(rulings_list) > 0,
                       'has_card': has_card, 'user_card': user_card,
                       'has_wish': has_wish, 'user_wish': user_wish,
                       'tcg_pricing': tcg_pricing,
                       'auth': request.user.is_authenticated}

            return render(request, 'Collection/card_display.html', context)

        except CardIDList.DoesNotExist:
            message = "Oracle ID incorrect.\nPlease check ID."
            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            context = {'font_family': font_family, 'should_translate': should_translate, 'message': message}
            return render(request, 'error.html', context)

class Card_Database(View):
    def post(self, request):
        logger.info("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
        init_mana_list = Symbol.get_base_symbols()
        card_id_list_full = CardIDList.get_cards()
        full_card_list_all = []
        for card_list_obj in card_id_list_full:
            full_card_list_all.append(card_list_obj.card_id)

        if 'collection_card_clear_search' in request.POST:
            request.session['collection_card_search_Term'] = ""
            request.session['collection_card_selected_mana'] = []
            request.session['collection_card_card_list'] = CardFace.objects.get_card_face(True)
            request.session['collection_card_clear'] = False
            request.session['collection_card_card_full'] = False
        elif 'collection_card_full_list' in request.POST:
            request.session['collection_card_search_Term'] = "Full List"
            request.session['collection_card_selected_mana'] = []
            request.session['collection_card_card_list'] = CardFace.objects.get_card_face(False)
            request.session['collection_card_clear'] = True
            request.session['collection_card_card_full'] = True
        else:
            text = request.POST.get('collection_card_search_Term')
            if text == "Full List":
                text = request.session['collection_card_search_Term'] = ""
            search_term = text
            selected_mana = []
            has_colorless = False
            has_color = False
            for selected in init_mana_list:
                mana_ele = request.POST.get("mana-" + str(selected.id))
                if mana_ele == '':
                    selected_mana.append(selected.symbol)
                    if selected.symbol == '{W}':
                        alt_mana = Symbol.get_white()
                    elif selected.symbol == '{U}':
                        alt_mana = Symbol.get_blue()
                    elif selected.symbol == '{B}':
                        alt_mana = Symbol.get_black()
                    elif selected.symbol == '{R}':
                        alt_mana = Symbol.get_red()
                    elif selected.symbol == '{G}':
                        alt_mana = Symbol.get_green()
                    elif selected.symbol == '{C}':
                        alt_mana = Symbol.get_colorless()
                    else:
                        alt_mana = []

                    for am in alt_mana:
                        if am.symbol not in selected_mana:
                            selected_mana.append(am.symbol)

            if len(selected_mana) > 0:
                colorless = ['{C}', '', '{X}', '{Y}', '{Z}', '{0}', '{1/2}', '{1}', '{2}', '{3}', '{4}', '{5}',
                             '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}',
                             '{16}', '{17}', '{18}', '{19}', '{20}', '{100}', '{1000000}', '{P}']

                has_colorless = any(item in selected_mana for item in colorless)
                has_color = True


            filtered_card_list = CardFace.objects.card_filter_by_color_term(
                selected_mana, search_term, has_colorless, has_color
            )

            request.session['collection_card_search_Term'] = search_term
            request.session['collection_card_selected_mana'] = selected_mana
            request.session['collection_card_card_list'] = filtered_card_list
            request.session['collection_card_clear'] = True
            request.session['collection_card_card_full'] = False
        return redirect('card_database')

    def get(self, request):
        """Display entire card database.

        Retrieves all cards from database in alphabetical order and displays them based on what 'page' is in request.

        @param request:

        :todo: Loading image for long searches
        """
        logger.info("Run: collection_display; Params: " + json.dumps(request.GET.dict()))
        SessionManager.clear_other_session_data(request, SessionManager.Card)

        init_mana_list = Symbol.get_base_symbols()
        try:
            search_term = request.session['collection_card_search_Term']
            selected_mana = request.session['collection_card_selected_mana']
            card_list = request.session['collection_card_card_list']
            clear_search = request.session['collection_card_clear']
            full_list = request.session['collection_card_card_full']
        except KeyError:
            search_term = request.session['collection_card_search_Term'] = ""
            selected_mana = request.session['collection_card_selected_mana'] = []
            card_list = request.session['collection_card_card_list'] = CardFace.objects.get_card_face(True)
            clear_search = request.session['collection_card_clear'] = False
            full_list = request.session['collection_card_card_full'] = False


        mana_list = []
        for init_mana in init_mana_list:
            if init_mana.symbol in selected_mana:
                mana_list.append(
                    {'symbol': init_mana.symbol, 'checked': True, 'image_url': init_mana.image_url,
                     'id': init_mana.id})
            else:
                mana_list.append(
                    {'symbol': init_mana.symbol, 'checked': False, 'image_url': init_mana.image_url,
                     'id': init_mana.id})

        card_list_split = list(card_list.split("},"))
        if card_list_split[0] == '':
            card_list_split = []
        page = request.GET.get('page', 1)
        paginator = Paginator(card_list_split, 20)
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)


        try:
            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards,
                       'search_Term': search_term, 'mana_list': mana_list, 'clearSearch': clear_search,
                       'full_list': full_list}
            return render(request, 'Collection/collection_display.html', context)
        except JSONDecodeError:
            request.session['collection_card_search_Term'] = ""
            request.session['collection_card_selected_mana'] = []
            request.session['collection_card_card_list'] = CardFace.objects.get_card_face(True)
            request.session['collection_card_clear'] = False
            request.session['collection_card_card_full'] = False

            message = "Invalid search. Please try again."
            font_family = UserProfile.get_font(request.user)
            should_translate = UserProfile.get_translate(request.user)
            context = {'font_family': font_family, 'should_translate': should_translate, 'message': message}
            return render(request, 'error.html', context)