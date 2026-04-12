"""
Features específicas de mercado NBA.
"""

import logging

logger = logging.getLogger(__name__)


def compute_market_features(base_features: dict, market: str) -> dict:
    """
    Añade features específicas del mercado sobre las features base.
    """
    if market == "moneyline":
        return _moneyline_features(base_features)
    elif market == "spread":
        return _spread_features(base_features)
    elif market == "totals":
        return _totals_features(base_features)
    elif market in ("player_pts", "player_reb", "player_ast", "player_pra"):
        return _props_features(base_features, market)
    return {}


def _moneyline_features(f: dict) -> dict:
    """Features adicionales para moneyline."""
    extra = {}
    for w in (5, 10):
        h_win = f.get(f"home_team_win_pct_{w}", 0)
        a_win = f.get(f"away_team_win_pct_{w}", 0)
        if h_win is not None and a_win is not None:
            extra[f"win_pct_diff_{w}"] = round(h_win - a_win, 4)
    return extra


def _spread_features(f: dict) -> dict:
    """Features adicionales para spread."""
    extra = {}
    for w in (5, 10):
        diff = f.get(f"pts_diff_{w}")
        if diff is not None:
            extra[f"spread_indicator_{w}"] = 1 if diff > 0 else 0
    return extra


def _totals_features(f: dict) -> dict:
    """Features adicionales para Over/Under totales."""
    extra = {}
    for w in (5, 10):
        proj = f.get(f"projected_total_{w}")
        if proj:
            extra[f"total_proj_{w}"] = proj
    return extra


def _props_features(f: dict, market: str) -> dict:
    """Features adicionales para props de jugadores."""
    # Las props usan PlayerFeatureSet directamente en inference
    return {}
