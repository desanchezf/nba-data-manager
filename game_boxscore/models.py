"""
Modelos para boxscores de partidos por jugador (traditional y advanced).
Cabeceras: game_boxscore_traditional.csv y game_boxscore_advanced.csv.
"""

from django.db import models
from game.enums import (
    SeasonChoices,
    SeasonTypeChoices,
    GameBoxscorePeriodChoices,
)
from roster.enums import TeamChoices


class GameBoxscoreTraditional(models.Model):
    """Boxscore tradicional por partido y jugador. CSV: GAME_ID, SEASON, ..."""
    game_id = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="ID del Juego",
        help_text="Identificador único del juego",
    )
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
    home_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo Local",
    )
    away_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo Visitante",
    )
    player_id = models.IntegerField(
        db_index=True,
        verbose_name="ID del Jugador",
    )
    player_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Jugador",
    )
    player_name_abb = models.CharField(
        max_length=50,
        verbose_name="Nombre Abreviado",
    )
    player_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo del Jugador",
    )
    player_pos = models.CharField(
        max_length=5,
        verbose_name="Posición",
        help_text="G, F, C, etc.",
    )
    player_dnp = models.BooleanField(
        default=False,
        verbose_name="No Jugó (DNP)",
    )
    period = models.CharField(
        max_length=10,
        choices=GameBoxscorePeriodChoices.choices(),
        verbose_name="Período",
    )
    min = models.CharField(
        max_length=10,
        verbose_name="Minutos",
        help_text="Formato MM:SS",
    )
    # Traditional stats
    fgm = models.IntegerField(default=0, verbose_name="Field Goals Made")
    fga = models.IntegerField(default=0, verbose_name="Field Goals Attempted")
    fg_pct = models.FloatField(
        default=0.0, verbose_name="Field Goal %", null=True, blank=True
    )
    fg3m = models.IntegerField(default=0, verbose_name="3 Pointers Made")
    fg3a = models.IntegerField(default=0, verbose_name="3 Pointers Attempted")
    fg3_pct = models.FloatField(
        default=0.0, verbose_name="3 Point %", null=True, blank=True
    )
    ftm = models.IntegerField(default=0, verbose_name="Free Throws Made")
    fta = models.IntegerField(default=0, verbose_name="Free Throws Attempted")
    ft_pct = models.FloatField(
        default=0.0, verbose_name="Free Throw %", null=True, blank=True
    )
    oreb = models.IntegerField(default=0, verbose_name="Offensive Rebounds")
    dreb = models.IntegerField(default=0, verbose_name="Defensive Rebounds")
    reb = models.IntegerField(default=0, verbose_name="Rebounds")
    ast = models.IntegerField(default=0, verbose_name="Assists")
    stl = models.IntegerField(default=0, verbose_name="Steals")
    blk = models.IntegerField(default=0, verbose_name="Blocks")
    to = models.IntegerField(default=0, verbose_name="Turnovers")
    pf = models.IntegerField(default=0, verbose_name="Personal Fouls")
    pts = models.IntegerField(default=0, verbose_name="Points")
    plus_minus = models.IntegerField(default=0, verbose_name="Plus/Minus")

    class Meta:
        verbose_name = "Game Boxscore Traditional"
        verbose_name_plural = "Game Boxscores Traditional"
        ordering = ["-game_id", "player_team_abb", "player_id"]
        unique_together = [["game_id", "player_id", "period"]]
        indexes = [
            models.Index(fields=["game_id"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["season", "season_type"]),
        ]

    def __str__(self):
        return f"{self.game_id} - {self.player_name} ({self.period})"


class GameBoxscoreAdvanced(models.Model):
    """Boxscore avanzado por partido. CSV: GAME_ID, ..., OFFRTG, DEFRTG, ..."""
    game_id = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="ID del Juego",
    )
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
    home_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo Local",
    )
    away_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo Visitante",
    )
    player_id = models.IntegerField(
        db_index=True,
        verbose_name="ID del Jugador",
    )
    player_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Jugador",
    )
    player_name_abb = models.CharField(
        max_length=50,
        verbose_name="Nombre Abreviado",
    )
    player_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo del Jugador",
    )
    player_pos = models.CharField(
        max_length=5,
        verbose_name="Posición",
    )
    player_dnp = models.BooleanField(
        default=False,
        verbose_name="No Jugó (DNP)",
    )
    period = models.CharField(
        max_length=10,
        choices=GameBoxscorePeriodChoices.choices(),
        verbose_name="Período",
    )
    min = models.CharField(
        max_length=10,
        verbose_name="Minutos",
    )
    # Advanced stats
    off_rtg = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Offensive Rating",
    )
    def_rtg = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Defensive Rating",
    )
    net_rtg = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Net Rating",
    )
    ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Assist %",
    )
    ast_to = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Assist/Turnover Ratio",
    )
    ast_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Assist Ratio",
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Offensive Rebound %",
    )
    dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Defensive Rebound %",
    )
    reb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Rebound %",
    )
    to_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Turnover Ratio",
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Effective FG %",
    )
    ts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="True Shooting %",
    )
    usg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Usage %",
    )
    pace = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Pace",
    )
    pie = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name="Player Impact Estimate",
    )

    class Meta:
        verbose_name = "Game Boxscore Advanced"
        verbose_name_plural = "Game Boxscores Advanced"
        ordering = ["-game_id", "player_team_abb", "player_id"]
        unique_together = [["game_id", "player_id", "period"]]
        indexes = [
            models.Index(fields=["game_id"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["season", "season_type"]),
        ]

    def __str__(self):
        return f"{self.game_id} - {self.player_name} ({self.period})"
