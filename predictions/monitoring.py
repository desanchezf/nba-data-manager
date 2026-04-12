"""
Monitoreo de rendimiento del modelo NBA: accuracy, log-loss, ROI simulado.
"""

import logging
from datetime import date, timedelta

import numpy as np

logger = logging.getLogger(__name__)


def compute_model_metrics(market: str, days_back: int = 30, alert_threshold: float = 0.55, stdout=None):
    """
    Calcula métricas de rendimiento del modelo para los últimos `days_back` días.
    Lanza advertencia si accuracy < alert_threshold.
    """

    def log(msg):
        if stdout:
            stdout.write(msg + "\n")

    from_date = date.today() - timedelta(days=days_back)

    try:
        from predictions.models import PredictionLog
        from core.models import Game

        logs = PredictionLog.objects.filter(
            market=market,
            created_at__date__gte=from_date,
            actual_home_win__isnull=False,
        )

        n = logs.count()
        if n == 0:
            log(f"[metrics] Sin predicciones evaluadas para {market} en los últimos {days_back} días.")
            return {"n": 0, "market": market}

        y_true = []
        y_pred = []

        for pred_log in logs.iterator():
            prob_home = pred_log.predicted_probs.get("home") or pred_log.predicted_value
            if prob_home is None:
                continue
            y_true.append(1 if pred_log.actual_home_win else 0)
            y_pred.append(float(prob_home))

        if not y_true:
            log(f"[metrics] Sin predicciones con probabilidades para {market}.")
            return {"n": 0, "market": market}

        y_true_arr = np.array(y_true)
        y_pred_arr = np.array(y_pred)
        binary = (y_pred_arr >= 0.5).astype(int)

        acc = float(np.mean(binary == y_true_arr))
        eps = 1e-7
        ll = float(-np.mean(
            y_true_arr * np.log(y_pred_arr + eps) +
            (1 - y_true_arr) * np.log(1 - y_pred_arr + eps)
        ))

        # ROI simulado con apuesta plana cuando prob > 0.55
        roi_series = []
        for prob, actual in zip(y_pred, y_true):
            if prob > 0.55:
                model_odds = 1.0 / prob if prob > 0 else 1.0
                ev = prob * (model_odds - 1) - (1 - prob)
                roi_series.append(ev)
        roi = round(float(np.mean(roi_series) * 100), 2) if roi_series else 0.0

        result = {
            "market": market,
            "days_back": days_back,
            "n": len(y_true),
            "accuracy": round(acc, 4),
            "log_loss": round(ll, 4),
            "roi_pct": roi,
        }

        log(f"[metrics] {market} ({days_back}d): n={len(y_true)}  acc={acc:.4f}  ll={ll:.4f}  roi={roi:.1f}%")

        if acc < alert_threshold:
            log(f"[metrics] ⚠️  ALERTA: accuracy {acc:.4f} < umbral {alert_threshold}")

        return result

    except Exception as exc:
        logger.error("compute_model_metrics error: %s", exc)
        return {"error": str(exc), "market": market}
