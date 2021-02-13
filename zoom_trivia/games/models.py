from datetime import timedelta

from admin_ordering.models import OrderableModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import now
from model_utils.models import TimeStampedModel

from zoom_trivia.games.helpers import rename
from zoom_trivia.teams.models import TeamAnswer

ROUND_STATE = (
    (0, "Not started"),
    (1, "View questions"),
    (2, "Answer"),
    (3, "Marked"),
)


class StateError(Exception):
    def __init__(self, start_state, end_state):
        errors = []
        for state in (start_state, end_state):
            if not 0 <= state <= len(ROUND_STATE)-1:
                errors.append(f'Invalid state {state}')
        if errors:
            super().__init__(errors[0])
        start = ROUND_STATE[start_state][1]
        end = ROUND_STATE[end_state][1]
        super().__init__(f"Cannot go from state {start_state} ({start}) to {end_state} ({end})")


class Game(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField(null=True, blank=True)
    current_round = models.ForeignKey('Round', related_name='current_game', on_delete=models.SET_NULL, null=True, blank=True)
    round_state = models.IntegerField(choices=ROUND_STATE, default=0)
    link = models.CharField(null=True, blank=True, max_length=255)

    def start_round(self):
        if self.round_state == 1:
            return
        elif not self.round_state == 0:
            raise StateError(self.round_state, 1)
        if not self.current_round:
            self.current_round = self.rounds.get(number=1)

        self.round_state = 1
        self.save()

    def start_marking(self):
        if not self.current_round:
            raise StateError(0, 2)
        self.round_state = 2
        self.save()

    def end_marking(self):
        if not self.current_round:
            raise StateError(0, 3)
        self.round_state = 3
        self.save()

    def end_round(self):
        if self.current_round:
            self.current_round.complete = True
            self.current_round.save()

        try:
            self.current_round = self.rounds.get(number=self.current_round.number + 1)
        except ObjectDoesNotExist:
            self.current_round = None
        finally:
            self.round_state = 0
            self.save()

    def save(self, *args, **kwargs):
        if self.current_round:
            for _round in self.rounds.all():
                if _round.number < self.current_round.number and not _round.complete:
                    _round.complete = True
                    _round.save()
                elif _round.number >= self.current_round.number and _round.complete:
                    _round.complete = False
                    _round.save()
        else:
            self.round_state = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Game {self.pk}: {self.name}"

    def __repr__(self):
        return f"Game {self.pk}: {self.name}"

    class Meta:
        ordering = ("start_time",)


class Round(OrderableModel, TimeStampedModel):
    game = models.ForeignKey(Game, related_name="rounds", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    complete = models.BooleanField(default=False)
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def num_questions(self):
        return self.questions.count()

    @property
    def current(self):
        return self.game.current_round == self

    @property
    def can_see_answers(self):
        return self.complete or (self.current and self.game.round_state == 3)

    @property
    def can_submit_answers(self):
        return self.current and self.game.round_state < 3

    def get_team_answers(self, team_id):
        return TeamAnswer.objects.filter(question__round=self, team_id=team_id).order_by('question__number')

    @property
    def time_left(self):
        if self.end_time:
            if self.end_time > now():
                return (self.end_time - now()).seconds
            return 0
        return None

    def set_countdown(self, seconds=60):
        self.end_time = now() + timedelta(seconds=seconds)
        self.save()

    def __str__(self):
        return f"Round: {self.name}"

    def __repr__(self):
        return f"Round {self.pk}: {self.name}"


class Question(OrderableModel, TimeStampedModel):
    round = models.ForeignKey(Round, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    image = models.ImageField(upload_to=rename, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    link_display = models.CharField(max_length=150, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    out_of = models.IntegerField(default=1)
    answer = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.text}"

    def __repr__(self):
        return f"{self.text}"
