from django.urls import path

from .views import answer_view, end_round, game_index, mark, question_view, start_round

app_name = "games"
urlpatterns = [
    path("<game_id>/", view=game_index, name="game"),
    path("", view=game_index, name="home"),
    path("<game_id>/round/<round_num>/mark", view=mark, name="mark"),
    path("<game_id>/round/<round_num>/end_round", view=end_round, name="end_round"),
    path(
        "<game_id>/round/<round_num>/start_round/", view=start_round, name="start_round"
    ),
    path(
        "<game_id>/round/<round_num>/question/<question_num>",
        view=question_view,
        name="question",
    ),
    path(
        "<game_id>/round/<round_num>/answer/<question_num>",
        view=answer_view,
        name="answer",
    ),
]
