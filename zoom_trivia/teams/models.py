from django.db import models
from model_utils.models import TimeStampedModel


class Team(TimeStampedModel):
    name = models.CharField(max_length=50)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='teams')
    score = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({self.score})"


class TeamAnswer(TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('games.Question', on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=255)
    submitted = models.BooleanField(default=False)
    points = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.team}: {self.answer}"

    def __repr__(self):
        return f"{self.question.round.number}.{self.question.number}: {self.answer} ({self.team})"

    class Meta:
        unique_together = ('team', 'question')

