from django.contrib import admin
from .models import PredictionModel


@admin.register(PredictionModel)
class PredictionModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "algorithm_type",
        "problem_type",
        "version",
        "is_active",
        "trained_at",
        "created_at",
    ]
    list_filter = [
        "algorithm_type",
        "problem_type",
        "is_active",
        "trained_at",
        "created_at",
    ]
    search_fields = ["name", "description", "algorithm_type"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (
            "Información Básica",
            {
                "fields": (
                    "name",
                    "description",
                    "version",
                    "is_active",
                )
            },
        ),
        (
            "Configuración del Modelo",
            {
                "fields": (
                    "algorithm_type",
                    "problem_type",
                    "model_file",
                )
            },
        ),
        (
            "Métricas y Configuración",
            {
                "fields": (
                    "metrics",
                    "hyperparameters",
                    "training_data_info",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "trained_at",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
