from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.db.models.aggregates import Sum
from django.urls import reverse
from django.utils.html import format_html

from zoom_trivia.games.models import Game, Question, Round


class RoundInline(OrderableAdmin, admin.TabularInline):
    model = Round
    extra = 0
    show_change_link = True
    ordering_field = "ordering"
    readonly_fields = ["num_questions", "current", "complete"]
    fields = ["ordering", "name", "num_questions", "state", "current", "complete"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "num_rounds", "rounds", "start_time"]
    search_fields = ["id", "name", "complete", "start_time"]
    inlines = (RoundInline,)

    def num_rounds(self, obj):
        return obj.rounds.count()

    def rounds(self, obj):
        url = reverse("admin:games_round_changelist")
        return format_html(f'<a href="{url}?game={obj.id}">See rounds</a>&nbsp;')

    rounds.short_description = "Rounds"
    rounds.allow_tags = True


class QuestionInline(OrderableAdmin, admin.StackedInline):
    model = Question
    extra = 0
    show_change_link = True
    ordering_field = "ordering"


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = [
        "game",
        "ordering",
        "name",
        "num_questions",
        "num_points",
        "complete",
    ]
    inlines = (QuestionInline,)
    readonly_fields = ["ordering"]

    def num_questions(self, obj):
        return obj.questions.count()

    def num_points(self, obj):
        return obj.num_points

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            num_points=Sum("questions__out_of"),
        )
        return queryset
