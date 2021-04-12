import logging

logger = logging.getLogger(__name__)


class SessionManager:
    All = "all"
    Card = "card"
    Deck = "deck"
    Profile = "profile"
    Search = "search"

    profile_session = ['user_search_deck_term', 'user_search_deck_cards', 'user_clear_deck_search',
                       'user_search_card_term', 'user_search_card_cards', 'user_clear_card_search',
                       'user_search_wish_term', 'user_search_wish_cards', 'user_clear_wish_search']

    card_session = ['collection_card_search_Term', 'collection_card_selected_mana', 'collection_card_card_list', 'collection_card_clear', 'collection_card_card_full']

    deck_session = ['collection_deck_search_Term', 'collection_deck_selected_mana', 'collection_deck_deck_list', 'collection_deck_clear', 'collection_deck_deck_full']

    @staticmethod
    def clear_other_session_data(request, data):
        if data == SessionManager.Profile:
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
        elif data == SessionManager.Card:
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        elif data == SessionManager.Deck:
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        else:
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)



    @staticmethod
    def clear_session_data(request, data):
        for key in data:
            try:
                del request.session[key]
                logger.info("Key removed: " + key)
            except KeyError:
                logger.info("Key does not exist: " + key)