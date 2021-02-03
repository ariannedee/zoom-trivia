import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from zoom_trivia.games.models import Game, Question
from zoom_trivia.teams.models import TeamAnswer


# ===================
# RENDER VIEWS
# ===================
def game_index(request, game_id=1):
    game = get_object_or_404(Game, pk=game_id)
    context = {"game": game}
    return render(request, "games/index.html", context=context)


def round_start_view(request, game_id, round_num):
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


def marking_view(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    context = {"round": _round}
    return render(request, "games/mark.html", context=context)


# ===================
# CHANGE STATE VIEWS
# ===================
def start_round(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if (not game.current_round and round_num == 1) or (game.current_round and game.current_round.number != round_num):
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/index.html", context={"game": game})
    game.start_round()
    _round = game.current_round
    return redirect("games:round_start", game_id, round_num)


def start_marking(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if not game.current_round or game.current_round.number != round_num:
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/index.html", context={"game": game})
    game.start_marking()
    return redirect("games:mark", game_id, round_num)


def end_marking(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if not game.current_round or game.current_round.number != round_num:
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/index.html", context={"game": game})
    game.end_marking()
    _round = game.current_round
    return redirect("games:answer", game_id, round_num, 1)


def end_round(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if not game.current_round or game.current_round.number != round_num:
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/index.html", context={"game": game})
    game.end_round()
    _round = game.current_round
    return redirect("games:game", game_id)


# ===================
# API VIEWS
# ===================

@require_POST
def score(request):
    body = json.loads(request.body)
    answer_id = body['answer']
    points = body['points']
    answer = get_object_or_404(TeamAnswer, pk=answer_id)
    answer.points = points
    answer.save()
    return HttpResponse('ok')
