"""
Admin para Game Boxscore Traditional y Advanced con import/export CSV.
Mapeo de cabeceras CSV a campos del modelo (ej. 3PM->fg3m, OFFRTG->off_rtg).
"""

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
from django.db import transaction, models
import csv
from io import StringIO
from django.template.response import TemplateResponse

from game_boxscore.models import GameBoxscoreTraditional, GameBoxscoreAdvanced


# Mapeo cabecera CSV (normalizada a minúsculas) -> campo modelo
# CSV: GAME_ID, SEASON, ..., FGM, FGA, FG_PERC, 3PM, 3PA, 3P_PERC, FTM, FTA, FT_PERC, ...
CSV_TRADITIONAL_MAP = {
    "3pm": "fg3m",
    "3pa": "fg3a",
    "3p_perc": "fg3_pct",
    "fg_perc": "fg_pct",
    "ft_perc": "ft_pct",
}

CSV_ADVANCED_MAP = {
    "offrtg": "off_rtg",
    "defrtg": "def_rtg",
    "netrtg": "net_rtg",
    "ast_perc": "ast_pct",
    "ast_to": "ast_to",
    "ast_ratio": "ast_ratio",
    "oreb_perc": "oreb_pct",
    "dreb_perc": "dreb_pct",
    "reb_perc": "reb_pct",
    "to_ratio": "to_ratio",
    "efg_perc": "efg_pct",
    "ts_perc": "ts_pct",
    "usg_perc": "usg_pct",
    "pace": "pace",
    "pie": "pie",
}


def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [f.name for f in meta.fields]
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f"attachment; filename={meta.verbose_name_plural}.csv"
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = []
        for field in meta.fields:
            value = getattr(obj, field.name)
            if hasattr(value, "__str__") and not isinstance(value, str):
                value = str(value)
            if value is None:
                value = ""
            row.append(value)
        writer.writerow(row)
    return response


export_as_csv.short_description = "Exportar seleccionados a CSV"


def _normalize_row(row, field_map):
    """Convierte fila CSV (keys pueden ser MAYUS, 3PM, etc.) a dict con keys = nombres de modelo."""
    out = {}
    for k, v in row.items():
        key = k.strip().lower().replace(" ", "_")
        if key in field_map:
            key = field_map[key]
        out[key] = v.strip() if v else ""
    return out


def _set_model_data_from_row(model_class, row_normalized, data):
    meta = model_class._meta
    for field_name in [f.name for f in meta.fields]:
        if field_name not in row_normalized:
            continue
        value = row_normalized[field_name]
        field = meta.get_field(field_name)
        if isinstance(field, models.BooleanField):
            data[field_name] = value.lower() in ("true", "1", "yes", "sí", "si")
        elif isinstance(field, models.IntegerField):
            try:
                data[field_name] = int(float(value)) if value else 0
            except (ValueError, TypeError):
                data[field_name] = 0
        elif isinstance(field, models.FloatField):
            try:
                data[field_name] = float(value) if value else 0.0
            except (ValueError, TypeError):
                data[field_name] = 0.0
        else:
            data[field_name] = value or ""


@admin.register(GameBoxscoreTraditional)
class GameBoxscoreTraditionalAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "player_name",
        "player_team_abb",
        "period",
        "min",
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
                name="game_boxscore_gameboxscoretraditional_import_csv",
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]
            try:
                decoded = csv_file.read().decode("utf-8")
                reader = csv.DictReader(StringIO(decoded))
                created_count = 0
                updated_count = 0
                errors = []
                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            row_norm = _normalize_row(row, CSV_TRADITIONAL_MAP)
                            data = {}
                            _set_model_data_from_row(GameBoxscoreTraditional, row_norm, data)
                            game_id = data.get("game_id", "")
                            player_id = data.get("player_id", 0)
                            period = data.get("period", "")
                            if not game_id or not period:
                                errors.append(f"Fila {row_num}: game_id y period requeridos")
                                continue
                            _, created = GameBoxscoreTraditional.objects.update_or_create(
                                game_id=game_id,
                                player_id=player_id,
                                period=period,
                                defaults=data,
                            )
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                        except Exception as e:
                            errors.append(f"Fila {row_num}: {str(e)}")
                if created_count > 0:
                    messages.success(request, f"Creados {created_count} registros.")
                if updated_count > 0:
                    messages.success(request, f"Actualizados {updated_count} registros.")
                for err in errors[:10]:
                    messages.error(request, err)
                if len(errors) > 10:
                    messages.warning(request, f"Y {len(errors) - 10} errores más.")
                return redirect("admin:game_boxscore_gameboxscoretraditional_changelist")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect("admin:game_boxscore_gameboxscoretraditional_changelist")
        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:game_boxscore_gameboxscoretraditional_import_csv",
            },
        )


@admin.register(GameBoxscoreAdvanced)
class GameBoxscoreAdvancedAdmin(admin.ModelAdmin):
    list_display = (
        "game_id",
        "season",
        "season_type",
        "player_name",
        "player_team_abb",
        "period",
        "min",
        "off_rtg",
        "def_rtg",
        "net_rtg",
        "ts_pct",
        "pie",
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
                name="game_boxscore_gameboxscoreadvanced_import_csv",
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]
            try:
                decoded = csv_file.read().decode("utf-8")
                reader = csv.DictReader(StringIO(decoded))
                created_count = 0
                updated_count = 0
                errors = []
                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            row_norm = _normalize_row(row, CSV_ADVANCED_MAP)
                            data = {}
                            _set_model_data_from_row(GameBoxscoreAdvanced, row_norm, data)
                            game_id = data.get("game_id", "")
                            player_id = data.get("player_id", 0)
                            period = data.get("period", "")
                            if not game_id or not period:
                                errors.append(f"Fila {row_num}: game_id y period requeridos")
                                continue
                            _, created = GameBoxscoreAdvanced.objects.update_or_create(
                                game_id=game_id,
                                player_id=player_id,
                                period=period,
                                defaults=data,
                            )
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                        except Exception as e:
                            errors.append(f"Fila {row_num}: {str(e)}")
                if created_count > 0:
                    messages.success(request, f"Creados {created_count} registros.")
                if updated_count > 0:
                    messages.success(request, f"Actualizados {updated_count} registros.")
                for err in errors[:10]:
                    messages.error(request, err)
                if len(errors) > 10:
                    messages.warning(request, f"Y {len(errors) - 10} errores más.")
                return redirect("admin:game_boxscore_gameboxscoreadvanced_changelist")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect("admin:game_boxscore_gameboxscoreadvanced_changelist")
        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:game_boxscore_gameboxscoreadvanced_import_csv",
            },
        )
