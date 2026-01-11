from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.contrib import messages
from django.db import transaction, models
import csv
from io import StringIO
from teams.models import (
    TeamsGeneralTraditional,
    TeamsGeneralAdvanced,
    TeamsGeneralFourFactors,
    TeamsGeneralMisc,
    TeamsGeneralScoring,
    TeamsGeneralOpponent,
    TeamsGeneralDefense,
    TeamsGeneralViolations,
    TeamsGeneralEstimatedAdvanced,
    TeamsClutchTraditional,
    TeamsClutchAdvanced,
    TeamsClutchFourFactors,
    TeamsClutchMisc,
    TeamsClutchScoring,
    TeamsClutchOpponent,
    TeamsPlaytypeIsolation,
    TeamsPlaytypeTransition,
    TeamsPlaytypeBallHandler,
    TeamsPlaytypeRollMan,
    TeamsPlaytypePostUp,
    TeamsPlaytypeSpotUp,
    TeamsPlaytypeHandOff,
    TeamsPlaytypeCut,
    TeamsPlaytypeOffScreen,
    TeamsPlaytypePutbacks,
    TeamsPlaytypeMisc,
    TeamsTrackingDrives,
    TeamsTrackingDefensiveImpact,
    TeamsTrackingCatchShoot,
    TeamsTrackingPassing,
    TeamsTrackingTouches,
    TeamsTrackingPullup,
    TeamsTrackingRebounding,
    TeamsTrackingOffensiveRebounding,
    TeamsTrackingDefensiveRebounding,
    TeamsTrackingShootingEfficiency,
    TeamsTrackingSpeedDistance,
    TeamsTrackingElbowTouch,
    TeamsTrackingPostUps,
    TeamsTrackingPaintTouch,
    TeamsDefenseDashboardOverall,
    TeamsDefenseDashboard3pt,
    TeamsDefenseDashboard2pt,
    TeamsDefenseDashboardLt6,
    TeamsDefenseDashboardLt10,
    TeamsDefenseDashboardGt15,
    TeamsShotDashboardGeneral,
    TeamsShotDashboardShotClock,
    TeamsShotDashboardDribbles,
    TeamsShotDashboardTouchTime,
    TeamsShotDashboardClosestDefender,
    TeamsShotDashboardClosestDefender10,
    TeamsAdvancedBoxScores,
    TeamsAdvancedBoxScoresAdvanced,
    TeamsAdvancedBoxScoresFourFactors,
    TeamsAdvancedBoxScoresMisc,
    TeamsAdvancedBoxScoresScoring,
    TeamsShooting,
    TeamsOpponentShootingOverall,
    TeamsOpponentShotsGeneral,
    TeamsOpponentShotsShotclock,
    TeamsOpponentShotsDribbles,
    TeamsOpponentShotsTouchTime,
    TeamsOpponentShotsClosestDefender,
    TeamsOpponentShotsClosestDefender10,
    TeamsHustle,
    TeamsBoxOuts,
)


def export_as_csv(modeladmin, request, queryset):
    """
    Acción de admin para exportar los registros seleccionados a CSV
    """
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f"attachment; filename={meta.verbose_name_plural}.csv"
    )

    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset:
        row = []
        for field in meta.fields:
            value = getattr(obj, field.name)
            # Manejar ForeignKey
            if hasattr(value, "__str__") and not isinstance(value, str):
                value = str(value)
            # Manejar valores None
            if value is None:
                value = ""
            row.append(value)
        writer.writerow(row)

    return response


export_as_csv.short_description = "Exportar seleccionados a CSV"


