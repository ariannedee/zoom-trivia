from django.shortcuts import get_object_or_404, render

from zoom_trivia.games.models import Game, Round


def game_index(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {"game": game}
    return render(request, "games/index.html", context=context)


def start_round(request, round_id):
    _round = get_object_or_404(Round, pk=round_id)
    context = {"round": _round}
    return render(request, "games/round_start.html", context=context)


def round_(request, round_id):
    _round = get_object_or_404(Round, pk=round_id)
    context = {"round": _round}
    return render(request, "games/questions.html", context=context)
