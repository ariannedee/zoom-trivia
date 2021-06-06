from django.urls import path

from zoom_trivia.teams.views import create_team, delete_team, join_team, leave_team

app_name = "teams"
urlpatterns = [
    path("<int:game_id>/create_team/", view=create_team, name="create_team"),
    path("<int:game_id>/leave_team/", view=leave_team, name="leave_team"),
    path("<int:game_id>/join_team/<int:team_id>", view=join_team, name="join_team"),
    path("<int:game_id>/delete_team/<int:team_id>", view=delete_team, name="delete_team"),
]
