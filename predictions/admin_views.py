"""
Lógica de negocio del Prediction Hub NBA.

Funciones de predicción para cada modo:
  - run_prepartido   → pronóstico pre-partido multi-mercado
  - run_live         → pronóstico en directo con datos parciales del juego
  - run_discovery    → jornada completa, ranking de mejores pronósticos
  - run_combinada    → apuesta combinada (acumulador) para N encuentros
"""

import json
import logging
from datetime import date, datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

BINARY_MARKETS = [
    "moneyline",
    "spread",
    "winner_match",
]

RISK_THRESHOLDS = {
    "conservative": 0.65,
    "moderate": 0.58,
    "aggressive": 0.52,
}


def _decimal_odds_to_prob(odds_decimal):
    if odds_decimal and float(odds_decimal) > 1:
        return round(1.0 / float(odds_decimal), 4)
    return None


def _ev(prob, odds_decimal):
    if prob is None or odds_decimal is None:
        return None
    return round(prob * (float(odds_decimal) - 1) - (1 - prob), 4)


def _score(candidate):
    ev = candidate.get("ev")
    if ev is not None:
        return ev
    return candidate.get("probability", 0)


def _predict_matchup_for_market(home_team_id, away_team_id, as_of_date, market):
    from predictions.inference import get_features_for_matchup, load_model, predict_proba

    features = get_features_for_matchup(
        home_team_id=str(home_team_id),
        away_team_id=str(away_team_id),
        as_of_date=as_of_date,
        market=market,
    )
    if not features:
        return None, {}

    model_payload = load_model(season_type="Regular_Season", market=market)
    if not model_payload:
        return None, features

    feature_names = model_payload.get("feature_names", list(features.keys()))
    prob_home = predict_proba(features, model_payload, feature_names)
    return prob_home, features


def _team_label(team_id):
    try:
        from core.models import Team
        t = Team.objects.filter(team_id=str(team_id)).first()
        return t.name or str(team_id) if t else str(team_id)
    except Exception:
        return str(team_id)


def _build_candidates(home_team_id, away_team_id, market, as_of_date,
                      odds_home=None, odds_away=None, risk_threshold=0.58):
    home_name = _team_label(home_team_id)
    away_name = _team_label(away_team_id)

    prob_home, _ = _predict_matchup_for_market(home_team_id, away_team_id, as_of_date, market)
    if prob_home is None:
        return []

    prob_away = round(1.0 - prob_home, 4)
    candidates = []

    for side, prob, team_name, odds in [
        ("home", prob_home, home_name, odds_home),
        ("away", prob_away, away_name, odds_away),
    ]:
        if prob < risk_threshold:
            continue

        ev_val = _ev(prob, odds) if odds else None
        model_odds = round(1.0 / prob, 3) if prob > 0 else None

        candidates.append({
            "market": market,
            "side": side,
            "home_team": home_name,
            "away_team": away_name,
            "selection": f"{team_name} gana ({market})",
            "probability": round(prob * 100, 1),
            "prob_raw": prob,
            "model_odds": model_odds,
            "odds_decimal": float(odds) if odds else None,
            "ev": ev_val,
            "score": _score({"ev": ev_val, "probability": prob}),
        })

    return candidates


# ─── Pre-partido ──────────────────────────────────────────────────────────────

def run_prepartido(home_team_id, away_team_id, market, risk_level,
                   n_predictions, odds_home=None, odds_away=None, match_date=None):
    as_of_date = match_date or date.today()
    risk_threshold = RISK_THRESHOLDS.get(risk_level, 0.58)
    markets = BINARY_MARKETS if market == "all" else [market]

    all_candidates = []
    errors = []

    for mkt in markets:
        try:
            candidates = _build_candidates(
                home_team_id, away_team_id, mkt, as_of_date,
                odds_home=odds_home, odds_away=odds_away,
                risk_threshold=risk_threshold,
            )
            all_candidates.extend(candidates)
        except Exception as exc:
            logger.warning("prepartido error market=%s: %s", mkt, exc)
            errors.append(f"{mkt}: {exc}")

    all_candidates.sort(key=_score, reverse=True)
    return all_candidates[:int(n_predictions)], errors


