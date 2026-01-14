"""
Modelos para estadísticas de jugadores por categoría
"""

from django.db import models
from data.enums import SeasonChoices, SeasonTypeChoices
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


class PlayersGeneralMisc(models.Model):
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
    )  # Estadísticas misceláneas del CSV
    pts_off_tov = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points Off Turnovers",
    )
    pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Second Chance Points",
    )
    pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Fast Break Points",
    )
    pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points in the Paint",
    )
    opp_pts_off_tov = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Points Off Turnovers",
    )
    opp_pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent 2nd Chance Points",
    )
    opp_pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Fast Break Points",
    )
    opp_pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Points in the Paint",
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks",
    )
    blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks Against",
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls",
    )
    pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls Drawn",
    )

    class Meta:
        verbose_name = "Players General Misc"
        verbose_name_plural = "Players General Misc"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersGeneralScoring(models.Model):
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
    pct_fga_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (2 Pointers)",
    )
    pct_fga_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (3 Pointers)",
    )
    pct_pts_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (2 Pointers)",
    )
    pct_pts_2pt_mr = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Mid-Range)",
    )
    pct_pts_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (3 Pointers)",
    )
    pct_pts_fb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Fast Break Points)",
    )
    pct_pts_ft = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Free Throws)",
    )
    pct_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Off Turnovers)",
    )
    pct_pts_paint = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Points in the Paint)",
    )
    pct_ast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Assisted",
    )
    pct_uast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Unassisted",
    )
    pct_ast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Assisted",
    )
    pct_uast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Unassisted",
    )
    pct_ast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Assisted",
    )
    pct_uast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Unassisted",
    )

    class Meta:
        verbose_name = "Players General Scoring"
        verbose_name_plural = "Players General Scoring"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersGeneralUsage(models.Model):
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
    pct_fga_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (2 Pointers)",
    )
    pct_fga_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (3 Pointers)",
    )
    pct_pts_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (2 Pointers)",
    )
    pct_pts_2pt_mr = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Mid-Range)",
    )
    pct_pts_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (3 Pointers)",
    )
    pct_pts_fb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Fast Break Points)",
    )
    pct_pts_ft = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Free Throws)",
    )
    pct_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Off Turnovers)",
    )
    pct_pts_paint = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Points in the Paint)",
    )
    pct_ast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Assisted",
    )
    pct_uast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Unassisted",
    )
    pct_ast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Assisted",
    )
    pct_uast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Unassisted",
    )
    pct_ast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Assisted",
    )
    pct_uast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Unassisted",
    )

    class Meta:
        verbose_name = "Players General Usage"
        verbose_name_plural = "Players General Usage"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersGeneralOpponent(models.Model):
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
    vs_player_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Jugador Oponente",
        null=True,
        blank=True,
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
    opp_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Field Goals Made",
    )
    opp_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Field Goals Attempted",
    )
    opp_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Opponent's Field Goal Percentage",
    )
    opp_fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's 3 Point Field Goals Made",
    )
    opp_fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's 3 Point Field Goals Attempted",
    )
    opp_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Opponent's 3 Point Field Goal Percentage",
    )
    opp_ftm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Free Throws Made",
    )
    opp_fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Free Throws Attempted",
    )
    opp_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Opponent's Free Throw Percentage",
    )
    opp_oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Offensive Rebounds",
    )
    opp_dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Defensive Rebounds",
    )
    opp_reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Rebounds",
    )
    opp_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Assists",
    )
    opp_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Opponent's Turnovers",
    )
    opp_stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Steals",
    )
    opp_blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Blocks",
    )
    opp_blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Blocked Field Goal Attempts",
    )
    opp_pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Personal Fouls",
    )
    opp_pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Personal Fouls Drawn",
    )
    opp_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent's Points",
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players General Opponent"
        verbose_name_plural = "Players General Opponent"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"Player {getattr(self, 'player_id', 'N/A')} - {self.season} ({self.season_type})"


