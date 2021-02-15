from django.urls import path

from .views import (
    answer_view,
    end_marking,
    end_round,
    game_index,
    game_table,
    mark_table,
    marking_view,
    player_answers,
    question_view,
    round_start_view,
    round_state,
    rules,
    score,
    set_timer,
    start_marking,
    start_round,
    submit_answers,
    team_table,
    time_left,
    view_game,
)

app_name = "games"
urlpatterns = [
    path("<int:game_id>/", view=view_game, name="game"),
    path("", view=game_index, name="home"),
    path("rules/", view=rules, name="rules"),
    path("rules/<int:game_id>/", view=rules, name="rules"),
    path(
        "<int:game_id>/round/<int:round_num>/", view=round_start_view, name="round_start"
    ),
    path("<int:game_id>/round/<int:round_num>/marking/", view=marking_view, name="mark"),
    path("<int:game_id>/round/<int:round_num>/mark/", view=start_marking, name="start_marking"),
    path("<int:game_id>/round/<int:round_num>/stop_marking/", view=end_marking, name="end_marking"),
    path("<int:game_id>/round/<int:round_num>/end_round/", view=end_round, name="end_round"),
    path("<int:game_id>/round/<int:round_num>/start_round/", view=start_round, name="start_round"),
    path("<int:game_id>/round/<int:round_num>/question/<int:question_num>/", view=question_view, name="question"),
    path("<int:game_id>/round/<int:round_num>/answer/<int:question_num>/", view=answer_view, name="answer"),
    path("<int:game_id>/round/<int:round_num>/answer/", view=player_answers, name="player_answers"),
    # API
    path("<int:game_id>/round/<int:round_num>/submit/", view=submit_answers, name="submit_answers"),
    path('score', view=score, name='score'),
    # Dynamic views
    path(
        "<int:game_id>/round/<int:round_num>/question/<int:question_num>/mark_table", view=mark_table, name="mark_table"
    ),
    path("<int:game_id>/game_table/", view=game_table, name="game_table"),
    path("<int:game_id>/round/<int:round_num>/state/", view=round_state, name="round_state"),
    path("<int:game_id>/team_table/", view=team_table, name="team_table"),
    path("<int:game_id>/round/<int:round_num>/time_left", view=time_left, name="time_left"),
    path("<int:game_id>/round/<int:round_num>/set_timer", view=set_timer, name="set_timer"),
]
