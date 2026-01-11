"""
Modelos para estadísticas de equipos por categoría
"""

from django.db import models
from data.enums import SeasonChoices, SeasonTypeChoices
from roster.enums import TeamChoices


def get_field_type(field_name):
    """
    Determina el tipo de campo Django basado en el nombre del campo
    """
    field_name_upper = field_name.upper()

    # Campos de texto/identificadores
    if field_name_upper in [
        "SEASON",
        "SEASON_TYPE",
        "TEAM_ABB",
        "MATCHUP",
        "GDATE",
        "WL",
        "G",
    ]:
        return models.CharField(max_length=50)

    # Campos de porcentaje
    if (
        "_PCT" in field_name_upper
        or "_PERCENTILE" in field_name_upper
        or "PCT_" in field_name_upper
        or "PERCENTILE" in field_name_upper
        or "RATE" in field_name_upper
        or "RATING" in field_name_upper
        or "PACE" in field_name_upper
        or "PIE" in field_name_upper
        or "PPP" in field_name_upper
        or "POSS_PCT" in field_name_upper
        or "FREQ" in field_name_upper
        or "PLUSMINUS" in field_name_upper
        or "PLUS_MINUS" in field_name_upper
        or "DIST" in field_name_upper
        or "SPEED" in field_name_upper
        or "AVG" in field_name_upper
        or "PER" in field_name_upper
        or "TO" in field_name_upper
        or "RATIO" in field_name_upper
    ):
        return models.FloatField(default=0.0, null=True, blank=True)

    # Campos numéricos enteros
    return models.IntegerField(default=0, null=True, blank=True)


def create_model_fields(fields_string):
    """
    Crea un diccionario de campos para un modelo basado en la cadena de campos
    """
    fields = {}
    field_names = [f.strip() for f in fields_string.split(",")]

    for field_name in field_names:
        field_type = get_field_type(field_name)

        # Campos especiales con choices
        if field_name == "SEASON":
            fields[field_name.lower()] = models.CharField(
                max_length=10,
                choices=SeasonChoices.choices(),
                verbose_name="Temporada",
                db_index=True,
            )
        elif field_name == "SEASON_TYPE":
            fields[field_name.lower()] = models.CharField(
                max_length=20,
                choices=SeasonTypeChoices.choices(),
                verbose_name="Tipo de Temporada",
                db_index=True,
            )
        elif field_name == "TEAM_ABB":
            fields[field_name.lower()] = models.CharField(
                max_length=10,
                choices=TeamChoices.choices(),
                verbose_name="Equipo",
                db_index=True,
            )
        elif field_name == "MATCHUP":
            fields[field_name.lower()] = models.CharField(
                max_length=50,
                verbose_name="Enfrentamiento",
                null=True,
                blank=True,
            )
        elif field_name == "GDATE":
            fields[field_name.lower()] = models.CharField(
                max_length=20,
                verbose_name="Fecha del Juego",
                null=True,
                blank=True,
            )
        elif field_name == "WL":
            fields[field_name.lower()] = models.CharField(
                max_length=1,
                verbose_name="Resultado",
                null=True,
                blank=True,
            )
        elif field_name == "MIN":
            fields[field_name.lower()] = models.IntegerField(
                default=0,
                verbose_name="Minutos",
                null=True,
                blank=True,
            )
        else:
            # Campo genérico
            field_name_lower = field_name.lower()
            if isinstance(field_type, models.FloatField):
                fields[field_name_lower] = models.FloatField(
                    default=0.0,
                    null=True,
                    blank=True,
                    verbose_name=field_name.replace("_", " ").title(),
                )
            else:
                fields[field_name_lower] = models.IntegerField(
                    default=0,
                    null=True,
                    blank=True,
                    verbose_name=field_name.replace("_", " ").title(),
                )

    return fields


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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
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


