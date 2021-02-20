from django.db import models
from django.db.models.aggregates import Sum
from model_utils.models import TimeStampedModel


class TeamQuerySet(models.QuerySet):
    def filter_for_user(self, user):
        return self.filter(game__allowed_users__user=user)


class TeamManager(models.Manager):
    def get_queryset(self):
        return TeamQuerySet(self.model, using=self._db)

    def filter_for_user(self, user):
        return self.filter(game__allowed_users__user=user)


class Team(TimeStampedModel):
    name = models.CharField(max_length=50)
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, related_name="teams")
    score = models.FloatField(default=0)

    objects = TeamManager()

    def update_score(self):
        self.score = self.answers.aggregate(Sum("points"))["points__sum"] or 0
        self.save()

    @property
    def display_score(self):
        return self.score if self.score % 1 else round(self.score)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({self.display_score})"

    class Meta:
        ordering = ("game", "-score", "name")


class TeamAnswer(TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey("games.Question", on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(max_length=255, blank=True, null=True)
    submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(blank=True, null=True)
    points = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.team}: {self.answer}"

    def __repr__(self):
        return f"{self.question.round.number}.{self.question.number}: {self.answer} ({self.team})"

    class Meta:
        unique_together = ("team", "question")
        ordering = (
            "question_id",
            "submitted_at",
        )
