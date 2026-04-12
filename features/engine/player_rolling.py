"""
Features rolling por jugador (últimos N partidos).
Calcula PTS, REB, AST, FG%, 3P%, TS% rolling.
"""

import logging
from datetime import date

logger = logging.getLogger(__name__)


def compute_player_rolling_features(
    player_id: str,
    as_of_date: date,
    windows=(5, 10, 20),
) -> dict:
    """
    Devuelve estadísticas rolling del jugador hasta as_of_date.
    """
    features = {}
    try:
        from core.models import GamePlayerLine

        qs = (
            GamePlayerLine.objects.filter(
                player__player_id=player_id,
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
            stl_list = [l.stl for l in lines]
            blk_list = [l.blk for l in lines]
            tov_list = [l.tov for l in lines]
            min_list = [l.min_played or 0 for l in lines]
            fgm_list = [l.fgm for l in lines]
            fga_list = [l.fga for l in lines]
            fg3m_list = [l.fg3m for l in lines]
            fg3a_list = [l.fg3a for l in lines]
            ftm_list = [l.ftm for l in lines]
            fta_list = [l.fta for l in lines]

            w = window
            features[f"player_pts_avg_{w}"] = round(sum(pts_list) / n, 2)
            features[f"player_reb_avg_{w}"] = round(sum(reb_list) / n, 2)
            features[f"player_ast_avg_{w}"] = round(sum(ast_list) / n, 2)
            features[f"player_stl_avg_{w}"] = round(sum(stl_list) / n, 2)
            features[f"player_blk_avg_{w}"] = round(sum(blk_list) / n, 2)
            features[f"player_tov_avg_{w}"] = round(sum(tov_list) / n, 2)
            features[f"player_min_avg_{w}"] = round(sum(min_list) / n, 2)

            total_fga = sum(fga_list)
            total_fg3a = sum(fg3a_list)
            total_fta = sum(fta_list)
            features[f"player_fg_pct_{w}"] = round(sum(fgm_list) / total_fga, 4) if total_fga else 0.0
            features[f"player_fg3_pct_{w}"] = round(sum(fg3m_list) / total_fg3a, 4) if total_fg3a else 0.0
            features[f"player_ft_pct_{w}"] = round(sum(ftm_list) / total_fta, 4) if total_fta else 0.0

            # TS% = PTS / (2 * (FGA + 0.44 * FTA))
            total_pts = sum(pts_list)
            denom = 2 * (total_fga + 0.44 * total_fta)
            features[f"player_ts_pct_{w}"] = round(total_pts / denom, 4) if denom else 0.0

            # PRA (Points + Rebounds + Assists)
            pra = [p + r + a for p, r, a in zip(pts_list, reb_list, ast_list)]
            features[f"player_pra_avg_{w}"] = round(sum(pra) / n, 2)

    except Exception as exc:
        logger.warning("player rolling features error player=%s: %s", player_id, exc)

    return features
