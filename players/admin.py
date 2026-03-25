from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from django.urls import path
from django.contrib import messages
from django.db import transaction, models
import csv
from io import StringIO
from players.models import (
    PlayersGeneralTraditional,
    PlayersGeneralAdvanced,
    PlayersGeneralMisc,
    PlayersGeneralScoring,
    PlayersGeneralUsage,
    PlayersGeneralOpponent,
    PlayersGeneralDefense,
    PlayersGeneralViolations,
    PlayersGeneralEstimatedAdvanced,
    PlayersClutchTraditional,
    PlayersClutchAdvanced,
    PlayersClutchMisc,
    PlayersClutchScoring,
    PlayersClutchUsage,
    PlayersPlaytypeIsolation,
    PlayersPlaytypeTransition,
    PlayersPlaytypeBallHandler,
    PlayersPlaytypeRollMan,
    PlayersPlaytypePostUp,
    PlayersPlaytypeSpotUp,
    PlayersPlaytypeHandOff,
    PlayersPlaytypeCut,
    PlayersPlaytypeOffScreen,
    PlayersPlaytypePutbacks,
    PlayersPlaytypeMisc,
    PlayersTrackingDrives,
    PlayersTrackingDefensiveImpact,
    PlayersTrackingCatchShoot,
    PlayersTrackingPassing,
    PlayersTrackingTouches,
    PlayersTrackingPullup,
    PlayersTrackingRebounding,
    PlayersTrackingOffensiveRebounding,
    PlayersTrackingDefensiveRebounding,
    PlayersTrackingShootingEfficiency,
    PlayersTrackingSpeedDistance,
    PlayersTrackingElbowTouch,
    PlayersTrackingPostUps,
    PlayersTrackingPaintTouch,
    PlayersDefenseDashboardOverall,
    PlayersDefenseDashboard3pt,
    PlayersDefenseDashboard2pt,
    PlayersDefenseDashboardLt6,
    PlayersDefenseDashboardLt10,
    PlayersDefenseDashboardGt15,
    PlayersShotDashboardGeneral,
    PlayersShotDashboardShotClock,
    PlayersShotDashboardDribbles,
    PlayersShotDashboardTouchTime,
    PlayersShotDashboardClosestDefender,
    PlayersShotDashboardClosestDefender10,
    PlayersBoxScores,
    PlayersAdvancedBoxScoresTraditional,
    PlayersAdvancedBoxScoresAdvanced,
    PlayersAdvancedBoxScoresMisc,
    PlayersAdvancedBoxScoresScoring,
    PlayersAdvancedBoxScoresUsage,
    PlayersShooting,
    PlayersDunkScores,
    PlayersOpponentShootingOverall,
    PlayersHustle,
    PlayersBoxOuts,
    PlayersBios,
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
                        # Filtrar campos _rank (no se usan en el sistema)
                        row_normalized = {
                            k.lower(): v 
                            for k, v in row.items() 
                            if not k.lower().endswith('_rank') and not k.upper().endswith('_RANK')
                        }

                        # Mapeo de columnas CSV normalizadas a campos del modelo
                        csv_field_map = {
                            "l": "lose",
                            "match_up": "matchup",
                            "fgpct": "fgperc",
                            "ftmpct": "ftmperc",
                        }
                        # Aplicar mapeo
                        for csv_key, model_key in csv_field_map.items():
                            if csv_key in row_normalized and model_key in field_names:
                                row_normalized[model_key] = row_normalized.pop(csv_key)

                        # Preparar datos para crear/actualizar
                        data = {}
                        for field_name in field_names:
                            if field_name in row_normalized:
                                value = (
                                    row_normalized[field_name].strip()
                                    if row_normalized[field_name]
                                    else ""
                                )

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
                        unique_fields = [
                            f for f in meta.fields if f.unique or f.primary_key
                        ]
                        unique_together = getattr(meta, "unique_together", None) or []

                        if unique_fields:
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
                                model_class.objects.create(**data)
                                created_count += 1
                        elif unique_together:
                            lookup_fields = unique_together[0]
                            lookup = {k: data.get(k) for k in lookup_fields if k in data}
                            if len(lookup) == len(lookup_fields):
                                obj, created = model_class.objects.update_or_create(
                                    defaults=data, **lookup
                                )
                                if created:
                                    created_count += 1
                                else:
                                    updated_count += 1
                            else:
                                model_class.objects.create(**data)
                                created_count += 1
                        else:
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


@admin.register(PlayersGeneralTraditional)
class PlayersGeneralTraditionalAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralAdvanced)
class PlayersGeneralAdvancedAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralMisc)
class PlayersGeneralMiscAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralScoring)
class PlayersGeneralScoringAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralUsage)
class PlayersGeneralUsageAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralOpponent)
class PlayersGeneralOpponentAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "vs_player_name", "player_id", "team_abb"]
    search_fields = ["vs_player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralDefense)
class PlayersGeneralDefenseAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralViolations)
class PlayersGeneralViolationsAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersGeneralEstimatedAdvanced)
class PlayersGeneralEstimatedAdvancedAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id"]
    search_fields = ["player_name", "player_id"]
    list_filter = ["season", "season_type"]
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


