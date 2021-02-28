from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from zoom_trivia.games.models import Game


class User(AbstractUser):
    """Default user for Zoom Trivia."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def save(self, *args, **kwargs):
        """ Allow new users to view admin """
        created = False
        if not self.pk:
            created = True
            self.is_staff = True
        super().save(*args, **kwargs)
        if created:
            from django.contrib.auth.models import Group

            try:
                game_creator_group = Group.objects.get(name="game_creator")
                game_creator_group.user_set.add(self)
            except Group.DoesNotExist:
                pass

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def can_view_games(self):
        return self.has_perm("games.view_game")


class GamePermissions(models.Model):
    class UserRole(models.TextChoices):
        CREATOR = "CR", _("Creator")
        COLLABORATOR = "CO", _("Collaborator")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allowed_games")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="allowed_users")
    role = models.CharField(max_length=2, choices=UserRole.choices, default=UserRole.CREATOR)

    def __str__(self):
        return f"{self.game.name} - {self.user.username}"

    def __repr__(self):
        return f"{self.game.name} - {self.user.username} ({self.get_role_display()})"
