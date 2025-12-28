from django.db import models

# Create your models here.

from data.enums import (
    SeasonChoices,
    SeasonTypeChoices,
    GameBoxscorePeriodChoices,
    GamePlayByPlayPeriodChoices,
)
from roster.enums import TeamChoices


class AdvancedBoxScore(models.Model):
    """
    Modelo para almacenar estadísticas avanzadas de box score de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2015-16)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(
        max_length=10, help_text="Código del equipo (ej: DET, SAS, BOS)"
    )
    match_up = models.CharField(
        max_length=50, help_text="Emparejamiento del partido (ej: DET VS. ATL)"
    )
    game_date = models.DateField(help_text="Fecha del partido")
    win_lose = models.CharField(max_length=1, help_text="Victoria (W) o Derrota (L)")

    # Estadísticas básicas
    min = models.IntegerField(help_text="Minutos jugados")
    pts = models.IntegerField(help_text="Puntos")
    fgm = models.IntegerField(help_text="Tiros de campo anotados")
    fga = models.IntegerField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    threepm = models.IntegerField(help_text="Triples anotados")
    threepa = models.IntegerField(help_text="Triples intentados")
    threep_percent = models.FloatField(help_text="Porcentaje de triples")
    ftm = models.IntegerField(help_text="Tiros libres anotados")
    fta = models.IntegerField(help_text="Tiros libres intentados")
    ft_percent = models.FloatField(help_text="Porcentaje de tiros libres")

    # Rebotes
    oreb = models.IntegerField(help_text="Rebotes ofensivos")
    dreb = models.IntegerField(help_text="Rebotes defensivos")
    reb = models.IntegerField(help_text="Rebotes totales")

    # Otras estadísticas
    ast = models.IntegerField(help_text="Asistencias")
    tov = models.IntegerField(help_text="Pérdidas de balón")
    stl = models.IntegerField(help_text="Robos")
    blk = models.IntegerField(help_text="Bloqueos")
    pf = models.IntegerField(help_text="Faltas personales")
    plus_minus = models.IntegerField(help_text="Diferencial de puntos (+/-)")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "advanced_box_scores"
        verbose_name = "Advanced Box Score"
        verbose_name_plural = "Advanced Box Scores"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} vs {self.match_up} - {self.game_date}"


class BoxOuts(models.Model):
    """
    Modelo para almacenar estadísticas de box outs de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2024-25)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de box outs
    min = models.FloatField(help_text="Minutos jugados")
    box_outs = models.FloatField(help_text="Box outs totales")
    off_box_outs = models.FloatField(help_text="Box outs ofensivos")
    def_box_outs = models.FloatField(help_text="Box outs defensivos")
    percent_box_outs_off = models.FloatField(
        help_text="Porcentaje de box outs ofensivos"
    )
    percent_box_outs_def = models.FloatField(
        help_text="Porcentaje de box outs defensivos"
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "box_outs"
        verbose_name = "Box Out"
        verbose_name_plural = "Box Outs"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class BoxScore(models.Model):
    """
    Modelo para almacenar estadísticas básicas de box score de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2015-16)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=10, help_text="Código del equipo")
    match_up = models.CharField(max_length=50, help_text="Emparejamiento del partido")
    game_date = models.DateField(help_text="Fecha del partido")
    win_lose = models.CharField(max_length=1, help_text="Victoria (W) o Derrota (L)")

    # Estadísticas básicas
    min = models.IntegerField(help_text="Minutos jugados")
    pts = models.IntegerField(help_text="Puntos")
    fgm = models.IntegerField(help_text="Tiros de campo anotados")
    fga = models.IntegerField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    threepm = models.IntegerField(help_text="Triples anotados")
    threepa = models.IntegerField(help_text="Triples intentados")
    threep_percent = models.FloatField(help_text="Porcentaje de triples")
    ftm = models.IntegerField(help_text="Tiros libres anotados")
    fta = models.IntegerField(help_text="Tiros libres intentados")
    ft_percent = models.FloatField(help_text="Porcentaje de tiros libres")

    # Rebotes
    oreb = models.IntegerField(help_text="Rebotes ofensivos")
    dreb = models.IntegerField(help_text="Rebotes defensivos")
    reb = models.IntegerField(help_text="Rebotes totales")

    # Otras estadísticas
    ast = models.IntegerField(help_text="Asistencias")
    stl = models.IntegerField(help_text="Robos")
    blk = models.IntegerField(help_text="Bloqueos")
    tov = models.IntegerField(help_text="Pérdidas de balón")
    pf = models.IntegerField(help_text="Faltas personales")
    plus_minus = models.IntegerField(help_text="Diferencial de puntos (+/-)")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "box_scores"
        verbose_name = "Box Score"
        verbose_name_plural = "Box Scores"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} vs {self.match_up} - {self.game_date}"


class CatchShoot(models.Model):
    """
    Modelo para almacenar estadísticas de catch & shoot de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de catch & shoot
    gp = models.IntegerField(help_text="Partidos jugados")
    min = models.FloatField(help_text="Minutos")
    pts = models.FloatField(help_text="Puntos")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    threepm = models.FloatField(help_text="Triples anotados")
    threepa = models.FloatField(help_text="Triples intentados")
    threep_percent = models.FloatField(help_text="Porcentaje de triples")
    efg_percent = models.FloatField(help_text="Porcentaje efectivo de tiros de campo")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catch_shoot"
        verbose_name = "Catch & Shoot"
        verbose_name_plural = "Catch & Shoot"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class Clutch(models.Model):
    """
    Modelo para almacenar estadísticas en situaciones clave de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2015-16)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas en situaciones clave
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    win_percent = models.FloatField(help_text="Porcentaje de victorias")
    min = models.FloatField(help_text="Minutos")
    pts = models.FloatField(help_text="Puntos")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    threepm = models.FloatField(help_text="Triples anotados")
    threepa = models.FloatField(help_text="Triples intentados")
    threep_percent = models.FloatField(help_text="Porcentaje de triples")
    ftm = models.FloatField(help_text="Tiros libres anotados")
    fta = models.FloatField(help_text="Tiros libres intentados")
    ft_percent = models.FloatField(help_text="Porcentaje de tiros libres")
    oreb = models.FloatField(help_text="Rebotes ofensivos")
    dreb = models.FloatField(help_text="Rebotes defensivos")
    reb = models.FloatField(help_text="Rebotes totales")
    ast = models.FloatField(help_text="Asistencias")
    tov = models.FloatField(help_text="Pérdidas de balón")
    stl = models.FloatField(help_text="Robos")
    blk = models.FloatField(help_text="Bloqueos")
    blka = models.FloatField(help_text="Tiros bloqueados contra")
    pf = models.FloatField(help_text="Faltas personales")
    pfd = models.FloatField(help_text="Faltas personales provocadas")
    plus_minus = models.FloatField(help_text="Diferencial de puntos (+/-)")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clutch"
        verbose_name = "Clutch"
        verbose_name_plural = "Clutch"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class DefenseDashboard(models.Model):
    """
    Modelo para almacenar estadísticas del dashboard defensivo de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2022-23)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas defensivas
    gp = models.IntegerField(help_text="Partidos jugados")
    g = models.IntegerField(help_text="Partidos")
    freq = models.FloatField(help_text="Frecuencia")
    dfgm = models.FloatField(help_text="Tiros de campo defendidos anotados")
    dfga = models.FloatField(help_text="Tiros de campo defendidos intentados")
    dfg_percent = models.FloatField(help_text="Porcentaje de tiros de campo defendidos")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    diff_percent = models.FloatField(help_text="Diferencia de porcentaje")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "defense_dashboard"
        verbose_name = "Defense Dashboard"
        verbose_name_plural = "Defense Dashboards"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class DefensiveImpact(models.Model):
    """
    Modelo para almacenar estadísticas de impacto defensivo de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2024-25)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de impacto defensivo
    gp = models.IntegerField(help_text="Partidos jugados")
    min = models.FloatField(help_text="Minutos")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    stl = models.FloatField(help_text="Robos")
    blk = models.FloatField(help_text="Bloqueos")
    dreb = models.FloatField(help_text="Rebotes defensivos")
    dfgm = models.FloatField(help_text="Tiros de campo defendidos anotados")
    dfga = models.FloatField(help_text="Tiros de campo defendidos intentados")
    dfg_percent = models.FloatField(help_text="Porcentaje de tiros de campo defendidos")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "defensive_impact"
        verbose_name = "Defensive Impact"
        verbose_name_plural = "Defensive Impacts"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class DefensiveRebounding(models.Model):
    """
    Modelo para almacenar estadísticas de rebotes defensivos de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de rebotes defensivos
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    dreb = models.FloatField(help_text="Rebotes defensivos")
    contested_dreb = models.FloatField(help_text="Rebotes defensivos disputados")
    contested_dreb_percent = models.FloatField(
        help_text="Porcentaje de rebotes defensivos disputados"
    )
    dreb_chances = models.FloatField(help_text="Oportunidades de rebotes defensivos")
    dreb_chance_percent = models.FloatField(
        help_text="Porcentaje de oportunidades de rebotes defensivos"
    )
    deferred_dreb_chances = models.FloatField(
        help_text="Oportunidades de rebotes defensivos diferidas"
    )
    adjusted_dreb_chance_percent = models.FloatField(
        help_text="Porcentaje ajustado de oportunidades de rebotes defensivos"
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "defensive_rebounding"
        verbose_name = "Defensive Rebounding"
        verbose_name_plural = "Defensive Reboundings"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class Drives(models.Model):
    """
    Modelo para almacenar estadísticas de drives de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de drives
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    drives = models.FloatField(help_text="Drives")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    ftm = models.FloatField(help_text="Tiros libres anotados")
    fta = models.FloatField(help_text="Tiros libres intentados")
    ft_percent = models.FloatField(help_text="Porcentaje de tiros libres")
    pts = models.FloatField(help_text="Puntos")
    pts_percent = models.FloatField(help_text="Porcentaje de puntos")
    pass_field = models.FloatField(help_text="Pases")
    pass_percent = models.FloatField(help_text="Porcentaje de pases")
    ast = models.FloatField(help_text="Asistencias")
    ast_percent = models.FloatField(help_text="Porcentaje de asistencias")
    to_field = models.FloatField(help_text="Pérdidas de balón")
    tov_percent = models.FloatField(help_text="Porcentaje de pérdidas de balón")
    pf = models.FloatField(help_text="Faltas personales")
    pf_percent = models.FloatField(help_text="Porcentaje de faltas personales")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "drives"
        verbose_name = "Drive"
        verbose_name_plural = "Drives"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class ElbowTouch(models.Model):
    """
    Modelo para almacenar estadísticas de elbow touches de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de elbow touches
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    touches = models.FloatField(help_text="Touches totales")
    elbow_touches = models.FloatField(help_text="Elbow touches")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    ftm = models.FloatField(help_text="Tiros libres anotados")
    fta = models.FloatField(help_text="Tiros libres intentados")
    ft_percent = models.FloatField(help_text="Porcentaje de tiros libres")
    pts = models.FloatField(help_text="Puntos")
    pts_percent = models.FloatField(help_text="Porcentaje de puntos")
    pass_field = models.FloatField(help_text="Pases")
    pass_percent = models.FloatField(help_text="Porcentaje de pases")
    ast = models.FloatField(help_text="Asistencias")
    ast_percent = models.FloatField(help_text="Porcentaje de asistencias")
    to_field = models.FloatField(help_text="Pérdidas de balón")
    tov_percent = models.FloatField(help_text="Porcentaje de pérdidas de balón")
    pf = models.FloatField(help_text="Faltas personales")
    pf_percent = models.FloatField(help_text="Porcentaje de faltas personales")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "elbow_touch"
        verbose_name = "Elbow Touch"
        verbose_name_plural = "Elbow Touches"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class Hustle(models.Model):
    """
    Modelo para almacenar estadísticas de hustle de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2015-16)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de hustle
    min = models.FloatField(help_text="Minutos")
    screen_assists = models.FloatField(help_text="Asistencias de pantalla")
    screen_assists_pts = models.FloatField(
        help_text="Puntos por asistencias de pantalla"
    )
    deflections = models.FloatField(help_text="Desviaciones")
    off_loose_balls_recovered = models.FloatField(
        help_text="Balones sueltos recuperados ofensivos"
    )
    def_loose_balls_recovered = models.FloatField(
        help_text="Balones sueltos recuperados defensivos"
    )
    loose_balls_recovered = models.FloatField(
        help_text="Balones sueltos recuperados totales"
    )
    percent_loose_balls_recovered_off = models.FloatField(
        help_text="Porcentaje de balones sueltos recuperados ofensivos"
    )
    percent_loose_balls_recovered_def = models.FloatField(
        help_text="Porcentaje de balones sueltos recuperados defensivos"
    )
    charges_drawn = models.FloatField(help_text="Cargas provocadas")
    contested_2pt_shots = models.FloatField(help_text="Tiros de 2 puntos disputados")
    contested_3pt_shots = models.FloatField(help_text="Tiros de 3 puntos disputados")
    contested_shots = models.FloatField(help_text="Tiros disputados totales")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hustle"
        verbose_name = "Hustle"
        verbose_name_plural = "Hustle"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class OffensiveRebounding(models.Model):
    """
    Modelo para almacenar estadísticas de rebotes ofensivos de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de rebotes ofensivos
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    oreb = models.FloatField(help_text="Rebotes ofensivos")
    contested_oreb = models.FloatField(help_text="Rebotes ofensivos disputados")
    contested_oreb_percent = models.FloatField(
        help_text="Porcentaje de rebotes ofensivos disputados"
    )
    oreb_chances = models.FloatField(help_text="Oportunidades de rebotes ofensivos")
    oreb_chance_percent = models.FloatField(
        help_text="Porcentaje de oportunidades de rebotes ofensivos"
    )
    deferred_oreb_chances = models.FloatField(
        help_text="Oportunidades de rebotes ofensivos diferidas"
    )
    adjusted_oreb_chance_percent = models.FloatField(
        help_text="Porcentaje ajustado de oportunidades de rebotes ofensivos"
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "offensive_rebounding"
        verbose_name = "Offensive Rebounding"
        verbose_name_plural = "Offensive Reboundings"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class OpponentShooting(models.Model):
    """
    Modelo para almacenar estadísticas de tiros del oponente de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de tiros del oponente por distancia
    less_than_5ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados menos de 5 pies"
    )
    less_than_5ft_fga = models.FloatField(
        help_text="Tiros de campo intentados menos de 5 pies"
    )
    less_than_5ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo menos de 5 pies"
    )

    five_to_9ft_fgm = models.FloatField(help_text="Tiros de campo anotados 5-9 pies")
    five_to_9ft_fga = models.FloatField(help_text="Tiros de campo intentados 5-9 pies")
    five_to_9ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 5-9 pies"
    )

    ten_to_14ft_fgm = models.FloatField(help_text="Tiros de campo anotados 10-14 pies")
    ten_to_14ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 10-14 pies"
    )
    ten_to_14ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 10-14 pies"
    )

    fifteen_to_19ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados 15-19 pies"
    )
    fifteen_to_19ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 15-19 pies"
    )
    fifteen_to_19ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 15-19 pies"
    )

    twenty_to_24ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados 20-24 pies"
    )
    twenty_to_24ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 20-24 pies"
    )
    twenty_to_24ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 20-24 pies"
    )

    twenty_five_to_29ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados 25-29 pies"
    )
    twenty_five_to_29ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 25-29 pies"
    )
    twenty_five_to_29ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 25-29 pies"
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "opponent_shooting"
        verbose_name = "Opponent Shooting"
        verbose_name_plural = "Opponent Shootings"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class PaintTouch(models.Model):
    """
    Modelo para almacenar estadísticas de paint touches de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de paint touches
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    touches = models.FloatField(help_text="Touches totales")
    paint_touches = models.FloatField(help_text="Paint touches")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    ftm = models.FloatField(help_text="Tiros libres anotados")
    fta = models.FloatField(help_text="Tiros libres intentados")
    ft_percent = models.FloatField(help_text="Porcentaje de tiros libres")
    pts = models.FloatField(help_text="Puntos")
    pts_percent = models.FloatField(help_text="Porcentaje de puntos")
    pass_field = models.FloatField(help_text="Pases")
    pass_percent = models.FloatField(help_text="Porcentaje de pases")
    ast = models.FloatField(help_text="Asistencias")
    ast_percent = models.FloatField(help_text="Porcentaje de asistencias")
    to_field = models.FloatField(help_text="Pérdidas de balón")
    tov_percent = models.FloatField(help_text="Porcentaje de pérdidas de balón")
    pf = models.FloatField(help_text="Faltas personales")
    pf_percent = models.FloatField(help_text="Porcentaje de faltas personales")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "paint_touch"
        verbose_name = "Paint Touch"
        verbose_name_plural = "Paint Touches"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class Passing(models.Model):
    """
    Modelo para almacenar estadísticas de pases de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de pases
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    passes_made = models.FloatField(help_text="Pases realizados")
    passes_received = models.FloatField(help_text="Pases recibidos")
    ast = models.FloatField(help_text="Asistencias")
    secondary_ast = models.FloatField(help_text="Asistencias secundarias")
    potential_ast = models.FloatField(help_text="Asistencias potenciales")
    ast_pts_created = models.FloatField(help_text="Puntos creados por asistencias")
    ast_adj = models.FloatField(help_text="Asistencias ajustadas")
    ast_to_pass_percent = models.FloatField(
        help_text="Porcentaje de asistencias por pase"
    )
    ast_to_pass_percent_adj = models.FloatField(
        help_text="Porcentaje ajustado de asistencias por pase"
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "passing"
        verbose_name = "Passing"
        verbose_name_plural = "Passing"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class PlayType(models.Model):
    """
    Modelo para almacenar estadísticas de tipos de jugada de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")
    play_type = models.CharField(max_length=50, help_text="Tipo de jugada")

    # Estadísticas de tipos de jugada
    gp = models.IntegerField(help_text="Partidos jugados")
    poss = models.FloatField(help_text="Posesiones")
    freq_percent = models.FloatField(help_text="Porcentaje de frecuencia")
    ppp = models.FloatField(help_text="Puntos por posesión")
    pts = models.FloatField(help_text="Puntos")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    efg_percent = models.FloatField(help_text="Porcentaje efectivo de tiros de campo")
    ft_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de tiros libres"
    )
    tov_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de pérdidas de balón"
    )
    sf_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de faltas de tiro"
    )
    and_one_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de and-one"
    )
    score_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de anotación"
    )
    percentile = models.FloatField(help_text="Percentil")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "play_type"
        verbose_name = "Play Type"
        verbose_name_plural = "Play Types"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.play_type} - {self.game_date}"


