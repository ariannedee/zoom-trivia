from django.contrib import admin

from zoom_trivia.teams.models import Team, TeamAnswer


class AnswerInline(admin.TabularInline):
    model = TeamAnswer
    extra = 0
    show_change_link = True


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
