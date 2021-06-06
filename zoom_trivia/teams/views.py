from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from zoom_trivia.games.models import Game
from zoom_trivia.teams.models import Team


@require_POST
def create_team(request, game_id):
    team_name = request.POST["team_name"]
    team = Team(name=team_name, game_id=game_id)
    team.save()
    request.session["team_id"] = team.pk
    return redirect("games:game", game_id)


def leave_team(request, game_id):
    del request.session["team_id"]
    return redirect("games:game", game_id)


def join_team(request, game_id, team_id):
    request.session["team_id"] = team_id
    return redirect("games:game", game_id)


def delete_team(request, game_id, team_id):
    game = get_object_or_404(Game, id=game_id)
    if game.user_is_admin(request.user):
        team = get_object_or_404(Team, game=game_id, id=team_id)
        team.delete()
    else:
        messages.add_message(request, messages.ERROR, "You don't have permission to delete teams")
    return redirect("games:game", game_id)