def get_csv_import_view(model_class):
    """
    Crea una función de vista para importar CSV para un modelo específico
    """
    from django.utils.dateparse import parse_datetime, parse_date

    def csv_import_view(request):
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            # Leer el archivo CSV
            decoded_file = csv_file.read().decode("utf-8")
            io_string = StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            meta = model_class._meta
            field_names = [field.name for field in meta.fields]

            created_count = 0
            updated_count = 0
            errors = []

            with transaction.atomic():
                for row_num, row in enumerate(
                    reader, start=2
                ):  # start=2 porque la fila 1 es el header
                    try:
                        # Normalizar las columnas del CSV a minúsculas para coincidir con los campos del modelo
                        # Los CSVs tienen columnas en mayúsculas (SEASON, TEAM_ABB) pero los modelos en minúsculas (season, team_abb)
                        row_normalized = {k.lower(): v for k, v in row.items()}
                        
                        # Preparar datos para crear/actualizar
                        data = {}
                        for field_name in field_names:
                            if field_name in row_normalized:
                                value = row_normalized[field_name].strip() if row_normalized[field_name] else ""

                                # Obtener el campo del modelo
                                field = meta.get_field(field_name)

                                # Manejar ForeignKey
                                if field.many_to_one:  # ForeignKey
                                    # Intentar encontrar el objeto relacionado
                                    related_model = field.related_model
                                    try:
                                        # Buscar por ID o por un campo único
                                        if value.isdigit():
                                            related_obj = related_model.objects.get(
                                                pk=int(value)
                                            )
                                        else:
                                            # Intentar buscar por el primer campo único o por __str__
                                            related_obj = related_model.objects.filter(
                                                **{related_model._meta.pk.name: value}
                                            ).first()
                                            if not related_obj:
                                                # Intentar por nombre si existe
                                                if hasattr(related_model, "name"):
                                                    related_obj = (
                                                        related_model.objects.filter(
                                                            name=value
                                                        ).first()
                                                    )

                                        if related_obj:
                                            data[field_name] = related_obj
                                        else:
                                            errors.append(
                                                f"Fila {row_num}: No se encontró el objeto relacionado para {field_name}={value}"
                                            )
                                            continue
                                    except Exception as e:
                                        errors.append(
                                            f"Fila {row_num}: Error al buscar {field_name}={value}: {str(e)}"
                                        )
                                        continue

                                # Manejar tipos de datos
                                elif isinstance(field, models.BooleanField):
                                    data[field_name] = value.lower() in (
                                        "true",
                                        "1",
                                        "yes",
                                        "sí",
                                        "si",
                                    )
                                elif isinstance(field, models.IntegerField):
                                    data[field_name] = int(value) if value else 0
                                elif isinstance(field, models.FloatField):
                                    data[field_name] = float(value) if value else 0.0
                                elif isinstance(field, models.DateTimeField):
                                    # Intentar parsear fecha
                                    parsed = parse_datetime(value)
                                    if parsed:
                                        data[field_name] = parsed
                                elif isinstance(field, models.DateField):
                                    parsed = parse_date(value)
                                    if parsed:
                                        data[field_name] = parsed
                                else:
                                    data[field_name] = value if value else ""

                        # Crear o actualizar el objeto
                        # Intentar encontrar un objeto existente por campos únicos
                        unique_fields = [
                            f for f in meta.fields if f.unique or f.primary_key
                        ]

                        if unique_fields:
                            # Buscar por el primer campo único
                            unique_field = unique_fields[0]
                            unique_value = data.get(unique_field.name)

                            if unique_value:
                                obj, created = model_class.objects.update_or_create(
                                    **{unique_field.name: unique_value}, defaults=data
                                )
                                if created:
                                    created_count += 1
                                else:
                                    updated_count += 1
                            else:
                                # Si no hay valor único, crear nuevo
                                model_class.objects.create(**data)
                                created_count += 1
                        else:
                            # Si no hay campos únicos, siempre crear nuevo
                            model_class.objects.create(**data)
                            created_count += 1

                    except Exception as e:
                        errors.append(f"Fila {row_num}: {str(e)}")
                        continue

            # Mensajes de resultado
            if created_count > 0:
                messages.success(
                    request, f"Se crearon {created_count} registros exitosamente."
                )
            if updated_count > 0:
                messages.success(
                    request, f"Se actualizaron {updated_count} registros exitosamente."
                )
            if errors:
                for error in errors[:10]:  # Mostrar solo los primeros 10 errores
                    messages.error(request, error)
                if len(errors) > 10:
                    messages.warning(
                        request,
                        f"Y {len(errors) - 10} errores más. Revise el archivo CSV.",
                    )

            return HttpResponse(
                f"Importación completada. Creados: {created_count}, Actualizados: {updated_count}, Errores: {len(errors)}"
            )

        return HttpResponse("Por favor, suba un archivo CSV válido.", status=400)

    return csv_import_view


