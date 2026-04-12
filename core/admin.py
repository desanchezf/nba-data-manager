from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Game,
    GameMetadata,
    GamePlayerLine,
    GameTeamLine,
    Player,
    Team,
    WinProbabilitySnapshot,
)


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ("team_id", "name", "abbreviation", "conference", "division")
    search_fields = ("team_id", "name", "abbreviation")
    list_filter = ("conference", "division")


@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    list_display = ("player_id", "name", "team")
    search_fields = ("player_id", "name")
    list_filter = ("team",)
    raw_id_fields = ("team",)


@admin.register(Game)
class GameAdmin(ImportExportModelAdmin):
    list_display = (
        "game_id", "date", "season", "season_type",
        "home_team", "away_team", "home_score", "away_score", "n_result",
    )
    list_filter = ("season", "season_type", "league")
    search_fields = ("game_id",)
    date_hierarchy = "date"
    raw_id_fields = ("home_team", "away_team")


@admin.register(GamePlayerLine)
class GamePlayerLineAdmin(ImportExportModelAdmin):
    list_display = (
        "game", "player", "team", "home_away", "period",
        "pts", "reb", "ast", "min_played",
    )
    list_filter = ("home_away", "period")
    search_fields = ("player__name", "game__game_id")
    raw_id_fields = ("game", "player", "team")


@admin.register(GameTeamLine)
class GameTeamLineAdmin(ImportExportModelAdmin):
    list_display = (
        "game", "team", "home_away", "period",
        "pts", "reb", "ast", "fgm", "fga",
    )
    list_filter = ("home_away", "period")
    search_fields = ("team__name", "game__game_id")
    raw_id_fields = ("game", "team")


@admin.register(WinProbabilitySnapshot)
class WinProbabilitySnapshotAdmin(ImportExportModelAdmin):
    list_display = ("game", "period", "time_remaining", "home_score", "away_score", "win_pct")
    list_filter = ("period",)
    raw_id_fields = ("game",)


@admin.register(GameMetadata)
class GameMetadataAdmin(ImportExportModelAdmin):
    list_display = ("game", "arena", "attendance", "scraped_at")
    raw_id_fields = ("game",)
