import html
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from Collection.models import CardIDList
from Models import DeckType, DeckCard, CardFace, Deck
from Users.models import UserProfile, UserCards
from static.python.session_manager import SessionManager

logger = logging.getLogger(__name__)


class Manage_Cards(View):
    user = User
    card = 'modify_deck_save_cards'
    list = 'modify_deck_list_cards'
    reset_card = 'modify_deck_reset_cards'

    def add_to_deck(self, request, deck_id, card_list, side):
        formatted_list = ''

        DeckCard.objects.empty_deck(deck_id, side, False)

        card_list = list(card_list.split("\n"))
        if card_list[0] == '':
            card_list = []
        for card_item in card_list:
            card_values = card_item.split(" ", 1)
            try:
                if card_values[0] != '':
                    card_quantity = int(card_values[0])
                    card_name = card_values[1].replace('\r', '')
                    card_info = CardIDList.get_card_by_name(card_name)
                    DeckCard.objects.deck_card_create(
                        deck_id,
                        card_info.oracle_id,
                        card_quantity,
                        side,
                        False
                    )
                    formatted_list = formatted_list + str(card_quantity) + " " + str(card_name) + '\n'
            except:
                messages.error(request, "List in incorrect format. " + card_values[1] + " not added to deck.")

        Deck.objects.set_card_list(deck_id, side, formatted_list)
        return formatted_list

    def post(self, request):
        deck_id = request.GET.get('deck_id', -1)
        side = False
        if request.GET.get('side', 'False') == 'True':
            side = True

        if str(self.reset_card) in request.POST:
            request.session[str(self.list)] = Deck.objects.get_card_list(deck_id, side)
        elif str(self.card) in request.POST:
            card_list = request.POST[str(self.list)]
            request.session[str(self.list)] = self.add_to_deck(request, deck_id, card_list, side)
        elif 'return' in request.POST:
            return HttpResponseRedirect(reverse('modify_deck') + '?user_id='+str(request.user.id)+'&deck_id=' + str(deck_id) + '&side=' + str(side))

        return HttpResponseRedirect(reverse('modify_cards') + '?deck_id=' + str(deck_id) + '&side=' + str(side))

    @login_required
    def get(self, request):
        """Displays list for selecting new avatar

        Displays full list of card art with search by name feature.

        @param request:

        :todo: None
        """
        SessionManager.clear_other_session_data(request, SessionManager.Commander)

        deck_id = request.GET.get('deck_id', -1)
        side = False
        title = " deck "
        if request.GET.get('side', 'False') == 'True':
            side = True
            title = " sideboard "

        try:
            modify_deck_list_cards = request.session[str(self.list)]
        except KeyError:
            modify_deck_list_cards = request.session[str(self.list)] = Deck.objects.get_card_list(deck_id, side)

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate,
                   str(self.list): modify_deck_list_cards,
                   'deck_id': deck_id, 'side': side, 'title': title}
        return render(request, 'Users/Profile/ProfileDecks/edit_cards.html', context)


