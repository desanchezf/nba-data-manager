"""
Registry de mercados NBA: mapea cada mercado a su tipo de modelo, feature market,
target de entrenamiento y estado de contemplación.

Tipos:
  PRIMARY   → necesita su propio modelo entrenado
  DERIVED   → se obtiene post-procesando uno o varios modelos primarios
  NOT_CONTEMPLATED → señal insuficiente o evento no predecible con los datos disponibles
"""

import logging

logger = logging.getLogger(__name__)

PRIMARY = "primary"
DERIVED = "derived"
NOT_CONTEMPLATED = "not_contemplated"


MARKET_REGISTRY: dict[str, dict] = {
    # ── GANADOR ──────────────────────────────────────────────────────────────
    "winner_match": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "moneyline", "target": "home_win", "contemplated": True,
    },

    # ── HÁNDICAP ─────────────────────────────────────────────────────────────
    "handicap_main": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "spread", "target": "margin", "contemplated": True,
    },
    "handicap_alternative":      {"kind": DERIVED, "derived_from": "handicap_main", "contemplated": True},
    "handicap_alternative_main": {"kind": DERIVED, "derived_from": "handicap_main", "contemplated": True},

    # ── TOTAL DE PUNTOS ───────────────────────────────────────────────────────
    "total_points_main": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "totals", "target": "total", "contemplated": True,
    },
    "total_points_alternative":      {"kind": DERIVED, "derived_from": "total_points_main", "contemplated": True},
    "total_points_alternative_main": {"kind": DERIVED, "derived_from": "total_points_main", "contemplated": True},

    # ── APUESTAS COMBINADAS ──────────────────────────────────────────────────
    "line_total_double":  {"kind": DERIVED, "derived_from": ["handicap_main", "total_points_main"], "contemplated": True},
    "winner_total_double": {"kind": DERIVED, "derived_from": ["winner_match", "total_points_main"], "contemplated": True},
    "double_result":      {"kind": DERIVED, "derived_from": ["first_half_winner", "winner_match"], "contemplated": True},

    # ── MARGEN DE VICTORIA ───────────────────────────────────────────────────
    "margin_exact": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "spread", "target": "margin", "contemplated": True,
    },
    "margin_simple":      {"kind": DERIVED, "derived_from": "margin_exact", "contemplated": True},
    "margin_bands":       {"kind": DERIVED, "derived_from": "margin_exact", "contemplated": True},
    "margin_four_bands":  {"kind": DERIVED, "derived_from": "margin_exact", "contemplated": True},
    "margin_10pt":        {"kind": DERIVED, "derived_from": "margin_exact", "contemplated": True},
    "margin_12":          {"kind": DERIVED, "derived_from": "margin_exact", "contemplated": True},

    # ── PRIMERA MITAD ─────────────────────────────────────────────────────────
    "first_half_winner": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "first_half", "target": "h1_home_win", "contemplated": True,
    },
    "first_half_total": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "first_half", "target": "h1_total", "contemplated": True,
    },
    "first_half_home_total": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "first_half", "target": "h1_home", "contemplated": True,
    },
    "first_half_away_total": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "first_half", "target": "h1_away", "contemplated": True,
    },
    "first_half_winner_no_draw":         {"kind": DERIVED, "derived_from": "first_half_winner", "contemplated": True},
    "first_half_result":                 {"kind": DERIVED, "derived_from": "first_half_winner", "contemplated": True},
    "first_half_handicap":               {"kind": DERIVED, "derived_from": ["first_half_home_total", "first_half_away_total"], "contemplated": True},
    "first_half_total_odd_even":         {"kind": DERIVED, "derived_from": "first_half_total", "contemplated": True},
    "first_half_total_alternative":      {"kind": DERIVED, "derived_from": "first_half_total", "contemplated": True},
    "first_half_total_alternative_main": {"kind": DERIVED, "derived_from": "first_half_total", "contemplated": True},
    "first_half_line_total_double":      {"kind": DERIVED, "derived_from": ["first_half_winner", "first_half_total"], "contemplated": True},
    "first_half_winner_total_double":    {"kind": DERIVED, "derived_from": ["first_half_winner", "first_half_total"], "contemplated": True},
    "first_half_winner_3way":            {"kind": DERIVED, "derived_from": "first_half_winner", "contemplated": True},
    "first_half_handicap_alternative":      {"kind": DERIVED, "derived_from": ["first_half_home_total", "first_half_away_total"], "contemplated": True},
    "first_half_handicap_alternative_main": {"kind": DERIVED, "derived_from": ["first_half_home_total", "first_half_away_total"], "contemplated": True},
    "first_half_margin":       {"kind": DERIVED, "derived_from": ["first_half_home_total", "first_half_away_total"], "contemplated": True},
    "first_half_margin_exact": {"kind": DERIVED, "derived_from": ["first_half_home_total", "first_half_away_total"], "contemplated": True},

    # ── SEGUNDA MITAD ─────────────────────────────────────────────────────────
    "second_half_winner": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "second_half", "target": "h2_home_win", "contemplated": True,
    },
    "second_half_total": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "second_half", "target": "h2_total", "contemplated": True,
    },
    "second_half_handicap":           {"kind": DERIVED, "derived_from": "second_half_winner", "contemplated": True},
    "second_half_line_total_double":  {"kind": DERIVED, "derived_from": ["second_half_winner", "second_half_total"], "contemplated": True},
    "second_half_winner_total_double": {"kind": DERIVED, "derived_from": ["second_half_winner", "second_half_total"], "contemplated": True},
    "second_half_winner_3way":        {"kind": DERIVED, "derived_from": "second_half_winner", "contemplated": True},

    # ── CUARTOS (Q1–Q4, generado programáticamente) ──────────────────────────
    **{
        f"q{q}_winner": {
            "kind": PRIMARY, "model_type": "classifier",
            "feature_market": f"q{q}", "target": f"q{q}_home_win", "contemplated": True,
        }
        for q in (1, 2, 3, 4)
    },
    **{
        f"q{q}_total": {
            "kind": PRIMARY, "model_type": "regressor",
            "feature_market": f"q{q}", "target": f"q{q}_total", "contemplated": True,
        }
        for q in (1, 2, 3, 4)
    },
    **{
        f"q{q}_home_total": {
            "kind": PRIMARY, "model_type": "regressor",
            "feature_market": f"q{q}", "target": f"q{q}_home", "contemplated": True,
        }
        for q in (1, 2, 3, 4)
    },
    **{
        f"q{q}_away_total": {
            "kind": PRIMARY, "model_type": "regressor",
            "feature_market": f"q{q}", "target": f"q{q}_away", "contemplated": True,
        }
        for q in (1, 2, 3, 4)
    },
    # Derived quarter markets
    "q1_winner_no_draw":       {"kind": DERIVED, "derived_from": "q1_winner", "contemplated": True},
    "q1_handicap":             {"kind": DERIVED, "derived_from": ["q1_home_total", "q1_away_total"], "contemplated": True},
    "q1_total_odd_even":       {"kind": DERIVED, "derived_from": "q1_total", "contemplated": True},
    "q1_winner_3way":          {"kind": DERIVED, "derived_from": "q1_winner", "contemplated": True},
    "q1_winner_total_double":  {"kind": DERIVED, "derived_from": ["q1_winner", "q1_total"], "contemplated": True},
    "q1_line_total_double":    {"kind": DERIVED, "derived_from": ["q1_home_total", "q1_away_total", "q1_total"], "contemplated": True},
    "q1_race_to_x":            {"kind": DERIVED, "derived_from": "race_to_x_points", "contemplated": True},
    "q1_handicap_alternative":      {"kind": DERIVED, "derived_from": ["q1_home_total", "q1_away_total"], "contemplated": True},
    "q1_handicap_alternative_main": {"kind": DERIVED, "derived_from": ["q1_home_total", "q1_away_total"], "contemplated": True},
    "q1_total_alternative":    {"kind": DERIVED, "derived_from": "q1_total", "contemplated": True},
    "q1_margin":               {"kind": DERIVED, "derived_from": ["q1_home_total", "q1_away_total"], "contemplated": True},
    "q1_margin_exact":         {"kind": DERIVED, "derived_from": ["q1_home_total", "q1_away_total"], "contemplated": True},
    "q1_winner_match_winner":  {"kind": DERIVED, "derived_from": ["q1_winner", "winner_match"], "contemplated": True},
    "q1_first_team_score":     {"kind": DERIVED, "derived_from": "first_basket_team", "contemplated": True},

    "q2_handicap":             {"kind": DERIVED, "derived_from": ["q2_home_total", "q2_away_total"], "contemplated": True},
    "q2_total_odd_even":       {"kind": DERIVED, "derived_from": "q2_total", "contemplated": True},
    "q2_race_to_x":            {"kind": DERIVED, "derived_from": "race_to_x_points", "contemplated": True},
    "q2_handicap_alternative":      {"kind": DERIVED, "derived_from": ["q2_home_total", "q2_away_total"], "contemplated": True},
    "q2_handicap_alternative_main": {"kind": DERIVED, "derived_from": ["q2_home_total", "q2_away_total"], "contemplated": True},
    "q2_total_alternative":    {"kind": DERIVED, "derived_from": "q2_total", "contemplated": True},
    "q2_margin":               {"kind": DERIVED, "derived_from": ["q2_home_total", "q2_away_total"], "contemplated": True},
    "q2_margin_exact":         {"kind": DERIVED, "derived_from": ["q2_home_total", "q2_away_total"], "contemplated": True},
    "q2_first_team_score":     {"kind": DERIVED, "derived_from": "first_basket_team", "contemplated": True},
    "q2_last_team_score":      {"kind": DERIVED, "derived_from": "first_basket_team", "contemplated": True},

    "q3_handicap":             {"kind": DERIVED, "derived_from": ["q3_home_total", "q3_away_total"], "contemplated": True},
    "q3_total_odd_even":       {"kind": DERIVED, "derived_from": "q3_total", "contemplated": True},
    "q3_winner_3way":          {"kind": DERIVED, "derived_from": "q3_winner", "contemplated": True},
    "q3_winner_total_double":  {"kind": DERIVED, "derived_from": ["q3_winner", "q3_total"], "contemplated": True},
    "q3_line_total_double":    {"kind": DERIVED, "derived_from": ["q3_home_total", "q3_away_total", "q3_total"], "contemplated": True},
    "q3_race_to_x":            {"kind": DERIVED, "derived_from": "race_to_x_points", "contemplated": True},
    "q3_handicap_alternative":      {"kind": DERIVED, "derived_from": ["q3_home_total", "q3_away_total"], "contemplated": True},
    "q3_handicap_alternative_main": {"kind": DERIVED, "derived_from": ["q3_home_total", "q3_away_total"], "contemplated": True},
    "q3_total_alternative":    {"kind": DERIVED, "derived_from": "q3_total", "contemplated": True},
    "q3_margin":               {"kind": DERIVED, "derived_from": ["q3_home_total", "q3_away_total"], "contemplated": True},
    "q3_margin_exact":         {"kind": DERIVED, "derived_from": ["q3_home_total", "q3_away_total"], "contemplated": True},
    "q3_first_team_score":     {"kind": DERIVED, "derived_from": "first_basket_team", "contemplated": True},

    "q4_handicap":             {"kind": DERIVED, "derived_from": ["q4_home_total", "q4_away_total"], "contemplated": True},
    "q4_total_odd_even":       {"kind": DERIVED, "derived_from": "q4_total", "contemplated": True},
    "q4_winner_3way":          {"kind": DERIVED, "derived_from": "q4_winner", "contemplated": True},
    "q4_winner_total_double":  {"kind": DERIVED, "derived_from": ["q4_winner", "q4_total"], "contemplated": True},
    "q4_line_total_double":    {"kind": DERIVED, "derived_from": ["q4_home_total", "q4_away_total", "q4_total"], "contemplated": True},
    "q4_race_to_x":            {"kind": DERIVED, "derived_from": "race_to_x_points", "contemplated": True},
    "q4_handicap_alternative":      {"kind": DERIVED, "derived_from": ["q4_home_total", "q4_away_total"], "contemplated": True},
    "q4_handicap_alternative_main": {"kind": DERIVED, "derived_from": ["q4_home_total", "q4_away_total"], "contemplated": True},
    "q4_total_alternative":    {"kind": DERIVED, "derived_from": "q4_total", "contemplated": True},
    "q4_margin":               {"kind": DERIVED, "derived_from": ["q4_home_total", "q4_away_total"], "contemplated": True},
    "q4_margin_exact":         {"kind": DERIVED, "derived_from": ["q4_home_total", "q4_away_total"], "contemplated": True},
    "q4_first_team_score":     {"kind": DERIVED, "derived_from": "first_basket_team", "contemplated": True},

    # ── MERCADOS DE EQUIPOS ──────────────────────────────────────────────────
    "home_team_total": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "totals", "target": "home_score", "contemplated": True,
    },
    "away_team_total": {
        "kind": PRIMARY, "model_type": "regressor",
        "feature_market": "totals", "target": "away_score", "contemplated": True,
    },
    "home_team_total_alternative":      {"kind": DERIVED, "derived_from": "home_team_total", "contemplated": True},
    "away_team_total_alternative":      {"kind": DERIVED, "derived_from": "away_team_total", "contemplated": True},
    "home_team_total_alternative_main": {"kind": DERIVED, "derived_from": "home_team_total", "contemplated": True},
    "away_team_total_alternative_main": {"kind": DERIVED, "derived_from": "away_team_total", "contemplated": True},
    "home_team_total_odd_even":         {"kind": DERIVED, "derived_from": "home_team_total", "contemplated": True},
    "away_team_total_odd_even":         {"kind": DERIVED, "derived_from": "away_team_total", "contemplated": True},

    # ── MERCADOS ESPECIALES (CONTEMPLADOS) ────────────────────────────────────
    "overtime": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "moneyline", "target": "ot", "contemplated": True,
    },
    "half_with_more_points": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "totals", "target": "first_half_more", "contemplated": True,
    },
    "quarter_with_more_points": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "totals", "target": "quarter_most", "contemplated": True,
    },
    "team_win_all_quarters": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "moneyline", "target": "home_win_all_q", "contemplated": True,
    },
    "team_win_both_halves": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "moneyline", "target": "home_win_both_h", "contemplated": True,
    },
    # Requiere preprocesado de GamePlayByPlay para extraer target
    "first_basket_team": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "moneyline", "target": "home_first_score", "contemplated": True,
    },
    "race_to_x_points": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "moneyline", "target": "home_first_score", "contemplated": True,
    },

    # ── MERCADOS DE JUGADORES ─────────────────────────────────────────────────
    "player_points_specific": {
        "kind": PRIMARY, "model_type": "props_regressor",
        "feature_market": "player_pts", "target": "player_pts", "contemplated": True,
    },
    "player_rebounds_specific": {
        "kind": PRIMARY, "model_type": "props_regressor",
        "feature_market": "player_reb", "target": "player_reb", "contemplated": True,
    },
    "player_assists_specific": {
        "kind": PRIMARY, "model_type": "props_regressor",
        "feature_market": "player_ast", "target": "player_ast", "contemplated": True,
    },
    "player_threes_specific": {
        "kind": PRIMARY, "model_type": "props_regressor",
        "feature_market": "player_3pm", "target": "player_3pm", "contemplated": True,
    },
    "player_blocks_specific": {
        "kind": PRIMARY, "model_type": "props_regressor",
        "feature_market": "player_blk", "target": "player_blk", "contemplated": True,
    },
    "player_steals_specific": {
        "kind": PRIMARY, "model_type": "props_regressor",
        "feature_market": "player_stl", "target": "player_stl", "contemplated": True,
    },
    "player_double_double": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "player_pts", "target": "dd", "contemplated": True,
    },
    "player_triple_double": {
        "kind": PRIMARY, "model_type": "classifier",
        "feature_market": "player_pts", "target": "td", "contemplated": True,
    },
    # Derived player markets
    "player_points_x_plus":          {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_rebounds_x_plus":         {"kind": DERIVED, "derived_from": "player_rebounds_specific", "contemplated": True},
    "player_assists_x_plus":          {"kind": DERIVED, "derived_from": "player_assists_specific", "contemplated": True},
    "player_threes_x_plus":           {"kind": DERIVED, "derived_from": "player_threes_specific", "contemplated": True},
    "player_blocks_x_plus":           {"kind": DERIVED, "derived_from": "player_blocks_specific", "contemplated": True},
    "player_steals_x_plus":           {"kind": DERIVED, "derived_from": "player_steals_specific", "contemplated": True},
    "player_points_alternative":      {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_points_assists":          {"kind": DERIVED, "derived_from": ["player_points_specific", "player_assists_specific"], "contemplated": True},
    "player_points_rebounds":         {"kind": DERIVED, "derived_from": ["player_points_specific", "player_rebounds_specific"], "contemplated": True},
    "player_points_rebounds_assists":        {"kind": DERIVED, "derived_from": ["player_points_specific", "player_rebounds_specific", "player_assists_specific"], "contemplated": True},
    "player_rebounds_assists":               {"kind": DERIVED, "derived_from": ["player_rebounds_specific", "player_assists_specific"], "contemplated": True},
    "player_points_alt_rebounds_assists":    {"kind": DERIVED, "derived_from": ["player_points_specific", "player_rebounds_specific", "player_assists_specific"], "contemplated": True},
    "player_points_alt_assists":             {"kind": DERIVED, "derived_from": ["player_points_specific", "player_assists_specific"], "contemplated": True},
    "player_points_alt_rebounds_assists_alt": {"kind": DERIVED, "derived_from": ["player_points_specific", "player_rebounds_specific", "player_assists_specific"], "contemplated": True},
    "player_points_each_quarter":     {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_points_q1":               {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_points_q1_x_plus":        {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_points_head_to_head":     {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_points_duo":              {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_points_trio":             {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_top_scorer":              {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},
    "player_top_scorer_team_win":     {"kind": DERIVED, "derived_from": ["player_points_specific", "winner_match"], "contemplated": True},
    "player_points_comparison":       {"kind": DERIVED, "derived_from": "player_points_specific", "contemplated": True},

    # ── NO CONTEMPLADOS ───────────────────────────────────────────────────────
    # Señal insuficiente: eventos iniciales extremadamente estocásticos
    "first_basket_player":        {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "first_basket_method":        {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "first_basket_team_player":   {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "first_basket_winner_double": {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "first_basket_q1_winner_double": {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "both_teams_score_first_minute": {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "three_pointers_first_3_min": {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "lead_from_start":            {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "special_bet":                {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
    "triple_bet":                 {"kind": NOT_CONTEMPLATED, "model_type": None, "contemplated": False},
}

NOT_CONTEMPLATED_MARKETS: set[str] = {
    k for k, v in MARKET_REGISTRY.items() if not v.get("contemplated", True)
}

PRIMARY_MARKETS: set[str] = {
    k for k, v in MARKET_REGISTRY.items() if v.get("kind") == PRIMARY
}

DERIVED_MARKETS: set[str] = {
    k for k, v in MARKET_REGISTRY.items() if v.get("kind") == DERIVED
}


def get_primary_market(market: str) -> str | None:
    """
    Resuelve el mercado primario de un mercado derivado.
    Para mercados derivados con varios primarios, devuelve el primero.
    Retorna None si el mercado no está contemplado.
    """
    cfg = MARKET_REGISTRY.get(market)
    if cfg is None or not cfg.get("contemplated"):
        return None
    if cfg["kind"] == PRIMARY:
        return market
    derived_from = cfg.get("derived_from")
    if isinstance(derived_from, list):
        return derived_from[0] if derived_from else None
    return derived_from


def extract_target(game_id: str, target: str) -> float | None:
    """
    Extrae el valor de entrenamiento (label) para un partido y tipo de target.
    Retorna None si no hay datos suficientes para calcularlo.
    """
    try:
        from core.models import Game
        game = Game.objects.select_related("home_team", "away_team").filter(game_id=game_id).first()
        if not game:
            return None

        h = game.home_score
        a = game.away_score

        if target == "home_win":
            return (1.0 if h > a else 0.0) if (h is not None and a is not None) else None
        if target == "total":
            return float(h + a) if (h is not None and a is not None) else None
        if target == "home_score":
            return float(h) if h is not None else None
        if target == "away_score":
            return float(a) if a is not None else None
        if target == "margin":
            return float(h - a) if (h is not None and a is not None) else None

        return _extract_summary_target(game, target)

    except Exception as exc:
        logger.warning("extract_target error game=%s target=%s: %s", game_id, target, exc)
        return None


def _extract_summary_target(game, target: str) -> float | None:
    """Targets que requieren GameSummary (cuartos, mitades, OT, etc.)."""
    try:
        from game.models import GameSummary

        home_abb = game.home_team.abbreviation if game.home_team else None
        away_abb = game.away_team.abbreviation if game.away_team else None
        if not home_abb or not away_abb:
            return None

        home_s = GameSummary.objects.filter(game_id=game.game_id, team_abb=home_abb).first()
        away_s = GameSummary.objects.filter(game_id=game.game_id, team_abb=away_abb).first()
        if not home_s or not away_s:
            return None

        def _q(summary, field: str) -> int:
            return getattr(summary, field, 0) or 0

        h = {q: _q(home_s, q) for q in ("q1", "q2", "q3", "q4")}
        a = {q: _q(away_s, q) for q in ("q1", "q2", "q3", "q4")}

        h1_home = h["q1"] + h["q2"]
        h1_away = a["q1"] + a["q2"]
        h2_home = h["q3"] + h["q4"]
        h2_away = a["q3"] + a["q4"]

        table: dict[str, float | None] = {
            # Mitades
            "h1_home_win": 1.0 if h1_home > h1_away else 0.0,
            "h1_total":    float(h1_home + h1_away),
            "h1_home":     float(h1_home),
            "h1_away":     float(h1_away),
            "h2_home_win": 1.0 if h2_home > h2_away else 0.0,
            "h2_total":    float(h2_home + h2_away),
            "h2_home":     float(h2_home),
            "h2_away":     float(h2_away),
            # Cuartos
            **{f"q{i}_home_win": 1.0 if h[f"q{i}"] > a[f"q{i}"] else 0.0 for i in range(1, 5)},
            **{f"q{i}_total": float(h[f"q{i}"] + a[f"q{i}"]) for i in range(1, 5)},
            **{f"q{i}_home": float(h[f"q{i}"]) for i in range(1, 5)},
            **{f"q{i}_away": float(a[f"q{i}"]) for i in range(1, 5)},
            # Especiales de partido
            "ot":              1.0 if (_q(home_s, "ot1") > 0) else 0.0,
            "first_half_more": 1.0 if (h1_home + h1_away) >= (h2_home + h2_away) else 0.0,
            "quarter_most":    float(max(range(1, 5), key=lambda i: h[f"q{i}"] + a[f"q{i}"])),
            "home_win_all_q":  1.0 if all(h[f"q{i}"] > a[f"q{i}"] for i in range(1, 5)) else 0.0,
            "home_win_both_h": 1.0 if (h1_home > h1_away and h2_home > h2_away) else 0.0,
            # Requiere GamePlayByPlay — sin implementar todavía
            "home_first_score": None,
        }
        return table.get(target)

    except Exception as exc:
        logger.warning("_extract_summary_target error: %s", exc)
        return None
