from django.urls import path

from zoom_trivia.teams.views import (
    create_team,
    leave_team,
)

app_name = "teams"
urlpatterns = [
    path("<int:game_id>/create_team/", view=create_team, name="create_team"),
    path("<int:game_id>/leave_team/", view=leave_team, name="leave_team"),
]
