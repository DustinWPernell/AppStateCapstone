from django.db import models

class DeckTypeManager(models.Manager):
    @staticmethod
    def get_types():
        type_list = DeckType.objects.all()
        type_json_list = ""
        i = 0
        for type_obj in type_list:
            type_json_list = type_json_list + type_obj.__str__()
            if len(type_list) > 1 and i + 1 < len(type_list):
                type_json_list = type_json_list + '},'
                i += 1
        return type_json_list.__str__()

    @staticmethod
    def get_deck_type_by_type(type_id):
        return DeckType.objects.get(id=type_id).__str__()

class DeckType(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    min_deck_size = models.IntegerField(default=60)
    max_deck_size = models.IntegerField(default=0)  # 0 for none
    side_board_size = models.IntegerField(default=15)
    card_copy_limit = models.IntegerField(default=4)
    has_commander = models.BooleanField(default=False)

    objects = DeckTypeManager()

    class Meta:
        app_label = "Management"

    def __str__(self):
        return '{"type_id": "' + str(self.id) + '", "type_name": "' + str(self.name) + '", "desc": "' + \
               str(self.desc) + '", "min_deck_size": "' + str(self.min_deck_size) + '", "max_deck_size": "' + \
               str(self.max_deck_size) + '", "side_board_size": "' + str(self.side_board_size) + \
               '", "card_copy_limit": "' + str(self.card_copy_limit) + '", "has_commander": "' + \
               str(self.has_commander) + '"}'