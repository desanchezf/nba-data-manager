from django.db import models

# Create your models here.


class Links(models.Model):
    """
    Modelo para almacenar enlaces de estadísticas de la NBA
    """

    category = models.CharField(
        max_length=100,
        help_text="Categoría de estadísticas (ej: boxscores-traditional, box-outs)",
    )
    season_type = models.CharField(
        max_length=20,
        help_text="Tipo de temporada (Pre+Season, Regular+Season, Playoffs, All+Star, PlayIn, IST)",
    )
    season = models.CharField(
        max_length=10, help_text="Temporada (ej: 2015-16, 2024-25)"
    )
    url = models.URLField(
        max_length=500, help_text="URL completa del enlace de NBA.com"
    )
    scraped = models.BooleanField(
        default=False,
        help_text="Indica si los datos de este enlace ya han sido extraídos",
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        ordering = ["category", "-season", "season_type"]
        unique_together = ["category", "season_type", "season"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["season_type"]),
            models.Index(fields=["season"]),
            models.Index(fields=["scraped"]),
            models.Index(fields=["category", "season_type", "season"]),
        ]

    def __str__(self):
        return f"{self.category} - {self.season} - {self.season_type}"


class Games(models.Model):
    """
    Modelo para almacenar información de partidos de la NBA
    """

    date = models.DateField(help_text="Fecha del partido")
    game_id = models.CharField(
        max_length=50, unique=True, help_text="Identificador único del partido"
    )
    home_team = models.CharField(max_length=50, help_text="Equipo local")
    away_team = models.CharField(max_length=50, help_text="Equipo visitante")
    scraped = models.BooleanField(
        default=False,
        help_text="Indica si los datos de este partido ya han sido extraídos",
    )

    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
        ordering = ["-date", "home_team"]
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["game_id"]),
            models.Index(fields=["home_team"]),
            models.Index(fields=["away_team"]),
            models.Index(fields=["scraped"]),
        ]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.date}"
