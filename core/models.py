"""
Modelos normalizados NBA: estructura unificada con ForeignKey a Game, Team y Player.
Los datos crudos siguen en game, game_boxscore, teams, players (copias de los CSV).
Aquí se almacenan datos derivados con unidades normalizadas e índices para consultas.
"""

from django.db import models


class Team(models.Model):
    """Equipo NBA. Creado/actualizado al sincronizar desde datos crudos."""

    team_id = models.CharField("ID del equipo", max_length=20, primary_key=True)
    name = models.CharField("Nombre (opcional)", max_length=80, blank=True)
    abbreviation = models.CharField("Abreviatura", max_length=10, blank=True)
    conference = models.CharField("Conferencia", max_length=10, blank=True)
    division = models.CharField("División", max_length=30, blank=True)

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ["name"]

    def __str__(self):
        return self.name or self.team_id


class Player(models.Model):
    """Jugador NBA. Creado/actualizado al sincronizar desde datos crudos."""

    player_id = models.CharField("ID del jugador", max_length=40, primary_key=True)
    name = models.CharField("Nombre (opcional)", max_length=120, blank=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
    )

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
        ordering = ["name"]

    def __str__(self):
        return self.name or self.player_id


class Game(models.Model):
    """
    Partido único NBA. Nodo central para joins.
    Índices: (season, date), (season, season_type).
    """

    game_id = models.CharField("ID del partido", max_length=64, primary_key=True)
    league = models.CharField("Liga", max_length=20, default="NBA", db_index=True)
    season = models.CharField("Temporada", max_length=10, blank=True, db_index=True)
    season_type = models.CharField("Tipo de temporada", max_length=20, blank=True, db_index=True)
    date = models.DateField("Fecha del partido", null=True, blank=True, db_index=True)
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_games",
        null=True,
        blank=True,
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_games",
        null=True,
        blank=True,
    )
    home_score = models.IntegerField("Puntos local", null=True, blank=True)
    away_score = models.IntegerField("Puntos visitante", null=True, blank=True)
    n_result = models.CharField("Resultado (ej. 110-98)", max_length=40, blank=True)

    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
        ordering = ["-date", "game_id"]
        indexes = [
            models.Index(fields=["season", "date"]),
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["league", "season", "date"]),
        ]

    def __str__(self):
        return f"{self.game_id} {self.n_result or '-'}"


class GamePlayerLine(models.Model):
    """
    Estadísticas de un jugador en un partido (boxscore por jugador).
    Cubre tanto estadísticas tradicionales como avanzadas.
    """

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="player_lines",
        db_index=True,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        related_name="game_lines",
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="game_player_lines",
        null=True,
        blank=True,
    )
    home_away = models.CharField("Home/Away", max_length=10, blank=True)
    position = models.CharField("Posición", max_length=20, blank=True)
    period = models.CharField("Período (ALL/Q1/Q2/…)", max_length=10, default="ALL", blank=True)

    # Tiempo en pista
    min_played = models.FloatField("Minutos jugados", null=True, blank=True)

    # Tiros de campo
    fgm = models.IntegerField("Tiros de campo anotados", default=0)
    fga = models.IntegerField("Tiros de campo intentados", default=0)
    fg_pct = models.FloatField("% Tiros de campo", null=True, blank=True)

    # Triples
    fg3m = models.IntegerField("Triples anotados", default=0)
    fg3a = models.IntegerField("Triples intentados", default=0)
    fg3_pct = models.FloatField("% Triples", null=True, blank=True)

    # Tiros libres
    ftm = models.IntegerField("Tiros libres anotados", default=0)
    fta = models.IntegerField("Tiros libres intentados", default=0)
    ft_pct = models.FloatField("% Tiros libres", null=True, blank=True)

    # Rebotes
    oreb = models.IntegerField("Rebotes ofensivos", default=0)
    dreb = models.IntegerField("Rebotes defensivos", default=0)
    reb = models.IntegerField("Rebotes totales", default=0)

    # Otras stats
    ast = models.IntegerField("Asistencias", default=0)
    stl = models.IntegerField("Robos", default=0)
    blk = models.IntegerField("Tapones", default=0)
    tov = models.IntegerField("Pérdidas", default=0)
    pf = models.IntegerField("Faltas personales", default=0)
    pts = models.IntegerField("Puntos", default=0)
    plus_minus = models.IntegerField("±", null=True, blank=True)

    # Métricas avanzadas (opcionales)
    off_rating = models.FloatField("Rating ofensivo", null=True, blank=True)
    def_rating = models.FloatField("Rating defensivo", null=True, blank=True)
    net_rating = models.FloatField("Net rating", null=True, blank=True)
    ast_pct = models.FloatField("% Asistencias", null=True, blank=True)
    ast_to = models.FloatField("AST/TO ratio", null=True, blank=True)
    ast_ratio = models.FloatField("AST ratio", null=True, blank=True)
    oreb_pct = models.FloatField("% Rebotes ofensivos", null=True, blank=True)
    dreb_pct = models.FloatField("% Rebotes defensivos", null=True, blank=True)
    reb_pct = models.FloatField("% Rebotes totales", null=True, blank=True)
    to_ratio = models.FloatField("TO ratio", null=True, blank=True)
    efg_pct = models.FloatField("eFG%", null=True, blank=True)
    ts_pct = models.FloatField("TS%", null=True, blank=True)
    usg_pct = models.FloatField("USG%", null=True, blank=True)
    pace = models.FloatField("Pace", null=True, blank=True)
    pie = models.FloatField("PIE", null=True, blank=True)

    class Meta:
        verbose_name = "Estadísticas jugador-partido"
        verbose_name_plural = "Estadísticas jugadores-partidos"
        ordering = ["game", "-pts"]
        indexes = [
            models.Index(fields=["game"]),
            models.Index(fields=["player", "game"]),
            models.Index(fields=["team", "game"]),
        ]

    def __str__(self):
        return (
            f"{self.game_id} {getattr(self.player, 'name', '?')} "
            f"({self.pts}pts)"
        )