class Manage_Deck(View):
    user = User
    name = 'deck_name_field'
    privacy = 'deck_privacy_field'
    desc = 'deck_description_field'
    type = 'deck_type_field'

    def post(self, request):
        user_id = int(request.GET.get('user_id', request.user.id))
        deck_id = int(request.GET.get('deck_id', -1))
        side = request.GET.get('side', 'False')

        if 'submitDeck' in request.POST:
            deck_name_field = html.escape(request.POST.get(self.name))
            deck_privacy_field = request.POST.get(self.privacy) == "True"
            deck_description_field = (html.escape(request.POST.get(self.desc))).rstrip().replace(',', '&#44;')
            deck_type_field = request.POST.get(self.type)

            if deck_id == "-1":
                try:
                    color_id = '{C}'
                    deck_obj = Deck.objects.deck_create(
                        deck_name_field,
                        int(deck_type_field),
                        deck_privacy_field,
                        deck_description_field,
                        color_id,
                        request.user.username,
                        request.user.username
                    )
                    deck_id = deck_obj.id
                except ObjectDoesNotExist:
                    messages.error(request, "Object does not exist. Deck not created.")
                except ValueError:
                    messages.error(request, "Value Error. Deck not created.")
            else:
                try:
                    deck_type_obj = DeckType.objects.get(id=int(deck_type_field))

                    Deck.objects.deck_update(
                        deck_id=deck_id,
                        deck_name_field=deck_name_field,
                        deck_type_field=deck_type_obj,
                        deck_privacy_field=deck_privacy_field,
                        deck_description_field=deck_description_field
                    )
                except ObjectDoesNotExist :
                    messages.error(request, "Object does not exist. Deck not modified.")
            return HttpResponseRedirect(reverse('modify_deck')+'?user_id='+str(user_id)+'deck_id='+str(deck_id))
        elif 'modify_cards' in request.POST:
            return HttpResponseRedirect(reverse('modify_cards')+'?user_id='+str(user_id)+'&deck_id='+str(deck_id)+'&side='+str(side))
        return HttpResponseRedirect(reverse('user_profile')+'?user_id='+str(user_id))


    @login_required
    def get(self, request):
        """Displays new deck page

        Redirects to new deck page

        @param request:

        :todo: Finish new deck page
        """
        user_id = int(request.GET.get('user_id', request.user.id))
        deck_id = int(request.GET.get('deck_id', -1))

        try:
            deck_obj = Deck.objects.get_deck(request.user.username, deck_id)
            deck_type_obj = Deck.objects.get_deck_type(deck_id)
            deck_private = deck_obj.is_private

            if deck_obj.deck_user != request.user.username:
                deck_obj = deck_obj.create_copy(request.user)
                messages.success(request, "Deck copied to your profile.")

        except ObjectDoesNotExist :
            deck_obj = "new"
            deck_type_obj = '{"type_id": "1"}'
            deck_private = UserProfile.get_deck_private(request.user)

        deck_types = DeckType.objects.get_types()
        deck_type_split = list(deck_types.split("},"))

        deck_commander = DeckCard.objects.deck_card_by_deck_side(deck_id, False, True)
        deck_cards = DeckCard.objects.deck_card_by_deck_side(deck_id, False, False)
        side_cards = DeckCard.objects.deck_card_by_deck_side(deck_id, True, False)

        commanders = list(deck_commander.split("},"))
        if commanders[0] == '':
            commanders = []
        deck_cards_list = list(deck_cards.split("},"))
        if deck_cards_list[0] == '':
            deck_cards_list = []
        side_cards_list = list(side_cards.split("},"))
        if side_cards_list[0] == '':
            side_cards_list = []

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {
            'font_family': font_family, 'should_translate': should_translate,
            'deck_obj': deck_obj, 'deck_types': deck_type_split, 'deck_id': deck_id,
            'is_private': deck_private, 'deck_type_obj': deck_type_obj,
            'commander': commanders, 'commander_len': len(deck_commander),
            'deck_cards': deck_cards_list, 'side_cards': side_cards_list,
            'user_id': user_id
        }
        return render(request, 'Users/Profile/ProfileDecks/modify_deck.html', context)


