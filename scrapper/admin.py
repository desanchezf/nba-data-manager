from django.contrib import admin
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.decorators import action
from scrapper.models import ScrapperLogs, ScrapperStatus
from django.utils.translation import gettext_lazy as _
from scrapper.services.links_service import LinksService
from scrapper.services.boxscore_scrapper import BoxscoreScraper


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
        "execute_all_scrappers",
        {
            "title": "Scrappers",
            "items": [
                "advanced_boxscore_scraper",
                "box_outs_scraper",
                "boxscore_scraper",
                "catch_and_shoot_scraper",
                "clutch_scraper",
                "defense_dashboard_scraper",
                "defensive_impact_scraper",
                "defensive_rebounding_scraper",
                "drives_scraper",
                "elbow_touch_scraper",
                "hustle_scraper",
                "offensive_rebounding_scraper",
                "opponent_shooting_scraper",
                "paint_touch_scraper",
                "passing_scraper",
                "playtipe_scraper",
                "post_ups_scraper",
                "pull_up_shooting_scraper",
                "rebounding_scraper",
                "shooting_efficiency_scraper",
                "shooting_scraper",
                "shot_dashboard_scraper",
                "speed_and_distance_scraper",
                "touches_scraper",
            ],
        },
    ]

    @action(
        description=_("Boxscore Scraper"),
        url_path="boxscore-scraper",
        icon="play_arrow",
    )
    def boxscore_scraper(self, request: HttpRequest):
        # Obtener enlace 
        # Ejecutar scraper (enlaces)
        links = LinksService("boxscore").get_links()
        scrapper = BoxscoreScraper()
        



    @action(
        description=_("Start all scrappers 🚀"),
        url_path="advanced-boxscore-scraper",
        icon="play_arrow",
    )
    def execute_all_scrappers(self, request: HttpRequest):
        print("Advanced Boxscore Scraper executed")
        # return redirect(reverse_lazy("admin:scrapper_scrapperstatus_changelist"))
        pass


    @action(
        description=_("Advanced Boxscore Scraper"),
        url_path="advanced-boxscore-scraper",
        icon="play_arrow",
    )
    def advanced_boxscore_scraper(self, request: HttpRequest):
        print("Advanced Boxscore Scraper executed")
        # return redirect(reverse_lazy("admin:scrapper_scrapperstatus_changelist"))
        pass

    @action(
        description=_("Box Outs Scraper"),
        url_path="box-outs-scraper",
        icon="play_arrow",
    )
    def box_outs_scraper(self, request: HttpRequest):
        print("Box Outs Scraper executed")
        pass



    @action(
        description=_("Catch & Shoot Scraper"),
        url_path="catch-and-shoot-scraper",
        icon="play_arrow",
    )
    def catch_and_shoot_scraper(self, request: HttpRequest):
        print("Catch & Shoot Scraper executed")
        pass

    @action(
        description=_("Clutch Scraper"),
        url_path="clutch-scraper",
        icon="play_arrow",
    )
    def clutch_scraper(self, request: HttpRequest):
        print("Clutch Scraper executed")
        pass

    @action(
        description=_("Defense Dashboard Scraper"),
        url_path="defense-dashboard-scraper",
        icon="play_arrow",
    )
    def defense_dashboard_scraper(self, request: HttpRequest):
        print("Defense Dashboard Scraper executed")
        pass

    @action(
        description=_("Defensive Impact Scraper"),
        url_path="defensive-impact-scraper",
        icon="play_arrow",
    )
    def defensive_impact_scraper(self, request: HttpRequest):
        print("Defensive Impact Scraper executed")
        pass

    @action(
        description=_("Defensive Rebounding Scraper"),
        url_path="defensive-rebounding-scraper",
        icon="play_arrow",
    )
    def defensive_rebounding_scraper(self, request: HttpRequest):
        print("Defensive Rebounding Scraper executed")
        pass

    @action(
        description=_("Drives Scraper"),
        url_path="drives-scraper",
        icon="play_arrow",
    )
    def drives_scraper(self, request: HttpRequest):
        print("Drives Scraper executed")
        pass

    @action(
        description=_("Elbow Touch Scraper"),
        url_path="elbow-touch-scraper",
        icon="play_arrow",
    )
    def elbow_touch_scraper(self, request: HttpRequest):
        print("Elbow Touch Scraper executed")
        pass

    @action(
        description=_("Hustle Scraper"),
        url_path="hustle-scraper",
        icon="play_arrow",
    )
    def hustle_scraper(self, request: HttpRequest):
        print("Hustle Scraper executed")
        pass

    @action(
        description=_("Offensive Rebounding Scraper"),
        url_path="offensive-rebounding-scraper",
        icon="play_arrow",
    )
    def offensive_rebounding_scraper(self, request: HttpRequest):
        print("Offensive Rebounding Scraper executed")
        pass

    @action(
        description=_("Opponent Shooting Scraper"),
        url_path="opponent-shooting-scraper",
        icon="play_arrow",
    )
    def opponent_shooting_scraper(self, request: HttpRequest):
        print("Opponent Shooting Scraper executed")
        pass

    @action(
        description=_("Paint Touch Scraper"),
        url_path="paint-touch-scraper",
        icon="play_arrow",
    )
    def paint_touch_scraper(self, request: HttpRequest):
        print("Paint Touch Scraper executed")
        pass

    @action(
        description=_("Passing Scraper"),
        url_path="passing-scraper",
        icon="play_arrow",
    )
    def passing_scraper(self, request: HttpRequest):
        print("Passing Scraper executed")
        pass

    @action(
        description=_("Playtipe Scraper"),
        url_path="playtipe-scraper",
        icon="play_arrow",
    )
    def playtipe_scraper(self, request: HttpRequest):
        print("Playtipe Scraper executed")
        pass

    @action(
        description=_("Post Ups Scraper"),
        url_path="post-ups-scraper",
        icon="play_arrow",
    )
    def post_ups_scraper(self, request: HttpRequest):
        print("Post Ups Scraper executed")
        pass

    @action(
        description=_("Pull Up Shooting Scraper"),
        url_path="pull-up-shooting-scraper",
        icon="play_arrow",
    )
    def pull_up_shooting_scraper(self, request: HttpRequest):
        print("Pull Up Shooting Scraper executed")
        pass

    @action(
        description=_("Rebounding Scraper"),
        url_path="rebounding-scraper",
        icon="play_arrow",
    )
    def rebounding_scraper(self, request: HttpRequest):
        print("Rebounding Scraper executed")
        pass

    @action(
        description=_("Shooting Efficiency Scraper"),
        url_path="shooting-efficiency-scraper",
        icon="play_arrow",
    )
    def shooting_efficiency_scraper(self, request: HttpRequest):
        print("Shooting Efficiency Scraper executed")
        pass

    @action(
        description=_("Shooting Scraper"),
        url_path="shooting-scraper",
        icon="play_arrow",
    )
    def shooting_scraper(self, request: HttpRequest):
        print("Shooting Scraper executed")
        pass

    @action(
        description=_("Shot Dashboard Scraper"),
        url_path="shot-dashboard-scraper",
        icon="play_arrow",
    )
    def shot_dashboard_scraper(self, request: HttpRequest):
        print("Shot Dashboard Scraper executed")
        pass

    @action(
        description=_("Speed & Distance Scraper"),
        url_path="speed-and-distance-scraper",
        icon="play_arrow",
    )
    def speed_and_distance_scraper(self, request: HttpRequest):
        print("Speed & Distance Scraper executed")
        pass

    @action(
        description=_("Touches Scraper"),
        url_path="touches-scraper",
        icon="play_arrow",
    )
    def touches_scraper(self, request: HttpRequest):
        print("Touches Scraper executed")
        pass