class GameTeamLine(models.Model):
    """
    Estadísticas de un equipo en un partido (totales del equipo).
    """

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="team_lines",
        db_index=True,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="game_team_lines",
    )
    home_away = models.CharField("Home/Away", max_length=10, blank=True)
    period = models.CharField("Período (ALL/Q1/Q2/…)", max_length=10, default="ALL", blank=True)

    # Totales del equipo
    fgm = models.IntegerField("FGM", default=0)
    fga = models.IntegerField("FGA", default=0)
    fg_pct = models.FloatField("FG%", null=True, blank=True)
    fg3m = models.IntegerField("3PM", default=0)
    fg3a = models.IntegerField("3PA", default=0)
    fg3_pct = models.FloatField("3P%", null=True, blank=True)
    ftm = models.IntegerField("FTM", default=0)
    fta = models.IntegerField("FTA", default=0)
    ft_pct = models.FloatField("FT%", null=True, blank=True)
    oreb = models.IntegerField("OREB", default=0)
    dreb = models.IntegerField("DREB", default=0)
    reb = models.IntegerField("REB", default=0)
    ast = models.IntegerField("AST", default=0)
    stl = models.IntegerField("STL", default=0)
    blk = models.IntegerField("BLK", default=0)
    tov = models.IntegerField("TOV", default=0)
    pf = models.IntegerField("PF", default=0)
    pts = models.IntegerField("PTS", default=0)

    class Meta:
        verbose_name = "Estadísticas equipo-partido"
        verbose_name_plural = "Estadísticas equipos-partidos"
        ordering = ["game", "team"]
        unique_together = [["game", "team", "period"]]
        indexes = [models.Index(fields=["game"]), models.Index(fields=["team"])]

    def __str__(self):
        return (
            f"{self.game_id} {getattr(self.team, 'name', '?')} "
            f"({self.pts}pts)"
        )


class WinProbabilitySnapshot(models.Model):
    """Snapshot de probabilidad de victoria en un momento del partido."""

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="win_probability_snapshots",
        db_index=True,
    )
    period = models.IntegerField("Período", null=True, blank=True)
    time_remaining = models.CharField("Tiempo restante", max_length=20, blank=True)
    home_score = models.IntegerField("Score local", null=True, blank=True)
    away_score = models.IntegerField("Score visitante", null=True, blank=True)
    win_pct = models.FloatField("Win % (local)", null=True, blank=True)

    class Meta:
        verbose_name = "Win probability snapshot"
        verbose_name_plural = "Win probability snapshots"
        ordering = ["game", "period"]
        indexes = [models.Index(fields=["game"])]

    def __str__(self):
        return f"{self.game_id} Q{self.period} {self.win_pct}%"


class GameMetadata(models.Model):
    """
    Metadatos enriquecidos por partido (starters, árbitros, arena, etc.).
    """

    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE,
        related_name="metadata",
        primary_key=True,
    )
    starters_json = models.JSONField(
        "Starters [{player_id, name, team, position}]",
        default=dict,
        blank=True,
    )
    arena = models.CharField("Arena", max_length=100, blank=True)
    attendance = models.IntegerField("Asistencia", null=True, blank=True)
    scraped_at = models.DateTimeField("Última actualización", null=True, blank=True)

    class Meta:
        verbose_name = "Metadatos de partido"
        verbose_name_plural = "Metadatos de partidos"

    def __str__(self):
        return f"{self.pk} (scraped: {self.scraped_at})"
