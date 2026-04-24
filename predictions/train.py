"""
Pipeline de entrenamiento NBA: XGBoost (clasificador/regresor) y Poisson GLM.
Split temporal: train historial, val penúltima temporada, test última temporada.
Calibración Platt scaling para clasificadores.
"""

from pathlib import Path

import joblib
import numpy as np


def get_market_type(market: str) -> str:
    """Determina el tipo de modelo para un mercado según el registry."""
    from predictions.registry import MARKET_REGISTRY, PRIMARY
    cfg = MARKET_REGISTRY.get(market, {})
    if cfg.get("kind") == PRIMARY:
        return cfg.get("model_type", "classifier")
    return "classifier"


def build_xy_from_features(feature_sets, target_key="home_win", fillna=0.0):
    """
    Convierte lista de dicts (GameFeatureSet.features + target) en X e y.
    """
    rows = []
    for fs in feature_sets:
        if isinstance(fs, dict):
            feats = fs.get("features")
            target = fs.get(target_key)
        else:
            feats = getattr(fs, "features", {})
            target = getattr(fs, "target", None)
        if feats:
            rows.append({"features": feats, "target": target})
    if not rows:
        return np.array([]), np.array([]), []

    all_keys = sorted(set().union(*(r["features"].keys() for r in rows)))
    X = np.array(
        [[float(r["features"].get(k, fillna)) for k in all_keys] for r in rows],
        dtype=np.float64,
    )
    y = np.array([
        float(r["target"]) if r["target"] is not None else np.nan
        for r in rows
    ])
    valid = ~np.isnan(y)
    return X[valid], y[valid], all_keys


def train_xgboost_classifier(X_train, y_train, X_val, y_val, **kwargs):
    """Entrena XGBoost para clasificación (home_win binario)."""
    try:
        import xgboost as xgb
    except ImportError:
        return None, None

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    params = {
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "max_depth": kwargs.get("max_depth", 6),
        "eta": kwargs.get("eta", 0.1),
        "subsample": 0.8,
        "colsample_bytree": 0.8,
    }
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=kwargs.get("num_rounds", 200),
        evals=[(dtrain, "train"), (dval, "val")],
        early_stopping_rounds=20,
        verbose_eval=False,
    )
    return model, params


def train_xgboost_regressor(X_train, y_train, X_val, y_val, **kwargs):
    """Entrena XGBoost para regresión (totales de puntos)."""
    try:
        import xgboost as xgb
    except ImportError:
        return None, None

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    params = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "max_depth": kwargs.get("max_depth", 6),
        "eta": kwargs.get("eta", 0.05),
        "subsample": 0.8,
        "colsample_bytree": 0.8,
    }
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=kwargs.get("num_rounds", 300),
        evals=[(dtrain, "train"), (dval, "val")],
        early_stopping_rounds=20,
        verbose_eval=False,
    )
    return model, params


def train_poisson_regressor(X_train, y_train):
    """Entrena un regresor Poisson GLM."""
    try:
        from sklearn.linear_model import PoissonRegressor
        model = PoissonRegressor(alpha=0.01, max_iter=300)
        model.fit(X_train, y_train)
        return model, {"type": "poisson"}
    except ImportError:
        return None, None


def platt_scaling(probs, y_true):
    """Calibración Platt: ajuste con regresión logística en validación."""
    from sklearn.linear_model import LogisticRegression
    eps = 1e-6
    p = np.clip(probs, eps, 1 - eps)
    logit = np.log(p / (1 - p)).reshape(-1, 1)
    lr = LogisticRegression(C=1e10, solver="lbfgs", max_iter=1000)
    lr.fit(logit, y_true)
    return lr


def train_and_save(
    season_type: str,
    market: str,
    model_dir: str | Path,
    stdout=None,
):
    """
    Entrena el modelo para un mercado y lo guarda en joblib.
    Retorna (success, message).
    """
    import io

    def log(msg):
        if stdout:
            stdout.write(msg + "\n")

    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    log(f"[train] Mercado: {market} | Tipo temporada: {season_type}")

    from predictions.registry import MARKET_REGISTRY, PRIMARY, NOT_CONTEMPLATED, extract_target

    registry_cfg = MARKET_REGISTRY.get(market, {})
    if registry_cfg.get("kind") == NOT_CONTEMPLATED:
        return False, f"Mercado '{market}' no contemplado (señal insuficiente)"
    if registry_cfg.get("kind") != PRIMARY:
        return False, f"Mercado '{market}' es derivado; entrena su mercado primario"

    market_type = get_market_type(market)
    target_key = registry_cfg.get("target", "home_win")
    feature_market = registry_cfg.get("feature_market", market)

    # Cargar feature sets
    try:
        from features.models import GameFeatureSet

        qs = GameFeatureSet.objects.filter(
            market=feature_market,
            season_type__icontains=season_type.split("_")[0],
        ).exclude(features={})

        log(f"[train] Feature sets encontrados: {qs.count()}")
        if qs.count() < 10:
            return False, f"Insuficientes datos ({qs.count()} partidos) para {market}"

        rows = []
        for fs in qs.iterator():
            target = extract_target(fs.game_id, target_key)
            if target is None:
                continue
            rows.append({"features": fs.features, "target": target})

    except Exception as exc:
        return False, f"Error cargando features: {exc}"

    if len(rows) < 10:
        return False, f"Insuficientes partidos con resultado para {market}"

    # Ordenar por fecha para split temporal
    # Split 80/10/10
    n = len(rows)
    train_end = int(n * 0.8)
    val_end = int(n * 0.9)

    train_rows = rows[:train_end]
    val_rows = rows[train_end:val_end]

    target_key = "target"

    try:
        X_train, y_train, feature_names = build_xy_from_features(train_rows, target_key)
        X_val, y_val, _ = build_xy_from_features(val_rows, target_key)
    except Exception as exc:
        return False, f"Error construyendo matrices: {exc}"

    if len(X_train) == 0 or len(X_val) == 0:
        return False, "No hay suficientes datos con target válido"

    log(f"[train] Train: {len(X_train)}, Val: {len(X_val)}, Features: {len(feature_names)}")

    model_obj = None
    platt = None

    if market_type == "classifier":
        model_obj, _ = train_xgboost_classifier(X_train, y_train, X_val, y_val)
        if model_obj is not None:
            try:
                import xgboost as xgb
                dval = xgb.DMatrix(X_val)
                probs = model_obj.predict(dval)
                platt = platt_scaling(probs, y_val)
                log("[train] Calibración Platt completada")
            except Exception as exc:
                log(f"[train] Warning: Platt scaling falló: {exc}")
        prefix = "xgb"
    elif market_type in ("regressor", "props_regressor"):
        model_obj, _ = train_xgboost_regressor(X_train, y_train, X_val, y_val)
        if model_obj is None:
            # Fallback a Poisson
            model_obj, _ = train_poisson_regressor(X_train, y_train)
        prefix = "xgbr" if market_type == "regressor" else "xgb"

    if model_obj is None:
        return False, f"No se pudo entrenar modelo para {market}"

    # Guardar payload
    season_type_clean = season_type.replace(" ", "_")
    path = model_dir / f"{prefix}_{season_type_clean}_{market}.joblib"
    payload = {
        "model": model_obj,
        "platt": platt,
        "feature_names": feature_names,
        "market": market,
        "season_type": season_type,
        "market_type": market_type,
        "n_train": len(X_train),
    }
    joblib.dump(payload, path)
    log(f"[train] Modelo guardado en {path}")

    return True, f"Modelo guardado: {path.name} ({len(X_train)} muestras)"
