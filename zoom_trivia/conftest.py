import pytest

from zoom_trivia.games.models import Game, Question, Round
from zoom_trivia.games.tests.factories import GameFactory, QuestionFactory, RoundFactory
from zoom_trivia.users.models import User
from zoom_trivia.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def game() -> Game:
    return GameFactory()


@pytest.fixture
def round_() -> Round:
    return RoundFactory()


@pytest.fixture
def question() -> Question:
    return QuestionFactory()
