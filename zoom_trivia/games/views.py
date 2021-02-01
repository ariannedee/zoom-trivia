import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from zoom_trivia.games.models import Game, Question
from zoom_trivia.teams.models import TeamAnswer


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
    return render(request, "games/question.html", context=context)


def answer_view(request, game_id, round_num, question_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    question = get_object_or_404(Question, round=_round, number=question_num)
    context = {"round": _round, "question": question}
    return render(request, "games/answer.html", context=context)


def mark(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    context = {"round": _round}
    return render(request, "games/mark.html", context=context)


def end_round(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    return redirect("games:answer", game_id, round_num, 1)


@require_POST
def score(request):
    body = json.loads(request.body)
    answer_id = body['answer']
    points = body['points']
    answer = get_object_or_404(TeamAnswer, pk=answer_id)
    answer.points = points
    answer.save()
    return HttpResponse('ok')
