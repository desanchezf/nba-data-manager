"""
Endpoints de predicción NBA (REST).
"""

from datetime import date

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def predict(request, game_id, market="moneyline"):
    """Predicción para un partido ya existente en BD."""
    try:
        from predictions.inference import get_features_for_game, load_model, predict_proba

        features = get_features_for_game(game_id, market=market)
        if not features:
            return JsonResponse({"error": "No features found for this game/market"}, status=404)

        model_payload = load_model(season_type="Regular_Season", market=market)
        if not model_payload:
            return JsonResponse({"error": f"No model found for market '{market}'"}, status=404)

        feature_names = model_payload.get("feature_names", list(features.keys()))
        prob_home = predict_proba(features, model_payload, feature_names)

        if prob_home is None:
            return JsonResponse({"error": "Inference error"}, status=500)

        return JsonResponse({
            "game_id": game_id,
            "market": market,
            "prob_home_win": round(float(prob_home), 4),
            "prob_away_win": round(1.0 - float(prob_home), 4),
            "model_odds_home": round(1.0 / prob_home, 3) if prob_home > 0 else None,
        })
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)


@require_http_methods(["GET"])
def predict_matchup(request):
    """
    Predicción para un enfrentamiento sin partido en BD.
    Parámetros: home_team, away_team, date (YYYY-MM-DD), market
    """
    home_team = request.GET.get("home_team", "")
    away_team = request.GET.get("away_team", "")
    date_str = request.GET.get("date", "")
    market = request.GET.get("market", "moneyline")

    if not home_team or not away_team:
        return JsonResponse({"error": "home_team and away_team are required"}, status=400)

    try:
        from predictions.inference import get_features_for_matchup, load_model, predict_proba
        from django.utils.dateparse import parse_date

        as_of_date = parse_date(date_str) if date_str else date.today()
        features = get_features_for_matchup(
            home_team_id=home_team,
            away_team_id=away_team,
            as_of_date=as_of_date,
            market=market,
        )
        if not features:
            return JsonResponse({"error": "No features could be computed for this matchup"}, status=404)

        model_payload = load_model(season_type="Regular_Season", market=market)
        if not model_payload:
            return JsonResponse({"error": f"No model found for market '{market}'"}, status=404)

        feature_names = model_payload.get("feature_names", list(features.keys()))
        prob_home = predict_proba(features, model_payload, feature_names)

        if prob_home is None:
            return JsonResponse({"error": "Inference error"}, status=500)

        return JsonResponse({
            "home_team": home_team,
            "away_team": away_team,
            "date": str(as_of_date),
            "market": market,
            "prob_home_win": round(float(prob_home), 4),
            "prob_away_win": round(1.0 - float(prob_home), 4),
            "model_odds_home": round(1.0 / prob_home, 3) if prob_home > 0 else None,
            "model_odds_away": round(1.0 / (1 - prob_home), 3) if prob_home < 1 else None,
        })
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)
