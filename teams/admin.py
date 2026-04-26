from django.contrib import admin
from teams.models import TeamsGeneralTraditional, TeamsGeneralAdvanced


@admin.register(TeamsGeneralTraditional)
class TeamsGeneralTraditionalAdmin(admin.ModelAdmin):
    list_display = ["team_abb", "team_name", "season", "season_type", "w_pct", "pts", "fg_pct"]
    list_filter = ["season", "season_type"]
    search_fields = ["team_abb", "team_name"]


@admin.register(TeamsGeneralAdvanced)
class TeamsGeneralAdvancedAdmin(admin.ModelAdmin):
    list_display = ["team_abb", "team_name", "season", "season_type", "off_rating", "def_rating", "net_rating", "pace"]
    list_filter = ["season", "season_type"]
    search_fields = ["team_abb", "team_name"]
