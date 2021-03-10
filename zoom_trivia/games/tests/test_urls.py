import pytest
from django.urls import resolve, reverse

from ..models import Game, Question, Round

pytestmark = pytest.mark.django_db


class TestGameUrls:
    @staticmethod
    def get_kwargs(game):
        return {"game_id": game.id}

    def test_home(self):
        assert reverse("games:home") == "/"
        assert resolve("/").view_name == "games:home"

    def test_game_page(self, game: Game):
        assert reverse("games:game", kwargs=self.get_kwargs(game)) == f"/{game.id}/"
        assert resolve(f"/{game.id}/").view_name == "games:game"

    def test_rules(self, game: Game):
        assert reverse("games:rules") == "/rules/"
        assert resolve("/rules/").view_name == "games:rules"

        assert reverse("games:rules", kwargs=self.get_kwargs(game)) == f"/{game.id}/rules/"
        assert resolve(f"/{game.id}/rules/").view_name == "games:rules"

    def test_game_table(self, game: Game):
        url = reverse("games:game_table", kwargs=self.get_kwargs(game))
        as_string = f"/{game.id}/game_table/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:game_table"

    def test_team_table(self, game: Game):
        url = reverse("games:team_table", kwargs=self.get_kwargs(game))
        as_string = f"/{game.id}/team_table/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:team_table"


class TestRoundUrls:
    @staticmethod
    def get_kwargs(round_):
        return {"game_id": round_.game.id, "round_num": round_.number}

    def test_round(self, round_: Round):
        url = reverse("games:round", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:round"

    def test_mark_round(self, round_: Round):
        url = reverse("games:mark", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/mark/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:mark"

    def test_start_marking(self, round_: Round):
        url = reverse("games:start_marking", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/start_marking/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:start_marking"

    def test_end_marking(self, round_: Round):
        url = reverse("games:end_marking", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/end_marking/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:end_marking"

    def test_start_round(self, round_: Round):
        url = reverse("games:start_round", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/start_round/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:start_round"

    def test_end_round(self, round_: Round):
        url = reverse("games:end_round", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/end_round/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:end_round"

    def test_player_answers(self, round_: Round):
        url = reverse("games:player_answers", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/answer/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:player_answers"

    def test_round_state(self, round_: Round):
        url = reverse("games:round_state", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/state/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:round_state"

    def test_time_left(self, round_: Round):
        url = reverse("games:time_left", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/time_left/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:time_left"

    def test_set_timer(self, round_: Round):
        url = reverse("games:set_timer", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/set_timer/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:set_timer"

    def test_set_current_round(self, round_: Round):
        url = reverse("games:make_current", kwargs=self.get_kwargs(round_))
        as_string = f"/{round_.game.id}/round/{round_.number}/make_current/"

        assert url == as_string
        assert resolve(as_string).view_name == "games:make_current"


class TestQuestionUrls:
    @staticmethod
    def get_kwargs(question):
        return {
            "game_id": question.round.game.id,
            "round_num": question.round.number,
            "question_num": question.round.number,
        }

    def test_question(self, question: Question):
        url = reverse("games:question", kwargs=self.get_kwargs(question))
        as_string = (
            f"/{question.round.game.id}/round/{question.round.number}/question/{question.number}/"
        )

        assert url == as_string
        assert resolve(as_string).view_name == "games:question"

    def test_answer(self, question: Question):
        url = reverse("games:answer", kwargs=self.get_kwargs(question))
        as_string = (
            f"/{question.round.game.id}/round/{question.round.number}/answer/{question.number}/"
        )

        assert url == as_string
        assert resolve(as_string).view_name == "games:answer"

    def test_mark_table(self, question: Question):
        url = reverse("games:mark_table", kwargs=self.get_kwargs(question))
        as_string = f"/{question.round.game.id}/round/{question.round.number}/question/{question.number}/mark_table"

        assert url == as_string
        assert resolve(as_string).view_name == "games:mark_table"
