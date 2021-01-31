from django.shortcuts import get_object_or_404, render

from zoom_trivia.games.models import Game, Question


def game_index(request, game_id=1):
    game = get_object_or_404(Game, pk=game_id)
    context = {"game": game}
    return render(request, "games/index.html", context=context)


def start_round(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    context = {"round": _round}
    return render(request, "games/round_start.html", context=context)


def question_view(request, game_id, round_num, question_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    question = get_object_or_404(Question, round=_round, number=question_num)
    context = {"round": _round, "question": question}
    return render(request, "games/questions.html", context=context)
