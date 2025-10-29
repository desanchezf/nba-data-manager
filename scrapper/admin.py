from django.contrib import admin
from django.core.management import call_command
import time
from django.db.models import QuerySet
from django.http import HttpRequest
from django.contrib import messages
from unfold.admin import ModelAdmin
from unfold.decorators import action

from scrapper.models import ScrapperLogs, ScrapperStatus


@admin.register(ScrapperLogs)
class ScrapperLogsAdmin(ModelAdmin):
    list_display = ("url", "category", "season", "season_type", "status", "created_at")
    search_fields = ("url", "category", "season", "season_type")
    list_filter = ("status", "created_at", "category", "season", "season_type")
    ordering = ("-created_at",)


@admin.register(ScrapperStatus)
class ScrapperStatusAdmin(ModelAdmin):
    list_display = (
        "get_scrapper_name_display",
        "last_execution",
        "last_link_scraped",
        "is_running",
    )
    search_fields = ("scrapper_name", "last_link_scraped")
    list_filter = ("is_running", "last_execution")
    ordering = ("-last_execution",)

    def get_scrapper_name_display(self, obj):
        """Mostrar el nombre legible del scrapper"""
        if not obj.scrapper_name:
            return "-"
        # Django automáticamente provee get_FIELD_display para campos con choices
        # pero lo customizamos para asegurar que siempre funcione
        choices_dict = dict(obj._meta.get_field("scrapper_name").choices)
        display_name = choices_dict.get(obj.scrapper_name, obj.scrapper_name)
        return str(display_name) if display_name else "-"

    get_scrapper_name_display.short_description = "Scrapper Name"
    get_scrapper_name_display.admin_order_field = "scrapper_name"

    # Lista de acciones disponibles
    actions_list = [
        "execute_scrapper",
    ]

    @action(description="🚀 Ejecutar Scrapper", icon="play_arrow")
    def execute_scrapper(self, request: HttpRequest, queryset: QuerySet):
        """Ejecutar scraper para URLs seleccionadas"""
        urls = list(queryset.values_list("url", flat=True))

        try:
            time.sleep(11200)

            call_command("run_scraper", urls=urls, verbosity=2)

            self.message_user(
                request,
                f"✅ Se ejecutó el scraper para {len(urls)} URLs.",
                messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request, f"❌ Error executing scraper: {str(e)}", messages.ERROR
            )
