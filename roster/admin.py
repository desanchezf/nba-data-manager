from django.contrib import admin
from roster.models import Teams, Players


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = (
        "team_name",
        "team_abb",
        "team_conference",
        "team_division",
    )
    search_fields = ("team_name", "team_abb", "team_conference", "team_division")
    list_filter = ("team_conference", "team_division")


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = (
        "player_name",
        "player_abb",
        "team",
        "season",
    )
    search_fields = ("player_name", "player_abb", "team__team_name", "season")
    list_filter = ("season", "team", "team__team_conference")
