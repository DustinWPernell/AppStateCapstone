import operator
from functools import reduce

from django.db.models import Q


class data_helpers():
    @staticmethod
    def mana_filter(is_colorless, has_color, mana):
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
        elif has_color:
            mana_filter = reduce(
                operator.or_, (
                    Q(color_id__contains=item) for item in mana
                )
            )
        else:
            mana_filter = Q(id__gt=-1)

        return mana_filter