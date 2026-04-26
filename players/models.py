"""
Modelos para estadísticas de jugadores por categoría
"""

from django.db import models
from game.enums import SeasonChoices, SeasonTypeChoices
from roster.enums import TeamChoices


class PlayersGeneralTraditional(models.Model):
    season = models.CharField(
        max_length=10,
        choices=SeasonChoices.choices(),
        verbose_name="Temporada",
        db_index=True,
    )
    season_type = models.CharField(
        max_length=20,
        choices=SeasonTypeChoices.choices(),
        verbose_name="Tipo de Temporada",
        db_index=True,
    )
    player_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Jugador",
        db_index=True,
    )
    player_id = models.IntegerField(
        verbose_name="ID del Jugador",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    age = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name="Edad",
        help_text="Age",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Wins",
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Losses",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutes Played",
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points",
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Field Goals Made",
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Field Goals Attempted",
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Percentage",
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="3 Point Field Goals Made",
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="3 Point Field Goals Attempted",
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="3 Point Field Goal Percentage",
    )
    ftm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Free Throws Made",
    )
    fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Free Throws Attempted",
    )
    ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Percentage",
    )
    oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Rebounds",
    )
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rebounds",
    )
    reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebounds",
    )
    ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Assists",
    )
    tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnovers",
    )
    stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Steals",
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks",
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls",
    )
    nba_fantasy_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dd2 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Double Doubles",
    )
    td3 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Triple Doubles",
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players General Traditional"
        verbose_name_plural = "Players General Traditional"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersGeneralAdvanced(models.Model):
    season = models.CharField(
        max_length=10,
        choices=SeasonChoices.choices(),
        verbose_name="Temporada",
        db_index=True,
    )
    season_type = models.CharField(
        max_length=20,
        choices=SeasonTypeChoices.choices(),
        verbose_name="Tipo de Temporada",
        db_index=True,
    )
    player_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Jugador",
        db_index=True,
    )
    player_id = models.IntegerField(
        verbose_name="ID del Jugador",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    age = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name="Edad",
        help_text="Age",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Wins",
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Losses",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutes Played",
    )
    off_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Offensive Rating",
    )
    def_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Defensive Rating",
    )
    net_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Net Rating",
    )
    ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Assist Percentage",
    )
    ast_to = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Assist to Turnover Ratio",
    )
    ast_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Assist Ratio",
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Offensive Rebounding Percentage",
    )
    dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Defensive Rebounding Percentage",
    )
    reb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Rebounding Percentage",
    )
    tm_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Ratio",
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="True Shooting Percentage",
    )
    usg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Usage Percentage",
    )
    pace = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Pace",
    )
    pie = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Player Impact Estimate",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Field Goals Made",
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Field Goals Attempted",
    )
    fgm_pg = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_pg = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Percentage",
    )

    class Meta:
        verbose_name = "Players General Advanced"
        verbose_name_plural = "Players General Advanced"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"
