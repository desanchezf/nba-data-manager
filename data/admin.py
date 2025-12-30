from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
from django.db import transaction, models
import csv
from io import StringIO
from django.template.response import TemplateResponse

from data.models import (
    GameBoxscoreTraditional,
    GamePlayByPlay,
    GameSummary,
    TeamBoxscoreTraditional,
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


@admin.register(GameBoxscoreTraditional)
class GameBoxscoreTraditionalAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "player_name",
        "player_team_abb",
        "period",
        "pts",
        "reb",
        "ast",
    )
    search_fields = (
        "game_id",
        "player_name",
        "player_name_abb",
        "player_team_abb",
        "home_team_abb",
        "away_team_abb",
        "season",
    )
    list_filter = (
        "season",
        "season_type",
        "home_team_abb",
        "away_team_abb",
        "player_team_abb",
        "player_pos",
        "period",
        "player_dnp",
    )
    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.import_csv_view,
                name="data_gameboxscoretraditional_import_csv",
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        """Vista para importar CSV"""
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            try:
                decoded_file = csv_file.read().decode("utf-8")
                io_string = StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                created_count = 0
                updated_count = 0
                errors = []

                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            # Obtener todos los campos del modelo
                            data = {}
                            for field in GameBoxscoreTraditional._meta.fields:
                                field_name = field.name
                                if field_name in row:
                                    value = row[field_name].strip()

                                    # Manejar tipos de datos
                                    if isinstance(field, models.BooleanField):
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
                                        data[field_name] = (
                                            float(value) if value else 0.0
                                        )
                                    else:
                                        data[field_name] = value if value else ""

                            # Crear o actualizar usando game_id, player_id, period como clave única
                            game_id = data.get("game_id", "")
                            player_id = data.get("player_id", 0)
                            period = data.get("period", "")

                            if not game_id or not player_id or not period:
                                errors.append(
                                    f"Fila {row_num}: game_id, player_id y period son requeridos"
                                )
                                continue

                            obj, created = (
                                GameBoxscoreTraditional.objects.update_or_create(
                                    game_id=game_id,
                                    player_id=player_id,
                                    period=period,
                                    defaults=data,
                                )
                            )

                            if created:
                                created_count += 1
                            else:
                                updated_count += 1

                        except Exception as e:
                            errors.append(f"Fila {row_num}: {str(e)}")
                            continue

                if created_count > 0:
                    messages.success(
                        request, f"Se crearon {created_count} registros exitosamente."
                    )
                if updated_count > 0:
                    messages.success(
                        request,
                        f"Se actualizaron {updated_count} registros exitosamente.",
                    )
                if errors:
                    for error in errors[:10]:
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f"Y {len(errors) - 10} errores más.")

                return redirect("admin:data_gameboxscoretraditional_changelist")

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
                return redirect("admin:data_gameboxscoretraditional_changelist")

        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:data_gameboxscoretraditional_import_csv",
            },
        )


@admin.register(GamePlayByPlay)
class GamePlayByPlayAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "team_abb",
        "period",
        "min",
        "player",
        "action",
    )
    search_fields = (
        "game_id",
        "player",
        "action",
        "team_abb",
        "season",
        "score",
    )
    list_filter = (
        "season",
        "season_type",
        "team_abb",
        "period",
    )
    readonly_fields = ("created_at", "updated_at")
    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.import_csv_view,
                name="data_gameplaybyplay_import_csv",
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        """Vista para importar CSV"""
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            try:
                decoded_file = csv_file.read().decode("utf-8")
                io_string = StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                created_count = 0
                errors = []

                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            data = {}
                            for field in GamePlayByPlay._meta.fields:
                                field_name = field.name
                                if field_name in row:
                                    value = row[field_name].strip()
                                    if isinstance(field, models.BooleanField):
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
                                        data[field_name] = (
                                            float(value) if value else 0.0
                                        )
                                    else:
                                        data[field_name] = value if value else ""

                            # Usar game_id, team_abb, period, min como clave única aproximada
                            game_id = data.get("game_id", "")
                            if not game_id:
                                errors.append(f"Fila {row_num}: game_id es requerido")
                                continue

                            # Crear nuevo registro
                            # (GamePlayByPlay puede tener múltiples registros)
                            GamePlayByPlay.objects.create(**data)
                            created_count += 1

                        except Exception as e:
                            errors.append(f"Fila {row_num}: {str(e)}")
                            continue

                if created_count > 0:
                    messages.success(
                        request, f"Se crearon {created_count} registros exitosamente."
                    )
                if errors:
                    for error in errors[:10]:
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f"Y {len(errors) - 10} errores más.")

                return redirect("admin:data_gameplaybyplay_changelist")

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
                return redirect("admin:data_gameplaybyplay_changelist")

        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:data_gameplaybyplay_import_csv",
            },
        )


