from decimal import Decimal

from django.db import models

from .enums import (
    PredictionCategoryChoices,
    PredictionMarketChoices,
    PredictionTypeChoices,
)
from ia.models import PredictionModel


class Prediction(models.Model):
    matchup = models.CharField(max_length=200)
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    prediction_type = models.CharField(
        max_length=50,
        choices=PredictionTypeChoices.choices(),
        help_text="Tipo de predicción: prepartido o en tiempo real",
    )
    prediction_category = models.CharField(
        max_length=50,
        choices=PredictionCategoryChoices.choices(),
        help_text="Categoría principal de la predicción",
    )
    prediction_market = models.CharField(
        max_length=100,
        choices=PredictionMarketChoices.choices(),
        help_text="Mercado específico de la predicción",
    )
    prediction_model = models.ForeignKey(
        PredictionModel, on_delete=models.CASCADE, related_name="predictions"
    )
    matchup_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-matchup_date", "-created_at"]
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"

    def __str__(self):
        return f"{self.matchup} - {self.get_prediction_market_display()} ({self.matchup_date})"


class PredictionsHistory(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    odds = models.DecimalField(max_digits=10, decimal_places=3)
    result = models.CharField(max_length=200)
    failure = models.BooleanField(default=False)
    failure_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.prediction.matchup} {self.prediction.matchup_date} - {self.result}"
        )


# ──────────────────────────────────────────────────────────────────────────────
# Prediction Hub models
# ──────────────────────────────────────────────────────────────────────────────

class PredictionLog(models.Model):
    """
    Log de predicciones ML para monitoreo y backtesting.
    """

    game_id = models.CharField("GAME_ID", max_length=64, db_index=True)
    market = models.CharField("Mercado", max_length=64, db_index=True)
    predicted_probs = models.JSONField("Probabilidades predichas", default=dict, blank=True)
    predicted_value = models.FloatField("Valor predicho (EV, puntos, etc.)", null=True, blank=True)
    actual_result = models.CharField("Resultado real", max_length=64, blank=True)
    actual_home_win = models.BooleanField("¿Ganó local?", null=True, blank=True)
    odds_used = models.JSONField("Cuotas usadas para EV", default=dict, blank=True)
    model_version = models.CharField("Versión modelo", max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Prediction log"
        verbose_name_plural = "Prediction logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["game_id", "market"]),
            models.Index(fields=["created_at", "market"]),
        ]

    def __str__(self):
        return f"{self.game_id} {self.market}"


class BettingRecord(models.Model):
    """
    Registro contable de apuestas generadas por el Prediction Hub NBA.
    Calcula P&L, ROI y rentabilidad por unidad invertida.
    """

    RISK_CHOICES = [
        ("conservative", "Conservador (≥65%)"),
        ("moderate", "Moderado (≥58%)"),
        ("aggressive", "Arriesgado (≥52%)"),
    ]
    RESULT_CHOICES = [
        ("pending", "Pendiente"),
        ("win", "Ganada"),
        ("loss", "Perdida"),
        ("void", "Anulada/Nula"),
    ]
    BET_TYPE_CHOICES = [
        ("single", "Simple"),
        ("combined", "Combinada/Acumulador"),
    ]
    PREDICTION_MODE_CHOICES = [
        ("prepartido", "Pre-partido"),
        ("live", "En directo"),
        ("discovery", "Prediction Discovery"),
        ("combinada", "Apuesta Combinada"),
    ]

    # Metadata
    prediction_mode = models.CharField(
        "Modo de predicción", max_length=20, choices=PREDICTION_MODE_CHOICES, default="prepartido"
    )
    bet_type = models.CharField(
        "Tipo de apuesta", max_length=20, choices=BET_TYPE_CHOICES, default="single"
    )
    risk_level = models.CharField(
        "Nivel de riesgo", max_length=20, choices=RISK_CHOICES, default="moderate"
    )

    # Game info
    game_id = models.CharField("ID partido", max_length=64, blank=True, db_index=True)
    market = models.CharField("Mercado", max_length=64)
    home_team = models.CharField("Equipo local", max_length=80, blank=True)
    away_team = models.CharField("Equipo visitante", max_length=80, blank=True)
    match_date = models.DateField("Fecha del partido", null=True, blank=True)

    # Bet details
    selection = models.CharField("Selección apostada", max_length=200)
    odds_decimal = models.FloatField("Cuota decimal")
    stake_euros = models.DecimalField("Stake (€)", max_digits=10, decimal_places=2)
    units = models.FloatField("Unidades", default=1.0)

    # Model prediction metadata
    prob_predicted = models.FloatField("Probabilidad predicha (%)", null=True, blank=True)
    ev_predicted = models.FloatField("Valor esperado (EV)", null=True, blank=True)

    # Combined bet selections stored as JSON list of dicts
    selections_json = models.JSONField("Selecciones combinadas", default=list, blank=True)

    # Result & accounting
    result = models.CharField(
        "Resultado", max_length=20, choices=RESULT_CHOICES, default="pending"
    )
    pnl_euros = models.DecimalField(
        "P&L (€)", max_digits=10, decimal_places=2, null=True, blank=True
    )

    notes = models.TextField("Notas", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    settled_at = models.DateTimeField("Fecha liquidación", null=True, blank=True)

    class Meta:
        verbose_name = "Registro de apuesta"
        verbose_name_plural = "Registros de apuestas"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["result", "prediction_mode"]),
            models.Index(fields=["created_at", "risk_level"]),
        ]

    def __str__(self):
        return (
            f"[{self.get_prediction_mode_display()}] {self.market} | "
            f"{self.selection} @ {self.odds_decimal} → {self.get_result_display()}"
        )

    def save(self, *args, **kwargs):
        if self.result == "win" and self.odds_decimal and self.stake_euros is not None:
            self.pnl_euros = Decimal(
                str(round((self.odds_decimal - 1) * float(self.stake_euros), 2))
            )
        elif self.result == "loss" and self.stake_euros is not None:
            self.pnl_euros = -self.stake_euros
        elif self.result == "void":
            self.pnl_euros = Decimal("0.00")
        super().save(*args, **kwargs)

    @property
    def roi_pct(self):
        if self.stake_euros and self.pnl_euros is not None:
            return round(float(self.pnl_euros) / float(self.stake_euros) * 100, 2)
        return None

    @property
    def pnl_units(self):
        if self.units and self.stake_euros and float(self.stake_euros):
            unit_value = float(self.stake_euros) / self.units
            if unit_value and self.pnl_euros is not None:
                return round(float(self.pnl_euros) / unit_value, 2)
        return None
