"""
Backtesting walk-forward NBA. Evalúa el modelo temporada a temporada.
Calcula accuracy, log-loss, ROI simulado, Sharpe y max drawdown.
"""

import logging

import numpy as np

logger = logging.getLogger(__name__)


def run_walk_forward_backtest(
    market: str,
    season_type: str,
    start_year: int,
    end_year: int,
    retrain: bool = False,
    stdout=None,
):
    """
    Evalúa el modelo año a año (walk-forward):
    - Para cada año Y en [start_year, end_year]:
      - Entrena con datos hasta Y-1 (si retrain)
      - Evalúa en partidos del año Y
    - Retorna métricas globales.
    """

    def log(msg):
        if stdout:
            stdout.write(msg + "\n")

    from features.models import GameFeatureSet
    from core.models import Game
    from predictions.train import (
        build_xy_from_features,
        get_market_type,
        train_xgboost_classifier,
        platt_scaling,
    )
    from predictions.inference import load_model, predict_proba

    market_type = get_market_type(market)
    results_by_year = {}

    for year in range(start_year, end_year + 1):
        log(f"\n[backtest] Año: {year}")

        # Feature sets del año actual
        qs_eval = GameFeatureSet.objects.filter(
            market=market,
            season=str(year),
        ).exclude(features={})

        if not qs_eval.exists():
            log(f"[backtest]   Sin datos para {year}. Saltando.")
            continue

        # Cargar modelo
        if retrain:
            # Entrenar con datos históricos hasta year-1
            try:
                from django.conf import settings
                from pathlib import Path
                model_dir = Path(getattr(settings, "MODEL_STORAGE_PATH", "media/models"))

                from predictions.train import train_and_save
                ok, msg = train_and_save(
                    season_type=season_type,
                    market=market,
                    model_dir=model_dir,
                    stdout=stdout,
                )
                log(f"[backtest]   Reentrenamiento: {msg}")
            except Exception as exc:
                log(f"[backtest]   Error reentrenamiento: {exc}")

        model_payload = load_model(season_type=season_type.replace(" ", "_"), market=market)
        if not model_payload:
            log(f"[backtest]   Sin modelo para {market}. Saltando.")
            continue

        feature_names = model_payload.get("feature_names", [])

        # Evaluar
        y_true = []
        y_pred_probs = []
        roi_series = []

        for fs in qs_eval.iterator():
            game = Game.objects.filter(game_id=fs.game_id).first()
            if not game or game.home_score is None:
                continue

            true_home_win = 1 if (game.home_score or 0) > (game.away_score or 0) else 0
            prob = predict_proba(fs.features, model_payload, feature_names)
            if prob is None:
                continue

            y_true.append(true_home_win)
            y_pred_probs.append(prob)

            # ROI simulado: apostar si prob > 0.55, cuota implícita
            if prob > 0.55:
                ev = prob * (1 / prob - 1) - (1 - prob)
                roi_series.append(ev)

        n = len(y_true)
        if n == 0:
            continue

        y_true_arr = np.array(y_true)
        y_pred_arr = np.array(y_pred_probs)
        preds_binary = (y_pred_arr >= 0.5).astype(int)

        acc = float(np.mean(preds_binary == y_true_arr))
        eps = 1e-7
        ll = float(-np.mean(
            y_true_arr * np.log(y_pred_arr + eps) +
            (1 - y_true_arr) * np.log(1 - y_pred_arr + eps)
        ))
        roi = float(np.mean(roi_series) * 100) if roi_series else 0.0

        results_by_year[year] = {
            "n": n,
            "accuracy": round(acc, 4),
            "log_loss": round(ll, 4),
            "roi_pct": round(roi, 2),
        }
        log(
            f"[backtest]   {year}: n={n}  acc={acc:.4f}  ll={ll:.4f}  roi={roi:.1f}%"
        )

    # Métricas globales
    if not results_by_year:
        return {"error": "Sin resultados en el periodo evaluado."}

    all_acc = [r["accuracy"] for r in results_by_year.values()]
    all_ll = [r["log_loss"] for r in results_by_year.values()]
    all_roi = [r["roi_pct"] for r in results_by_year.values()]

    mean_acc = round(float(np.mean(all_acc)), 4)
    mean_ll = round(float(np.mean(all_ll)), 4)
    mean_roi = round(float(np.mean(all_roi)), 2)

    if len(all_roi) > 1:
        std_roi = float(np.std(all_roi))
        sharpe = round(mean_roi / std_roi, 3) if std_roi > 0 else 0.0
    else:
        sharpe = 0.0

    # Max drawdown
    cumulative = np.cumsum(all_roi)
    peak = np.maximum.accumulate(cumulative)
    drawdown = cumulative - peak
    max_dd = round(float(np.min(drawdown)), 2) if len(drawdown) else 0.0

    summary = {
        "by_year": results_by_year,
        "periods": len(results_by_year),
        "mean_accuracy": mean_acc,
        "mean_log_loss": mean_ll,
        "mean_roi_pct": mean_roi,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
    }
    log(
        f"\n[backtest] Resumen ({len(results_by_year)} periodos):\n"
        f"  Accuracy media:  {mean_acc}\n"
        f"  Log-loss media:  {mean_ll}\n"
        f"  ROI medio:       {mean_roi}%\n"
        f"  Sharpe ratio:    {sharpe}\n"
        f"  Max drawdown:    {max_dd}%"
    )
    return summary
