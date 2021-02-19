import admin_thumbnails
from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.db import models
from django.db.models.aggregates import Sum
from django.forms import Textarea
from django.urls import reverse
from django.utils.html import format_html

from zoom_trivia.games.models import Game, Question, Round
from zoom_trivia.teams.models import TeamAnswer
from zoom_trivia.users.models import GamePermissions


class WidgetStyleMixin:
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 3,
                   'cols': 40,
                   'style': 'height: 3em;'}
        )},
    }


class RoundInline(OrderableAdmin, admin.TabularInline):
    model = Round
    extra = 0
    show_change_link = True
    readonly_fields = ["num_questions", "current", "complete"]
    fields = ["number", "name", "lightning", "num_questions", "current", "complete"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "num_rounds", "rounds", "start_time"]
    search_fields = ["id", "name", "complete", "start_time"]
    inlines = (RoundInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser and request.user.can_view_games:
            queryset = queryset.filter_for_user(request.user)
        return queryset

    def num_rounds(self, obj):
        return obj.rounds.count()

    def rounds(self, obj):
        url = reverse("admin:games_round_changelist")
        return format_html(f'<a href="{url}?game={obj.id}">See rounds</a>&nbsp;')

    rounds.short_description = "Rounds"
    rounds.allow_tags = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            GamePermissions.objects.create(game=obj, user=request.user, role=GamePermissions.UserRole.CREATOR)


@admin_thumbnails.thumbnail('image')
class QuestionInline(WidgetStyleMixin, OrderableAdmin, admin.TabularInline):
    model = Question
    extra = 0
    show_change_link = True
    exclude = ('link', 'link_display')


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = [
        "game",
        "number",
        "name",
        "lightning",
        "num_questions",
        "num_points",
        "complete",
    ]
    inlines = (QuestionInline,)

    def num_questions(self, obj):
        return obj.questions.count()

    def num_points(self, obj):
        return obj.num_points

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            num_points=Sum("questions__out_of"),
        )
        if not request.user.is_superuser and request.user.can_view_games:
            queryset = queryset.filter_for_user(request.user)
        return queryset


class AnswerInline(admin.TabularInline):
    model = TeamAnswer
    extra = 0
    show_change_link = True


@admin_thumbnails.thumbnail('image')
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    list_display = ["text", "round", "number"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser and request.user.can_view_games:
            queryset = queryset.filter_for_user(request.user)
        return queryset
