from django.urls import path

from .views import game_index, round_, start_round

app_name = "games"
urlpatterns = [
    path("<game_id>/", view=game_index, name="game"),
    path("round/<round_id>/start_round/", view=start_round, name="start_round"),
    path("round/<round_id>", view=round_, name="round"),
]