@admin.register(GameSummary)
class GameSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "team_abb",
        "final",
        "q1",
        "q2",
        "q3",
        "q4",
        "lead_changes",
        "times_tied",
    )
    search_fields = (
        "game_id",
        "team_abb",
        "season",
    )
    list_filter = (
        "season",
        "season_type",
        "team_abb",
    )
    readonly_fields = ("created_at", "updated_at")
    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/", self.import_csv_view, name="data_gamesummary_import_csv"
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        """Vista para importar CSV"""
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            try:
                decoded_file = csv_file.read().decode("utf-8")
                io_string = StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                created_count = 0
                updated_count = 0
                errors = []

                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            data = {}
                            for field in GameSummary._meta.fields:
                                field_name = field.name
                                if field_name in row:
                                    value = row[field_name].strip()
                                    if isinstance(field, models.BooleanField):
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
                                        data[field_name] = (
                                            float(value) if value else 0.0
                                        )
                                    else:
                                        data[field_name] = value if value else ""

                            game_id = data.get("game_id", "")
                            team_abb = data.get("team_abb", "")

                            if not game_id or not team_abb:
                                errors.append(
                                    f"Fila {row_num}: game_id y team_abb son requeridos"
                                )
                                continue

                            obj, created = GameSummary.objects.update_or_create(
                                game_id=game_id, team_abb=team_abb, defaults=data
                            )

                            if created:
                                created_count += 1
                            else:
                                updated_count += 1

                        except Exception as e:
                            errors.append(f"Fila {row_num}: {str(e)}")
                            continue

                if created_count > 0:
                    messages.success(
                        request, f"Se crearon {created_count} registros exitosamente."
                    )
                if updated_count > 0:
                    messages.success(
                        request,
                        f"Se actualizaron {updated_count} registros exitosamente.",
                    )
                if errors:
                    for error in errors[:10]:
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f"Y {len(errors) - 10} errores más.")

                return redirect("admin:data_gamesummary_changelist")

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
                return redirect("admin:data_gamesummary_changelist")

        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:data_gamesummary_import_csv",
            },
        )


@admin.register(TeamBoxscoreTraditional)
class TeamBoxscoreTraditionalAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "team_abb",
        "matchup",
        "home_away",
        "wl",
        "pts",
        "fg_pct",
        "reb",
        "ast",
        "plus_minus",
    )
    search_fields = (
        "game_id",
        "team_abb",
        "matchup",
        "season",
        "gdate",
    )
    list_filter = (
        "season",
        "season_type",
        "team_abb",
        "home_away",
        "wl",
        "gdate",
    )
    readonly_fields = ("created_at", "updated_at")
    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.import_csv_view,
                name="data_teamboxscoretraditional_import_csv",
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        """Vista para importar CSV"""
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            try:
                decoded_file = csv_file.read().decode("utf-8")
                io_string = StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                created_count = 0
                updated_count = 0
                errors = []

                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            data = {}
                            for field in TeamBoxscoreTraditional._meta.fields:
                                field_name = field.name
                                if field_name in row:
                                    value = row[field_name].strip()
                                    if isinstance(field, models.BooleanField):
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
                                        data[field_name] = (
                                            float(value) if value else 0.0
                                        )
                                    else:
                                        data[field_name] = value if value else ""

                            game_id = data.get("game_id", "")
                            team_abb = data.get("team_abb", "")

                            if not game_id or not team_abb:
                                errors.append(
                                    f"Fila {row_num}: game_id y team_abb son requeridos"
                                )
                                continue

                            obj, created = (
                                TeamBoxscoreTraditional.objects.update_or_create(
                                    game_id=game_id, team_abb=team_abb, defaults=data
                                )
                            )

                            if created:
                                created_count += 1
                            else:
                                updated_count += 1

                        except Exception as e:
                            errors.append(f"Fila {row_num}: {str(e)}")
                            continue

                if created_count > 0:
                    messages.success(
                        request, f"Se crearon {created_count} registros exitosamente."
                    )
                if updated_count > 0:
                    messages.success(
                        request,
                        f"Se actualizaron {updated_count} registros exitosamente.",
                    )
                if errors:
                    for error in errors[:10]:
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f"Y {len(errors) - 10} errores más.")

                return redirect("admin:data_teamboxscoretraditional_changelist")

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
                return redirect("admin:data_teamboxscoretraditional_changelist")

        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:data_teamboxscoretraditional_import_csv",
            },
        )
