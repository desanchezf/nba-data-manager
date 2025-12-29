from django.db import models
from data.enums import SeasonChoices


# Create your models here.
class Teams(models.Model):
    team_id = models.IntegerField(
        db_index=True,
        verbose_name="ID del Equipo",
        help_text="Identificador numérico único del equipo",
    )
    team_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Equipo",
        help_text="Nombre completo del equipo",
    )
    team_abb = models.CharField(
        max_length=10,
        verbose_name="Abreviación del Equipo",
        help_text="Abreviación del equipo",
    )
    team_conference = models.CharField(
        max_length=20,
        verbose_name="Conferencia del Equipo",
        help_text="Conferencia del equipo",
    )
    team_division = models.CharField(
        max_length=20,
        verbose_name="División del Equipo",
        help_text="División del equipo",
    )

    def __str__(self):
        return f"{self.team_abb} - {self.team_name}"

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ["team_name"]
        indexes = [
            models.Index(fields=["team_name"]),
        ]


class Players(models.Model):
    player_id = models.IntegerField(
        db_index=True,
        verbose_name="ID del Jugador",
        help_text="Identificador numérico único del jugador",
    )
    player_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Jugador",
        help_text="Nombre completo del jugador",
    )
    player_abb = models.CharField(
        max_length=50,
        verbose_name="Abreviación del Jugador",
        help_text="Abreviación del jugador",
    )
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    season = models.CharField(
        max_length=10,
        choices=SeasonChoices.choices(),
        verbose_name="Temporada",
        help_text="Temporada del jugador (formato: YYYY-YY, ej: 2015-16)",
    )

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        ordering = ["player_name"]
        indexes = [
            models.Index(fields=["player_name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["player_id", "season", "team"],
                name="unique_player_season_team",
            ),
        ]
