from django.urls import path

from .views import (
    answer_view,
    end_round,
    game_index,
    marking_view,
    question_view,
    round_start_view,
    score,
    start_marking,
    start_round,
)

app_name = "games"
urlpatterns = [
    path("<int:game_id>/", view=game_index, name="game"),
    path("", view=game_index, name="home"),
    path(
        "<int:game_id>/round/<int:round_num>/", view=round_start_view, name="round_start"
    ),
    path("<int:game_id>/round/<int:round_num>/marking/", view=marking_view, name="mark"),
    path("<int:game_id>/round/<int:round_num>/mark/", view=start_marking, name="start_marking"),
    path("<int:game_id>/round/<int:round_num>/end_round/", view=end_round, name="end_round"),
    path("<int:game_id>/round/<int:round_num>/start_round/", view=start_round, name="start_round"),
    path("<int:game_id>/round/<int:round_num>/question/<int:question_num>/", view=question_view, name="question"),
    path("<int:game_id>/round/<int:round_num>/answer/<int:question_num>/", view=answer_view, name="answer"),
    path('score', view=score, name='score')
]
