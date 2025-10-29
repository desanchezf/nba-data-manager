from django.contrib import admin
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.decorators import action
from scrapper.models import ScrapperLogs, ScrapperStatus
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse_lazy


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
    # actions_list = [
    #     "execute_scrapper",
    # ]

    actions_list = [
        "execute_scrapper",
        {
            "title": "Dropdown action",
            "icon": "person",  # Optional, will display icon in the dropdown title
            "items": [
                "action3",
                "action4",
            ],
        },
    ]

    @action(
        description=_("Start all scrapers 🚀 "),
        url_path="changelist-action",
        permissions=["execute_scrapper"],
        icon="play_arrow",  # Ahora usando un emoji de cohete
    )
    def execute_scrapper(self, request: HttpRequest):
        # Se ejecuta el scrapper en segundo plano
        print("Scrapper executed")
        return redirect(reverse_lazy("admin:scrapper_scrapperstatus_changelist"))

    def has_execute_scrapper_permission(self, request: HttpRequest):
        # Write your own bussiness logic. Code below will always display an action.
        return True

    # Accion para el dropdown de actions
    @action(
        description=_("Start all scrapers 🚀 "),
        url_path="changelist-action",
        permissions=["execute_scrapper"],
        icon="play_arrow",  # Ahora usando un emoji de cohete
    )
    def action3(self, request: HttpRequest):
        # Se ejecuta el scrapper en segundo plano
        print("Scrapper executed")
        pass

    @action(
        description=_("Start all scrapers 🚀 "),
        url_path="changelist-action",
        permissions=["execute_scrapper"],
        icon="play_arrow",  # Ahora usando un emoji de cohete
    )
    def action4(self, request: HttpRequest):
        # Se ejecuta el scrapper en segundo plano
        print("Scrapper executed")
        pass