# ─── En directo ───────────────────────────────────────────────────────────────

def run_live(game_id, home_team_id, away_team_id, market, risk_level, live_data_json):
    errors = []
    risk_threshold = RISK_THRESHOLDS.get(risk_level, 0.58)

    try:
        if isinstance(live_data_json, str):
            live_data = json.loads(live_data_json)
        else:
            live_data = live_data_json
    except json.JSONDecodeError as e:
        return None, [f"JSON inválido: {e}"]

    live_home_id = live_data.get("home_team_id") or home_team_id
    live_away_id = live_data.get("away_team_id") or away_team_id
    period = live_data.get("period", 1)
    home_score = live_data.get("home_score", 0)
    away_score = live_data.get("away_score", 0)
    win_prob_home_raw = live_data.get("win_probability_home")

    from predictions.inference import load_model, predict_proba
    features = {}

    if game_id:
        try:
            from predictions.inference import get_features_for_game
            features = get_features_for_game(game_id, market=market) or {}
        except Exception as exc:
            logger.warning("live: no features from game_id=%s: %s", game_id, exc)

    if not features:
        try:
            from predictions.inference import get_features_for_matchup
            features = get_features_for_matchup(
                home_team_id=str(live_home_id),
                away_team_id=str(live_away_id),
                market=market,
            ) or {}
        except Exception as exc:
            errors.append(f"No se pudieron calcular features: {exc}")
            return None, errors

    if not features:
        return None, ["Sin features disponibles para este partido."]

    # Enriquecer con datos en directo
    if win_prob_home_raw is not None:
        features["win_prob_home_live"] = float(win_prob_home_raw)
    features["period_current"] = float(period)
    features["home_score_live"] = float(home_score)
    features["away_score_live"] = float(away_score)
    features["score_diff_live"] = float(home_score) - float(away_score)

    model_payload = load_model(season_type="Regular_Season", market=market)
    if not model_payload:
        if win_prob_home_raw is not None:
            prob_home = float(win_prob_home_raw)
        else:
            return None, [f"No hay modelo entrenado para mercado '{market}'."]
    else:
        feature_names = model_payload.get("feature_names", list(features.keys()))
        prob_home = predict_proba(features, model_payload, feature_names)
        if prob_home is None:
            return None, ["Error durante la inferencia del modelo."]

    home_name = _team_label(live_home_id)
    away_name = _team_label(live_away_id)

    result = {
        "game_id": game_id or f"{live_home_id}-vs-{live_away_id}",
        "home_team": home_name,
        "away_team": away_name,
        "market": market,
        "period": period,
        "home_score": home_score,
        "away_score": away_score,
        "prob_home": round(prob_home * 100, 1),
        "prob_away": round((1 - prob_home) * 100, 1),
        "prob_home_raw": prob_home,
        "model_odds_home": round(1.0 / prob_home, 3) if prob_home > 0 else None,
        "model_odds_away": round(1.0 / (1 - prob_home), 3) if prob_home < 1 else None,
        "above_threshold": prob_home >= risk_threshold or (1 - prob_home) >= risk_threshold,
        "favored": home_name if prob_home >= 0.5 else away_name,
        "favored_prob": round(max(prob_home, 1 - prob_home) * 100, 1),
    }

    return result, errors


# ─── Prediction Discovery ─────────────────────────────────────────────────────

def run_discovery(matchday_json, market, n_top, risk_level):
    errors = []
    risk_threshold = RISK_THRESHOLDS.get(risk_level, 0.58)

    try:
        if isinstance(matchday_json, str):
            matchday = json.loads(matchday_json)
        else:
            matchday = matchday_json
        if not isinstance(matchday, list):
            matchday = [matchday]
    except json.JSONDecodeError as e:
        return [], [f"JSON inválido: {e}"]

    all_candidates = []

    for i, match in enumerate(matchday):
        if not isinstance(match, dict):
            continue
        home_id = match.get("home_team_id")
        away_id = match.get("away_team_id")
        if not home_id or not away_id:
            errors.append(f"Partido {i+1}: faltan home_team_id o away_team_id.")
            continue

        date_str = match.get("date")
        as_of_date = None
        if date_str:
            try:
                as_of_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass
        as_of_date = as_of_date or date.today()

        odds_home = match.get("odds_home")
        odds_away = match.get("odds_away")
        markets = BINARY_MARKETS if market == "all" else [market]

        for mkt in markets:
            try:
                candidates = _build_candidates(
                    home_id, away_id, mkt, as_of_date,
                    odds_home=odds_home, odds_away=odds_away,
                    risk_threshold=risk_threshold,
                )
                all_candidates.extend(candidates)
            except Exception as exc:
                logger.warning("discovery error match=%s market=%s: %s", i+1, mkt, exc)
                errors.append(f"Partido {i+1} ({mkt}): {exc}")

    all_candidates.sort(key=_score, reverse=True)
    return all_candidates[:int(n_top)], errors


