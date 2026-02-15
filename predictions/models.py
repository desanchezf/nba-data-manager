from django.db import models
from .enums import (
    PredictionTypeChoices,
    PredictionCategoryChoices,
    PredictionMarketChoices,
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
