from django.contrib import admin
from .models import Prediction, PredictionsHistory


class PredictionsHistoryInline(admin.TabularInline):
    """Inline para mostrar el historial de predicciones"""

    model = PredictionsHistory
    extra = 0
    readonly_fields = ["created_at", "updated_at"]
    fields = ["odds", "result", "failure", "failure_reason", "created_at"]


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = [
        "matchup",
        "home_team",
        "away_team",
        "prediction_type",
        "prediction_category",
        "prediction_market",
        "prediction_model",
        "matchup_date",
        "created_at",
    ]
    list_filter = [
        "prediction_type",
        "prediction_category",
        "prediction_market",
        "prediction_model",
        "matchup_date",
        "created_at",
    ]
    search_fields = [
        "matchup",
        "home_team",
        "away_team",
        "prediction_model__name",
    ]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["prediction_model"]
    date_hierarchy = "matchup_date"
    ordering = ["-matchup_date", "-created_at"]
    inlines = [PredictionsHistoryInline]
    fieldsets = (
        (
            "Información del Partido",
            {
                "fields": (
                    "matchup",
                    "home_team",
                    "away_team",
                    "matchup_date",
                )
            },
        ),
        (
            "Configuración de la Predicción",
            {
                "fields": (
                    "prediction_type",
                    "prediction_category",
                    "prediction_market",
                    "prediction_model",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(PredictionsHistory)
class PredictionsHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "prediction",
        "odds",
        "result",
        "failure",
        "created_at",
    ]
    list_filter = [
        "failure",
        "created_at",
        "prediction__prediction_type",
        "prediction__prediction_category",
    ]
    search_fields = [
        "prediction__matchup",
        "prediction__home_team",
        "prediction__away_team",
        "result",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    fieldsets = (
        (
            "Información de la Predicción",
            {"fields": ("prediction",)},
        ),
        (
            "Resultado",
            {
                "fields": (
                    "odds",
                    "result",
                    "failure",
                    "failure_reason",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
