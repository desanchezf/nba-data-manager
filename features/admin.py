from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import GameFeatureSet, PlayerFeatureSet


@admin.register(GameFeatureSet)
class GameFeatureSetAdmin(ImportExportModelAdmin):
    list_display = ("game_id", "market", "season", "season_type", "computed_at")
    list_filter = ("market", "season", "season_type")
    search_fields = ("game_id",)
    readonly_fields = ("computed_at",)


@admin.register(PlayerFeatureSet)
class PlayerFeatureSetAdmin(ImportExportModelAdmin):
    list_display = ("player_id", "context", "as_of_date", "season", "computed_at")
    list_filter = ("context", "season")
    search_fields = ("player_id",)
    readonly_fields = ("computed_at",)
