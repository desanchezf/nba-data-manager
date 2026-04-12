"""
Admin del módulo predictions NBA:
  - PredictionAdmin / PredictionsHistoryAdmin → predicciones básicas
  - PredictionLogAdmin → log de predicciones ML
  - BettingRecordAdmin → registro contable de apuestas + Prediction Hub
    URLs del Hub:
      /admin/predictions/bettingrecord/hub/              → página principal
      /admin/predictions/bettingrecord/hub/prepartido/   → pre-partido
      /admin/predictions/bettingrecord/hub/live/         → en directo
      /admin/predictions/bettingrecord/hub/discovery/    → prediction discovery
      /admin/predictions/bettingrecord/hub/combinada/    → apuesta combinada
"""

from django.contrib import admin, messages
from django.db.models import Count, Sum
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import (
    BettingRecord,
    Prediction,
    PredictionLog,
    PredictionsHistory,
)


# ─── Prediction / PredictionsHistory ─────────────────────────────────────────

class PredictionsHistoryInline(admin.TabularInline):
    model = PredictionsHistory
    extra = 0
    readonly_fields = ["created_at", "updated_at"]
    fields = ["odds", "result", "failure", "failure_reason", "created_at"]


@admin.register(Prediction)
class PredictionAdmin(ImportExportModelAdmin):
    list_display = [
        "matchup", "home_team", "away_team",
        "prediction_type", "prediction_category", "prediction_market",
        "prediction_model", "matchup_date", "created_at",
    ]
    list_filter = [
        "prediction_type", "prediction_category", "prediction_market",
        "prediction_model", "matchup_date", "created_at",
    ]
    search_fields = ["matchup", "home_team", "away_team", "prediction_model__name"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["prediction_model"]
    date_hierarchy = "matchup_date"
    ordering = ["-matchup_date", "-created_at"]
    inlines = [PredictionsHistoryInline]
    fieldsets = (
        ("Información del Partido", {"fields": ("matchup", "home_team", "away_team", "matchup_date")}),
        ("Configuración", {"fields": ("prediction_type", "prediction_category", "prediction_market", "prediction_model")}),
        ("Fechas", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(PredictionsHistory)
class PredictionsHistoryAdmin(ImportExportModelAdmin):
    list_display = ["prediction", "odds", "result", "failure", "created_at"]
    list_filter = ["failure", "created_at", "prediction__prediction_type"]
    search_fields = ["prediction__matchup", "result"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"


# ─── PredictionLog ────────────────────────────────────────────────────────────

@admin.register(PredictionLog)
class PredictionLogAdmin(ImportExportModelAdmin):
    list_display = ("game_id", "market", "predicted_value", "actual_result", "actual_home_win", "created_at")
    list_filter = ("market", "created_at")
    search_fields = ("game_id",)
    date_hierarchy = "created_at"


# ─── BettingRecord + Prediction Hub ──────────────────────────────────────────

@admin.register(BettingRecord)
class BettingRecordAdmin(ImportExportModelAdmin):
    list_display = (
        "created_at_short", "prediction_mode", "market", "selection_short",
        "odds_decimal", "stake_euros", "units", "risk_level",
        "result_badge", "pnl_euros", "roi_display",
    )
    list_filter = ("prediction_mode", "result", "risk_level", "market", "bet_type")
    search_fields = ("selection", "home_team", "away_team", "game_id", "notes")
    date_hierarchy = "created_at"
    readonly_fields = ("pnl_euros", "created_at", "roi_display_readonly", "pnl_units_display")
    fieldsets = (
        ("Contexto", {
            "fields": (
                ("prediction_mode", "bet_type", "risk_level"),
                ("game_id", "market"),
                ("home_team", "away_team", "match_date"),
            )
        }),
        ("Selección apostada", {
            "fields": (
                "selection",
                ("odds_decimal", "stake_euros", "units"),
                ("prob_predicted", "ev_predicted"),
            )
        }),
        ("Combinada", {
            "classes": ("collapse",),
            "fields": ("selections_json",),
        }),
        ("Resultado & Contabilidad", {
            "fields": (
                ("result", "settled_at"),
                ("pnl_euros", "roi_display_readonly", "pnl_units_display"),
            )
        }),
        ("Notas", {"fields": ("notes",)}),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("hub/", self.admin_site.admin_view(self.hub_view), name="predictions_prediction_hub"),
            path("hub/prepartido/", self.admin_site.admin_view(self.prepartido_view), name="predictions_hub_prepartido"),
            path("hub/live/", self.admin_site.admin_view(self.live_view), name="predictions_hub_live"),
            path("hub/discovery/", self.admin_site.admin_view(self.discovery_view), name="predictions_hub_discovery"),
            path("hub/combinada/", self.admin_site.admin_view(self.combinada_view), name="predictions_hub_combinada"),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["hub_url"] = reverse("admin:predictions_prediction_hub")
        extra_context["accounting"] = self._get_accounting()
        return super().changelist_view(request, extra_context=extra_context)

    def _get_accounting(self):
        qs = BettingRecord.objects.exclude(result="pending")
        agg = qs.aggregate(
            total_bets=Count("id"),
            total_staked=Sum("stake_euros"),
            total_pnl=Sum("pnl_euros"),
        )
        total_bets = agg["total_bets"] or 0
        won = qs.filter(result="win").count()
        total_staked = float(agg["total_staked"] or 0)
        total_pnl = float(agg["total_pnl"] or 0)
        roi = round(total_pnl / total_staked * 100, 2) if total_staked else None
        winrate = round(won / total_bets * 100, 1) if total_bets else None
        return {
            "total_bets": total_bets,
            "won": won,
            "lost": qs.filter(result="loss").count(),
            "void": qs.filter(result="void").count(),
            "pending": BettingRecord.objects.filter(result="pending").count(),
            "winrate": winrate,
            "total_staked": round(total_staked, 2),
            "total_pnl": round(total_pnl, 2),
            "roi": roi,
        }

    # ── Display helpers ───────────────────────────────────────────────────────

    @admin.display(description="Fecha")
    def created_at_short(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M") if obj.created_at else "-"

    @admin.display(description="Selección")
    def selection_short(self, obj):
        s = obj.selection or ""
        return s[:50] + "…" if len(s) > 50 else s

    @admin.display(description="Resultado")
    def result_badge(self, obj):
        colors = {
            "win": "#28a745", "loss": "#dc3545",
            "void": "#6c757d", "pending": "#ffc107",
        }
        color = colors.get(obj.result, "#6c757d")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:0.85em">{}</span>',
            color, obj.get_result_display(),
        )

    @admin.display(description="ROI %")
    def roi_display(self, obj):
        v = obj.roi_pct
        if v is None:
            return "-"
        color = "green" if v > 0 else ("red" if v < 0 else "gray")
        return format_html('<span style="color:{}">{:+.1f}%</span>', color, v)

    @admin.display(description="ROI %")
    def roi_display_readonly(self, obj):
        return self.roi_display(obj)

    @admin.display(description="P&L (unidades)")
    def pnl_units_display(self, obj):
        v = obj.pnl_units
        return f"{v:+.2f}" if v is not None else "-"

    # ── Hub views ─────────────────────────────────────────────────────────────

    def _admin_context(self, request, title, extra=None):
        ctx = self.admin_site.each_context(request)
        ctx.update({
            "title": title,
            "opts": self.model._meta,
            "app_label": self.model._meta.app_label,
        })
        if extra:
            ctx.update(extra)
        return ctx

    def hub_view(self, request):
        ctx = self._admin_context(request, "Prediction Hub", {
            "hub_url": reverse("admin:predictions_prediction_hub"),
            "prepartido_url": reverse("admin:predictions_hub_prepartido"),
            "live_url": reverse("admin:predictions_hub_live"),
            "discovery_url": reverse("admin:predictions_hub_discovery"),
            "combinada_url": reverse("admin:predictions_hub_combinada"),
            "accounting": self._get_accounting(),
        })
        return render(request, "admin/predictions/prediction_hub.html", ctx)

    def prepartido_view(self, request):
        from core.models import Team
        from .forms import PreMatchForm
        from .admin_views import run_prepartido, save_prepartido_bet

        teams = list(Team.objects.all().order_by("name"))
        team_choices = [("", "-- Seleccione --")] + [
            (t.team_id, t.name or t.team_id) for t in teams
        ]

        form = PreMatchForm(request.POST or None)
        form.fields["home_team"].choices = team_choices
        form.fields["away_team"].choices = team_choices

        predictions = []
        errors = []
        saved_records = []

        if request.method == "POST" and form.is_valid():
            cd = form.cleaned_data
            predictions, errors = run_prepartido(
                home_team_id=cd["home_team"],
                away_team_id=cd["away_team"],
                market=cd["market"],
                risk_level=cd["risk_level"],
                n_predictions=cd["n_predictions"],
                odds_home=cd.get("odds_home"),
                odds_away=cd.get("odds_away"),
                match_date=cd.get("match_date"),
            )
            if cd.get("save_bet") and cd.get("stake_euros") and predictions:
                for p in predictions:
                    rec = save_prepartido_bet(p, cd["stake_euros"], cd["risk_level"])
                    saved_records.append(rec)
                messages.success(request, f"{len(saved_records)} apuesta(s) guardadas.")

        ctx = self._admin_context(request, "Pre-partido", {
            "form": form,
            "predictions": predictions,
            "errors": errors,
            "saved_records": saved_records,
            "hub_url": reverse("admin:predictions_prediction_hub"),
        })
        return render(request, "admin/predictions/prepartido.html", ctx)

    def live_view(self, request):
        from core.models import Team
        from .forms import LivePredictionForm
        from .admin_views import run_live

        teams = list(Team.objects.all().order_by("name"))
        team_choices = [("", "-- Seleccione --")] + [
            (t.team_id, t.name or t.team_id) for t in teams
        ]

        form = LivePredictionForm(request.POST or None)
        form.fields["home_team"].choices = team_choices
        form.fields["away_team"].choices = team_choices

        result = None
        errors = []
        history = request.session.get("live_history_nba", [])

        if request.GET.get("clear_history"):
            request.session.pop("live_history_nba", None)
            history = []
        elif request.method == "POST" and form.is_valid():
            cd = form.cleaned_data
            result, errors = run_live(
                game_id=cd.get("game_id", ""),
                home_team_id=cd["home_team"],
                away_team_id=cd["away_team"],
                market=cd["market"],
                risk_level=cd["risk_level"],
                live_data_json=cd["live_data_json"],
            )
            if result:
                history.append(result)
                request.session["live_history_nba"] = history[-20:]

        ctx = self._admin_context(request, "En directo", {
            "form": form,
            "result": result,
            "errors": errors,
            "history": list(reversed(history[-10:])),
            "hub_url": reverse("admin:predictions_prediction_hub"),
        })
        return render(request, "admin/predictions/live.html", ctx)

    def discovery_view(self, request):
        from .forms import DiscoveryForm
        from .admin_views import run_discovery

        form = DiscoveryForm(request.POST or None)
        predictions = []
        errors = []

        if request.method == "POST" and form.is_valid():
            cd = form.cleaned_data
            predictions, errors = run_discovery(
                matchday_json=cd["matchday_json"],
                market=cd["market"],
                n_top=cd["n_top"],
                risk_level=cd["risk_level"],
            )

        ctx = self._admin_context(request, "Prediction Discovery", {
            "form": form,
            "predictions": predictions,
            "errors": errors,
            "hub_url": reverse("admin:predictions_prediction_hub"),
        })
        return render(request, "admin/predictions/discovery.html", ctx)

    def combinada_view(self, request):
        from .forms import CombinedBetForm
        from .admin_views import run_combinada, save_combined_bet

        form = CombinedBetForm(request.POST or None)
        result = None
        errors = []
        saved_record = None

        if request.method == "POST" and form.is_valid():
            cd = form.cleaned_data
            result = run_combinada(
                matches_json=cd["matches_json"],
                market=cd["market"],
                n_selections=cd["n_selections"],
                risk_level=cd["risk_level"],
                stake_euros=cd.get("stake_euros"),
            )
            errors = result.get("errors", [])
            if cd.get("save_bet") and cd.get("stake_euros") and result.get("selections"):
                saved_record = save_combined_bet(
                    result["selections"],
                    result["summary"],
                    cd["stake_euros"],
                    cd["risk_level"],
                )
                messages.success(request, "Apuesta combinada guardada.")

        ctx = self._admin_context(request, "Apuesta Combinada", {
            "form": form,
            "result": result,
            "errors": errors,
            "saved_record": saved_record,
            "hub_url": reverse("admin:predictions_prediction_hub"),
        })
        return render(request, "admin/predictions/combinada.html", ctx)
