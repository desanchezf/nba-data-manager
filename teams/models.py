"""
Modelos para estadísticas de equipos por categoría
"""

from django.db import models
from game.enums import SeasonChoices, SeasonTypeChoices


# Teams - General
class TeamsGeneralTraditional(models.Model):
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
    team_abb = models.CharField(
        max_length=50,
        verbose_name="Equipo",
        db_index=True,
        null=True,
        blank=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0, null=True, blank=True, help_text="Partidos Jugados"
    )
    win = models.IntegerField(default=0, null=True, blank=True, help_text="Victorias")
    lose = models.IntegerField(default=0, null=True, blank=True, help_text="Derrotas")
    w_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje de Victorias"
    )
    min = models.IntegerField(
        default=0, null=True, blank=True, help_text="Minutos Jugados"
    )
    pts = models.IntegerField(default=0, null=True, blank=True, help_text="Puntos")
    fgm = models.IntegerField(
        default=0, null=True, blank=True, help_text="Tiros de Campo Anotados"
    )
    fga = models.IntegerField(
        default=0, null=True, blank=True, help_text="Tiros de Campo Intentados"
    )
    fg_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje de Tiros de Campo"
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo de Tres Puntos Anotados",
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo de Tres Puntos Intentados",
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo de Tres Puntos",
    )
    ftm = models.IntegerField(
        default=0, null=True, blank=True, help_text="Tiros Libres Anotados"
    )
    fta = models.IntegerField(
        default=0, null=True, blank=True, help_text="Tiros Libres Intentados"
    )
    ft_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje de Tiros Libres"
    )
    oreb = models.IntegerField(
        default=0, null=True, blank=True, help_text="Rebotes Ofensivos"
    )
    dreb = models.IntegerField(
        default=0, null=True, blank=True, help_text="Rebotes Defensivos"
    )
    reb = models.IntegerField(default=0, null=True, blank=True, help_text="Rebotes")
    ast = models.IntegerField(default=0, null=True, blank=True, help_text="Asistencias")
    tov = models.IntegerField(
        default=0, null=True, blank=True, help_text="Pérdidas de Balón"
    )
    stl = models.IntegerField(default=0, null=True, blank=True, help_text="Robos")
    blk = models.IntegerField(default=0, null=True, blank=True, help_text="Tapones")
    blka = models.IntegerField(
        default=0, null=True, blank=True, help_text="Tapones Recibidos"
    )
    pf = models.IntegerField(
        default=0, null=True, blank=True, help_text="Faltas Personales"
    )
    pfd = models.IntegerField(
        default=0, null=True, blank=True, help_text="Faltas Personales Provocadas"
    )
    plus_minus = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Más/Menos"
    )

    class Meta:
        verbose_name = "Teams General Traditional"
        verbose_name_plural = "Teams General Traditional"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsGeneralAdvanced(models.Model):
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
    team_abb = models.CharField(
        max_length=50,
        verbose_name="Equipo",
        db_index=True,
        null=True,
        blank=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0, null=True, blank=True, help_text="Partidos Jugados"
    )
    win = models.IntegerField(default=0, null=True, blank=True, help_text="Victorias")
    lose = models.IntegerField(default=0, null=True, blank=True, help_text="Derrotas")
    min = models.IntegerField(
        default=0, null=True, blank=True, help_text="Minutos Jugados"
    )
    off_rating = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Clasificación Ofensiva"
    )
    def_rating = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Clasificación Defensiva"
    )
    net_rating = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Clasificación Neta"
    )
    ast_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje de Asistencias"
    )
    ast_to = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Ratio de Asistencias por Pérdida de Balón",
    )
    ast_ratio = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Ratio de Asistencias"
    )
    oreb_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje de Rebotes Ofensivos"
    )
    dreb_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje de Rebotes Defensivos"
    )
    reb_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje de Rebotes"
    )
    tm_tov_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Ratio de Pérdidas de Balón"
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje Efectivo de Tiros de Campo",
    )
    ts_pct = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Porcentaje Real de Tiros"
    )
    pace = models.FloatField(
        default=0.0, null=True, blank=True, help_text="Ritmo de Juego"
    )
    pie = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimación de Impacto del Jugador",
    )
    poss = models.IntegerField(default=0, null=True, blank=True, help_text="Posesiones")

    class Meta:
        verbose_name = "Teams General Advanced"
        verbose_name_plural = "Teams General Advanced"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"
