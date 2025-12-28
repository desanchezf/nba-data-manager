from django.db import models

# Create your models here.

from data.enums import (
    SeasonChoices,
    SeasonTypeChoices,
    GameBoxscorePeriodChoices,
    GamePlayByPlayPeriodChoices,
)
from roster.enums import TeamChoices


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
