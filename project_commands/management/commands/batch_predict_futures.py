"""
Predicciones batch para partidos futuros NBA (sin resultado todavía).
Registra en PredictionLog.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Genera predicciones batch para partidos NBA futuros"

    def add_arguments(self, parser):
        parser.add_argument("--season", type=str, default="", help="Temporada (ej. 2026)")
        parser.add_argument("--market", type=str, default="moneyline", help="Mercado")
        parser.add_argument("--limit", type=int, default=0, help="Límite de partidos")

    def handle(self, *args, **options):
        from datetime import date

        season = options["season"]
        market = options["market"]
        limit = options["limit"]

        self.stdout.write(f"[batch_predict] Temporada: {season or 'actual'} | Mercado: {market}")

        from core.models import Game
        from predictions.inference import get_features_for_matchup, load_model, predict_proba
        from predictions.models import PredictionLog

        today = date.today()
        qs = Game.objects.filter(
            home_score__isnull=True,  # Sin resultado = futuro
            date__gte=today,
        ).exclude(home_team__isnull=True).exclude(away_team__isnull=True)

        if season:
            qs = qs.filter(season=season)
        if limit:
            qs = qs[:limit]

        model_payload = load_model(season_type="Regular_Season", market=market)
        if not model_payload:
            self.stderr.write(self.style.ERROR(f"No hay modelo para mercado '{market}'"))
            return

        feature_names = model_payload.get("feature_names", [])
        count = 0
        errors = 0

        for game in qs.select_related("home_team", "away_team").iterator():
            try:
                features = get_features_for_matchup(
                    home_team_id=game.home_team.team_id,
                    away_team_id=game.away_team.team_id,
                    as_of_date=game.date or today,
                    market=market,
                )
                if not features:
                    continue

                prob_home = predict_proba(features, model_payload, feature_names)
                if prob_home is None:
                    continue

                PredictionLog.objects.update_or_create(
                    game_id=game.game_id,
                    market=market,
                    defaults={
                        "predicted_probs": {
                            "home": round(float(prob_home), 4),
                            "away": round(1.0 - float(prob_home), 4),
                        },
                        "predicted_value": round(float(prob_home), 4),
                        "model_version": f"xgb_{market}",
                    },
                )
                count += 1

            except Exception as exc:
                errors += 1
                self.stderr.write(f"Error en {game.game_id}: {exc}")

        self.stdout.write(self.style.SUCCESS(
            f"✅ Predicciones guardadas: {count}. Errores: {errors}"
        ))