class PlayersGeneralDefense(models.Model):
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
    def_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Defensive Rating",
    )
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rebounds",
    )
    dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Defensive Rebounding Percentage",
    )
    pct_dreb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Defensive Rebounds",
    )
    stl = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Steals",
    )
    pct_stl = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Steals",
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks",
    )
    pct_blk = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Blocks",
    )
    opp_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Opponent Points Off Turnovers",
    )
    opp_pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent 2nd Chance Points",
    )
    opp_pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Fast Break Points",
    )
    opp_pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Points in the Paint",
    )
    def_ws = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players General Defense"
        verbose_name_plural = "Players General Defense"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersGeneralViolations(models.Model):
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
    travel = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Travel",
    )
    double_dribble = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Double Dribble",
    )
    discontinued_dribble = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Discontinued Dribble",
    )
    off_three_sec = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Three Seconds",
    )
    inbound = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Inbound Violation",
    )
    backcourt = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Backcourt Violation",
    )
    off_goaltending = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Goaltending",
    )
    palming = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Palming",
    )
    off_foul = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Foul",
    )
    def_three_sec = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Three Seconds",
    )
    charge = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Charge",
    )
    def_goaltending = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Goaltending",
    )
    lane = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Lane Violation",
    )
    jump_ball = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Jump Ball",
    )
    kicked_ball = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Kicked Ball",
    )

    class Meta:
        verbose_name = "Players General Violations"
        verbose_name_plural = "Players General Violations"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersGeneralEstimatedAdvanced(models.Model):
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
    e_off_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Offensive Rating",
    )
    e_def_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Defensive Rating",
    )
    e_net_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Net Rating",
    )
    e_ast_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Assist Ratio",
    )
    e_oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Offensive Rebound Percentage",
    )
    e_dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Defensive Rebound Percentage",
    )
    e_reb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Rebound Percentage",
    )
    e_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    e_usg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    e_pace = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Pace",
    )

    class Meta:
        verbose_name = "Players General Estimated Advanced"
        verbose_name_plural = "Players General Estimated Advanced"
        unique_together = [["season", "season_type", "player_id"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersClutchTraditional(models.Model):
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
    e_off_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Offensive Rating",
    )
    e_def_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Defensive Rating",
    )
    e_net_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Net Rating",
    )
    e_ast_ratio = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Assist Ratio",
    )
    e_oreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Offensive Rebound Percentage",
    )
    e_dreb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Defensive Rebound Percentage",
    )
    e_reb_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Rebound Percentage",
    )
    e_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    e_usg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    e_pace = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Estimated Pace",
    )

    class Meta:
        verbose_name = "Players Clutch Traditional"
        verbose_name_plural = "Players Clutch Traditional"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersClutchAdvanced(models.Model):
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
        verbose_name = "Players Clutch Advanced"
        verbose_name_plural = "Players Clutch Advanced"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersClutchMisc(models.Model):
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
    pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Off Turnovers",
    )
    pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Second Chance Points",
    )
    pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Fast Break Points",
    )
    pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points in the Paint",
    )
    opp_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Opponent Points Off Turnovers",
    )
    opp_pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent 2nd Chance Points",
    )
    opp_pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Fast Break Points",
    )
    opp_pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Points in the Paint",
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks",
    )
    blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks Against",
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls",
    )
    pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls Drawn",
    )

    class Meta:
        verbose_name = "Players Clutch Misc"
        verbose_name_plural = "Players Clutch Misc"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersClutchScoring(models.Model):
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
    pct_fga_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (2 Pointers)",
    )
    pct_fga_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (3 Pointers)",
    )
    pct_pts_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (2 Pointers)",
    )
    pct_pts_2pt_mr = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Mid-Range)",
    )
    pct_pts_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (3 Pointers)",
    )
    pct_pts_fb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Fast Break Points)",
    )
    pct_pts_ft = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Free Throws)",
    )
    pct_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Off Turnovers)",
    )
    pct_pts_paint = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Points in the Paint)",
    )
    pct_ast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Assisted",
    )
    pct_uast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Unassisted",
    )
    pct_ast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Assisted",
    )
    pct_uast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Unassisted",
    )
    pct_ast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Assisted",
    )
    pct_uast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Unassisted",
    )

    class Meta:
        verbose_name = "Players Clutch Scoring"
        verbose_name_plural = "Players Clutch Scoring"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersClutchUsage(models.Model):
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
    usg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Usage Percentage",
    )
    pct_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Field Goals Made",
    )
    pct_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Field Goals Attempted",
    )
    pct_fg3m = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_fg3a = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Free Throws Made",
    )
    pct_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Free Throws Attempted",
    )
    pct_oreb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Offensive Rebounds",
    )
    pct_dreb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Defensive Rebounds",
    )
    pct_reb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Total Rebounds",
    )
    pct_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Assists",
    )
    pct_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Turnovers",
    )
    pct_stl = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Steals",
    )
    pct_blk = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Blocks",
    )
    pct_blka = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Blocked Field Goal Attempts",
    )
    pct_pf = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Personal Fouls",
    )
    pct_pfd = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Personal Fouls Drawn",
    )
    pct_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Points",
    )

    class Meta:
        verbose_name = "Players Clutch Usage"
        verbose_name_plural = "Players Clutch Usage"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeIsolation(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Isolation"
        verbose_name_plural = "Players Playtype Isolation"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeTransition(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Transition"
        verbose_name_plural = "Players Playtype Transition"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeBallHandler(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Ball Handler"
        verbose_name_plural = "Players Playtype Ball Handler"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeRollMan(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Roll Man"
        verbose_name_plural = "Players Playtype Roll Man"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypePostUp(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Post Up"
        verbose_name_plural = "Players Playtype Post Up"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeSpotUp(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Spot Up"
        verbose_name_plural = "Players Playtype Spot Up"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeHandOff(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Hand Off"
        verbose_name_plural = "Players Playtype Hand Off"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeCut(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Cut"
        verbose_name_plural = "Players Playtype Cut"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeOffScreen(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Off Screen"
        verbose_name_plural = "Players Playtype Off Screen"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypePutbacks(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Putbacks"
        verbose_name_plural = "Players Playtype Putbacks"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersPlaytypeMisc(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Possessions",
    )
    poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Possession Percentage",
    )
    ppp = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Possession",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    ft_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Free Throw Possession Percentage",
    )
    tov_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnover Possession Percentage",
    )
    sf_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Shooting Foul Possession Percentage",
    )
    plusone_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="And One Possession Percentage",
    )
    score_poss_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Score Possession Percentage",
    )
    percentile = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percentile",
    )

    class Meta:
        verbose_name = "Players Playtype Misc"
        verbose_name_plural = "Players Playtype Misc"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingDrives(models.Model):
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
    drives = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drives",
    )
    drive_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Field Goals Made",
    )
    drive_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Field Goals Attempted",
    )
    drive_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Field Goal Percentage",
    )
    drive_ftm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Free Throws Made",
    )
    drive_fta = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Free Throws Attempted",
    )
    drive_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Free Throw Percentage",
    )
    drive_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Points",
    )
    drive_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Points Percentage",
    )
    drive_passes = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Passes",
    )
    drive_passes_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Passes Percentage",
    )
    drive_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Assists",
    )
    drive_ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Assists Percentage",
    )
    drive_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Turnovers",
    )
    drive_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Turnovers Percentage",
    )
    drive_pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Personal Fouls",
    )
    drive_pf_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Personal Fouls Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Drives"
        verbose_name_plural = "Players Tracking Drives"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingDefensiveImpact(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutes Played",
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
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rebounds",
    )
    def_rim_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rim Field Goals Made",
    )
    def_rim_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rim Field Goals Attempted",
    )
    def_rim_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Defensive Rim Field Goal Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Defensive Impact"
        verbose_name_plural = "Players Tracking Defensive Impact"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingCatchShoot(models.Model):
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
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutes Played",
    )
    catch_shoot_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Catch and Shoot Points",
    )
    catch_shoot_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Catch and Shoot Field Goals Made",
    )
    catch_shoot_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Catch and Shoot Field Goals Attempted",
    )
    catch_shoot_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Catch and Shoot Field Goal Percentage",
    )
    catch_shoot_fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Catch and Shoot 3 Point Field Goals Made",
    )
    catch_shoot_fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Catch and Shoot 3 Point Field Goals Attempted",
    )
    catch_shoot_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Catch and Shoot 3 Point Field Goal Percentage",
    )
    catch_shoot_efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Catch and Shoot Effective Field Goal Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Catch Shoot"
        verbose_name_plural = "Players Tracking Catch Shoot"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingPassing(models.Model):
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
    passes_made = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Passes Made",
    )
    passes_received = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Passes Received",
    )
    ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Assists",
    )
    secondary_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Secondary Assists",
    )
    potential_ast = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Potential Assists",
    )
    ast_pts_created = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    ast_points_created = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Assist Points Created",
    )
    ast_adj = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Adjusted Assists",
    )
    ast_to_pass_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Assist to Pass Percentage",
    )
    ast_to_pass_pct_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Adjusted Assist to Pass Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Passing"
        verbose_name_plural = "Players Tracking Passing"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingTouches(models.Model):
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
    points = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points",
    )
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Touches",
    )
    front_ct_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Front Court Touches",
    )
    time_of_poss = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Time of Possession",
    )
    avg_sec_per_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Average Seconds Per Touch",
    )
    avg_drib_per_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Average Dribbles Per Touch",
    )
    pts_per_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Touch",
    )
    elbow_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touches",
    )
    post_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touches",
    )
    paint_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touches",
    )
    pts_per_elbow_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Elbow Touch",
    )
    pts_per_post_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Post Touch",
    )
    pts_per_paint_touch = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Per Paint Touch",
    )

    class Meta:
        verbose_name = "Players Tracking Touches"
        verbose_name_plural = "Players Tracking Touches"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingPullup(models.Model):
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
    pull_up_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pull Up Points",
    )
    pull_up_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pull Up Field Goals Made",
    )
    pull_up_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pull Up Field Goals Attempted",
    )
    pull_up_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Pull Up Field Goal Percentage",
    )
    pull_up_fg3m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pull Up 3 Point Field Goals Made",
    )
    pull_up_fg3a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pull Up 3 Point Field Goals Attempted",
    )
    pull_up_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Pull Up 3 Point Field Goal Percentage",
    )
    pull_up_efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Pull Up Effective Field Goal Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Pullup"
        verbose_name_plural = "Players Tracking Pullup"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingRebounding(models.Model):
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
    reb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebounds",
    )
    reb_contest = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebounds Contested",
    )
    reb_contest_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Contested Rebound Percentage",
    )
    reb_chances = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebound Chances",
    )
    reb_chance_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Rebound Chance Percentage",
    )
    reb_chance_defer = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Rebound Chances Deferred",
    )
    reb_chance_pct_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Adjusted Rebound Chance Percentage",
    )
    avg_reb_dist = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players Tracking Rebounding"
        verbose_name_plural = "Players Tracking Rebounding"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingOffensiveRebounding(models.Model):
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
    oreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Rebounds",
    )
    oreb_contest = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Rebounds Contested",
    )
    oreb_contest_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Contested Offensive Rebound Percentage",
    )
    oreb_chances = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Rebound Chances",
    )
    oreb_chance_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Offensive Rebound Chance Percentage",
    )
    oreb_chance_defer = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Rebound Chances Deferred",
    )
    oreb_chance_pct_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Adjusted Offensive Rebound Chance Percentage",
    )
    avg_oreb_dist = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players Tracking Offensive Rebounding"
        verbose_name_plural = "Players Tracking Offensive Rebounding"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingDefensiveRebounding(models.Model):
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
    dreb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rebounds",
    )
    dreb_contest = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rebounds Contested",
    )
    dreb_contest_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Contested Defensive Rebound Percentage",
    )
    dreb_chances = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rebound Chances",
    )
    dreb_chance_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Defensive Rebound Chance Percentage",
    )
    dreb_chance_defer = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Rebound Chances Deferred",
    )
    dreb_chance_pct_adj = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Adjusted Defensive Rebound Chance Percentage",
    )
    avg_dreb_dist = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players Tracking Defensive Rebounding"
        verbose_name_plural = "Players Tracking Defensive Rebounding"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingShootingEfficiency(models.Model):
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
    points = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points",
    )
    drive_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Drive Points",
    )
    drive_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Drive Field Goal Percentage",
    )
    catch_shoot_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Catch and Shoot Points",
    )
    catch_shoot_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Catch and Shoot Field Goal Percentage",
    )
    pull_up_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Pull Up Points",
    )
    pull_up_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Pull Up Field Goal Percentage",
    )
    paint_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Points",
    )
    paint_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Field Goal Percentage",
    )
    post_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Points",
    )
    post_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Field Goal Percentage",
    )
    elbow_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Points",
    )
    elbow_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Field Goal Percentage",
    )
    eff_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Shooting Efficiency"
        verbose_name_plural = "Players Tracking Shooting Efficiency"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingSpeedDistance(models.Model):
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
    dist_feet = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Distance Feet",
    )
    dist_miles = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Distance Miles",
    )
    dist_miles_off = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Distance Miles Offense",
    )
    dist_miles_def = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Distance Miles Defense",
    )
    avg_speed = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Average Speed",
    )
    avg_speed_off = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Average Speed Offense",
    )
    avg_speed_def = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Average Speed Defense",
    )

    class Meta:
        verbose_name = "Players Tracking Speed Distance"
        verbose_name_plural = "Players Tracking Speed Distance"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingElbowTouch(models.Model):
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
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Touches",
    )
    elbow_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touches",
    )
    elbow_touch_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Field Goals Made",
    )
    elbow_touch_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Field Goals Attempted",
    )
    elbow_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Field Goal Percentage",
    )
    elbow_touch_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Free Throws Made",
    )
    elbow_touch_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Free Throws Attempted",
    )
    elbow_touch_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Free Throw Percentage",
    )
    elbow_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Points",
    )
    elbow_touch_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Points Percentage",
    )
    elbow_touch_passes = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Passes",
    )
    elbow_touch_passes_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Passes Percentage",
    )
    elbow_touch_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Assists",
    )
    elbow_touch_ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Percent of Team's Assists",
    )
    elbow_touch_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Turnovers",
    )
    elbow_touch_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Percent of Team's Turnovers",
    )
    elbow_touch_fouls = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Fouls",
    )
    elbow_touch_fouls_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Elbow Touch Fouls Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Elbow Touch"
        verbose_name_plural = "Players Tracking Elbow Touch"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingPostUps(models.Model):
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
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Touches",
    )
    post_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touches",
    )
    post_touch_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Field Goals Made",
    )
    post_touch_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Field Goals Attempted",
    )
    post_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Field Goal Percentage",
    )
    post_touch_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Free Throws Made",
    )
    post_touch_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Free Throws Attempted",
    )
    post_touch_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Free Throw Percentage",
    )
    post_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Points",
    )
    post_touch_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Points Percentage",
    )
    post_touch_passes = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Passes",
    )
    post_touch_passes_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Passes Percentage",
    )
    post_touch_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Assists",
    )
    post_touch_ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Percent of Team's Assists",
    )
    post_touch_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Turnovers",
    )
    post_touch_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Percent of Team's Turnovers",
    )
    post_touch_fouls = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Fouls",
    )
    post_touch_fouls_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Post Touch Fouls Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Post Ups"
        verbose_name_plural = "Players Tracking Post Ups"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersTrackingPaintTouch(models.Model):
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
    touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Touches",
    )
    paint_touches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touches",
    )
    paint_touch_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Field Goals Made",
    )
    paint_touch_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Field Goals Attempted",
    )
    paint_touch_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Field Goal Percentage",
    )
    paint_touch_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Free Throws Made",
    )
    paint_touch_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Free Throws Attempted",
    )
    paint_touch_ft_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Free Throw Percentage",
    )
    paint_touch_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Points",
    )
    paint_touch_pts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Points Percentage",
    )
    paint_touch_passes = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Passes",
    )
    paint_touch_passes_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Passes Percentage",
    )
    paint_touch_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Assists",
    )
    paint_touch_ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Percent of Team's Assists",
    )
    paint_touch_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Turnovers",
    )
    paint_touch_tov_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Percent of Team's Turnovers",
    )
    paint_touch_fouls = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Fouls",
    )
    paint_touch_fouls_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Paint Touch Fouls Percentage",
    )

    class Meta:
        verbose_name = "Players Tracking Paint Touch"
        verbose_name_plural = "Players Tracking Paint Touch"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersDefenseDashboardOverall(models.Model):
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
    player_position = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Posición",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    freq = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Frequency",
    )
    d_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defended Field Goals Made",
    )
    d_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defended Field Goals Attempted",
    )
    d_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Defended Field Goal Percentage",
    )
    normal_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Normal Field Goal Percentage",
    )
    pct_plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players Defense Dashboard Overall"
        verbose_name_plural = "Players Defense Dashboard Overall"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersDefenseDashboard3pt(models.Model):
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
    player_position = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Posición",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    freq = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Frequency",
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
    ns_fg3_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="No Screen 3 Point Field Goal Percentage",
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players Defense Dashboard 3Pt"
        verbose_name_plural = "Players Defense Dashboard 3Pt"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersDefenseDashboard2pt(models.Model):
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
    player_position = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Posición",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    freq = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Frequency",
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Made",
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Attempted",
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Percentage",
    )
    ns_fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="No Screen 2 Point Field Goal Percentage",
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players Defense Dashboard 2Pt"
        verbose_name_plural = "Players Defense Dashboard 2Pt"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersDefenseDashboardLt6(models.Model):
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
    player_position = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Posición",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    freq = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Frequency",
    )
    fgm_lt_06 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Less Than 0.6 ft. Field Goals Made",
    )
    fga_lt_06 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Less Than 0.6 ft. Field Goals Attempted",
    )
    lt_06_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Less Than 0.6 ft. Field Goal Percentage",
    )
    ns_lt_06_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="No Screen Less Than 0.6 ft. Field Goal Percentage",
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players Defense Dashboard Lt6"
        verbose_name_plural = "Players Defense Dashboard Lt6"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersDefenseDashboardLt10(models.Model):
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
    player_position = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Posición",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    freq = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Frequency",
    )
    fgm_lt_10 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Less Than 10 ft. Field Goals Made",
    )
    fga_lt_10 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Less Than 10 ft. Field Goals Attempted",
    )
    lt_10_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Less Than 10 ft. Field Goal Percentage",
    )
    ns_lt_10_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="No Screen Less Than 10 ft. Field Goal Percentage",
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players Defense Dashboard Lt10"
        verbose_name_plural = "Players Defense Dashboard Lt10"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersDefenseDashboardGt15(models.Model):
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
    player_position = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Posición",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    freq = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Frequency",
    )
    fgm_gt_15 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Greater Than 15 ft. Field Goals Made",
    )
    fga_gt_15 = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Greater Than 15 ft. Field Goals Attempted",
    )
    gt_15_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Greater Than 15 ft. Field Goal Percentage",
    )
    ns_gt_15_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="No Screen Greater Than 15 ft. Field Goal Percentage",
    )
    plusminus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players Defense Dashboard Gt15"
        verbose_name_plural = "Players Defense Dashboard Gt15"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersShotDashboardGeneral(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Attempt Frequency",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Attempt Frequency",
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Made",
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Attempted",
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Percentage",
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="3 Point Field Goal Attempt Frequency",
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

    class Meta:
        verbose_name = "Players Shot Dashboard General"
        verbose_name_plural = "Players Shot Dashboard General"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersShotDashboardShotClock(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Attempt Frequency",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Attempt Frequency",
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Made",
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Attempted",
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Percentage",
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="3 Point Field Goal Attempt Frequency",
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

    class Meta:
        verbose_name = "Players Shot Dashboard Shot Clock"
        verbose_name_plural = "Players Shot Dashboard Shot Clock"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersShotDashboardDribbles(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Attempt Frequency",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Attempt Frequency",
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Made",
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Attempted",
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Percentage",
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="3 Point Field Goal Attempt Frequency",
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

    class Meta:
        verbose_name = "Players Shot Dashboard Dribbles"
        verbose_name_plural = "Players Shot Dashboard Dribbles"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersShotDashboardTouchTime(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Attempt Frequency",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Attempt Frequency",
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Made",
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Attempted",
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Percentage",
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="3 Point Field Goal Attempt Frequency",
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

    class Meta:
        verbose_name = "Players Shot Dashboard Touch Time"
        verbose_name_plural = "Players Shot Dashboard Touch Time"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersShotDashboardClosestDefender(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Attempt Frequency",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Attempt Frequency",
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Made",
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Attempted",
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Percentage",
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="3 Point Field Goal Attempt Frequency",
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

    class Meta:
        verbose_name = "Players Shot Dashboard Closest Defender"
        verbose_name_plural = "Players Shot Dashboard Closest Defender"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersShotDashboardClosestDefender10(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    fga_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Field Goal Attempt Frequency",
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
    efg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Effective Field Goal Percentage",
    )
    fg2a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Attempt Frequency",
    )
    fg2m = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Made",
    )
    fg2a = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="2 Point Field Goals Attempted",
    )
    fg2_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="2 Point Field Goal Percentage",
    )
    fg3a_frequency = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="3 Point Field Goal Attempt Frequency",
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

    class Meta:
        verbose_name = "Players Shot Dashboard Closest Defender 10"
        verbose_name_plural = "Players Shot Dashboard Closest Defender 10"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersBoxScores(models.Model):
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
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
        help_text="Matchup",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
        help_text="Game Date",
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
    tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnovers",
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls",
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )
    fantasy_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players Box Scores"
        verbose_name_plural = "Players Box Scores"
        unique_together = [
            ["season", "season_type", "player_id", "team_abb", "matchup", "gdate"]
        ]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersAdvancedBoxScoresTraditional(models.Model):
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
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
        help_text="Matchup",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
        help_text="Game Date",
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
    fgperc = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
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
    ftmperc = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
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
    tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Turnovers",
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls",
    )
    plus_minus = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Plus-Minus",
    )

    class Meta:
        verbose_name = "Players Advanced Box Scores Traditional"
        verbose_name_plural = "Players Advanced Box Scores Traditional"
        unique_together = [
            ["season", "season_type", "player_id", "team_abb", "matchup", "gdate"]
        ]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersAdvancedBoxScoresAdvanced(models.Model):
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
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
        help_text="Matchup",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
        help_text="Game Date",
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

    class Meta:
        verbose_name = "Players Advanced Box Scores Advanced"
        verbose_name_plural = "Players Advanced Box Scores Advanced"
        unique_together = [
            ["season", "season_type", "player_id", "team_abb", "matchup", "gdate"]
        ]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersAdvancedBoxScoresMisc(models.Model):
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
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
        help_text="Matchup",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
        help_text="Game Date",
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
        help_text="Minutes Played",
    )
    pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Points Off Turnovers",
    )
    pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Second Chance Points",
    )
    pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Fast Break Points",
    )
    pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points in the Paint",
    )
    opp_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Opponent Points Off Turnovers",
    )
    opp_pts_2nd_chance = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent 2nd Chance Points",
    )
    opp_pts_fb = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Fast Break Points",
    )
    opp_pts_paint = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Opponent Points in the Paint",
    )
    blk = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks",
    )
    blka = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Blocks Against",
    )
    pf = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls",
    )
    pfd = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Personal Fouls Drawn",
    )

    class Meta:
        verbose_name = "Players Advanced Box Scores Misc"
        verbose_name_plural = "Players Advanced Box Scores Misc"
        unique_together = [
            ["season", "season_type", "player_id", "team_abb", "matchup", "gdate"]
        ]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersAdvancedBoxScoresScoring(models.Model):
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
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
        help_text="Matchup",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
        help_text="Game Date",
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
        help_text="Minutes Played",
    )
    pct_fga_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (2 Pointers)",
    )
    pct_fga_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Attempted (3 Pointers)",
    )
    pct_pts_2pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (2 Pointers)",
    )
    pct_pts_2pt_mr = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Mid-Range)",
    )
    pct_pts_3pt = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (3 Pointers)",
    )
    pct_pts_fb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Fast Break Points)",
    )
    pct_pts_ft = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Free Throws)",
    )
    pct_pts_off_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Off Turnovers)",
    )
    pct_pts_paint = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Points (Points in the Paint)",
    )
    pct_ast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Assisted",
    )
    pct_uast_2pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 2 Point Field Goals Made Unassisted",
    )
    pct_ast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Assisted",
    )
    pct_uast_3pm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of 3 Point Field Goals Made Unassisted",
    )
    pct_ast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Assisted",
    )
    pct_uast_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Field Goals Made Unassisted",
    )

    class Meta:
        verbose_name = "Players Advanced Box Scores Scoring"
        verbose_name_plural = "Players Advanced Box Scores Scoring"
        unique_together = [
            ["season", "season_type", "player_id", "team_abb", "matchup", "gdate"]
        ]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersAdvancedBoxScoresUsage(models.Model):
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
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
        help_text="Matchup",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
        help_text="Game Date",
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
        help_text="Minutes Played",
    )
    usg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Usage Percentage",
    )
    pct_fgm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Field Goals Made",
    )
    pct_fga = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Field Goals Attempted",
    )
    pct_fg3m = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_fg3a = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_ftm = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Free Throws Made",
    )
    pct_fta = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Free Throws Attempted",
    )
    pct_oreb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Offensive Rebounds",
    )
    pct_dreb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Defensive Rebounds",
    )
    pct_reb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Total Rebounds",
    )
    pct_ast = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Assists",
    )
    pct_tov = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Turnovers",
    )
    pct_stl = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Steals",
    )
    pct_blk = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Blocks",
    )
    pct_blka = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Blocked Field Goal Attempts",
    )
    pct_pf = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Personal Fouls",
    )
    pct_pfd = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Personal Fouls Drawn",
    )
    pct_pts = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Team's Points",
    )

    class Meta:
        verbose_name = "Players Advanced Box Scores Usage"
        verbose_name_plural = "Players Advanced Box Scores Usage"
        unique_together = [
            ["season", "season_type", "player_id", "team_abb", "matchup", "gdate"]
        ]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersShooting(models.Model):
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
    ft_less_than_5_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="less_than_5_ft__fgm",
    )
    ft_less_than_5_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="less_than_5_ft__fga",
    )
    ft_less_than_5_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="less_than_5_ft__fg_pct",
    )
    ft_5_9_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="5_9_ft__fgm",
    )
    ft_5_9_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="5_9_ft__fga",
    )
    ft_5_9_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="5_9_ft__fg_pct",
    )
    ft_10_14_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="10_14_ft__fgm",
    )
    ft_10_14_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="10_14_ft__fga",
    )
    ft_10_14_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="10_14_ft__fg_pct",
    )
    ft_15_19_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="15_19_ft__fgm",
    )
    ft_15_19_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="15_19_ft__fga",
    )
    ft_15_19_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="15_19_ft__fg_pct",
    )
    ft_20_24_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="20_24_ft__fgm",
    )
    ft_20_24_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="20_24_ft__fga",
    )
    ft_20_24_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="20_24_ft__fg_pct",
    )
    ft_25_29_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="25_29_ft__fgm",
    )
    ft_25_29_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="25_29_ft__fga",
    )
    ft_25_29_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="25_29_ft__fg_pct",
    )

    class Meta:
        verbose_name = "Players Shooting"
        verbose_name_plural = "Players Shooting"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersDunkScores(models.Model):
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
    playername = models.CharField(
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
    matchup = models.CharField(
        max_length=50,
        verbose_name="Enfrentamiento",
        null=True,
        blank=True,
        help_text="Matchup",
    )
    gdate = models.CharField(
        max_length=20,
        verbose_name="Fecha del Juego",
        null=True,
        blank=True,
        help_text="Game Date",
    )
    dunkscore = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Dunk Score",
    )
    jumpsubscore = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    powersubscore = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    stylesubscore = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    defensivecontestsubscore = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    playervertical = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    hangtime = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    takeoffdistance = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    dunkinghand = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    maxballheight = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ballspeedthroughrim = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    ballreachback = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    tipintext = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    alleyooptext = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players Dunk Scores"
        verbose_name_plural = "Players Dunk Scores"
        unique_together = [
            ["season", "season_type", "player_id", "team_abb", "matchup", "gdate"]
        ]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersOpponentShootingOverall(models.Model):
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
    ft_less_than_5_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="less_than_5_ft__fgm",
    )
    ft_less_than_5_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="less_than_5_ft__fga",
    )
    ft_less_than_5_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="less_than_5_ft__fg_pct",
    )
    ft_5_9_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="5_9_ft__fgm",
    )
    ft_5_9_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="5_9_ft__fga",
    )
    ft_5_9_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="5_9_ft__fg_pct",
    )
    ft_10_14_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="10_14_ft__fgm",
    )
    ft_10_14_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="10_14_ft__fga",
    )
    ft_10_14_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="10_14_ft__fg_pct",
    )
    ft_15_19_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="15_19_ft__fgm",
    )
    ft_15_19_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="15_19_ft__fga",
    )
    ft_15_19_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="15_19_ft__fg_pct",
    )
    ft_20_24_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="20_24_ft__fgm",
    )
    ft_20_24_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="20_24_ft__fga",
    )
    ft_20_24_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="20_24_ft__fg_pct",
    )
    ft_25_29_fgm = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="25_29_ft__fgm",
    )
    ft_25_29_fga = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        db_column="25_29_ft__fga",
    )
    ft_25_29_fg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        db_column="25_29_ft__fg_pct",
    )

    class Meta:
        verbose_name = "Players Opponent Shooting Overall"
        verbose_name_plural = "Players Opponent Shooting Overall"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersHustle(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutes Played",
    )
    screen_assists = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Screen Assists",
    )
    screen_ast_pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Screen Assist Points",
    )
    deflections = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Deflections",
    )
    off_loose_balls_recovered = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Loose Balls Recovered",
    )
    def_loose_balls_recovered = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Loose Balls Recovered",
    )
    loose_balls_recovered = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Total Loose Balls Recovered",
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
        help_text="Charges Drawn",
    )
    contested_shots_2pt = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Contested Shots (2 Point)",
    )
    contested_shots_3pt = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Contested Shots (3 Point)",
    )
    contested_shots = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Total Contested Shots",
    )

    class Meta:
        verbose_name = "Players Hustle"
        verbose_name_plural = "Players Hustle"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersBoxOuts(models.Model):
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
    g = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games",
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
        help_text="Minutes Played",
    )
    box_outs = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Box Outs",
    )
    off_boxouts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Offensive Box Outs",
    )
    def_boxouts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Defensive Box Outs",
    )
    box_out_player_team_rebs = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    box_out_player_rebs = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    pct_box_outs_off = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Box Outs (Offensive)",
    )
    pct_box_outs_def = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Percent of Box Outs (Defensive)",
    )
    pct_box_outs_team_reb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    pct_box_outs_reb = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Players Box Outs"
        verbose_name_plural = "Players Box Outs"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"


class PlayersBios(models.Model):
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
    player_height_inches = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    player_weight = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
    )
    college = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="College",
    )
    country = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Country",
    )
    draft_year = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Draft Year",
    )
    draft_round = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Draft Round",
    )
    draft_number = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Draft Number",
    )
    gp = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Games Played",
    )
    pts = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Points",
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
    net_rating = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Net Rating",
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
    usg_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Usage Percentage",
    )
    ts_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="True Shooting Percentage",
    )
    ast_pct = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        help_text="Assist Percentage",
    )

    class Meta:
        verbose_name = "Players Bios"
        verbose_name_plural = "Players Bios"
        unique_together = [["season", "season_type", "player_id", "team_abb"]]
        indexes = [
            models.Index(fields=["season", "season_type"]),
            models.Index(fields=["player_id"]),
            models.Index(fields=["team_abb"]),
        ]

    def __str__(self):
        return f"{getattr(self, 'player_name', getattr(self, 'playername', 'N/A'))} - {self.season} ({self.season_type})"
