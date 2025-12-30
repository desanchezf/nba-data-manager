from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
from django.db import transaction
import csv
from io import StringIO
from django.template.response import TemplateResponse
from roster.models import Teams, Players


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


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = (
        "team_name",
        "team_abb",
        "team_conference",
        "team_division",
    )
    search_fields = ("team_name", "team_abb", "team_conference", "team_division")
    list_filter = ("team_conference", "team_division")
    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-csv/", self.import_csv_view, name="roster_teams_import_csv"),
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
                            team_id = int(row.get("team_id", 0))
                            team_name = row.get("team_name", "").strip()
                            team_abb = row.get("team_abb", "").strip()
                            team_conference = row.get("team_conference", "").strip()
                            team_division = row.get("team_division", "").strip()

                            if not team_id or not team_name:
                                errors.append(
                                    f"Fila {row_num}: team_id y team_name son requeridos"
                                )
                                continue

                            obj, created = Teams.objects.update_or_create(
                                team_id=team_id,
                                defaults={
                                    "team_name": team_name,
                                    "team_abb": team_abb,
                                    "team_conference": team_conference,
                                    "team_division": team_division,
                                },
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
                        request, f"Se crearon {created_count} equipos exitosamente."
                    )
                if updated_count > 0:
                    messages.success(
                        request,
                        f"Se actualizaron {updated_count} equipos exitosamente.",
                    )
                if errors:
                    for error in errors[:10]:
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f"Y {len(errors) - 10} errores más.")

                return redirect("admin:roster_teams_changelist")

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
                return redirect("admin:roster_teams_changelist")

        # Renderizar formulario simple
        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:roster_teams_import_csv",
            },
        )


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = (
        "player_name",
        "player_abb",
        "team_name",
        "season",
    )
    search_fields = ("player_name", "player_abb", "team__team_name", "season")
    list_filter = ("season", "team", "team__team_conference")
    actions = [export_as_csv]

    def team_name(self, obj):
        return obj.team.team_abb + " - " + obj.team.team_name

    team_name.short_description = "Team name"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_import_button"] = True
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-csv/", self.import_csv_view, name="roster_players_import_csv"),
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
                            player_id = int(row.get("player_id", 0))
                            player_name = row.get("player_name", "").strip()
                            player_abb = row.get("player_abb", "").strip()
                            season = row.get("season", "").strip()

                            # Manejar ForeignKey team
                            team_value = row.get("team", "").strip()
                            if team_value.isdigit():
                                team = Teams.objects.filter(
                                    team_id=int(team_value)
                                ).first()
                            else:
                                # Intentar buscar por team_abb
                                team = Teams.objects.filter(team_abb=team_value).first()

                            if not team:
                                errors.append(
                                    f"Fila {row_num}: No se encontró el equipo '{team_value}'"
                                )
                                continue

                            if not player_id or not player_name or not season:
                                errors.append(
                                    f"Fila {row_num}: player_id, player_name y season son requeridos"
                                )
                                continue

                            obj, created = Players.objects.update_or_create(
                                player_id=player_id,
                                season=season,
                                team=team,
                                defaults={
                                    "player_name": player_name,
                                    "player_abb": player_abb,
                                },
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
                        request, f"Se crearon {created_count} jugadores exitosamente."
                    )
                if updated_count > 0:
                    messages.success(
                        request,
                        f"Se actualizaron {updated_count} jugadores exitosamente.",
                    )
                if errors:
                    for error in errors[:10]:
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f"Y {len(errors) - 10} errores más.")

                return redirect("admin:roster_players_changelist")

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
                return redirect("admin:roster_players_changelist")

        # Renderizar formulario simple
        return TemplateResponse(
            request,
            "admin/import_csv.html",
            {
                "title": "Importar CSV",
                "opts": self.model._meta,
                "has_view_permission": self.has_view_permission(request),
                "import_url": "admin:roster_players_import_csv",
            },
        )
