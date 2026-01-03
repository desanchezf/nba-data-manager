from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.contrib import messages
from django.db import transaction, models
import csv
from io import StringIO
from players.models import (
    PlayersGeneralTraditional, PlayersGeneralAdvanced, PlayersGeneralMisc,
    PlayersGeneralScoring, PlayersGeneralUsage, PlayersGeneralOpponent,
    PlayersGeneralDefense, PlayersGeneralViolations,
    PlayersGeneralEstimatedAdvanced, PlayersClutchTraditional,
    PlayersClutchAdvanced, PlayersClutchMisc, PlayersClutchScoring,
    PlayersClutchUsage, PlayersPlaytypeIsolation, PlayersPlaytypeTransition,
    PlayersPlaytypeBallHandler, PlayersPlaytypeRollMan, PlayersPlaytypePostUp,
    PlayersPlaytypeSpotUp, PlayersPlaytypeHandOff, PlayersPlaytypeCut,
    PlayersPlaytypeOffScreen, PlayersPlaytypePutbacks, PlayersPlaytypeMisc,
    PlayersTrackingDrives, PlayersTrackingDefensiveImpact,
    PlayersTrackingCatchShoot, PlayersTrackingPassing, PlayersTrackingTouches,
    PlayersTrackingPullup, PlayersTrackingRebounding,
    PlayersTrackingOffensiveRebounding, PlayersTrackingDefensiveRebounding,
    PlayersTrackingShootingEfficiency, PlayersTrackingSpeedDistance,
    PlayersTrackingElbowTouch, PlayersTrackingPostUps,
    PlayersTrackingPaintTouch, PlayersDefenseDashboardOverall,
    PlayersDefenseDashboard3pt, PlayersDefenseDashboard2pt,
    PlayersDefenseDashboardLt6, PlayersDefenseDashboardLt10,
    PlayersDefenseDashboardGt15, PlayersShotDashboardGeneral,
    PlayersShotDashboardShotClock, PlayersShotDashboardDribbles,
    PlayersShotDashboardTouchTime, PlayersShotDashboardClosestDefender,
    PlayersShotDashboardClosestDefender10, PlayersBoxScores,
    PlayersAdvancedBoxScoresTraditional, PlayersAdvancedBoxScoresAdvanced,
    PlayersAdvancedBoxScoresMisc, PlayersAdvancedBoxScoresScoring,
    PlayersAdvancedBoxScoresUsage, PlayersShooting, PlayersDunkScores,
    PlayersOpponentShootingOverall, PlayersHustle, PlayersBoxOuts, PlayersBios
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
                        # Preparar datos para crear/actualizar
                        data = {}
                        for field_name in field_names:
                            if field_name in row:
                                value = row[field_name].strip()

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

@admin.register(PlayersGeneralTraditional)
class PlayersGeneralTraditionalAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralAdvancedAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralMiscAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralScoringAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralUsageAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralOpponentAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'vs_player_name', 'player_id', 'team_abb']
    search_fields = ['vs_player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralDefenseAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralViolationsAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersGeneralEstimatedAdvancedAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id']
    search_fields = ['player_name', 'player_id']
    list_filter = ['season', 'season_type']
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
class PlayersClutchTraditionalAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersClutchAdvancedAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersClutchMiscAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersClutchScoringAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersClutchUsageAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeIsolationAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeTransitionAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeBallHandlerAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeRollManAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypePostUpAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeSpotUpAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeHandOffAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeCutAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeOffScreenAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypePutbacksAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersPlaytypeMiscAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingDrivesAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingDefensiveImpactAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingCatchShootAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingPassingAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingTouchesAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingPullupAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingReboundingAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingOffensiveReboundingAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingDefensiveReboundingAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingShootingEfficiencyAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingSpeedDistanceAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingElbowTouchAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingPostUpsAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersTrackingPaintTouchAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersDefenseDashboardOverallAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersDefenseDashboard3ptAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersDefenseDashboard2ptAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersDefenseDashboardLt6Admin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersDefenseDashboardLt10Admin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersDefenseDashboardGt15Admin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersShotDashboardGeneralAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersShotDashboardShotClockAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersShotDashboardDribblesAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersShotDashboardTouchTimeAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersShotDashboardClosestDefenderAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersShotDashboardClosestDefender10Admin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersBoxScoresAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersAdvancedBoxScoresTraditionalAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersAdvancedBoxScoresAdvancedAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersAdvancedBoxScoresMiscAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersAdvancedBoxScoresScoringAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersAdvancedBoxScoresUsageAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersShootingAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersDunkScoresAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'playername', 'player_id', 'team_abb']
    search_fields = ['playername', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersOpponentShootingOverallAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersHustleAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersBoxOutsAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
class PlayersBiosAdmin(admin.ModelAdmin):
    list_display = ['season', 'season_type', 'player_name', 'player_id', 'team_abb']
    search_fields = ['player_name', 'player_id', 'team_abb']
    list_filter = ['season', 'season_type', 'team_abb']
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
