import logging

logger = logging.getLogger(__name__)


class SessionManager:
    All = "all"
    Avatar = "avatar"
    Card = "card"
    Commander = "commander"
    Deck = "deck"
    DeckImage = 'deck_image'
    Profile = "profile"
    Search = "search"

    profile_session = ['user_search_deck_term', 'user_search_deck_cards', 'user_clear_deck_search',
                       'user_search_card_term', 'user_search_card_cards', 'user_clear_card_search',
                       'user_search_wish_term', 'user_search_wish_cards', 'user_clear_wish_search',
                       'user_view'
                      ]

    card_session = ['collection_card_search_Term', 'collection_card_selected_mana', 'collection_card_card_list', 'collection_card_clear', 'collection_card_card_full']

    deck_session = ['collection_deck_search_Term', 'collection_deck_selected_mana', 'collection_deck_deck_list', 'collection_deck_clear', 'collection_deck_deck_full']

    avatar_session = ['avatar_search_term', 'avatar_card_list' 'avatar_clear_search']

    commander_session = ['user_search_commander_term', 'user_search_commander_cards' 'user_clear_commander_search']

    deck_image_session = ['user_search_commander_term', 'user_search_commander_cards' 'user_clear_commander_search']

    @staticmethod
    def clear_other_session_data(request, data):
        if data == SessionManager.Avatar:
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        elif data == SessionManager.Card:
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        elif data == SessionManager.Commander:
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        elif data == SessionManager.Deck:
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        elif data == SessionManager.DeckImage:
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        elif data == SessionManager.Profile:
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
        else:
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)



    @staticmethod
    def clear_session_data(request, data):
        for key in data:
            try:
                del request.session[key]
                logger.info("Key removed: " + key)
            except KeyError:
                logger.info("Key does not exist: " + key)