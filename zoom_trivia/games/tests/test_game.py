import pytest

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
