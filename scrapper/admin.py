from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.contrib import messages
from unfold.admin import ModelAdmin
from unfold.decorators import action
from scrapper.models import ScrapperLogs


@admin.register(ScrapperLogs)
class ScrapperLogsAdmin(ModelAdmin):
    list_display = ("url", "category", "season", "season_type", "status", "created_at")
    search_fields = ("url", "category", "season", "season_type")
    list_filter = ("status", "created_at", "category", "season", "season_type")
    ordering = ("-created_at",)

    # Lista de acciones disponibles
    actions_list = [
        "execute_scrapper",
        "reprocess_selected",
        "export_to_csv",
        "mark_as_processed",
        "delete_old_logs",
    ]

    @action(description="🚀 Ejecutar Scrapper", icon="play_arrow")
    def execute_scrapper(self, request: HttpRequest, queryset: QuerySet):
        """Ejecutar scraper para URLs seleccionadas"""
        urls = list(queryset.values_list("url", flat=True))

        try:
            # Aquí iría la lógica para ejecutar el scraper
            # Por ejemplo, llamar a un comando de management
            from django.core.management import call_command

            call_command("run_scraper", urls=urls, verbosity=2)

            self.message_user(
                request,
                f"✅ Se ejecutó el scraper para {len(urls)} URLs.",
                messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request, f"❌ Error al ejecutar scraper: {str(e)}", messages.ERROR
            )

    @action(description="🔄 Re-procesar Logs", icon="refresh")
    def reprocess_selected(self, request: HttpRequest, queryset: QuerySet):
        """Re-procesar logs seleccionados"""
        count = 0
        for log in queryset:
            if log.status != "success":
                log.status = "pending"
                log.save()
                count += 1

        self.message_user(
            request,
            f"🔄 Se marcaron {count} logs para re-procesamiento.",
            messages.SUCCESS,
        )

    @action(description="📊 Exportar CSV", icon="download")
    def export_to_csv(self, request: HttpRequest, queryset: QuerySet):
        """Exportar logs seleccionados a CSV"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="scrapper_logs.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ["URL", "Category", "Season", "Season Type", "Status", "Created At"]
        )

        for log in queryset:
            writer.writerow(
                [
                    log.url,
                    log.category,
                    log.season,
                    log.season_type,
                    log.status,
                    log.created_at,
                ]
            )

        return response

    @action(description="✅ Marcar como Procesados", icon="check_circle")
    def mark_as_processed(self, request: HttpRequest, queryset: QuerySet):
        """Marcar logs como procesados exitosamente"""
        updated = queryset.update(status="success")
        self.message_user(
            request, f"✅ Se marcaron {updated} logs como procesados.", messages.SUCCESS
        )

    @action(description="🗑️ Eliminar Logs Antiguos", icon="delete")
    def delete_old_logs(self, request: HttpRequest, queryset: QuerySet):
        """Eliminar logs más antiguos de 30 días"""
        from datetime import datetime, timedelta

        old_date = datetime.now() - timedelta(days=30)
        old_logs = queryset.filter(created_at__lt=old_date)
        count = old_logs.count()
        old_logs.delete()

        self.message_user(
            request, f"🗑️ Se eliminaron {count} logs antiguos.", messages.SUCCESS
        )
