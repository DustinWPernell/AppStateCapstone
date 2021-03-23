from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from LifeCounter.models import Game, GameType
from Users.models import UserProfile


@login_required
def index(request):
    """Display landing page for life counter.

    This page is not currently used by the application.

    :param request: Does not utilize any portions of this param.

    :returns: "Hello World From LifeCounter"

    :todo: None
    """
    game_code = ""
    if request.method == "POST":
        game_code = request.POST.get("game_code")
        if 'join_game' in request.POST:
            game = Game.get_by_code(game_code)
            if game == None:
                messages.error(request, 'Game code invalid.')
            else:
                Game.set_game_player_stats(request.user.id, {})

                return redirect(
                    'game/' + game_code
                )
        else:

            #todo finish create
            game_type = request.POST.get("game_type")
            game = Game.create_new(request.user, game_type)
            return redirect(
                'game/' + Game.game_code
            )

    game_types = GameType.objects.all()

    font_family = UserProfile.get_font(request.user)
    should_translate = UserProfile.get_translate(request.user)
    context = {'font_family': font_family, 'should_translate': should_translate, 'game_code': game_code, 'game_types': game_types}
    return render(request, "LifeCounter/game_selector.html", context)

@login_required
def game(request, game_code):
    game = Game.get_by_code(game_code)

    player_data = Game.get_all_game_players_but_indicated(request.user)
    current_player = Game.get_game_player_stats(request.user)

    font_family = UserProfile.get_font(request.user)
    context = {
        'font_family': font_family,
        'game_code': game_code,
        'current_player':current_player,
        'other_players': player_data,
    }
    return render(request, 'LifeCounter/game.html', context)