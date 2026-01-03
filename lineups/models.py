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
    tov = models.IntegerField(
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
    )
    min = models.IntegerField(
        default=0,
        verbose_name="Minutos",
        null=True,
        blank=True,
    )
    pts_off_tov = models.IntegerField(
        default=0,
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
    opp_pts_off_tov = models.IntegerField(
        default=0,
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
    opp_tov = models.IntegerField(
        default=0,
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
