"""
Features de estadísticas rolling por equipo (últimos N partidos).
Calcula promedios de PTS, REB, AST, FG%, 3P%, TOV, etc.
"""

import logging
from datetime import date

logger = logging.getLogger(__name__)


def compute_rolling_team_features(
    team_id: str,
    as_of_date: date,
    windows=(5, 10),
) -> dict:
    """
    Devuelve estadísticas rolling del equipo como local o visitante.
    Usa GameTeamLine normalizado.
    """
    features = {}
    try:
        from core.models import GameTeamLine

        qs = (
            GameTeamLine.objects.filter(
                team__team_id=team_id,
                game__date__lt=as_of_date,
                period="ALL",
            )
            .select_related("game")
            .order_by("-game__date")
        )

        for window in windows:
            lines = list(qs[:window])
            n = len(lines)
            if n == 0:
                continue

            pts_list = [l.pts for l in lines]
            reb_list = [l.reb for l in lines]
            ast_list = [l.ast for l in lines]
            tov_list = [l.tov for l in lines]
            stl_list = [l.stl for l in lines]
            blk_list = [l.blk for l in lines]
            fgm_list = [l.fgm for l in lines]
            fga_list = [l.fga for l in lines]
            fg3m_list = [l.fg3m for l in lines]
            fg3a_list = [l.fg3a for l in lines]
            ftm_list = [l.ftm for l in lines]
            fta_list = [l.fta for l in lines]

            w = window
            features[f"team_pts_avg_{w}"] = round(sum(pts_list) / n, 2)
            features[f"team_reb_avg_{w}"] = round(sum(reb_list) / n, 2)
            features[f"team_ast_avg_{w}"] = round(sum(ast_list) / n, 2)
            features[f"team_tov_avg_{w}"] = round(sum(tov_list) / n, 2)
            features[f"team_stl_avg_{w}"] = round(sum(stl_list) / n, 2)
            features[f"team_blk_avg_{w}"] = round(sum(blk_list) / n, 2)

            total_fga = sum(fga_list)
            total_fg3a = sum(fg3a_list)
            total_fta = sum(fta_list)
            features[f"team_fg_pct_{w}"] = round(sum(fgm_list) / total_fga, 4) if total_fga else 0.0
            features[f"team_fg3_pct_{w}"] = round(sum(fg3m_list) / total_fg3a, 4) if total_fg3a else 0.0
            features[f"team_ft_pct_{w}"] = round(sum(ftm_list) / total_fta, 4) if total_fta else 0.0

            # Puntos por partido oponente
            opp_scores = []
            for line in lines:
                game = line.game
                if game.home_team_id == team_id:
                    opp_scores.append(game.away_score or 0)
                else:
                    opp_scores.append(game.home_score or 0)
            if opp_scores:
                features[f"team_pts_allowed_avg_{w}"] = round(sum(opp_scores) / len(opp_scores), 2)
                features[f"team_point_diff_avg_{w}"] = round(
                    features[f"team_pts_avg_{w}"] - features[f"team_pts_allowed_avg_{w}"], 2
                )

    except Exception as exc:
        logger.warning("rolling team features error team=%s: %s", team_id, exc)

    return features


def compute_win_pct_features(team_id: str, as_of_date: date, windows=(5, 10)) -> dict:
    """
    Win% en los últimos N partidos del equipo.
    """
    features = {}
    try:
        from core.models import Game

        games = (
            Game.objects.filter(
                date__lt=as_of_date,
            )
            .filter(
                models.Q(home_team__team_id=team_id) | models.Q(away_team__team_id=team_id)
            )
            .order_by("-date")
        )

        # Usar Django Q objects
        from django.db.models import Q
        games = (
            Game.objects.filter(
                date__lt=as_of_date,
            )
            .filter(Q(home_team__team_id=team_id) | Q(away_team__team_id=team_id))
            .exclude(home_score__isnull=True)
            .order_by("-date")
        )

        for window in windows:
            window_games = list(games[:window])
            n = len(window_games)
            if n == 0:
                continue
            wins = 0
            for g in window_games:
                if g.home_team_id == team_id and (g.home_score or 0) > (g.away_score or 0):
                    wins += 1
                elif g.away_team_id == team_id and (g.away_score or 0) > (g.home_score or 0):
                    wins += 1
            features[f"team_win_pct_{window}"] = round(wins / n, 4)

    except Exception as exc:
        logger.warning("win_pct features error team=%s: %s", team_id, exc)

    return features