class Commander_Picker(View):
    user = User
    term = 'user_search_commander_term'
    cards = 'user_search_commander_cards'
    clear = 'user_clear_commander_search'

    def post(self, request):
        deck_id = request.GET.get('deck_id', -1)

        if str(self.clear) in request.POST:
            request.session[str(self.term)] = ""
            request.session[str(self.cards)] = CardFace.objects.card_face_commander_filter("")
            request.session[str(self.clear)] = False
        elif str(self.term) in request.POST:
            user_search_commander_term = request.session[self.term] =request.POST.get(str(self.term))
            request.session[str(self.cards)] = CardFace.objects.card_face_commander_filter(user_search_commander_term)
            request.session[str(self.clear)] = True
        else:
            user_selected_commander = request.POST.get('user_selected_commander')

            DeckCard.objects.deck_card_create(deck_id, user_selected_commander, 1, False, True)

            return HttpResponseRedirect(reverse('modify_deck') + '?deck_id=' + str(deck_id))

        return HttpResponseRedirect(reverse('select_commander')+'?deck_id='+str(deck_id))

    @login_required
    def get(self, request):
        """Displays list for selecting new avatar

        Displays full list of card art with search by name feature.

        @param request:

        :todo: None
        """
        SessionManager.clear_other_session_data(request, SessionManager.Commander)

        deck_id = request.GET.get('deck_id', -1)

        try:
            user_search_commander_term = request.session[str(self.term)]
            commander_list = request.session[str(self.cards)]
            clear_commander = request.session[str(self.clear)]
        except KeyError:
            user_search_commander_term = request.session[str(self.term)] = ""
            commander_list = request.session[str(self.cards)] = CardFace.objects.card_face_commander_filter("")
            clear_commander = request.session[str(self.clear)] = False

        commander_list_split = list(commander_list.split("},"))
        if commander_list_split[0] == '':
            commander_list_split = []
        page = request.GET.get('page', 1)
        paginator = Paginator(commander_list_split, 20)
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards, 'deck_id': deck_id,
                   str(self.term): user_search_commander_term, str(self.clear): clear_commander}
        return render(request, 'Users/Profile/ProfileDecks/select_commander.html', context)


class Image_Picker(View):
    user = User
    term = 'user_search_deck_image_term'
    cards = 'user_search_deck_image_cards'
    clear = 'user_clear_deck_image_search'

    def post(self, request):
        deck_id = request.GET.get('deck_id', -1)

        if self.clear in request.POST:
            request.session[self.term] = ""
            request.session[self.cards] = CardFace.objects.card_face_commander_filter("")
            request.session[self.clear] = False
        if self.term in request.POST:
            user_search_deck_image_term = request.session[self.term] = request.POST.get(self.term)
            request.session[self.cards] = CardFace.objects.card_filter_by_color_term([], user_search_deck_image_term)
            request.session[self.clear] = True
        else:
            user_selected_deck_image = request.POST.get('user_selected_deck_image')

            return HttpResponseRedirect(reverse('modify_deck') + '?deck_id=' + str(deck_id))

        return HttpResponseRedirect(reverse('select_deck_image') + '?deck_id=' + str(deck_id))

    @login_required
    def get(self, request):
        """Displays list for selecting new avatar

        Displays full list of card art with search by name feature.

        @param request:

        :todo: None
        """
        deck_id = request.GET.get('deck_id', -1)

        try:
            user_search_deck_image_term = request.session[self.term]
            deck_image_list = request.session[self.cards]
            clear_deck_image = request.session[self.clear]
        except KeyError:
            user_search_deck_image_term = request.session[self.term] = ""
            deck_image_list = request.session[self.cards] = CardFace.objects.card_face_commander_filter(user_search_deck_image_term)
            clear_deck_image = request.session[self.clear] = False

        deck_image_list_split = list(deck_image_list.split("},"))
        if deck_image_list_split[0] == '':
            deck_image_list_split = []
        page = request.GET.get('page', 1)
        paginator = Paginator(deck_image_list_split, 20)
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)

        font_family = UserProfile.get_font(request.user)
        should_translate = UserProfile.get_translate(request.user)
        context = {'font_family': font_family, 'should_translate': should_translate, 'pages': cards, 'deck_id': deck_id,
                   str(self.term): user_search_deck_image_term,
                   str(self.clear): clear_deck_image}
        return render(request, 'Users/Profile/ProfileDecks/select_deck_image.html', context)