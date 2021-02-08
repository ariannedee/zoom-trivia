from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from zoom_trivia.teams.models import Team


@require_POST
def create_team(request, game_id):
    team_name = request.POST['team_name']
    team = Team(name=team_name, game_id=game_id)
    team.save()
    request.session['team_id'] = team.pk
    return redirect("games:game", game_id)


def leave_team(request, game_id):
    del request.session['team_id']
    return redirect("games:game", game_id)