# ─── Apuesta Combinada ────────────────────────────────────────────────────────

def run_combinada(matches_json, market, n_selections, risk_level, stake_euros=None):
    all_candidates, errors = run_discovery(
        matchday_json=matches_json,
        market=market,
        n_top=50,
        risk_level=risk_level,
    )

    n = int(n_selections)
    selections = all_candidates[:n]

    if not selections:
        return {"selections": [], "summary": {}, "errors": errors}

    combined_odds = 1.0
    combined_prob = 1.0

    for sel in selections:
        odds = sel.get("odds_decimal") or sel.get("model_odds")
        prob = sel.get("prob_raw", 0)
        if odds:
            combined_odds *= float(odds)
        combined_prob *= prob

    combined_odds = round(combined_odds, 3)
    combined_prob_pct = round(combined_prob * 100, 2)

    stake = float(stake_euros) if stake_euros else None
    potential_return = round(combined_odds * stake, 2) if stake else None
    potential_profit = round((combined_odds - 1) * stake, 2) if stake else None

    summary = {
        "n_selections": len(selections),
        "combined_odds": combined_odds,
        "combined_prob_pct": combined_prob_pct,
        "stake_euros": stake,
        "potential_return": potential_return,
        "potential_profit": potential_profit,
        "ev_combined": round(combined_prob * (combined_odds - 1) - (1 - combined_prob), 4) if combined_odds else None,
    }

    return {
        "selections": selections,
        "summary": summary,
        "errors": errors,
    }


# ─── Guardar apuesta ──────────────────────────────────────────────────────────

def save_prepartido_bet(candidate, stake_euros, risk_level, prediction_mode="prepartido"):
    from predictions.models import BettingRecord

    record = BettingRecord(
        prediction_mode=prediction_mode,
        bet_type="single",
        risk_level=risk_level,
        market=candidate.get("market", ""),
        home_team=candidate.get("home_team", ""),
        away_team=candidate.get("away_team", ""),
        selection=candidate.get("selection", ""),
        odds_decimal=candidate.get("odds_decimal") or candidate.get("model_odds") or 1.0,
        stake_euros=Decimal(str(stake_euros)) if stake_euros else Decimal("0.00"),
        units=1.0,
        prob_predicted=candidate.get("prob_raw"),
        ev_predicted=candidate.get("ev"),
        result="pending",
    )
    record.save()
    return record


def save_combined_bet(selections, summary, stake_euros, risk_level):
    from predictions.models import BettingRecord

    combined_label = " + ".join(
        s.get("selection", "?")[:40] for s in selections[:5]
    )

    record = BettingRecord(
        prediction_mode="combinada",
        bet_type="combined",
        risk_level=risk_level,
        market=selections[0].get("market", "") if selections else "",
        home_team=selections[0].get("home_team", "") if selections else "",
        away_team=selections[0].get("away_team", "") if selections else "",
        selection=combined_label,
        odds_decimal=summary.get("combined_odds", 1.0),
        stake_euros=Decimal(str(stake_euros)) if stake_euros else Decimal("0.00"),
        units=1.0,
        prob_predicted=summary.get("combined_prob_pct", 0) / 100 if summary.get("combined_prob_pct") else None,
        ev_predicted=summary.get("ev_combined"),
        selections_json=selections,
        result="pending",
        notes=f"Acumulador {len(selections)} selecciones. Cuota: {summary.get('combined_odds')}",
    )
    record.save()
    return record
