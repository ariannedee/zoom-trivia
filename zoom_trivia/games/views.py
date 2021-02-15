import json
from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from zoom_trivia.games.models import Game, Question
from zoom_trivia.teams.models import Team, TeamAnswer


# ===================
# RENDER VIEWS
# ===================
def game_index(request):
    context = {}
    upcoming_games = Game.objects.upcoming_games()
    if request.user.is_staff:
        your_games = Game.objects.filter_for_user(request.user)
        context['your_games'] = your_games
        upcoming_games = upcoming_games.exclude(id__in=your_games)
    context['games'] = upcoming_games
    return render(request, "games/game_list.html", context=context)


def view_game(request, game_id=1):
    game = get_object_or_404(Game, pk=game_id)
    context = {"game": game}
    team_id = request.session.get('team_id')
    if team_id:
        context['team'] = Team.objects.get(id=team_id)
    if request.user.is_anonymous and not team_id:
        return render(request, "games/game_intro.html", context=context)
    return render(request, "games/game_lobby.html", context=context)


def rules(request):
    game = get_object_or_404(Game, pk=1)
    context = {"game": game}
    return render(request, "games/rules.html", context=context)


@staff_member_required(redirect_field_name="games:index")
def round_start_view(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    context = {"round": _round}
    return render(request, "games/view_round.html", context=context)


@staff_member_required(redirect_field_name="games:index")
def question_view(request, game_id, round_num, question_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    question = get_object_or_404(Question, round=_round, number=question_num)
    context = {"round": _round, "question": question}
    return render(request, "games/view_question.html", context=context)


def answer_view(request, game_id, round_num, question_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    if request.user.is_anonymous and not _round.can_see_answers:
        messages.add_message(request, messages.ERROR, 'You cannot see the answers for this round')
        return redirect("games:game", game_id)
    question = get_object_or_404(Question, round=_round, number=question_num)
    context = {"round": _round, "question": question}
    if _round.lightning:
        return render(request, "games/view_lightning_answer.html", context=context)
    return render(request, "games/view_answer.html", context=context)


@staff_member_required
def marking_view(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    context = {"round": _round}
    return render(request, "games/admin_mark_round.html", context=context)


def player_answers(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    if _round != game.current_round:
        messages.add_message(request, messages.ERROR, 'You can only answer the current round')
        return redirect("games:game", game_id)
    if game.round_state == 3:
        messages.add_message(request, messages.ERROR, 'The round has already been marked')
        return redirect("games:game", game_id)
    if _round.lightning:
        messages.add_message(request, messages.ERROR, 'You cannot submit answers for lightning rounds')
        return redirect("games:game", game_id)
    team_id = request.session.get('team_id')
    context = {"round": _round, "team": team_id}
    if team_id:
        context["answers"] = {answer.question.pk: answer.answer for answer in _round.get_team_answers(team_id)}
    else:
        messages.add_message(request, messages.WARNING,
            mark_safe(
                f"""You can't answer questions if you don't have a team set.
                Go to the <a target=\"_blank\" href=\"{game.get_absolute_url()}\">lobby</a> to select a team."""))
    return render(request, "games/player_answer_round.html", context=context)


# ===================
# CHANGE STATE VIEWS
# ===================
@staff_member_required
def start_round(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if (not game.current_round and round_num == 1) or (game.current_round and game.current_round.number != round_num):
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/game_lobby.html", context={"game": game})
    game.start_round()
    _round = game.current_round
    if _round.lightning:
        return redirect("games:start_marking", game_id, round_num)
    return redirect("games:round_start", game_id, round_num)


@staff_member_required
def start_marking(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if not game.current_round or game.current_round.number != round_num:
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/game_lobby.html", context={"game": game})
    game.start_marking()
    return redirect("games:mark", game_id, round_num)


@staff_member_required
def end_marking(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if not game.current_round or game.current_round.number != round_num:
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/game_lobby.html", context={"game": game})
    game.end_marking()
    _round = game.current_round
    return redirect("games:answer", game_id, round_num, 1)


@staff_member_required
def end_round(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    if not game.current_round or game.current_round.number != round_num:
        messages.add_message(request, messages.ERROR, 'That is not the current round')
        return render(request, "games/game_lobby.html", context={"game": game})
    game.end_round()
    _round = game.current_round
    return redirect("games:game", game_id)


# ===================
# API VIEWS
# ===================
def submit_answers(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    team_id = request.session.get('team_id')
    if not _round.can_submit_answers:
        messages.add_message(request, messages.ERROR, "This round has already been marked")
        return redirect("games:answer", game_id, round_num, 1)
    if request.method == 'POST':
        if not team_id or not Team.objects.filter(id=team_id).count():
            messages.add_message(request, messages.WARNING,
                mark_safe(
                    f"""You don't have a team set.
Go to the <a target=\"_blank\" href=\"{game.get_absolute_url()}\">lobby</a> to select a team first."""))
            context = {"round": _round}
            return render(request, "games/player_answer_round.html", context=context)

        for question in _round.questions.all():
            team_answer, created = TeamAnswer.objects.get_or_create(team_id=team_id, question=question)
            answer = request.POST.get(str(question.pk))
            if not answer:
                messages.add_message(request, messages.WARNING, f'No answer submitted for question {question.number}')
            else:
                team_answer.answer = answer
                team_answer.submitted = True
                team_answer.submitted_at = datetime.now()
                if not created:
                    team_answer.points = None
                team_answer.save()
    context = {"round": _round}
    return render(request, "games/post_player_answer.html", context=context)


@require_POST
def score(request):
    body = json.loads(request.body)
    answer_id = body['answer']
    points = body['points']
    answer = get_object_or_404(TeamAnswer, pk=answer_id)
    answer.points = points
    answer.save()
    return HttpResponse('ok')


# ===================
# Dynamic views
# ===================
def mark_table(request, game_id, round_num, question_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    question = get_object_or_404(Question, round=_round, number=question_num)
    context = {"round": _round, "question": question}
    return render(request, "games/partials/mark_answer_table.html", context=context)


def game_table(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {"game": game}
    return render(request, "games/partials/round_table_player.html", context=context)


def team_table(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {"game": game}
    return render(request, "games/partials/team_table.html", context=context)


def round_state(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    return HttpResponse(_round.can_see_answers)


def time_left(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    return HttpResponse(_round.time_left)


def set_timer(request, game_id, round_num):
    game = get_object_or_404(Game, pk=game_id)
    _round = game.rounds.get(number=round_num)
    _round.set_countdown(60)
    return HttpResponse(_round.time_left)
