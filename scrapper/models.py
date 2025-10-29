from django.db import models

from scrapper.enums import ScrapperName


# Create your models here.
class ScrapperLogs(models.Model):
    """
    Modelo para almacenar logs de scraper
    """

    url = models.URLField(max_length=500, help_text="URL de la página web")
    category = models.CharField(max_length=100, help_text="Categoría de la página web")
    season = models.CharField(max_length=10, help_text="Temporada de la página web")
    season_type = models.CharField(
        max_length=20, help_text="Tipo de temporada de la página web"
    )
    status = models.CharField(max_length=10, help_text="Estado de la página web")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error = models.TextField(help_text="Error de la página web", null=True, blank=True)

    class Meta:
        verbose_name = "Scrapper Log"
        verbose_name_plural = "Scrapper Logs"


class ScrapperStatus(models.Model):
    """
    Modelo para almacenar el estado del scraper
    """

    scrapper_name = models.CharField(
        max_length=100,
        help_text="Nombre del scraper",
        choices=ScrapperName.choices(),
    )
    last_execution = models.DateTimeField(auto_now_add=True)
    last_link_scraped = models.URLField(
        max_length=500, help_text="Último enlace scrapeado", null=True, blank=True
    )
    is_running = models.BooleanField(
        default=False, help_text="Indica si el scraper está en ejecución"
    )

    class Meta:
        verbose_name = "Scrapper Status"
        verbose_name_plural = "Scrapper Status"

    def __str__(self):
        return f"{self.scrapper_name} - {'Running' if self.is_running else 'Stopped'}"
