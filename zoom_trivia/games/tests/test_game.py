from datetime import timedelta

import pytest
from django.utils.timezone import now

from ..models import RoundState
from .factories import GameFactory, RoundFactory

pytestmark = pytest.mark.django_db


class TestGame:
    def test_game_states_normal_round(self):
        game = GameFactory()
        round1 = RoundFactory(game=game)
        round2 = RoundFactory(game=game)

        assert game.current_round is None
        assert game.round_state == RoundState.NOT_STARTED

        game.start_round()
        assert game.current_round == round1
        assert game.round_state == RoundState.QUESTIONS

        game.start_marking()
        assert game.round_state == RoundState.ANSWER

        game.stop_answering()
        assert game.round_state == RoundState.MARKING

        game.end_marking()
        assert game.round_state == RoundState.MARKED

        game.end_round()
        assert game.current_round == round2
        assert game.round_state == RoundState.NOT_STARTED

        round1.refresh_from_db()
        assert round1.complete is True

        game.start_round()
        game.start_marking()
        game.stop_answering()
        game.end_marking()
        game.end_round()

        assert game.current_round is None
        assert game.round_state == RoundState.NOT_STARTED
        assert game.complete is True

        round2.refresh_from_db()
        assert round2.complete is True

    def test_game_states_lightning_round(self):
        game = GameFactory()
        round1 = RoundFactory(game=game, lightning=True)
        round2 = RoundFactory(game=game)

        assert game.current_round is None
        assert game.round_state == RoundState.NOT_STARTED

        game.start_round()
        assert game.current_round == round1
        assert game.round_state == RoundState.QUESTIONS

        game.end_round()
        assert game.current_round == round2
        assert game.round_state == RoundState.NOT_STARTED

    def test_game_not_visible_to_players_time(self):
        more_than_15_mins_future = now() + timedelta(minutes=16)
        game = GameFactory(start_time=more_than_15_mins_future, visible=True)
        assert not game.players_can_see_details

    def test_game_not_visible_to_players_visibility(self):
        past = now() - timedelta(hours=8) - timedelta(minutes=1)
        game = GameFactory(start_time=past, visible=False)
        assert not game.players_can_see_details

    def test_game_visible_to_players(self):
        less_than_15_mins_future = now() - timedelta(hours=8) + timedelta(minutes=14)
        game = GameFactory(start_time=less_than_15_mins_future, visible=True)
        assert game.players_can_see_details

    def test_past_game_visible_to_players(self):
        past = now() - timedelta(hours=8) - timedelta(minutes=1)
        game = GameFactory(start_time=past, visible=True)
        assert game.players_can_see_details

    def test_set_current_round(self):
        game = GameFactory()
        round1 = RoundFactory(game=game, complete=True)
        round2 = RoundFactory(game=game, complete=True)
        round3 = RoundFactory(game=game, complete=True)

        game.current_round = round3
        game.round_state = RoundState.MARKING
        game.save()

        game.set_current_round(2)
        assert game.current_round == round2
        assert game.round_state == RoundState.NOT_STARTED

        round1.refresh_from_db()
        round2.refresh_from_db()
        round3.refresh_from_db()
        assert round1.complete is True
        assert round2.complete is False
        assert round3.complete is False