class PostUps(models.Model):
    """
    Modelo para almacenar estadísticas de post ups de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de post ups
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    touches = models.FloatField(help_text="Touches totales")
    post_ups = models.FloatField(help_text="Post ups")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    ftm = models.FloatField(help_text="Tiros libres anotados")
    fta = models.FloatField(help_text="Tiros libres intentados")
    ft_percent = models.FloatField(help_text="Porcentaje de tiros libres")
    pts = models.FloatField(help_text="Puntos")
    pts_percent = models.FloatField(help_text="Porcentaje de puntos")
    pass_field = models.FloatField(help_text="Pases")
    pass_percent = models.FloatField(help_text="Porcentaje de pases")
    ast = models.FloatField(help_text="Asistencias")
    ast_percent = models.FloatField(help_text="Porcentaje de asistencias")
    to_field = models.FloatField(help_text="Pérdidas de balón")
    tov_percent = models.FloatField(help_text="Porcentaje de pérdidas de balón")
    pf = models.FloatField(help_text="Faltas personales")
    pf_percent = models.FloatField(help_text="Porcentaje de faltas personales")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post_ups"
        verbose_name = "Post Up"
        verbose_name_plural = "Post Ups"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class PullUpShooting(models.Model):
    """
    Modelo para almacenar estadísticas de pull up shooting de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de pull up shooting
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    pts = models.FloatField(help_text="Puntos")
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    threepm = models.FloatField(help_text="Triples anotados")
    threepa = models.FloatField(help_text="Triples intentados")
    threep_percent = models.FloatField(help_text="Porcentaje de triples")
    efg_percent = models.FloatField(help_text="Porcentaje efectivo de tiros de campo")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pull_up_shooting"
        verbose_name = "Pull Up Shooting"
        verbose_name_plural = "Pull Up Shootings"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class Rebounding(models.Model):
    """
    Modelo para almacenar estadísticas de rebotes de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de rebotes
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    reb = models.FloatField(help_text="Rebotes totales")
    contested_reb = models.FloatField(help_text="Rebotes disputados")
    contested_reb_percent = models.FloatField(
        help_text="Porcentaje de rebotes disputados"
    )
    reb_chances = models.FloatField(help_text="Oportunidades de rebotes")
    reb_chance_percent = models.FloatField(
        help_text="Porcentaje de oportunidades de rebotes"
    )
    deferred_reb_chances = models.FloatField(
        help_text="Oportunidades de rebotes diferidas"
    )
    adjusted_reb_chance_percent = models.FloatField(
        help_text="Porcentaje ajustado de oportunidades de rebotes"
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rebounding"
        verbose_name = "Rebounding"
        verbose_name_plural = "Rebounding"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class ShootingEfficiency(models.Model):
    """
    Modelo para almacenar estadísticas de eficiencia de tiro de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de eficiencia de tiro
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    pts = models.FloatField(help_text="Puntos")
    drive_pts = models.FloatField(help_text="Puntos por drives")
    drive_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo por drives"
    )
    cs_pts = models.FloatField(help_text="Puntos por catch & shoot")
    cs_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo por catch & shoot"
    )
    pull_up_pts = models.FloatField(help_text="Puntos por pull up")
    pull_up_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo por pull up"
    )
    paint_touch_pts = models.FloatField(help_text="Puntos por paint touches")
    paint_touch_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo por paint touches"
    )
    post_touch_pts = models.FloatField(help_text="Puntos por post touches")
    post_touch_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo por post touches"
    )
    elbow_touch_pts = models.FloatField(help_text="Puntos por elbow touches")
    elbow_touch_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo por elbow touches"
    )
    efg_percent = models.FloatField(help_text="Porcentaje efectivo de tiros de campo")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shooting_efficiency"
        verbose_name = "Shooting Efficiency"
        verbose_name_plural = "Shooting Efficiencies"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class Shooting(models.Model):
    """
    Modelo para almacenar estadísticas de tiro de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de tiro por distancia
    less_than_5ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados menos de 5 pies"
    )
    less_than_5ft_fga = models.FloatField(
        help_text="Tiros de campo intentados menos de 5 pies"
    )
    less_than_5ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo menos de 5 pies"
    )

    five_to_9ft_fgm = models.FloatField(help_text="Tiros de campo anotados 5-9 pies")
    five_to_9ft_fga = models.FloatField(help_text="Tiros de campo intentados 5-9 pies")
    five_to_9ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 5-9 pies"
    )

    ten_to_14ft_fgm = models.FloatField(help_text="Tiros de campo anotados 10-14 pies")
    ten_to_14ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 10-14 pies"
    )
    ten_to_14ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 10-14 pies"
    )

    fifteen_to_19ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados 15-19 pies"
    )
    fifteen_to_19ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 15-19 pies"
    )
    fifteen_to_19ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 15-19 pies"
    )

    twenty_to_24ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados 20-24 pies"
    )
    twenty_to_24ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 20-24 pies"
    )
    twenty_to_24ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 20-24 pies"
    )

    twenty_five_to_29ft_fgm = models.FloatField(
        help_text="Tiros de campo anotados 25-29 pies"
    )
    twenty_five_to_29ft_fga = models.FloatField(
        help_text="Tiros de campo intentados 25-29 pies"
    )
    twenty_five_to_29ft_fg_percent = models.FloatField(
        help_text="Porcentaje de tiros de campo 25-29 pies"
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shooting"
        verbose_name = "Shooting"
        verbose_name_plural = "Shooting"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class ShotDashboard(models.Model):
    """
    Modelo para almacenar estadísticas del dashboard de tiros de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2024-25)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas del dashboard de tiros
    gp = models.IntegerField(help_text="Partidos jugados")
    g = models.IntegerField(help_text="Partidos")

    # Tiros de campo
    fg_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de tiros de campo"
    )
    fgm = models.FloatField(help_text="Tiros de campo anotados")
    fga = models.FloatField(help_text="Tiros de campo intentados")
    fg_percent = models.FloatField(help_text="Porcentaje de tiros de campo")
    efg_percent = models.FloatField(help_text="Porcentaje efectivo de tiros de campo")

    # Tiros de 2 puntos
    two_fg_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de tiros de 2 puntos"
    )
    two_fgm = models.FloatField(help_text="Tiros de 2 puntos anotados")
    two_fga = models.FloatField(help_text="Tiros de 2 puntos intentados")
    two_fg_percent = models.FloatField(help_text="Porcentaje de tiros de 2 puntos")

    # Tiros de 3 puntos
    three_fg_freq_percent = models.FloatField(
        help_text="Porcentaje de frecuencia de tiros de 3 puntos"
    )
    threepm = models.FloatField(help_text="Triples anotados")
    threepa = models.FloatField(help_text="Triples intentados")
    threep_percent = models.FloatField(help_text="Porcentaje de triples")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shot_dashboard"
        verbose_name = "Shot Dashboard"
        verbose_name_plural = "Shot Dashboards"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class SpeedDistance(models.Model):
    """
    Modelo para almacenar estadísticas de velocidad y distancia de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de velocidad y distancia
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    dist_feet = models.FloatField(help_text="Distancia en pies")
    dist_miles = models.FloatField(help_text="Distancia en millas")
    dist_miles_off = models.FloatField(help_text="Distancia en millas ofensiva")
    dist_miles_def = models.FloatField(help_text="Distancia en millas defensiva")
    avg_speed = models.FloatField(help_text="Velocidad promedio")
    avg_speed_off = models.FloatField(help_text="Velocidad promedio ofensiva")
    avg_speed_def = models.FloatField(help_text="Velocidad promedio defensiva")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "speed_distance"
        verbose_name = "Speed Distance"
        verbose_name_plural = "Speed Distances"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


class Touches(models.Model):
    """
    Modelo para almacenar estadísticas de touches de equipos de la NBA
    """

    season = models.CharField(max_length=10, help_text="Temporada (ej: 2025-26)")
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Preseason, Regular Season, Playoffs)",
    )
    match_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )

    # Información del equipo y partido
    team = models.CharField(max_length=50, help_text="Nombre del equipo")
    game_date = models.DateField(help_text="Fecha del partido")

    # Estadísticas de touches
    gp = models.IntegerField(help_text="Partidos jugados")
    win = models.IntegerField(help_text="Victorias")
    lose = models.IntegerField(help_text="Derrotas")
    min = models.FloatField(help_text="Minutos")
    pts = models.FloatField(help_text="Puntos")
    touches = models.FloatField(help_text="Touches totales")
    front_ct_touches = models.FloatField(help_text="Touches en campo delantero")
    time_of_poss = models.FloatField(help_text="Tiempo de posesión")
    avg_sec_per_touch = models.FloatField(help_text="Segundos promedio por touch")
    avg_drib_per_touch = models.FloatField(help_text="Dribbles promedio por touch")
    pts_per_touch = models.FloatField(help_text="Puntos por touch")
    elbow_touches = models.FloatField(help_text="Elbow touches")
    post_ups = models.FloatField(help_text="Post ups")
    paint_touches = models.FloatField(help_text="Paint touches")
    pts_per_elbow_touch = models.FloatField(help_text="Puntos por elbow touch")
    pts_per_post_touch = models.FloatField(help_text="Puntos por post touch")
    pts_per_paint_touch = models.FloatField(help_text="Puntos por paint touch")

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "touches"
        verbose_name = "Touch"
        verbose_name_plural = "Touches"
        ordering = ["-game_date", "team"]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team"]),
            models.Index(fields=["game_date"]),
            models.Index(fields=["match_id"]),
        ]

    def __str__(self):
        return f"{self.team} - {self.game_date}"


# Nuevos modelos para datos de partidos
class GameBoxscoreTraditional(models.Model):
    # Información del juego
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
        help_text="Temporada del juego (formato: YYYY-YY, ej: 2015-16)",
    )
    season_type = models.CharField(
        max_length=20,
        choices=SeasonTypeChoices.choices(),
        verbose_name="Tipo de Temporada",
        help_text="Tipo de temporada (pre-season, regular-season, playoffs)",
    )
    home_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo Local",
        help_text="Abreviación del equipo local",
    )
    away_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo Visitante",
        help_text="Abreviación del equipo visitante",
    )

    # Información del jugador
    player_id = models.IntegerField(
        db_index=True,
        verbose_name="ID del Jugador",
        help_text="Identificador único del jugador",
    )
    player_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Jugador",
        help_text="Nombre completo del jugador",
    )
    player_name_abb = models.CharField(
        max_length=50,
        verbose_name="Nombre Abreviado",
        help_text="Nombre abreviado del jugador",
    )
    player_team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo del Jugador",
        help_text="Abreviación del equipo del jugador",
    )
    player_pos = models.CharField(
        max_length=5,
        verbose_name="Posición",
        help_text="Posición del jugador (G, F, C, etc.)",
    )
    player_dnp = models.BooleanField(
        default=False,
        verbose_name="No Jugó",
        help_text="Indica si el jugador no jugó (Did Not Play)",
    )

    # Información del período
    period = models.CharField(
        max_length=10,
        choices=GameBoxscorePeriodChoices.choices(),
        verbose_name="Período",
        help_text="Período del juego (1, 2, 3, 4, OT, All, etc.)",
    )
    min = models.CharField(
        max_length=10,
        verbose_name="Minutos",
        help_text="Minutos jugados en formato MM:SS",
    )

    # Estadísticas de tiros
    fgm = models.IntegerField(
        default=0,
        verbose_name="Tiros de Campo Anotados",
        help_text="Tiros de campo anotados (Field Goals Made)",
    )
    fga = models.IntegerField(
        default=0,
        verbose_name="Tiros de Campo Intentados",
        help_text="Tiros de campo intentados (Field Goals Attempted)",
    )
    fg_perc = models.FloatField(
        default=0.0,
        verbose_name="% Tiros de Campo",
        help_text="Porcentaje de tiros de campo (Field Goal Percentage)",
    )
    threepm = models.IntegerField(
        default=0,
        verbose_name="Triples Anotados",
        help_text="Triples anotados (3 Pointers Made)",
    )
    threepa = models.IntegerField(
        default=0,
        verbose_name="Triples Intentados",
        help_text="Triples intentados (3 Pointers Attempted)",
    )
    threep_perc = models.FloatField(
        default=0.0,
        verbose_name="% Triples",
        help_text="Porcentaje de triples (3 Point Percentage)",
    )
    ftm = models.IntegerField(
        default=0,
        verbose_name="Tiros Libres Anotados",
        help_text="Tiros libres anotados (Free Throws Made)",
    )
    fta = models.IntegerField(
        default=0,
        verbose_name="Tiros Libres Intentados",
        help_text="Tiros libres intentados (Free Throws Attempted)",
    )
    ft_perc = models.FloatField(
        default=0.0,
        verbose_name="% Tiros Libres",
        help_text="Porcentaje de tiros libres (Free Throw Percentage)",
    )

    # Rebotes
    oreb = models.IntegerField(
        default=0,
        verbose_name="Rebotes Ofensivos",
        help_text="Rebotes ofensivos (Offensive Rebounds)",
    )
    dreb = models.IntegerField(
        default=0,
        verbose_name="Rebotes Defensivos",
        help_text="Rebotes defensivos (Defensive Rebounds)",
    )
    reb = models.IntegerField(
        default=0,
        verbose_name="Rebotes Totales",
        help_text="Total de rebotes (Total Rebounds)",
    )

    # Otras estadísticas
    ast = models.IntegerField(
        default=0,
        verbose_name="Asistencias",
        help_text="Asistencias (Assists)",
    )
    stl = models.IntegerField(
        default=0,
        verbose_name="Robos",
        help_text="Robos de balón (Steals)",
    )
    blk = models.IntegerField(
        default=0,
        verbose_name="Tapones",
        help_text="Tapones (Blocks)",
    )
    to = models.IntegerField(
        default=0,
        verbose_name="Pérdidas",
        help_text="Pérdidas de balón (Turnovers)",
    )
    pf = models.IntegerField(
        default=0,
        verbose_name="Faltas Personales",
        help_text="Faltas personales (Personal Fouls)",
    )
    pts = models.IntegerField(
        default=0,
        verbose_name="Puntos",
        help_text="Puntos anotados (Points)",
    )
    plus_minus = models.IntegerField(
        default=0,
        verbose_name="Plus/Minus",
        help_text="Diferencia de puntos cuando el jugador está en cancha",
    )

    class Meta:
        verbose_name = "Game Boxscore Traditional"
        verbose_name_plural = "Game Boxscore Tradicionals"
        ordering = ["-game_id"]
        indexes = [
            models.Index(fields=["game_id"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["season", "season_type"]),
        ]


class GamePlayByPlay(models.Model):
    # Información del juego
    season = models.CharField(
        max_length=10,
        choices=SeasonChoices.choices(),
        verbose_name="Temporada",
        help_text="Temporada del juego (formato: YYYY-YY, ej: 2015-16)",
    )
    season_type = models.CharField(
        max_length=20,
        choices=SeasonTypeChoices.choices(),
        verbose_name="Tipo de Temporada",
        help_text="Tipo de temporada (pre-season, regular-season, playoffs)",
    )
    game_id = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="ID del Juego",
        help_text="Identificador único del juego",
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        help_text="Abreviación del equipo",
    )
    period = models.CharField(
        max_length=10,
        choices=GamePlayByPlayPeriodChoices.choices(),
        verbose_name="Período",
        help_text="Período del juego (Q1, Q2, Q3, Q4, OT1, All, etc.)",
    )
    min = models.CharField(
        max_length=10,
        verbose_name="Minutos",
        help_text="Tiempo restante en el período (formato MM:SS)",
    )
    score = models.CharField(
        max_length=20,
        verbose_name="Marcador",
        help_text="Marcador del juego en ese momento (formato: X - Y o -)",
    )
    player = models.CharField(
        max_length=100,
        verbose_name="Jugador",
        help_text="Nombre del jugador que realiza la acción",
    )
    action = models.CharField(
        max_length=500,
        verbose_name="Acción",
        help_text="Descripción de la acción realizada en el juego",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora de creación del registro",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización",
        help_text="Fecha y hora de última actualización del registro",
    )

    class Meta:
        verbose_name = "Game Play by Play"
        verbose_name_plural = "Game Play by Plays"
        ordering = ["-game_id", "period", "min"]
        indexes = [
            models.Index(fields=["game_id"]),
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["player"]),
        ]


class GameSummary(models.Model):
    # Información del juego
    season = models.CharField(
        max_length=10,
        choices=SeasonChoices.choices(),
        verbose_name="Temporada",
        help_text="Temporada del juego (formato: YYYY-YY, ej: 2015-16)",
    )
    season_type = models.CharField(
        max_length=20,
        choices=SeasonTypeChoices.choices(),
        verbose_name="Tipo de Temporada",
        help_text="Tipo de temporada (pre-season, regular-season, playoffs)",
    )
    game_id = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="ID del Juego",
        help_text="Identificador único del juego",
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        help_text="Abreviación del equipo",
    )

    # Puntos por período
    q1 = models.IntegerField(
        default=0,
        verbose_name="1er Cuarto",
        help_text="Puntos anotados en el primer cuarto",
    )
    q2 = models.IntegerField(
        default=0,
        verbose_name="2do Cuarto",
        help_text="Puntos anotados en el segundo cuarto",
    )
    q3 = models.IntegerField(
        default=0,
        verbose_name="3er Cuarto",
        help_text="Puntos anotados en el tercer cuarto",
    )
    q4 = models.IntegerField(
        default=0,
        verbose_name="4to Cuarto",
        help_text="Puntos anotados en el cuarto cuarto",
    )
    ot1 = models.IntegerField(
        default=0,
        verbose_name="Tiempo Extra 1",
        help_text="Puntos anotados en el primer tiempo extra",
    )
    ot2 = models.IntegerField(
        default=0,
        verbose_name="Tiempo Extra 2",
        help_text="Puntos anotados en el segundo tiempo extra",
    )
    ot3 = models.IntegerField(
        default=0,
        verbose_name="Tiempo Extra 3",
        help_text="Puntos anotados en el tercer tiempo extra",
    )
    ot4 = models.IntegerField(
        default=0,
        verbose_name="Tiempo Extra 4",
        help_text="Puntos anotados en el cuarto tiempo extra",
    )
    final = models.IntegerField(
        default=0,
        verbose_name="Puntos Finales",
        help_text="Total de puntos anotados en el juego",
    )

    # Estadísticas del equipo
    pitp = models.IntegerField(
        default=0,
        verbose_name="Puntos en la Pintura",
        help_text="Points in the Paint - Puntos anotados en la zona",
    )
    fb_pts = models.IntegerField(
        default=0,
        verbose_name="Puntos de Contraataque",
        help_text="Fast Break Points - Puntos en contraataques",
    )
    big_ld = models.IntegerField(
        default=0,
        verbose_name="Mayor Ventaja",
        help_text="Biggest Lead - Mayor ventaja en puntos durante el juego",
    )
    bpts = models.IntegerField(
        default=0,
        verbose_name="Puntos del Banco",
        help_text="Bench Points - Puntos anotados por jugadores del banco",
    )
    treb = models.IntegerField(
        default=0,
        verbose_name="Rebotes Totales",
        help_text="Total Rebounds - Total de rebotes del equipo",
    )
    tov = models.IntegerField(
        default=0,
        verbose_name="Pérdidas",
        help_text="Turnovers - Pérdidas de balón del equipo",
    )
    ttov = models.IntegerField(
        default=0,
        verbose_name="Pérdidas del Equipo",
        help_text="Team Turnovers - Pérdidas de balón del equipo",
    )
    pot = models.IntegerField(
        default=0,
        verbose_name="Puntos tras Pérdidas",
        help_text="Points off Turnovers - Puntos anotados tras pérdidas",
    )
    lead_changes = models.IntegerField(
        default=0,
        verbose_name="Cambios de Liderazgo",
        help_text="Número de veces que cambió el equipo líder",
    )
    times_tied = models.IntegerField(
        default=0,
        verbose_name="Veces Empatado",
        help_text="Número de veces que el marcador estuvo empatado",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora de creación del registro",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización",
        help_text="Fecha y hora de última actualización del registro",
    )

    class Meta:
        verbose_name = "Game Summary"
        verbose_name_plural = "Game Summaries"
        ordering = ["-game_id", "team_abb"]
        indexes = [
            models.Index(fields=["game_id"]),
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["team_abb"]),
        ]


class TeamBoxscoreTraditional(models.Model):
    # Información del juego
    season = models.CharField(
        max_length=10,
        choices=SeasonChoices.choices(),
        verbose_name="Temporada",
        help_text="Temporada del juego (formato: YYYY-YY, ej: 2015-16)",
    )
    season_type = models.CharField(
        max_length=20,
        choices=SeasonTypeChoices.choices(),
        verbose_name="Tipo de Temporada",
        help_text="Tipo de temporada (pre-season, regular-season, playoffs)",
    )
    team_id = models.IntegerField(
        db_index=True,
        verbose_name="ID del Equipo",
        help_text="Identificador numérico único del equipo",
    )
    team_abb = models.CharField(
        max_length=10,
        choices=TeamChoices.choices(),
        verbose_name="Equipo",
        help_text="Abreviación del equipo",
    )
    game_id = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="ID del Juego",
        help_text="Identificador único del juego",
    )
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        help_text="Descripción del enfrentamiento (ej: ATL@DET, BOSvs.PHI)",
    )
    home_away = models.CharField(
        max_length=10,
        verbose_name="Local/Visitante",
        help_text="Indica si el equipo jugó como local o visitante",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        help_text="Fecha del juego (formato: DD/MM/YYYY)",
    )
    wl = models.CharField(
        max_length=1,
        verbose_name="Resultado",
        help_text="Resultado del juego: W (Win/Victoria) o L (Loss/Derrota)",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos Totales",
        help_text="Minutos totales jugados (240 = juego completo)",
    )

    # Estadísticas de puntos
    pts = models.IntegerField(
        default=0,
        verbose_name="Puntos",
        help_text="Puntos totales anotados por el equipo",
    )

    # Estadísticas de tiros de campo
    fgm = models.IntegerField(
        default=0,
        verbose_name="Tiros de Campo Anotados",
        help_text="Field Goals Made - Tiros de campo anotados",
    )
    fga = models.IntegerField(
        default=0,
        verbose_name="Tiros de Campo Intentados",
        help_text="Field Goals Attempted - Tiros de campo intentados",
    )
    fg_pct = models.FloatField(
        default=0.0,
        verbose_name="% Tiros de Campo",
        help_text="Field Goal Percentage - Porcentaje de tiros de campo",
    )

    # Estadísticas de triples
    fg3m = models.IntegerField(
        default=0,
        verbose_name="Triples Anotados",
        help_text="3 Pointers Made - Triples anotados",
    )
    fg3a = models.IntegerField(
        default=0,
        verbose_name="Triples Intentados",
        help_text="3 Pointers Attempted - Triples intentados",
    )
    fg3_pct = models.FloatField(
        default=0.0,
        verbose_name="% Triples",
        help_text="3 Point Percentage - Porcentaje de triples",
    )

    # Estadísticas de tiros libres
    ftm = models.IntegerField(
        default=0,
        verbose_name="Tiros Libres Anotados",
        help_text="Free Throws Made - Tiros libres anotados",
    )
    fta = models.IntegerField(
        default=0,
        verbose_name="Tiros Libres Intentados",
        help_text="Free Throws Attempted - Tiros libres intentados",
    )
    ft_pct = models.FloatField(
        default=0.0,
        verbose_name="% Tiros Libres",
        help_text="Free Throw Percentage - Porcentaje de tiros libres",
    )

    # Rebotes
    oreb = models.IntegerField(
        default=0,
        verbose_name="Rebotes Ofensivos",
        help_text="Offensive Rebounds - Rebotes ofensivos",
    )
    dreb = models.IntegerField(
        default=0,
        verbose_name="Rebotes Defensivos",
        help_text="Defensive Rebounds - Rebotes defensivos",
    )
    reb = models.IntegerField(
        default=0,
        verbose_name="Rebotes Totales",
        help_text="Total Rebounds - Total de rebotes",
    )

    # Otras estadísticas
    ast = models.IntegerField(
        default=0,
        verbose_name="Asistencias",
        help_text="Assists - Asistencias del equipo",
    )
    stl = models.IntegerField(
        default=0,
        verbose_name="Robos",
        help_text="Steals - Robos de balón del equipo",
    )
    blk = models.IntegerField(
        default=0,
        verbose_name="Tapones",
        help_text="Blocks - Tapones del equipo",
    )
    tov = models.IntegerField(
        default=0,
        verbose_name="Pérdidas",
        help_text="Turnovers - Pérdidas de balón del equipo",
    )
    pf = models.IntegerField(
        default=0,
        verbose_name="Faltas Personales",
        help_text="Personal Fouls - Faltas personales del equipo",
    )
    plus_minus = models.IntegerField(
        default=0,
        verbose_name="Plus/Minus",
        help_text="Diferencia de puntos del equipo en el juego",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora de creación del registro",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización",
        help_text="Fecha y hora de última actualización del registro",
    )

    class Meta:
        verbose_name = "Team Boxscore Traditional"
        verbose_name_plural = "Team Boxscore Tradicionals"
        ordering = ["-game_id", "team_abb"]
        indexes = [
            models.Index(fields=["game_id"]),
            models.Index(fields=["team_id"]),
            models.Index(fields=["team_abb"]),
            models.Index(fields=["season", "season_type"]),
        ]
