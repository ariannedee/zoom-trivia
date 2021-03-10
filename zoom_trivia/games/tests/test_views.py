from random import randint

import pytest
from django.test import Client
from django.urls import reverse
from django.utils.timezone import now

from zoom_trivia.users.tests.factories import UserFactory

from .factories import GameFactory

pytestmark = pytest.mark.django_db


def template_used(response, template_name):
    template_names = [t.name for t in response.templates if t.name is not None]
    if not template_names:
        return False
    return template_name in template_names


class TestRenderViews:
    def setup_method(self):
        self.client = Client()
        self.admin_user = UserFactory(is_superuser=True)

    def test_index_page_anon(self):
        num_games = randint(0, 5)
        GameFactory.create_batch(num_games, visible=True, start_time=now())

        url = reverse("games:home")
        response = self.client.get(url)
        assert response.status_code == 200
        assert template_used(response, "games/game_list.html")
        assert len(response.context["games"]) == num_games
        assert "your_games" not in response.context

    def test_index_page_admin(self):
        num_games = randint(0, 5)
        GameFactory.create_batch(num_games, visible=False)

        self.client.force_login(self.admin_user)

        url = reverse("games:home")
        response = self.client.get(url)

        assert response.status_code == 200
        assert template_used(response, "games/game_list.html")
        assert len(response.context["games"]) == 0
        assert len(response.context["your_games"]) == num_games


class TestDynamicViews:
    def setup_method(self):
        self.client = Client()
        self.admin_user = UserFactory(is_superuser=True)

    def test_player_round_table(self):
        game = GameFactory()
        url = reverse("games:game_table", kwargs={"game_id": game.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert template_used(response, "games/partials/round_table_player.html")
        assert response.context["game"] == game

    def test_player_round_admin(self):
        game = GameFactory()
        self.client.force_login(self.admin_user)
        url = reverse("games:game_table", kwargs={"game_id": game.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert template_used(response, "games/partials/round_table_admin.html")
        assert response.context["game"] == game
