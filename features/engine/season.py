"""
Features de estadísticas de temporada por equipo y jugador.
Usa TeamsGeneralTraditional, TeamsGeneralAdvanced, PlayersGeneralTraditional, PlayersGeneralAdvanced.
"""

import logging
from datetime import date

logger = logging.getLogger(__name__)


def _season_from_date(as_of_date: date) -> str:
    """Deriva la temporada NBA a partir de una fecha. Oct–Jun = misma temporada."""
    y = as_of_date.year
    if as_of_date.month >= 10:
        return f"{y}-{str(y + 1)[-2:]}"
    return f"{y - 1}-{str(y)[-2:]}"


def compute_season_team_features(
    team_abb: str,
    season: str,
    season_type: str = "Regular Season",
) -> dict:
    """
    Devuelve features de temporada completa del equipo.
    Combina TeamsGeneralTraditional (tradicionales) y TeamsGeneralAdvanced (avanzadas).
    """
    features = {}
    try:
        from teams.models import TeamsGeneralTraditional, TeamsGeneralAdvanced

        trad = TeamsGeneralTraditional.objects.filter(
            team_abb=team_abb,
            season=season,
            season_type__icontains=season_type.split()[0],
        ).first()

        if trad and trad.gp:
            gp = trad.gp
            features["season_w_pct"] = round(trad.w_pct or 0.0, 4)
            features["season_pts_pg"] = round((trad.pts or 0) / gp, 2)
            features["season_reb_pg"] = round((trad.reb or 0) / gp, 2)
            features["season_ast_pg"] = round((trad.ast or 0) / gp, 2)
            features["season_tov_pg"] = round((trad.tov or 0) / gp, 2)
            features["season_stl_pg"] = round((trad.stl or 0) / gp, 2)
            features["season_blk_pg"] = round((trad.blk or 0) / gp, 2)
            features["season_fg_pct"] = round(trad.fg_pct or 0.0, 4)
            features["season_fg3_pct"] = round(trad.fg3_pct or 0.0, 4)
            features["season_ft_pct"] = round(trad.ft_pct or 0.0, 4)

        adv = TeamsGeneralAdvanced.objects.filter(
            team_abb=team_abb,
            season=season,
            season_type__icontains=season_type.split()[0],
        ).first()

        if adv:
            features["season_off_rtg"] = round(adv.off_rating or 0.0, 2)
            features["season_def_rtg"] = round(adv.def_rating or 0.0, 2)
            features["season_net_rtg"] = round(adv.net_rating or 0.0, 2)
            features["season_pace"] = round(adv.pace or 0.0, 2)
            features["season_efg_pct"] = round(adv.efg_pct or 0.0, 4)
            features["season_ts_pct"] = round(adv.ts_pct or 0.0, 4)
            features["season_oreb_pct"] = round(adv.oreb_pct or 0.0, 4)
            features["season_dreb_pct"] = round(adv.dreb_pct or 0.0, 4)
            features["season_tm_tov_pct"] = round(adv.tm_tov_pct or 0.0, 4)

    except Exception as exc:
        logger.warning("season team features error team=%s season=%s: %s", team_abb, season, exc)

    return features


def compute_season_player_features(
    player_id: str,
    season: str,
    season_type: str = "Regular Season",
) -> dict:
    """
    Devuelve features de temporada del jugador.
    Combina PlayersGeneralTraditional (promedios) y PlayersGeneralAdvanced (avanzadas).
    """
    features = {}
    try:
        from players.models import PlayersGeneralTraditional, PlayersGeneralAdvanced

        trad = PlayersGeneralTraditional.objects.filter(
            player_id=player_id,
            season=season,
            season_type__icontains=season_type.split()[0],
        ).first()

        if trad and trad.gp:
            gp = trad.gp
            features["season_pts_pg"] = round((trad.pts or 0) / gp, 2)
            features["season_reb_pg"] = round((trad.reb or 0) / gp, 2)
            features["season_ast_pg"] = round((trad.ast or 0) / gp, 2)
            features["season_stl_pg"] = round((trad.stl or 0) / gp, 2)
            features["season_blk_pg"] = round((trad.blk or 0) / gp, 2)
            features["season_tov_pg"] = round((trad.tov or 0) / gp, 2)
            features["season_fg_pct"] = round(trad.fg_pct or 0.0, 4)
            features["season_fg3_pct"] = round(trad.fg3_pct or 0.0, 4)
            features["season_ft_pct"] = round(trad.ft_pct or 0.0, 4)
            features["season_dd2"] = trad.dd2 or 0
            features["season_td3"] = trad.td3 or 0

        adv = PlayersGeneralAdvanced.objects.filter(
            player_id=player_id,
            season=season,
            season_type__icontains=season_type.split()[0],
        ).first()

        if adv:
            features["season_usg_pct"] = round(adv.usg_pct or 0.0, 4)
            features["season_ts_pct"] = round(adv.ts_pct or 0.0, 4)
            features["season_efg_pct"] = round(adv.efg_pct or 0.0, 4)
            features["season_off_rtg"] = round(adv.off_rating or 0.0, 2)
            features["season_def_rtg"] = round(adv.def_rating or 0.0, 2)
            features["season_net_rtg"] = round(adv.net_rating or 0.0, 2)
            features["season_ast_pct"] = round(adv.ast_pct or 0.0, 4)
            features["season_reb_pct"] = round(adv.reb_pct or 0.0, 4)
            features["season_oreb_pct"] = round(adv.oreb_pct or 0.0, 4)
            features["season_dreb_pct"] = round(adv.dreb_pct or 0.0, 4)

    except Exception as exc:
        logger.warning("season player features error player=%s season=%s: %s", player_id, season, exc)

    return features