def compute_rolling_quarter_features(
    team_id: str,
    as_of_date: date,
    quarter: str = "Q1",
    windows: tuple = (5, 10),
) -> dict:
    """Rolling de puntos/FG/TOV de un equipo en un cuarto específico (Q1..Q4)."""
    features = {}
    prefix = quarter.lower()
    try:
        from core.models import GameTeamLine

        qs = (
            GameTeamLine.objects.filter(
                team__team_id=team_id,
                game__date__lt=as_of_date,
                period=quarter,
            )
            .select_related("game")
            .order_by("-game__date")
        )

        for window in windows:
            lines = list(qs[:window])
            n = len(lines)
            if n == 0:
                continue

            pts = [l.pts for l in lines]
            fgm = [l.fgm for l in lines]
            fga = [l.fga for l in lines]
            fg3m = [l.fg3m for l in lines]
            fg3a = [l.fg3a for l in lines]
            tov = [l.tov for l in lines]

            total_fga = sum(fga)
            total_fg3a = sum(fg3a)

            features[f"team_{prefix}_pts_avg_{window}"] = round(sum(pts) / n, 2)
            features[f"team_{prefix}_tov_avg_{window}"] = round(sum(tov) / n, 2)
            features[f"team_{prefix}_fg_pct_{window}"] = (
                round(sum(fgm) / total_fga, 4) if total_fga else 0.0
            )
            features[f"team_{prefix}_fg3_pct_{window}"] = (
                round(sum(fg3m) / total_fg3a, 4) if total_fg3a else 0.0
            )

    except Exception as exc:
        logger.warning(
            "quarter rolling error team=%s quarter=%s: %s", team_id, quarter, exc
        )

    return features


def compute_rolling_half_features(
    team_id: str,
    as_of_date: date,
    half: int = 1,
    windows: tuple = (5, 10),
) -> dict:
    """
    Rolling de puntos de equipo en primera (Q1+Q2) o segunda (Q3+Q4) mitad.
    Suma las filas Q1/Q2 o Q3/Q4 de GameTeamLine por partido.
    """
    features = {}
    quarters = ("Q1", "Q2") if half == 1 else ("Q3", "Q4")
    prefix = f"h{half}"

    try:
        from django.db.models import Q as DQ
        from core.models import GameTeamLine, Game

        game_qs = (
            Game.objects.filter(date__lt=as_of_date)
            .filter(
                DQ(home_team__team_id=team_id) | DQ(away_team__team_id=team_id)
            )
            .order_by("-date")
        )

        for window in windows:
            recent_game_ids = list(
                game_qs.values_list("game_id", flat=True)[:window]
            )
            if not recent_game_ids:
                continue

            pts_by_game: dict[str, int] = {gid: 0 for gid in recent_game_ids}
            for qtr in quarters:
                rows = GameTeamLine.objects.filter(
                    game__game_id__in=recent_game_ids,
                    team__team_id=team_id,
                    period=qtr,
                ).values("game__game_id", "pts")
                for row in rows:
                    gid = row["game__game_id"]
                    pts_by_game[gid] = pts_by_game.get(gid, 0) + (row["pts"] or 0)

            pts_list = [v for v in pts_by_game.values() if v > 0]
            n = len(pts_list)
            if n == 0:
                continue

            features[f"team_{prefix}_pts_avg_{window}"] = round(sum(pts_list) / n, 2)

    except Exception as exc:
        logger.warning(
            "half rolling error team=%s half=%s: %s", team_id, half, exc
        )

    return features
