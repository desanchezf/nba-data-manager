from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from import_export.admin import ImportExportModelAdmin

from .models import (
    ChatMessage,
    ChatSession,
    OllamaModelConfig,
    OllamaServer,
    PredictionModel,
    SystemPrompt,
)


# ─── PredictionModel ──────────────────────────────────────────────────────────

@admin.register(PredictionModel)
class PredictionModelAdmin(ImportExportModelAdmin):
    list_display = ["name", "algorithm_type", "problem_type", "version", "is_active", "trained_at", "created_at"]
    list_filter = ["algorithm_type", "problem_type", "is_active", "trained_at", "created_at"]
    search_fields = ["name", "description", "algorithm_type"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Información Básica", {"fields": ("name", "description", "version", "is_active")}),
        ("Configuración del Modelo", {"fields": ("algorithm_type", "problem_type", "model_file")}),
        ("Métricas y Configuración", {"fields": ("metrics", "hyperparameters", "training_data_info"), "classes": ("collapse",)}),
        ("Fechas", {"fields": ("trained_at", "created_at", "updated_at"), "classes": ("collapse",)}),
    )
    date_hierarchy = "created_at"
    ordering = ["-created_at"]


# ─── SystemPrompt ─────────────────────────────────────────────────────────────

@admin.register(SystemPrompt)
class SystemPromptAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "content")
    readonly_fields = ("created_at", "updated_at")
    fields = ("name", "description", "content", "is_active", "created_at", "updated_at")


# ─── OllamaServer ─────────────────────────────────────────────────────────────

@admin.register(OllamaServer)
class OllamaServerAdmin(ImportExportModelAdmin):
    list_display = ("name", "base_url", "enabled", "created_at")
    list_filter = ("enabled",)
    change_list_template = "admin/ia/ollamaserver/change_list.html"

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        custom = [
            path(
                "pull-model/",
                self.admin_site.admin_view(self.pull_model_view),
                name="%s_%s_pullmodel" % info,
            ),
        ]
        return custom + urls

    def pull_model_view(self, request):
        if not self.has_change_permission(request):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied

        from .ollama_utils import ollama_pull, resolve_ollama_base_url

        servers = list(OllamaServer.objects.filter(enabled=True).order_by("name"))
        if request.method == "POST":
            sid = request.POST.get("server_id")
            model_name = (request.POST.get("model_name") or "").strip()
            server = None
            if sid:
                server = OllamaServer.objects.filter(pk=sid).first()
            if not server:
                messages.error(request, "Seleccione un servidor válido.")
            elif not model_name:
                messages.error(request, "Indique el nombre del modelo (ej. llama3.2, qwen2.5-coder).")
            else:
                base = resolve_ollama_base_url(server.base_url)
                ok, msg = ollama_pull(base, model_name)
                if ok:
                    messages.success(request, f"Modelo «{model_name}» en «{server.name}»: {msg}")
                else:
                    messages.error(request, f"No se pudo descargar «{model_name}»: {msg}")
            return redirect("admin:ia_ollamaserver_changelist")

        context = {
            **self.admin_site.each_context(request),
            "title": "Descargar modelo (Ollama pull)",
            "opts": self.model._meta,
            "servers": servers,
            "has_view_permission": self.has_view_permission(request),
        }
        return TemplateResponse(request, "admin/ia/ollamaserver/pull_model.html", context)


# ─── OllamaModelConfig ────────────────────────────────────────────────────────

@admin.register(OllamaModelConfig)
class OllamaModelConfigAdmin(ImportExportModelAdmin):
    list_display = (
        "alias", "server", "model_name",
        "ollama_installed", "ollama_up_to_date", "ollama_sync_at",
        "is_default", "deprecated", "temperature", "max_tokens",
    )
    list_filter = ("server", "is_default", "deprecated", "ollama_installed", "ollama_up_to_date")
    readonly_fields = (
        "ollama_sync_at", "ollama_installed", "ollama_local_digest",
        "ollama_registry_digest", "ollama_up_to_date", "ollama_sync_detail",
        "created_at", "updated_at",
    )
    actions = ["pull_selected_models"]

    @admin.action(description="Descargar modelos seleccionados en Ollama (pull)")
    def pull_selected_models(self, request, queryset):
        from .ollama_utils import ollama_pull, resolve_ollama_base_url

        ok_count = 0
        err_count = 0
        for cfg in queryset.select_related("server"):
            if not cfg.server or not cfg.server.enabled:
                messages.warning(request, f"Servidor no disponible para «{cfg.alias}». Omitido.")
                err_count += 1
                continue
            base = resolve_ollama_base_url(cfg.server.base_url)
            ok, msg = ollama_pull(base, cfg.model_name)
            if ok:
                messages.success(request, f"«{cfg.alias}» ({cfg.model_name}) descargado: {msg}")
                ok_count += 1
            else:
                messages.error(request, f"Error al descargar «{cfg.alias}»: {msg}")
                err_count += 1


# ─── ChatSession / ChatMessage ────────────────────────────────────────────────

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ("role", "content", "created_at")
    can_delete = True


@admin.register(ChatSession)
class ChatSessionAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "model_key", "created_at", "updated_at")
    list_filter = ("user",)
    search_fields = ("user__username", "model_key")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(ImportExportModelAdmin):
    list_display = ("id", "session", "role", "content_preview", "created_at")
    list_filter = ("role", "session__user")
    search_fields = ("content",)
    readonly_fields = ("session", "role", "content", "created_at")

    def content_preview(self, obj):
        raw = obj.content or ""
        return raw[:80] + ("..." if len(raw) > 80 else "")
    content_preview.short_description = "Contenido"
