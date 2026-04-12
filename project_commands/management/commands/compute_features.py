"""
Calcula features por partido/mercado NBA y las guarda en DB/Redis.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Calcula features NBA por partido y mercado"

    def add_arguments(self, parser):
        parser.add_argument("--season", type=str, default="", help="Temporada (ej. 2025)")
        parser.add_argument("--season-type", type=str, default="Regular Season", help="Tipo temporada")
        parser.add_argument("--market", type=str, default="base", help="Mercado (moneyline, totals, spread, etc.)")
        parser.add_argument("--game-id", type=str, default="", help="Solo un partido (opcional)")
        parser.add_argument("--limit", type=int, default=0, help="Límite de partidos")
        parser.add_argument("--to-redis", action="store_true", help="Escribir también en Redis")

    def handle(self, *args, **options):
        season = options["season"]
        season_type = options["season_type"]
        market = options["market"]
        game_id = options["game_id"]
        limit = options["limit"]
        to_redis = options["to_redis"]

        self.stdout.write(f"[compute_features] Mercado: {market} | Temporada: {season or 'todas'}")

        from core.models import Game
        from features.engine.matchup import compute_features_for_matchup
        from features.engine.market import compute_market_features
        from features.engine.base import save_game_features

        qs = Game.objects.exclude(home_team__isnull=True).exclude(away_team__isnull=True)
        if game_id:
            qs = qs.filter(game_id=game_id)
        if season:
            qs = qs.filter(season=season)
        if season_type:
            qs = qs.filter(season_type__icontains=season_type)
        if limit:
            qs = qs[:limit]

        count = 0
        errors = 0

        for game in qs.select_related("home_team", "away_team").iterator(chunk_size=500):
            try:
                features = compute_features_for_matchup(
                    home_team_id=game.home_team.team_id,
                    away_team_id=game.away_team.team_id,
                    as_of_date=game.date,
                    market=market,
                )

                # Añadir features específicas del mercado
                market_extras = compute_market_features(features, market)
                features.update(market_extras)

                # Añadir target si el partido tiene resultado
                if game.home_score is not None and game.away_score is not None:
                    features["home_win"] = 1 if game.home_score > game.away_score else 0
                    features["total_pts"] = game.home_score + game.away_score
                    features["home_pts"] = game.home_score
                    features["away_pts"] = game.away_score

                save_game_features(
                    game_id=game.game_id,
                    market=market,
                    features=features,
                    season=game.season,
                    season_type=game.season_type,
                    to_redis=to_redis,
                )
                count += 1

                if count % 100 == 0:
                    self.stdout.write(f"  {count} partidos procesados...")

            except Exception as exc:
                errors += 1
                self.stderr.write(f"Error en {game.game_id}: {exc}")

        self.stdout.write(self.style.SUCCESS(
            f"✅ Features calculadas: {count} partidos. Errores: {errors}"
        ))
