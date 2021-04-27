import logging

logger = logging.getLogger(__name__)


class SessionManager:
    All = "all"
    Avatar = "avatar"
    BulkCard = "bulk_card"
    Card = "card"
    Commander = "commander"
    Deck = "deck"
    DeckImage = 'deck_image'
    EditCard = 'edit_card'
    Profile = "profile"
    Search = "search"
    UserCard = "user_card"

    edit_card_session = ['modify_deck_save_cards']

    profile_session = ['user_search_deck_term', 'user_search_deck_cards', 'user_clear_deck_search', 'user_search_card_term', 'user_search_card_cards', 'user_clear_card_search', 'user_search_wish_term', 'user_search_wish_cards', 'user_clear_wish_search', 'user_view']

    card_session = ['collection_card_search_Term', 'collection_card_selected_mana', 'collection_card_card_list', 'collection_card_clear', 'collection_card_card_full']

    deck_session = ['collection_deck_search_Term', 'collection_deck_selected_mana', 'collection_deck_deck_list', 'collection_deck_clear', 'collection_deck_deck_full']

    avatar_session = ['avatar_search_term', 'avatar_card_list' 'avatar_clear_search']

    commander_session = ['user_search_commander_term', 'user_search_commander_cards' 'user_clear_commander_search']

    deck_image_session = ['user_search_deck_image_term', 'user_search_deck_image_cards' 'user_clear_deck_image_search']

    user_card_session = ['user_card_list_search_Term', 'user_card_list_selected_mana', 'user_card_list_card_list', 'user_card_list_clear']

    bulk_card_session = ['user_card_list']

    @staticmethod
    def clear_other_session_data(request, data):
        if data == SessionManager.Avatar:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        elif data == SessionManager.Card:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        elif data == SessionManager.Commander:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        elif data == SessionManager.Deck:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        elif data == SessionManager.DeckImage:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        elif data == SessionManager.EditCard:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        elif data == SessionManager.Profile:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        elif data == SessionManager.UserCard:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
        elif data == SessionManager.BulkCard:
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)
        else:
            SessionManager.clear_session_data(request, SessionManager.bulk_card_session)
            SessionManager.clear_session_data(request, SessionManager.avatar_session)
            SessionManager.clear_session_data(request, SessionManager.card_session)
            SessionManager.clear_session_data(request, SessionManager.commander_session)
            SessionManager.clear_session_data(request, SessionManager.deck_session)
            SessionManager.clear_session_data(request, SessionManager.deck_image_session)
            SessionManager.clear_session_data(request, SessionManager.edit_card_session)
            SessionManager.clear_session_data(request, SessionManager.profile_session)
            SessionManager.clear_session_data(request, SessionManager.user_card_session)



    @staticmethod
    def clear_session_data(request, data):
        for key in data:
            try:
                del request.session[key]
                logger.info("Key removed: " + key)
            except KeyError:
                logger.info("Key does not exist: " + key)