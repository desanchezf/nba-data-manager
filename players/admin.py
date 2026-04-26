from django.contrib import admin
from players.models import PlayersGeneralTraditional, PlayersGeneralAdvanced


@admin.register(PlayersGeneralTraditional)
class PlayersGeneralTraditionalAdmin(admin.ModelAdmin):
    list_display = [
        "player_name", "player_id", "team_abb", "season", "season_type",
        "pts", "reb", "ast", "fg_pct",
    ]
    list_filter = ["season", "season_type", "team_abb"]
    search_fields = ["player_name", "team_abb"]


@admin.register(PlayersGeneralAdvanced)
class PlayersGeneralAdvancedAdmin(admin.ModelAdmin):
    list_display = [
        "player_name", "player_id", "team_abb", "season", "season_type",
        "off_rating", "def_rating", "net_rating", "ts_pct", "usg_pct",
    ]
    list_filter = ["season", "season_type", "team_abb"]
    search_fields = ["player_name", "team_abb"]
