from django.contrib import admin

# Register your models here.

from data.models import (
    AdvancedBoxScore,
    BoxOuts,
    BoxScore,
    CatchShoot,
    Clutch,
    DefenseDashboard,
    DefensiveImpact,
    DefensiveRebounding,
    Drives,
    ElbowTouch,
    Hustle,
    OffensiveRebounding,
    OpponentShooting,
    PaintTouch,
    Passing,
    PlayType,
    PostUps,
    PullUpShooting,
    Rebounding,
    Shooting,
    ShootingEfficiency,
    ShotDashboard,
    SpeedDistance,
    Touches,
    GameBoxscoreTraditional,
    GamePlayByPlay,
    GameSummary,
    TeamBoxscoreTraditional,
)


@admin.register(AdvancedBoxScore)
class AdvancedBoxScoreAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "match_up",
        "game_date",
        "season",
        "season_type",
        "pts",
    )
    search_fields = ("team", "match_up", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "win_lose",
        "pts",
        "fg_percent",
        "threep_percent",
        "ft_percent",
        "reb",
        "ast",
        "stl",
        "blk",
        "tov",
        "pf",
        "plus_minus",
    )


@admin.register(BoxOuts)
class BoxOutsAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type", "box_outs")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "box_outs",
        "off_box_outs",
        "def_box_outs",
    )


@admin.register(BoxScore)
class BoxScoreAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "match_up",
        "game_date",
        "season",
        "season_type",
        "pts",
    )
    search_fields = ("team", "match_up", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "win_lose",
        "pts",
        "fg_percent",
        "threep_percent",
        "ft_percent",
        "reb",
        "ast",
        "stl",
        "blk",
        "tov",
        "pf",
        "plus_minus",
    )


@admin.register(CatchShoot)
class CatchShootAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "pts",
        "fg_percent",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "pts",
        "fgm",
        "fga",
        "fg_percent",
        "threep_percent",
        "efg_percent",
    )


@admin.register(Clutch)
class ClutchAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "pts",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "pts",
        "fg_percent",
        "threep_percent",
        "ft_percent",
        "reb",
        "ast",
        "stl",
        "blk",
        "tov",
        "pf",
        "plus_minus",
    )


@admin.register(DefenseDashboard)
class DefenseDashboardAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
    )


@admin.register(DefensiveImpact)
class DefensiveImpactAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type", "stl", "blk")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "stl",
        "blk",
    )


@admin.register(DefensiveRebounding)
class DefensiveReboundingAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type", "dreb")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "dreb",
    )


@admin.register(Drives)
class DrivesAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "drives",
        "pts",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "drives",
        "pts",
    )


@admin.register(ElbowTouch)
class ElbowTouchAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "elbow_touches",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "elbow_touches",
    )


@admin.register(Hustle)
class HustleAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "screen_assists",
        "deflections",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "screen_assists",
        "deflections",
    )


@admin.register(OffensiveRebounding)
class OffensiveReboundingAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type", "oreb")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "oreb",
    )


@admin.register(OpponentShooting)
class OpponentShootingAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
    )


@admin.register(PaintTouch)
class PaintTouchAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "paint_touches",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "paint_touches",
    )


@admin.register(Passing)
class PassingAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "ast",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "ast",
    )


@admin.register(PlayType)
class PlayTypeAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "play_type",
        "game_date",
        "season",
        "season_type",
        "pts",
    )
    search_fields = ("team", "season", "season_type", "play_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "play_type",
        "game_date",
        "pts",
        "fg_percent",
        "efg_percent",
    )


@admin.register(PostUps)
class PostUpsAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "post_ups",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "post_ups",
    )


@admin.register(PullUpShooting)
class PullUpShootingAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "pts",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "pts",
        "fg_percent",
        "efg_percent",
    )


@admin.register(Rebounding)
class ReboundingAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type", "reb")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "reb",
        "contested_reb",
        "reb_chances",
    )


@admin.register(Shooting)
class ShootingAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "less_than_5ft_fg_percent",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "less_than_5ft_fg_percent",
        "five_to_9ft_fg_percent",
        "ten_to_14ft_fg_percent",
    )


@admin.register(ShootingEfficiency)
class ShootingEfficiencyAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "pts",
        "efg_percent",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "pts",
        "efg_percent",
        "drive_fg_percent",
        "cs_fg_percent",
        "pull_up_fg_percent",
    )


@admin.register(ShotDashboard)
class ShotDashboardAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "game_date",
        "season",
        "season_type",
        "fg_percent",
    )
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "fg_percent",
        "efg_percent",
        "two_fg_percent",
        "threep_percent",
    )


@admin.register(SpeedDistance)
class SpeedDistanceAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
    )


@admin.register(Touches)
class TouchesAdmin(admin.ModelAdmin):
    list_display = ("team", "game_date", "season", "season_type", "touches")
    search_fields = ("team", "season", "season_type", "game_date")
    list_filter = (
        "season",
        "season_type",
        "team",
        "game_date",
        "touches",
        "pts",
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
