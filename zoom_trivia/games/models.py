from admin_ordering.models import OrderableModel
from django.db import models
from model_utils.models import TimeStampedModel


class Game(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game: {self.name} ({self.id})"

    def __repr__(self):
        return f"Game {self.pk}: {self.name} ({self.id})"

    class Meta:
        ordering = ("start_time",)


ROUND_STATE = (
    (0, "Not started"),
    (1, "View questions"),
    (2, "Answer"),
    (3, "Marked"),
)


class Round(OrderableModel, TimeStampedModel):
    game = models.ForeignKey(Game, related_name="rounds", on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    state = models.IntegerField(choices=ROUND_STATE, default=0)
    name = models.CharField(max_length=60)
    complete = models.BooleanField(default=False)

    @property
    def num_questions(self):
        return self.questions.count()

    def __str__(self):
        return f"Round: {self.name}"

    def __repr__(self):
        return f"Round {self.pk}: {self.name}"


class Question(OrderableModel, TimeStampedModel):
    round = models.ForeignKey(Round, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    out_of = models.IntegerField(default=1)
    answer = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.text}"

    def __repr__(self):
        return f"{self.text}"
