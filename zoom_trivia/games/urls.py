from django.urls import path

from .views import game_index, question_view, start_round

app_name = "games"
urlpatterns = [
    path("<game_id>/", view=game_index, name="game"),
    path("", view=game_index, name="home"),
    path(
        "<game_id>/round/<round_num>/start_round/", view=start_round, name="start_round"
    ),
    path(
        "<game_id>/round/<round_num>/question/<question_num>",
        view=question_view,
        name="question",
    ),
]
