"""
Inferencia NBA: carga features (Redis/DB), modelo (joblib), calibra probs, calcula EV.
"""

import json
from pathlib import Path

from django.conf import settings


def load_model(season_type="Regular_Season", market="moneyline"):
    """Carga modelo y calibración desde joblib."""
    model_dir = Path(getattr(settings, "MODEL_STORAGE_PATH", settings.MEDIA_ROOT / "models"))
    # Intentar diferentes prefijos de modelo
    for prefix in ("xgb", "poisson", "xgbr"):
        path = model_dir / f"{prefix}_{season_type}_{market}.joblib"
        if path.exists():
            import joblib
            return joblib.load(path)
    # Fallback: Regular_Season
    for prefix in ("xgb", "poisson", "xgbr"):
        path = model_dir / f"{prefix}_Regular_Season_{market}.joblib"
        if path.exists():
            import joblib
            return joblib.load(path)
    return None


def get_features_for_game(game_id, market="base"):
    """Carga features desde Redis o DB."""
    from features.engine.base import get_game_features
    return get_game_features(game_id, market=market)


def get_features_for_matchup(home_team_id, away_team_id, as_of_date=None, market="moneyline"):
    """
    Calcula features para un matchup sin partido en BD.
    Usa historial anterior a as_of_date.
    """
    from features.engine.matchup import compute_features_for_matchup
    return compute_features_for_matchup(
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        as_of_date=as_of_date,
        market=market,
    )


def predict_proba(features_dict, model_payload, feature_names):
    """
    Predice probabilidad con el modelo y aplica calibración si existe.
    """
    import numpy as np
    X = np.array([[float(features_dict.get(k, 0.0)) for k in feature_names]], dtype=np.float64)
    model = model_payload.get("model")
    if model is None:
        return None
    try:
        import xgboost as xgb
        d = xgb.DMatrix(X)
        p = model.predict(d)[0]
    except Exception:
        try:
            p = float(model.predict_proba(X)[0, 1])
        except Exception:
            return None

    platt = model_payload.get("platt")
    if platt is not None:
        eps = 1e-6
        p = np.clip(p, eps, 1 - eps)
        logit = np.log(p / (1 - p)).reshape(1, -1)
        p = platt.predict_proba(logit)[0, 1]
    return float(p)


def ev_vs_odds(prob_home_win, odds_home, odds_away):
    """EV para moneyline en cuotas decimales."""
    if odds_home is None or odds_away is None:
        return None, None
    try:
        dh = float(odds_home)
        da = float(odds_away)
    except (TypeError, ValueError):
        return None, None
    ev_home = prob_home_win * (dh - 1) - (1 - prob_home_win)
    ev_away = (1 - prob_home_win) * (da - 1) - prob_home_win
    return ev_home, ev_away
