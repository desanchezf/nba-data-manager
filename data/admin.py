from django.contrib import admin

# Register your models here.

from data.models import (
    GameBoxscoreTraditional,
    GamePlayByPlay,
    GameSummary,
    TeamBoxscoreTraditional,
)


@admin.register(GameBoxscoreTraditional)
class GameBoxscoreTraditionalAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "player_name",
        "player_team_abb",
        "period",
        "pts",
        "reb",
        "ast",
    )
    search_fields = (
        "game_id",
        "player_name",
        "player_name_abb",
        "player_team_abb",
        "home_team_abb",
        "away_team_abb",
        "season",
    )
    list_filter = (
        "season",
        "season_type",
        "home_team_abb",
        "away_team_abb",
        "player_team_abb",
        "player_pos",
        "period",
        "player_dnp",
    )


@admin.register(GamePlayByPlay)
class GamePlayByPlayAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "team_abb",
        "period",
        "min",
        "player",
        "action",
    )
    search_fields = (
        "game_id",
        "player",
        "action",
        "team_abb",
        "season",
        "score",
    )
    list_filter = (
        "season",
        "season_type",
        "team_abb",
        "period",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(GameSummary)
class GameSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "team_abb",
        "final",
        "q1",
        "q2",
        "q3",
        "q4",
        "lead_changes",
        "times_tied",
    )
    search_fields = (
        "game_id",
        "team_abb",
        "season",
    )
    list_filter = (
        "season",
        "season_type",
        "team_abb",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(TeamBoxscoreTraditional)
class TeamBoxscoreTraditionalAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "team_abb",
        "matchup",
        "home_away",
        "wl",
        "pts",
        "fg_pct",
        "reb",
        "ast",
        "plus_minus",
    )
    search_fields = (
        "game_id",
        "team_abb",
        "matchup",
        "season",
        "gdate",
    )
    list_filter = (
        "season",
        "season_type",
        "team_abb",
        "home_away",
        "wl",
        "gdate",
    )
    readonly_fields = ("created_at", "updated_at")
