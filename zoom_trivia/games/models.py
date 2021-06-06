from datetime import timedelta

from admin_ordering.models import OrderableModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils.timezone import localdate, localtime, now
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from zoom_trivia.games.helpers import rename
from zoom_trivia.teams.models import TeamAnswer


class StateError(Exception):
    pass


class RoundState(models.IntegerChoices):
    NOT_STARTED = 0, _("Not started")
    QUESTIONS = 1, _("View questions")
    ANSWER = 2, _("Submitting answers")
    MARKING = 3, _("Marking")
    MARKED = 4, _("Marked")


class GameQuerySet(models.QuerySet):
    def filter_for_user(self, user):
        if user.is_superuser:
            return self
        return self.filter(allowed_users__user=user)


class GameManager(models.Manager):
    def get_queryset(self):
        return GameQuerySet(self.model, using=self._db)

    def filter_for_user(self, user):
        if user.is_superuser:
            return self.all()
        return self.filter(allowed_users__user=user)

    def upcoming_games(self):
        return self.filter(start_time__gte=localdate(), visible=True)


class Game(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField(null=True, blank=True)
    current_round = models.ForeignKey(
        "Round",
        related_name="current_game",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    round_state = models.IntegerField(choices=RoundState.choices, default=RoundState.NOT_STARTED)
    link = models.CharField(null=True, blank=True, max_length=255)
    complete = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)

    objects = GameManager()

    def update_scores(self):
        for team in self.teams.all():
            team.update_score()

    def get_absolute_url(self):
        return reverse("games:game", kwargs={"game_id": self.id})

    def set_current_round(self, round_num):
        round_ = self.rounds.get(number=round_num)
        self.current_round = round_
        self.round_state = RoundState.NOT_STARTED
        self.save(update_complete=True)
        self.rounds.update(end_time=None)

    @property
    def zoom_link(self):
        if self.link:
            return f'<a href="{self.link}" target="_blank">{self.link}</a>'
        return "Not set"

    @property
    def start_time_display(self):
        return localtime(self.start_time).strftime("%A, %b %-d @ %-I:%M %p")

    @property
    def time(self):
        return localtime(self.start_time).time()

    @property
    def date(self):
        return localtime(self.start_time).date()

    @property
    def players_can_see_details(self):
        return (
            self.visible
            and self.start_time
            and self.start_time - localtime() < timedelta(minutes=15)
        )

    @property
    def has_started(self):
        return (
            self.visible
            and self.start_time
            and self.start_time + timedelta(minutes=15) < localtime()
        )

    def user_is_admin(self, user):
        return user.is_superuser or (
            user.is_staff and user.can_view_games and user.allowed_games.filter(id=self.id).exists()
        )

    # CHECK STATE
    @property
    def not_started(self):
        return self.round_state == RoundState.NOT_STARTED

    @property
    def view_questions(self):
        return self.round_state == RoundState.QUESTIONS

    @property
    def answering(self):
        return self.round_state == RoundState.ANSWER

    @property
    def marking(self):
        return self.round_state == RoundState.MARKING

    @property
    def marked(self):
        return self.round_state == RoundState.MARKED

    # STATE TRANSITIONS
    def start_round(self):
        if not self.current_round:
            self.current_round = self.go_to_next_round()

        if not self.round_state == RoundState.NOT_STARTED:
            raise StateError(
                f"Invalid state transition from {self.round_state} to {RoundState.QUESTIONS}"
            )

        if self.current_round.lightning:
            self.current_round.create_team_answers()

        self.round_state = RoundState.QUESTIONS
        self.save()

    def start_marking(self):
        if not self.current_round:
            raise StateError("There is no current round set")
        self.current_round.end_time = None
        self.round_state = RoundState.ANSWER
        self.save()

    def stop_answering(self):
        if not self.current_round:
            raise StateError("There is no current round set")
        elif self.round_state == RoundState.NOT_STARTED:
            raise StateError("This round has not been started")
        self.round_state = RoundState.MARKING
        self.save()

    def end_marking(self):
        if not self.current_round:
            raise StateError("There is no current round set")
        elif self.round_state == RoundState.NOT_STARTED:
            raise StateError("This round has not been started")
        self.current_round.end_time = None
        self.current_round.save()
        self.round_state = RoundState.MARKED
        self.save()

    def end_round(self):
        if not self.current_round:
            raise StateError("There is no current round set")
        elif self.round_state == RoundState.NOT_STARTED:
            raise StateError("This round has not been started")
        elif self.round_state == RoundState.QUESTIONS and not self.current_round.lightning:
            raise StateError("This round has not been marked")

        self.current_round.complete = True
        self.current_round.save()
        self.update_scores()
        self.round_state = RoundState.NOT_STARTED
        self.save()
        self.go_to_next_round()

    def go_to_next_round(self):
        if self.complete:
            raise StateError("This game is already over")
        elif not self.current_round:
            round_num = 1
        else:
            round_num = self.current_round.number + 1
        try:
            self.current_round = self.rounds.get(number=round_num)
        except ObjectDoesNotExist:
            self.complete = True
            self.current_round = None
        finally:
            self.save()
        return self.current_round

    # BASE MODEL OVERRIDES
    def save(self, update_complete=False, *args, **kwargs):
        if update_complete:
            if self.current_round:
                for _round in self.rounds.all():
                    if _round.number < self.current_round.number and not _round.complete:
                        _round.complete = True
                        _round.save()
                    elif _round.number >= self.current_round.number and _round.complete:
                        _round.complete = False
                        _round.save()
            else:
                self.round_state = RoundState.NOT_STARTED
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Game {self.pk}: {self.name}"

    def __repr__(self):
        return f"Game {self.pk}: {self.name}"

    class Meta:
        ordering = ("start_time",)


class RoundQuerySet(models.QuerySet):
    def filter_for_user(self, user):
        return self.filter(game__allowed_users__user=user)


class RoundManager(models.Manager):
    def get_queryset(self):
        return RoundQuerySet(self.model, using=self._db)

    def filter_for_user(self, user):
        return self.filter(game__allowed_users__user=user)


class Round(OrderableModel, TimeStampedModel):
    game = models.ForeignKey(Game, related_name="rounds", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255, null=True, blank=True)
    complete = models.BooleanField(default=False)
    end_time = models.DateTimeField(null=True, blank=True)
    lightning = models.BooleanField(default=False)

    objects = RoundManager()

    @property
    def num_questions(self):
        return self.questions.count()

    @property
    def current(self):
        return self.game.current_round == self

    @property
    def can_see_answers(self):
        return self.complete or (self.current and self.game.round_state == RoundState.MARKED)

    @property
    def can_submit_answers(self):
        return self.current and self.game.round_state < RoundState.MARKING

    def get_team_answers(self, team_id):
        return TeamAnswer.objects.filter(question__round=self, team_id=team_id).order_by(
            "question__number"
        )

    def create_team_answers(self):
        for team in self.game.teams.all():
            for question in self.questions.all():
                TeamAnswer.objects.get_or_create(question=question, team=team)

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
        return f"Game {self.game.id} - round {self.number}: {self.name}"

    def __repr__(self):
        return f"Round {self.pk}: {self.name}"


class QuestionQuerySet(models.QuerySet):
    def filter_for_user(self, user):
        return self.filter(round__game__allowed_users__user=user)


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def filter_for_user(self, user):
        return self.filter(round__game__allowed_users__user=user)


class Question(OrderableModel, TimeStampedModel):
    round = models.ForeignKey(Round, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    image = models.ImageField(upload_to=rename, null=True, blank=True)
    image_in_question = models.BooleanField(default=True, verbose_name="View in question")
    link = models.CharField(max_length=500, null=True, blank=True)
    link_display = models.CharField(max_length=150, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    out_of = models.IntegerField(default=1)
    answer = models.CharField(max_length=300)
    audio = models.FileField(upload_to=rename, null=True, blank=True)

    objects = QuestionManager()

    @property
    def is_last(self):
        return self.number == self.round.questions.count()

    def get_team_answer(self, team_id):
        return TeamAnswer.objects.filter(question=self, team_id=team_id)

    def delete(self, *args, **kwargs):
        super(OrderableModel, self).delete(*args, **kwargs)
        cur_num = 1
        for obj in Question.objects.filter(round=self.round).order_by("number"):
            if obj.number != cur_num:
                obj.number = cur_num
                obj.save()
            cur_num += 1

    def __str__(self):
        return f"{self.text}"

    def __repr__(self):
        return f"{self.text}"

    class Meta:
        ordering = ("round__number", "number")