class TeamsGeneralFourFactors(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(default=0, null=True, blank=True)
    win = models.IntegerField(default=0, null=True, blank=True)
    lose = models.IntegerField(default=0, null=True, blank=True)
    w_pct = models.FloatField(default=0.0, null=True, blank=True)
    min = models.IntegerField(default=0, null=True, blank=True)
    efg_pct = models.FloatField(default=0.0, null=True, blank=True)
    fta_rate = models.FloatField(default=0.0, null=True, blank=True)
    tm_tov_pct = models.FloatField(default=0.0, null=True, blank=True)
    oreb_pct = models.FloatField(default=0.0, null=True, blank=True)
    opp_efg_pct = models.FloatField(default=0.0, null=True, blank=True)
    opp_fta_rate = models.FloatField(default=0.0, null=True, blank=True)
    opp_tov_pct = models.FloatField(default=0.0, null=True, blank=True)
    opp_oreb_pct = models.FloatField(default=0.0, null=True, blank=True)

    class Meta:
        verbose_name = "Teams General Four Factors"
        verbose_name_plural = "Teams General Four Factors"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsGeneralMisc(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(default=0, null=True, blank=True)
    win = models.IntegerField(default=0, null=True, blank=True)
    lose = models.IntegerField(default=0, null=True, blank=True)
    min = models.IntegerField(default=0, null=True, blank=True)
    pts_off_tov = models.IntegerField(default=0, null=True, blank=True)
    pts_2nd_chance = models.IntegerField(default=0, null=True, blank=True)
    pts_fb = models.IntegerField(default=0, null=True, blank=True)
    pts_paint = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_off_tov = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_2nd_chance = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_fb = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_paint = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Teams General Misc"
        verbose_name_plural = "Teams General Misc"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsGeneralScoring(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(default=0, null=True, blank=True)
    win = models.IntegerField(default=0, null=True, blank=True)
    lose = models.IntegerField(default=0, null=True, blank=True)
    min = models.IntegerField(default=0, null=True, blank=True)
    pct_fga_2pt = models.FloatField(default=0.0, null=True, blank=True)
    pct_fga_3pt = models.FloatField(default=0.0, null=True, blank=True)
    pct_pts_2pt = models.FloatField(default=0.0, null=True, blank=True)
    pct_pts_2pt_mr = models.FloatField(default=0.0, null=True, blank=True)
    pct_pts_3pt = models.FloatField(default=0.0, null=True, blank=True)
    pct_pts_fb = models.FloatField(default=0.0, null=True, blank=True)
    pct_pts_ft = models.FloatField(default=0.0, null=True, blank=True)
    pct_pts_off_tov = models.FloatField(default=0.0, null=True, blank=True)
    pct_pts_paint = models.FloatField(default=0.0, null=True, blank=True)
    pct_ast_2pm = models.FloatField(default=0.0, null=True, blank=True)
    pct_uast_2pm = models.FloatField(default=0.0, null=True, blank=True)
    pct_ast_3pm = models.FloatField(default=0.0, null=True, blank=True)
    pct_uast_3pm = models.FloatField(default=0.0, null=True, blank=True)
    pct_ast_fgm = models.FloatField(default=0.0, null=True, blank=True)
    pct_uast_fgm = models.FloatField(default=0.0, null=True, blank=True)

    class Meta:
        verbose_name = "Teams General Scoring"
        verbose_name_plural = "Teams General Scoring"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsGeneralOpponent(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(default=0, null=True, blank=True)
    win = models.IntegerField(default=0, null=True, blank=True)
    lose = models.IntegerField(default=0, null=True, blank=True)
    min = models.IntegerField(default=0, null=True, blank=True)
    opp_fgm = models.IntegerField(default=0, null=True, blank=True)
    opp_fga = models.IntegerField(default=0, null=True, blank=True)
    opp_fg_pct = models.FloatField(default=0.0, null=True, blank=True)
    opp_fg3m = models.IntegerField(default=0, null=True, blank=True)
    opp_fg3a = models.IntegerField(default=0, null=True, blank=True)
    opp_fg3_pct = models.FloatField(default=0.0, null=True, blank=True)
    opp_ftm = models.IntegerField(default=0, null=True, blank=True)
    opp_fta = models.IntegerField(default=0, null=True, blank=True)
    opp_ft_pct = models.FloatField(default=0.0, null=True, blank=True)
    opp_oreb = models.IntegerField(default=0, null=True, blank=True)
    opp_dreb = models.IntegerField(default=0, null=True, blank=True)
    opp_reb = models.IntegerField(default=0, null=True, blank=True)
    opp_ast = models.IntegerField(default=0, null=True, blank=True)
    opp_tov = models.IntegerField(default=0, null=True, blank=True)
    opp_stl = models.IntegerField(default=0, null=True, blank=True)
    opp_blk = models.IntegerField(default=0, null=True, blank=True)
    opp_blka = models.IntegerField(default=0, null=True, blank=True)
    opp_pf = models.IntegerField(default=0, null=True, blank=True)
    opp_pfd = models.IntegerField(default=0, null=True, blank=True)
    opp_pts = models.IntegerField(default=0, null=True, blank=True)
    plus_minus = models.FloatField(default=0.0, null=True, blank=True)

    class Meta:
        verbose_name = "Teams General Opponent"
        verbose_name_plural = "Teams General Opponent"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsGeneralDefense(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(default=0, null=True, blank=True)
    win = models.IntegerField(default=0, null=True, blank=True)
    lose = models.IntegerField(default=0, null=True, blank=True)
    min = models.IntegerField(default=0, null=True, blank=True)
    def_rating = models.FloatField(default=0.0, null=True, blank=True)
    dreb = models.IntegerField(default=0, null=True, blank=True)
    dreb_pct = models.FloatField(default=0.0, null=True, blank=True)
    stl = models.IntegerField(default=0, null=True, blank=True)
    blk = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_off_tov = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_2nd_chance = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_fb = models.IntegerField(default=0, null=True, blank=True)
    opp_pts_paint = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Teams General Defense"
        verbose_name_plural = "Teams General Defense"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsGeneralViolations(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(default=0, null=True, blank=True)
    win = models.IntegerField(default=0, null=True, blank=True)
    lose = models.IntegerField(default=0, null=True, blank=True)
    w_pct = models.FloatField(default=0.0, null=True, blank=True)
    travel = models.IntegerField(default=0, null=True, blank=True)
    double_dribble = models.IntegerField(default=0, null=True, blank=True)
    discontinued_dribble = models.IntegerField(default=0, null=True, blank=True)
    off_three_sec = models.IntegerField(default=0, null=True, blank=True)
    five_sec = models.IntegerField(default=0, null=True, blank=True)
    eight_sec = models.IntegerField(default=0, null=True, blank=True)
    shot_clock = models.IntegerField(default=0, null=True, blank=True)
    inbound = models.IntegerField(default=0, null=True, blank=True)
    backcourt = models.IntegerField(default=0, null=True, blank=True)
    off_goaltending = models.IntegerField(default=0, null=True, blank=True)
    palming = models.IntegerField(default=0, null=True, blank=True)
    off_foul = models.IntegerField(default=0, null=True, blank=True)
    def_three_sec = models.IntegerField(default=0, null=True, blank=True)
    charge = models.IntegerField(default=0, null=True, blank=True)
    delay_of_game = models.IntegerField(default=0, null=True, blank=True)
    def_goaltending = models.IntegerField(default=0, null=True, blank=True)
    lane = models.IntegerField(default=0, null=True, blank=True)
    jump_ball = models.IntegerField(default=0, null=True, blank=True)
    kicked_ball = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Teams General Violations"
        verbose_name_plural = "Teams General Violations"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsGeneralEstimatedAdvanced(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(default=0, null=True, blank=True)
    win = models.IntegerField(default=0, null=True, blank=True)
    lose = models.IntegerField(default=0, null=True, blank=True)
    min = models.IntegerField(default=0, null=True, blank=True)
    e_off_rating = models.FloatField(default=0.0, null=True, blank=True)
    e_def_rating = models.FloatField(default=0.0, null=True, blank=True)
    e_net_rating = models.FloatField(default=0.0, null=True, blank=True)
    e_ast_ratio = models.FloatField(default=0.0, null=True, blank=True)
    e_oreb_pct = models.FloatField(default=0.0, null=True, blank=True)
    e_dreb_pct = models.FloatField(default=0.0, null=True, blank=True)
    e_reb_pct = models.FloatField(default=0.0, null=True, blank=True)
    e_tm_tov_pct = models.FloatField(default=0.0, null=True, blank=True)
    e_pace = models.FloatField(default=0.0, null=True, blank=True)

    class Meta:
        verbose_name = "Teams General Estimated Advanced"
        verbose_name_plural = "Teams General Estimated Advanced"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsClutchTraditional(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    win = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ftm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Clutch Traditional"
        verbose_name_plural = "Teams Clutch Traditional"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsClutchAdvanced(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    win = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    off_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    def_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    net_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ast_to = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ast_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    reb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tm_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pace = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pie = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Clutch Advanced"
        verbose_name_plural = "Teams Clutch Advanced"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsClutchFourFactors(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    win = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fta_rate = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tm_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_fta_rate = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Clutch Four Factors"
        verbose_name_plural = "Teams Clutch Four Factors"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsClutchMisc(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    win = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Clutch Misc"
        verbose_name_plural = "Teams Clutch Misc"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsClutchScoring(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    win = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pct_fga_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_fga_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_2pt_mr = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_fb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_ft = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_paint = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_uast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_uast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_uast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Clutch Scoring"
        verbose_name_plural = "Teams Clutch Scoring"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsClutchOpponent(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    win = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    opp_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_ftm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Clutch Opponent"
        verbose_name_plural = "Teams Clutch Opponent"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeIsolation(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Isolation"
        verbose_name_plural = "Teams Playtype Isolation"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeTransition(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Transition"
        verbose_name_plural = "Teams Playtype Transition"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeBallHandler(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Ball Handler"
        verbose_name_plural = "Teams Playtype Ball Handler"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeRollMan(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Roll Man"
        verbose_name_plural = "Teams Playtype Roll Man"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypePostUp(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Post Up"
        verbose_name_plural = "Teams Playtype Post Up"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeSpotUp(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Spot Up"
        verbose_name_plural = "Teams Playtype Spot Up"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeHandOff(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Hand Off"
        verbose_name_plural = "Teams Playtype Hand Off"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeCut(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Cut"
        verbose_name_plural = "Teams Playtype Cut"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeOffScreen(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Off Screen"
        verbose_name_plural = "Teams Playtype Off Screen"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypePutbacks(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Putbacks"
        verbose_name_plural = "Teams Playtype Putbacks"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsPlaytypeMisc(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Playtype Misc"
        verbose_name_plural = "Teams Playtype Misc"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingDrives(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drives = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    drive_ftast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    drive_passes = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    drive_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    drive_distance = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Drives"
        verbose_name_plural = "Teams Tracking Drives"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingDefensiveImpact(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    l = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    def_rim_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    def_rim_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    def_rim_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Defensive Impact"
        verbose_name_plural = "Teams Tracking Defensive Impact"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingCatchShoot(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    catch_shoot_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    catch_shoot_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    catch_shoot_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    catch_shoot_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    catch_shoot_fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    catch_shoot_fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    catch_shoot_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    catch_shoot_efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Catch Shoot"
        verbose_name_plural = "Teams Tracking Catch Shoot"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingPassing(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    passes_made = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    passes_received = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    secondary_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    potential_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ast_points_created = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ast_adj = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ast_to_pass_perc = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ast_to_pass_perc_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Passing"
        verbose_name_plural = "Teams Tracking Passing"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingTouches(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    l = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    points = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="POINTS",
    )
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    front_ct_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="FRONT_CT_TOUCHES",
    )
    time_of_poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    avg_sec_per_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    avg_drib_per_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts_per_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    post_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts_per_elbow_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts_per_post_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts_per_paint_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Touches"
        verbose_name_plural = "Teams Tracking Touches"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingPullup(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pull_up_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pull_up_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pull_up_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pull_up_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pull_up_fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pull_up_fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pull_up_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pull_up_efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Pullup"
        verbose_name_plural = "Teams Tracking Pullup"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingRebounding(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    reb_contest = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    reb_contest_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    reb_chances = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    reb_chance_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    reb_chance_defer = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    reb_chance_pct_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Rebounding"
        verbose_name_plural = "Teams Tracking Rebounding"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingOffensiveRebounding(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    oreb_contest = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    oreb_contest_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb_chances = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    oreb_chance_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb_chance_defer = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    oreb_chance_pct_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Offensive Rebounding"
        verbose_name_plural = "Teams Tracking Offensive Rebounding"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingDefensiveRebounding(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dreb_contest = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dreb_contest_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dreb_chances = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dreb_chance_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dreb_chance_defer = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dreb_chance_pct_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Defensive Rebounding"
        verbose_name_plural = "Teams Tracking Defensive Rebounding"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingShootingEfficiency(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    drive_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    catch_shoot_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    catch_shoot_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pull_up_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pull_up_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    post_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    post_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    eff_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Shooting Efficiency"
        verbose_name_plural = "Teams Tracking Shooting Efficiency"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingSpeedDistance(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    dist_feet = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dist_miles = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dist_miles_off = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dist_miles_def = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    avg_speed = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    avg_speed_off = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    avg_speed_def = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Speed Distance"
        verbose_name_plural = "Teams Tracking Speed Distance"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingElbowTouch(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_passes = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_passes_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fouls = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fouls_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Elbow Touch"
        verbose_name_plural = "Teams Tracking Elbow Touch"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingPostUps(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_passes = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_passes_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fouls = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    elbow_touch_fouls_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Post Ups"
        verbose_name_plural = "Teams Tracking Post Ups"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsTrackingPaintTouch(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    w = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lose = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_passes = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_passes_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_fouls = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    paint_touch_fouls_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Tracking Paint Touch"
        verbose_name_plural = "Teams Tracking Paint Touch"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsDefenseDashboardOverall(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    freq_whole_num = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    d_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    d_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    d_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    normal_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Defense Dashboard Overall"
        verbose_name_plural = "Teams Defense Dashboard Overall"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsDefenseDashboard3pt(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    freq_whole_num = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    d_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    d_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    d_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    normal_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Defense Dashboard 3Pt"
        verbose_name_plural = "Teams Defense Dashboard 3Pt"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsDefenseDashboard2pt(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    freq_whole_num = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dfgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dfga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dfg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ns_fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Defense Dashboard 2Pt"
        verbose_name_plural = "Teams Defense Dashboard 2Pt"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsDefenseDashboardLt6(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    freq_whole_num = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_lt_06 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_lt_06 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lt_06_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ns_lt_06_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Defense Dashboard Lt6"
        verbose_name_plural = "Teams Defense Dashboard Lt6"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsDefenseDashboardLt10(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    freq_whole_num = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dfgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dfga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dfg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ns_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Defense Dashboard Lt10"
        verbose_name_plural = "Teams Defense Dashboard Lt10"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsDefenseDashboardGt15(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    freq_whole_num = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_lt_10 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_lt_10 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    lt_10_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ns_lt_10_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Defense Dashboard Gt15"
        verbose_name_plural = "Teams Defense Dashboard Gt15"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsShotDashboardGeneral(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Shot Dashboard General"
        verbose_name_plural = "Teams Shot Dashboard General"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsShotDashboardShotClock(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Shot Dashboard Shot Clock"
        verbose_name_plural = "Teams Shot Dashboard Shot Clock"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsShotDashboardDribbles(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Shot Dashboard Dribbles"
        verbose_name_plural = "Teams Shot Dashboard Dribbles"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsShotDashboardTouchTime(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Shot Dashboard Touch Time"
        verbose_name_plural = "Teams Shot Dashboard Touch Time"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsShotDashboardClosestDefender(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Shot Dashboard Closest Defender"
        verbose_name_plural = "Teams Shot Dashboard Closest Defender"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsShotDashboardClosestDefender10(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Shot Dashboard Closest Defender 10"
        verbose_name_plural = "Teams Shot Dashboard Closest Defender 10"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsAdvancedBoxScores(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
    )
    wl = models.CharField(
        max_length=1,
        verbose_name="Resultado",
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ftm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Advanced Box Scores"
        verbose_name_plural = "Teams Advanced Box Scores"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsAdvancedBoxScoresAdvanced(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
    )
    wl = models.CharField(
        max_length=1,
        verbose_name="Resultado",
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    off_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    def_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    net_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ast_to = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ast_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    reb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tm_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pace = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pie = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Advanced Box Scores Advanced"
        verbose_name_plural = "Teams Advanced Box Scores Advanced"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsAdvancedBoxScoresFourFactors(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
    )
    wl = models.CharField(
        max_length=1,
        verbose_name="Resultado",
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fta_rate = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    tm_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_fta_rate = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Advanced Box Scores Four Factors"
        verbose_name_plural = "Teams Advanced Box Scores Four Factors"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsAdvancedBoxScoresMisc(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
    )
    wl = models.CharField(
        max_length=1,
        verbose_name="Resultado",
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    opp_pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    opp_pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Advanced Box Scores Misc"
        verbose_name_plural = "Teams Advanced Box Scores Misc"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsAdvancedBoxScoresScoring(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
    )
    wl = models.CharField(
        max_length=1,
        verbose_name="Resultado",
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pct_fga_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_fga_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_2pt_mr = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_fb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_ft = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_pts_paint = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_uast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_uast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_uast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Advanced Box Scores Scoring"
        verbose_name_plural = "Teams Advanced Box Scores Scoring"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsShooting(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    fgm_lt5 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_lt5 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_lt5 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_5_9 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_5_9 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_5_9 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_10_14 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_10_14 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_10_14 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_15_19 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_15_19 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_15_19 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_20_24 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_20_24 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_20_24 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_25_29 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_25_29 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_25_29 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Shooting"
        verbose_name_plural = "Teams Shooting"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsOpponentShootingOverall(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    fgm_lt5 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_lt5 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_lt5 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_5_9 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_5_9 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_5_9 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_10_14 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_10_14 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_10_14 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_15_19 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_15_19 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_15_19 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_20_24 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_20_24 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_20_24 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm_25_29 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_25_29 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct_25_29 = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Opponent Shooting Overall"
        verbose_name_plural = "Teams Opponent Shooting Overall"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsOpponentShotsGeneral(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Opponent Shots General"
        verbose_name_plural = "Teams Opponent Shots General"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsOpponentShotsShotclock(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Opponent Shots Shotclock"
        verbose_name_plural = "Teams Opponent Shots Shotclock"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsOpponentShotsDribbles(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Opponent Shots Dribbles"
        verbose_name_plural = "Teams Opponent Shots Dribbles"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsOpponentShotsTouchTime(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Opponent Shots Touch Time"
        verbose_name_plural = "Teams Opponent Shots Touch Time"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsOpponentShotsClosestDefender(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Opponent Shots Closest Defender"
        verbose_name_plural = "Teams Opponent Shots Closest Defender"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsOpponentShotsClosestDefender10(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Opponent Shots Closest Defender 10"
        verbose_name_plural = "Teams Opponent Shots Closest Defender 10"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsHustle(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    screen_assists = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    screen_ast_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    deflections = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    off_loose_balls_recovered = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    def_loose_balls_recovered = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    loose_balls_recovered = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pct_loose_balls_recovered_off = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_loose_balls_recovered_def = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    charges_drawn = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    contested_shots_2pt = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    contested_shots_3pt = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    contested_shots = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Hustle"
        verbose_name_plural = "Teams Hustle"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"


class TeamsBoxOuts(models.Model):
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
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        db_index=True,
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        null=True,
        blank=True,
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    box_outs = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    off_boxouts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    def_boxouts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pct_box_outs_off = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_box_outs_def = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teams Box Outs"
        verbose_name_plural = "Teams Box Outs"
        unique_together = [["season", "season_type", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{self.team_abb} - {self.season} ({self.season_type})"
