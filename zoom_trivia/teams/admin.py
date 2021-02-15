from django.contrib import admin

from zoom_trivia.teams.models import Team, TeamAnswer


class AnswerInline(admin.TabularInline):
    model = TeamAnswer
    extra = 0
    show_change_link = True


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser and request.user.can_view_games:
            queryset = queryset.filter_for_user(request.user)
        return queryset
