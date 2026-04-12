"""
Feature engineering para un matchup NBA (local vs visitante).
Combina rolling stats de ambos equipos para generar el vector de features.
"""

import logging
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)


def compute_features_for_matchup(
    home_team_id: str,
    away_team_id: str,
    as_of_date: Optional[date] = None,
    market: str = "base",
) -> dict:
    """
    Genera el vector de features para un enfrentamiento NBA dado.

    Incluye:
    - Rolling stats de ambos equipos (PTS, REB, AST, TOV, FG%, etc.)
    - Win% de ambos equipos
    - Head-to-head histórico
    - Features específicas por mercado
    """
    if as_of_date is None:
        as_of_date = date.today()

    features = {}

    from features.engine.rolling import compute_rolling_team_features, compute_win_pct_features
    from features.engine.h2h import compute_h2h_features

    # Rolling stats local
    home_rolling = compute_rolling_team_features(home_team_id, as_of_date)
    for k, v in home_rolling.items():
        features[f"home_{k}"] = v

    # Rolling stats visitante
    away_rolling = compute_rolling_team_features(away_team_id, as_of_date)
    for k, v in away_rolling.items():
        features[f"away_{k}"] = v

    # Win % local y visitante
    home_win = compute_win_pct_features(home_team_id, as_of_date)
    away_win = compute_win_pct_features(away_team_id, as_of_date)
    for k, v in home_win.items():
        features[f"home_{k}"] = v
    for k, v in away_win.items():
        features[f"away_{k}"] = v

    # Diferenciales
    for w in (5, 10):
        h_pts = features.get(f"home_team_pts_avg_{w}", 0)
        a_pts = features.get(f"away_team_pts_avg_{w}", 0)
        h_def = features.get(f"home_team_pts_allowed_avg_{w}", 0)
        a_def = features.get(f"away_team_pts_allowed_avg_{w}", 0)
        features[f"pts_diff_{w}"] = round(h_pts - a_pts, 2)
        features[f"def_diff_{w}"] = round(h_def - a_def, 2)

    # H2H
    h2h = compute_h2h_features(home_team_id, away_team_id, as_of_date)
    features.update(h2h)

    # Features de mercado
    if market == "totals":
        features.update(_totals_features(home_team_id, away_team_id, features))
    elif market == "spread":
        features.update(_spread_features(features))

    return features


def _totals_features(home_team_id, away_team_id, base_features) -> dict:
    """Features específicas para mercado O/U totales."""
    f = {}
    for w in (5, 10):
        h_pts = base_features.get(f"home_team_pts_avg_{w}", 0)
        a_pts = base_features.get(f"away_team_pts_avg_{w}", 0)
        h_def = base_features.get(f"home_team_pts_allowed_avg_{w}", 0)
        a_def = base_features.get(f"away_team_pts_allowed_avg_{w}", 0)
        if h_pts and a_pts and h_def and a_def:
            # Proyección de totales
            home_proj = (h_pts + a_def) / 2
            away_proj = (a_pts + h_def) / 2
            f[f"projected_total_{w}"] = round(home_proj + away_proj, 2)
    return f


def _spread_features(base_features) -> dict:
    """Features específicas para mercado spread."""
    f = {}
    for w in (5, 10):
        diff = base_features.get(f"pts_diff_{w}")
        if diff is not None:
            f[f"spread_proj_{w}"] = diff
    return f
