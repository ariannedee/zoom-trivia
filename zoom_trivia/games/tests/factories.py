from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory

from zoom_trivia.games.models import Game, Question, Round


class GameFactory(DjangoModelFactory):

    name = Sequence(lambda n: f"Game {n}")

    class Meta:
        model = Game
        django_get_or_create = ["name"]


class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round

    game = SubFactory(GameFactory)
    name = Sequence(lambda n: f"Round {n}")


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    game = SubFactory(RoundFactory)
    text = Faker("sentence")
    answer = Faker("sentence")
