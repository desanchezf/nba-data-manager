"""
Features de historial head-to-head (H2H) entre dos equipos NBA.
"""

import logging
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)


def compute_h2h_features(
    home_team_id: str,
    away_team_id: str,
    as_of_date: Optional[date] = None,
    last_n: int = 10,
) -> dict:
    """
    Devuelve estadísticas H2H entre local y visitante en los últimos `last_n` enfrentamientos.
    """
    features = {}
    if as_of_date is None:
        as_of_date = date.today()

    try:
        from django.db.models import Q, Avg
        from core.models import Game

        h2h_games = (
            Game.objects.filter(
                Q(home_team__team_id=home_team_id, away_team__team_id=away_team_id)
                | Q(home_team__team_id=away_team_id, away_team__team_id=home_team_id),
                date__lt=as_of_date,
                home_score__isnull=False,
                away_score__isnull=False,
            )
            .order_by("-date")[:last_n]
        )

        games = list(h2h_games)
        n = len(games)
        if n == 0:
            return features

        home_wins = 0
        home_pts_list = []
        away_pts_list = []
        margins = []

        for g in games:
            if g.home_team_id == home_team_id:
                h = g.home_score or 0
                a = g.away_score or 0
            else:
                h = g.away_score or 0
                a = g.home_score or 0
            home_pts_list.append(h)
            away_pts_list.append(a)
            margins.append(h - a)
            if h > a:
                home_wins += 1

        features["h2h_games"] = n
        features["h2h_home_win_pct"] = round(home_wins / n, 4)
        features["h2h_home_pts_avg"] = round(sum(home_pts_list) / n, 2)
        features["h2h_away_pts_avg"] = round(sum(away_pts_list) / n, 2)
        features["h2h_margin_avg"] = round(sum(margins) / n, 2)
        features["h2h_total_pts_avg"] = round(
            (sum(home_pts_list) + sum(away_pts_list)) / n, 2
        )

    except Exception as exc:
        logger.warning("h2h features error: %s", exc)

    return features
