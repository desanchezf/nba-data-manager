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
    - Features específicas por mercado (cuartos, mitades, totales, spread)
    """
    if as_of_date is None:
        as_of_date = date.today()

    features = {}

    from features.engine.rolling import (
        compute_rolling_team_features,
        compute_win_pct_features,
    )
    from features.engine.h2h import compute_h2h_features

    # Rolling stats base (ALL periods)
    for prefix, team_id in (("home", home_team_id), ("away", away_team_id)):
        for k, v in compute_rolling_team_features(team_id, as_of_date).items():
            features[f"{prefix}_{k}"] = v
        for k, v in compute_win_pct_features(team_id, as_of_date).items():
            features[f"{prefix}_{k}"] = v

    # Diferenciales derivados
    for w in (5, 10):
        h_pts = features.get(f"home_team_pts_avg_{w}", 0)
        a_pts = features.get(f"away_team_pts_avg_{w}", 0)
        h_def = features.get(f"home_team_pts_allowed_avg_{w}", 0)
        a_def = features.get(f"away_team_pts_allowed_avg_{w}", 0)
        features[f"pts_diff_{w}"] = round(h_pts - a_pts, 2)
        features[f"def_diff_{w}"] = round(h_def - a_def, 2)

    # H2H
    features.update(compute_h2h_features(home_team_id, away_team_id, as_of_date))

    # Features específicas de mercado
    if market == "totals":
        features.update(_totals_features(home_team_id, away_team_id, features))
    elif market == "spread":
        features.update(_spread_features(features))
    elif market == "first_half":
        features.update(_half_features(home_team_id, away_team_id, as_of_date, half=1))
    elif market == "second_half":
        features.update(_half_features(home_team_id, away_team_id, as_of_date, half=2))
    elif market in ("q1", "q2", "q3", "q4"):
        qtr = market.upper()
        features.update(_quarter_features(home_team_id, away_team_id, as_of_date, quarter=qtr))

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


def _half_features(home_team_id, away_team_id, as_of_date, half=1) -> dict:
    from features.engine.rolling import compute_rolling_half_features
    f = {}
    for prefix, team_id in (("home", home_team_id), ("away", away_team_id)):
        for k, v in compute_rolling_half_features(team_id, as_of_date, half=half).items():
            f[f"{prefix}_{k}"] = v
    return f


def _quarter_features(home_team_id, away_team_id, as_of_date, quarter="Q1") -> dict:
    from features.engine.rolling import compute_rolling_quarter_features
    f = {}
    for prefix, team_id in (("home", home_team_id), ("away", away_team_id)):
        for k, v in compute_rolling_quarter_features(team_id, as_of_date, quarter=quarter).items():
            f[f"{prefix}_{k}"] = v
    return f
