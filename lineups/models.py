"""
Modelos para estadísticas de lineups por categoría
"""

from django.db import models
from data.enums import SeasonChoices, SeasonTypeChoices
from roster.enums import TeamChoices


class LineupsTraditional(models.Model):
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
    lineup = models.CharField(
        max_length=200,
        verbose_name="Lineup",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Partidos Jugados",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutos Jugados",
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos",
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo Anotados",
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo Intentados",
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo",
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
        default=0,
        null=True,
        blank=True,
        help_text="Tiros Libres Anotados",
    )
    fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros Libres Intentados",
    )
    ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros Libres",
    )
    oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebotes Ofensivos",
    )
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebotes Defensivos",
    )
    reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebotes",
    )
    ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Asistencias",
    )
    tov = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pérdidas de Balón",
    )
    stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Robos",
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tapones",
    )
    blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tapones Recibidos",
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Faltas Personales",
    )
    pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Faltas Personales Provocadas",
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Más/Menos",
    )

    class Meta:
        verbose_name = "Lineups Traditional"
        verbose_name_plural = "Lineups Traditional"
        unique_together = [["season", "season_type", "lineup", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["lineup"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.lineup} - {self.season} ({self.season_type})"


class LineupsAdvanced(models.Model):
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
    lineup = models.CharField(
        max_length=200,
        verbose_name="Lineup",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Partidos Jugados",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutos Jugados",
    )
    off_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Clasificación Ofensiva",
    )
    def_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Clasificación Defensiva",
    )
    net_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Clasificación Neta",
    )
    ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Asistencias",
    )
    ast_to = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Ratio de Asistencias por Pérdida de Balón",
    )
    ast_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Ratio de Asistencias",
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Rebotes Ofensivos",
    )
    dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Rebotes Defensivos",
    )
    reb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Rebotes",
    )
    tm_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Ratio de Pérdidas de Balón",
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje Efectivo de Tiros de Campo",
    )
    ts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje Real de Tiros",
    )
    pace = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Ritmo de Juego",
    )
    pie = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimación de Impacto del Jugador",
    )

    class Meta:
        verbose_name = "Lineups Advanced"
        verbose_name_plural = "Lineups Advanced"
        unique_together = [["season", "season_type", "lineup", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["lineup"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.lineup} - {self.season} ({self.season_type})"


class LineupsMisc(models.Model):
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
    lineup = models.CharField(
        max_length=200,
        verbose_name="Lineup",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Partidos Jugados",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutos Jugados",
    )
    pts_off_tov = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos Tras Pérdidas de Balón",
    )
    pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos de Segunda Oportunidad",
    )
    pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos al Contraataque",
    )
    pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos en la Zona Pintada",
    )
    opp_pts_off_tov = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos del Oponente Tras Pérdidas de Balón",
    )
    opp_pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos de Segunda Oportunidad del Oponente",
    )
    opp_pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos al Contraataque del Oponente",
    )
    opp_pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos en la Zona Pintada del Oponente",
    )

    class Meta:
        verbose_name = "Lineups Misc"
        verbose_name_plural = "Lineups Misc"
        unique_together = [["season", "season_type", "lineup", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["lineup"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.lineup} - {self.season} ({self.season_type})"


class LineupsFourFactors(models.Model):
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
    lineup = models.CharField(
        max_length=200,
        verbose_name="Lineup",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Partidos Jugados",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutos Jugados",
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje Efectivo de Tiros de Campo",
    )
    fta_rate = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Tasa de Intentos de Tiros Libres",
    )
    tm_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Ratio de Pérdidas de Balón",
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Rebotes Ofensivos",
    )
    opp_efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje Efectivo de Tiros de Campo del Oponente",
    )
    opp_fta_rate = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Tasa de Intentos de Tiros Libres del Oponente",
    )
    opp_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Ratio de Pérdidas de Balón del Oponente",
    )
    opp_oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Rebotes Ofensivos del Oponente",
    )

    class Meta:
        verbose_name = "Lineups Four Factors"
        verbose_name_plural = "Lineups Four Factors"
        unique_together = [["season", "season_type", "lineup", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["lineup"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.lineup} - {self.season} ({self.season_type})"


class LineupsScoring(models.Model):
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
    lineup = models.CharField(
        max_length=200,
        verbose_name="Lineup",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Partidos Jugados",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutos Jugados",
    )
    pct_fga_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Intentos de Tiros de Campo (2 Puntos)",
    )
    pct_fga_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Intentos de Tiros de Campo (3 Puntos)",
    )
    pct_pts_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Puntos (2 Puntos)",
    )
    pct_pts_2pt_mr = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Puntos (Media Distancia)",
    )
    pct_pts_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Puntos (3 Puntos)",
    )
    pct_pts_fb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Puntos (Puntos de Contraataque)",
    )
    pct_pts_ft = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Puntos (Tiros Libres)",
    )
    pct_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Puntos (Tras Pérdidas de Balón)",
    )
    pct_pts_paint = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Puntos (Puntos en la Pintura)",
    )
    pct_ast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo de 2 Puntos Anotados Asistidos",
    )
    pct_uast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo de 2 Puntos Anotados Sin Asistencia",
    )
    pct_ast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo de 3 Puntos Anotados Asistidos",
    )
    pct_uast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo de 3 Puntos Anotados Sin Asistencia",
    )
    pct_ast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo Anotados Asistidos",
    )
    pct_uast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo Anotados Sin Asistencia",
    )

    class Meta:
        verbose_name = "Lineups Scoring"
        verbose_name_plural = "Lineups Scoring"
        unique_together = [["season", "season_type", "lineup", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["lineup"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.lineup} - {self.season} ({self.season_type})"


class LineupsOpponent(models.Model):
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
    lineup = models.CharField(
        max_length=200,
        verbose_name="Lineup",
        db_index=True,
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Partidos Jugados",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutos Jugados",
    )
    opp_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo Anotados por el Oponente",
    )
    opp_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo Intentados por el Oponente",
    )
    opp_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo del Oponente",
    )
    opp_fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo de 3 Puntos Anotados por el Oponente",
    )
    opp_fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo de 3 Puntos Intentados por el Oponente",
    )
    opp_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros de Campo de 3 Puntos del Oponente",
    )
    opp_ftm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros Libres Anotados por el Oponente",
    )
    opp_fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros Libres Intentados por el Oponente",
    )
    opp_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Porcentaje de Tiros Libres del Oponente",
    )
    opp_oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebotes Ofensivos del Oponente",
    )
    opp_dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebotes Defensivos del Oponente",
    )
    opp_reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebotes del Oponente",
    )
    opp_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Asistencias del Oponente",
    )
    opp_tov = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pérdidas de Balón del Oponente",
    )
    opp_stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Robos del Oponente",
    )
    opp_blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tapones del Oponente",
    )
    opp_blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Tiros de Campo Bloqueados Intentados por el Oponente",
    )
    opp_pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Faltas Personales del Oponente",
    )
    opp_pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Faltas Personales Recibidas por el Oponente",
    )
    opp_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos del Oponente",
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Más/Menos",
    )

    class Meta:
        verbose_name = "Lineups Opponent"
        verbose_name_plural = "Lineups Opponent"
        unique_together = [["season", "season_type", "lineup", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["lineup"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.lineup} - {self.season} ({self.season_type})"