@admin.register(PlayersClutchTraditional)
class PlayersClutchTraditionalAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersClutchAdvanced)
class PlayersClutchAdvancedAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersClutchMisc)
class PlayersClutchMiscAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersClutchScoring)
class PlayersClutchScoringAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersClutchUsage)
class PlayersClutchUsageAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeIsolation)
class PlayersPlaytypeIsolationAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeTransition)
class PlayersPlaytypeTransitionAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeBallHandler)
class PlayersPlaytypeBallHandlerAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeRollMan)
class PlayersPlaytypeRollManAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypePostUp)
class PlayersPlaytypePostUpAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeSpotUp)
class PlayersPlaytypeSpotUpAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeHandOff)
class PlayersPlaytypeHandOffAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeCut)
class PlayersPlaytypeCutAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeOffScreen)
class PlayersPlaytypeOffScreenAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypePutbacks)
class PlayersPlaytypePutbacksAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersPlaytypeMisc)
class PlayersPlaytypeMiscAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingDrives)
class PlayersTrackingDrivesAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingDefensiveImpact)
class PlayersTrackingDefensiveImpactAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingCatchShoot)
class PlayersTrackingCatchShootAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingPassing)
class PlayersTrackingPassingAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingTouches)
class PlayersTrackingTouchesAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingPullup)
class PlayersTrackingPullupAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingRebounding)
class PlayersTrackingReboundingAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingOffensiveRebounding)
class PlayersTrackingOffensiveReboundingAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingDefensiveRebounding)
class PlayersTrackingDefensiveReboundingAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingShootingEfficiency)
class PlayersTrackingShootingEfficiencyAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingSpeedDistance)
class PlayersTrackingSpeedDistanceAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingElbowTouch)
class PlayersTrackingElbowTouchAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingPostUps)
class PlayersTrackingPostUpsAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersTrackingPaintTouch)
class PlayersTrackingPaintTouchAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersDefenseDashboardOverall)
class PlayersDefenseDashboardOverallAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersDefenseDashboard3pt)
class PlayersDefenseDashboard3ptAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersDefenseDashboard2pt)
class PlayersDefenseDashboard2ptAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersDefenseDashboardLt6)
class PlayersDefenseDashboardLt6Admin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersDefenseDashboardLt10)
class PlayersDefenseDashboardLt10Admin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersDefenseDashboardGt15)
class PlayersDefenseDashboardGt15Admin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersShotDashboardGeneral)
class PlayersShotDashboardGeneralAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersShotDashboardShotClock)
class PlayersShotDashboardShotClockAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersShotDashboardDribbles)
class PlayersShotDashboardDribblesAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersShotDashboardTouchTime)
class PlayersShotDashboardTouchTimeAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersShotDashboardClosestDefender)
class PlayersShotDashboardClosestDefenderAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersShotDashboardClosestDefender10)
class PlayersShotDashboardClosestDefender10Admin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersBoxScores)
class PlayersBoxScoresAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersAdvancedBoxScoresTraditional)
class PlayersAdvancedBoxScoresTraditionalAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersAdvancedBoxScoresAdvanced)
class PlayersAdvancedBoxScoresAdvancedAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersAdvancedBoxScoresMisc)
class PlayersAdvancedBoxScoresMiscAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersAdvancedBoxScoresScoring)
class PlayersAdvancedBoxScoresScoringAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersAdvancedBoxScoresUsage)
class PlayersAdvancedBoxScoresUsageAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersShooting)
class PlayersShootingAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersDunkScores)
class PlayersDunkScoresAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "playername", "player_id", "team_abb"]
    search_fields = ["playername", "player_id", "team_abb"]
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


@admin.register(PlayersOpponentShootingOverall)
class PlayersOpponentShootingOverallAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersHustle)
class PlayersHustleAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersBoxOuts)
class PlayersBoxOutsAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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


@admin.register(PlayersBios)
class PlayersBiosAdmin(ImportExportModelAdmin):
    list_display = ["season", "season_type", "player_name", "player_id", "team_abb"]
    search_fields = ["player_name", "player_id", "team_abb"]
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
