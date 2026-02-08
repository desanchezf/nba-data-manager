# Generated manually for game_boxscore

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GameBoxscoreTraditional",
            fields=[
                ("id", models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name="ID"
                )),
                ("game_id", models.CharField(
                    db_index=True, max_length=20,
                    verbose_name="ID del Juego"
                )),
                ("season", models.CharField(
                    db_index=True, max_length=10,
                    verbose_name="Temporada"
                )),
                ("season_type", models.CharField(
                    db_index=True, max_length=20,
                    verbose_name="Tipo de Temporada"
                )),
                ("home_team_abb", models.CharField(
                    max_length=10, verbose_name="Equipo Local"
                )),
                ("away_team_abb", models.CharField(
                    max_length=10, verbose_name="Equipo Visitante"
                )),
                ("player_id", models.IntegerField(
                    db_index=True, verbose_name="ID del Jugador"
                )),
                ("player_name", models.CharField(
                    max_length=100, verbose_name="Nombre del Jugador"
                )),
                ("player_name_abb", models.CharField(
                    max_length=50, verbose_name="Nombre Abreviado"
                )),
                ("player_team_abb", models.CharField(
                    max_length=10, verbose_name="Equipo del Jugador"
                )),
                ("player_pos", models.CharField(
                    max_length=5, verbose_name="Posición"
                )),
                ("player_dnp", models.BooleanField(
                    default=False, verbose_name="No Jugó (DNP)"
                )),
                ("period", models.CharField(
                    max_length=10, verbose_name="Período"
                )),
                ("min", models.CharField(
                    max_length=10, verbose_name="Minutos"
                )),
                ("fgm", models.IntegerField(default=0)),
                ("fga", models.IntegerField(default=0)),
                ("fg_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("fg3m", models.IntegerField(default=0)),
                ("fg3a", models.IntegerField(default=0)),
                ("fg3_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("ftm", models.IntegerField(default=0)),
                ("fta", models.IntegerField(default=0)),
                ("ft_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("oreb", models.IntegerField(default=0)),
                ("dreb", models.IntegerField(default=0)),
                ("reb", models.IntegerField(default=0)),
                ("ast", models.IntegerField(default=0)),
                ("stl", models.IntegerField(default=0)),
                ("blk", models.IntegerField(default=0)),
                ("to", models.IntegerField(default=0)),
                ("pf", models.IntegerField(default=0)),
                ("pts", models.IntegerField(default=0)),
                ("plus_minus", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Game Boxscore Traditional",
                "verbose_name_plural": "Game Boxscores Traditional",
                "ordering": ["-game_id", "player_team_abb", "player_id"],
                "unique_together": {("game_id", "player_id", "period")},
                "indexes": [
                    models.Index(fields=["game_id"], name="game_boxsco_game_id_7a8b2d_idx"),
                    models.Index(fields=["player_id"], name="game_boxsco_player__a1c3e5_idx"),
                    models.Index(
                        fields=["season", "season_type"],
                        name="game_boxsco_season_9d4f6b_idx",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="GameBoxscoreAdvanced",
            fields=[
                ("id", models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name="ID"
                )),
                ("game_id", models.CharField(
                    db_index=True, max_length=20,
                    verbose_name="ID del Juego"
                )),
                ("season", models.CharField(
                    db_index=True, max_length=10,
                    verbose_name="Temporada"
                )),
                ("season_type", models.CharField(
                    db_index=True, max_length=20,
                    verbose_name="Tipo de Temporada"
                )),
                ("home_team_abb", models.CharField(
                    max_length=10, verbose_name="Equipo Local"
                )),
                ("away_team_abb", models.CharField(
                    max_length=10, verbose_name="Equipo Visitante"
                )),
                ("player_id", models.IntegerField(
                    db_index=True, verbose_name="ID del Jugador"
                )),
                ("player_name", models.CharField(
                    max_length=100, verbose_name="Nombre del Jugador"
                )),
                ("player_name_abb", models.CharField(
                    max_length=50, verbose_name="Nombre Abreviado"
                )),
                ("player_team_abb", models.CharField(
                    max_length=10, verbose_name="Equipo del Jugador"
                )),
                ("player_pos", models.CharField(
                    max_length=5, verbose_name="Posición"
                )),
                ("player_dnp", models.BooleanField(
                    default=False, verbose_name="No Jugó (DNP)"
                )),
                ("period", models.CharField(
                    max_length=10, verbose_name="Período"
                )),
                ("min", models.CharField(
                    max_length=10, verbose_name="Minutos"
                )),
                ("off_rtg", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("def_rtg", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("net_rtg", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("ast_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("ast_to", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("ast_ratio", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("oreb_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("dreb_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("reb_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("to_ratio", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("efg_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("ts_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("usg_pct", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("pace", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
                ("pie", models.FloatField(
                    blank=True, default=0.0, null=True
                )),
            ],
            options={
                "verbose_name": "Game Boxscore Advanced",
                "verbose_name_plural": "Game Boxscores Advanced",
                "ordering": ["-game_id", "player_team_abb", "player_id"],
                "unique_together": {("game_id", "player_id", "period")},
                "indexes": [
                    models.Index(fields=["game_id"], name="game_boxsco_game_id_8b9c0d_idx"),
                    models.Index(fields=["player_id"], name="game_boxsco_player__b2d4f6_idx"),
                    models.Index(
                        fields=["season", "season_type"],
                        name="game_boxsco_season_0e1a2c_idx",
                    ),
                ],
            },
        ),
    ]