@admin.register(TeamsGeneralTraditional)
class TeamsGeneralTraditionalAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralAdvanced)
class TeamsGeneralAdvancedAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralFourFactors)
class TeamsGeneralFourFactorsAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralMisc)
class TeamsGeneralMiscAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralScoring)
class TeamsGeneralScoringAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralOpponent)
class TeamsGeneralOpponentAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralDefense)
class TeamsGeneralDefenseAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralViolations)
class TeamsGeneralViolationsAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsGeneralEstimatedAdvanced)
class TeamsGeneralEstimatedAdvancedAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsClutchTraditional)
class TeamsClutchTraditionalAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsClutchAdvanced)
class TeamsClutchAdvancedAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsClutchFourFactors)
class TeamsClutchFourFactorsAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsClutchMisc)
class TeamsClutchMiscAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsClutchScoring)
class TeamsClutchScoringAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsClutchOpponent)
class TeamsClutchOpponentAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeIsolation)
class TeamsPlaytypeIsolationAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeTransition)
class TeamsPlaytypeTransitionAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeBallHandler)
class TeamsPlaytypeBallHandlerAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeRollMan)
class TeamsPlaytypeRollManAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypePostUp)
class TeamsPlaytypePostUpAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeSpotUp)
class TeamsPlaytypeSpotUpAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeHandOff)
class TeamsPlaytypeHandOffAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeCut)
class TeamsPlaytypeCutAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeOffScreen)
class TeamsPlaytypeOffScreenAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypePutbacks)
class TeamsPlaytypePutbacksAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsPlaytypeMisc)
class TeamsPlaytypeMiscAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingDrives)
class TeamsTrackingDrivesAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingDefensiveImpact)
class TeamsTrackingDefensiveImpactAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingCatchShoot)
class TeamsTrackingCatchShootAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingPassing)
class TeamsTrackingPassingAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingTouches)
class TeamsTrackingTouchesAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingPullup)
class TeamsTrackingPullupAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingRebounding)
class TeamsTrackingReboundingAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingOffensiveRebounding)
class TeamsTrackingOffensiveReboundingAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingDefensiveRebounding)
class TeamsTrackingDefensiveReboundingAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingShootingEfficiency)
class TeamsTrackingShootingEfficiencyAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingSpeedDistance)
class TeamsTrackingSpeedDistanceAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingElbowTouch)
class TeamsTrackingElbowTouchAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingPostUps)
class TeamsTrackingPostUpsAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsTrackingPaintTouch)
class TeamsTrackingPaintTouchAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsDefenseDashboardOverall)
class TeamsDefenseDashboardOverallAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsDefenseDashboard3pt)
class TeamsDefenseDashboard3ptAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsDefenseDashboard2pt)
class TeamsDefenseDashboard2ptAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsDefenseDashboardLt6)
class TeamsDefenseDashboardLt6Admin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsDefenseDashboardLt10)
class TeamsDefenseDashboardLt10Admin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsDefenseDashboardGt15)
class TeamsDefenseDashboardGt15Admin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsShotDashboardGeneral)
class TeamsShotDashboardGeneralAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsShotDashboardShotClock)
class TeamsShotDashboardShotClockAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsShotDashboardDribbles)
class TeamsShotDashboardDribblesAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsShotDashboardTouchTime)
class TeamsShotDashboardTouchTimeAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsShotDashboardClosestDefender)
class TeamsShotDashboardClosestDefenderAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsShotDashboardClosestDefender10)
class TeamsShotDashboardClosestDefender10Admin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsAdvancedBoxScores)
class TeamsAdvancedBoxScoresAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsAdvancedBoxScoresAdvanced)
class TeamsAdvancedBoxScoresAdvancedAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsAdvancedBoxScoresFourFactors)
class TeamsAdvancedBoxScoresFourFactorsAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsAdvancedBoxScoresMisc)
class TeamsAdvancedBoxScoresMiscAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsAdvancedBoxScoresScoring)
class TeamsAdvancedBoxScoresScoringAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsShooting)
class TeamsShootingAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsOpponentShootingOverall)
class TeamsOpponentShootingOverallAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsOpponentShotsGeneral)
class TeamsOpponentShotsGeneralAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsOpponentShotsShotclock)
class TeamsOpponentShotsShotclockAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsOpponentShotsDribbles)
class TeamsOpponentShotsDribblesAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsOpponentShotsTouchTime)
class TeamsOpponentShotsTouchTimeAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsOpponentShotsClosestDefender)
class TeamsOpponentShotsClosestDefenderAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsOpponentShotsClosestDefender10)
class TeamsOpponentShotsClosestDefender10Admin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsHustle)
class TeamsHustleAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TeamsBoxOuts)
class TeamsBoxOutsAdmin(admin.ModelAdmin):
    list_display = ["season", "season_type", "team_abb"]
    search_fields = ["team_abb"]
    list_filter = ["season", "season_type", "team_abb"]
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.csv_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_import_csv",
            ),
        ]
        return custom_urls + urls

    def csv_import_view(self, request):
        return get_csv_import_view(self.model)(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)
