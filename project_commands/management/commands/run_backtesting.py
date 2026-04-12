"""
Backtesting walk-forward NBA: evalúa el modelo temporada a temporada.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backtesting walk-forward NBA: Sharpe, max drawdown y ROI por temporada"

    def add_arguments(self, parser):
        parser.add_argument("--market", type=str, default="moneyline", help="Mercado a evaluar")
        parser.add_argument("--season-type", type=str, default="Regular Season", help="Tipo temporada")
        parser.add_argument("--start-year", type=int, default=2020, help="Año inicio evaluación")
        parser.add_argument("--end-year", type=int, default=2024, help="Año fin evaluación")
        parser.add_argument("--retrain", action="store_true", help="Re-entrenar modelo en cada fold")

    def handle(self, *args, **options):
        market = options["market"]
        season_type = options["season_type"]
        start_year = options["start_year"]
        end_year = options["end_year"]
        retrain = options["retrain"]

        self.stdout.write(
            f"[backtesting] Mercado: {market} | {start_year}-{end_year} | "
            f"Tipo: {season_type} | Reentrenar: {retrain}"
        )

        from predictions.backtesting import run_walk_forward_backtest

        result = run_walk_forward_backtest(
            market=market,
            season_type=season_type,
            start_year=start_year,
            end_year=end_year,
            retrain=retrain,
            stdout=self.stdout,
        )

        if "error" in result:
            self.stderr.write(self.style.ERROR(f"❌ {result['error']}"))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ Resumen ({result.get('periods')} periodos):\n"
                f"  Accuracy media:  {result.get('mean_accuracy')}\n"
                f"  Log-loss media:  {result.get('mean_log_loss')}\n"
                f"  ROI medio:       {result.get('mean_roi_pct')}%\n"
                f"  Sharpe ratio:    {result.get('sharpe_ratio')}\n"
                f"  Max drawdown:    {result.get('max_drawdown')}%"
            ))
