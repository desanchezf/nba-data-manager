"""
Calcula métricas de rendimiento del modelo NBA (accuracy, log-loss, ROI simulado).
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Calcula métricas de rendimiento del modelo NBA"

    def add_arguments(self, parser):
        parser.add_argument("--market", type=str, default="moneyline", help="Mercado a evaluar")
        parser.add_argument("--days", type=int, default=30, help="Días atrás")
        parser.add_argument("--alert-threshold", type=float, default=0.55, help="Umbral de alerta accuracy")

    def handle(self, *args, **options):
        market = options["market"]
        days = options["days"]
        threshold = options["alert_threshold"]

        self.stdout.write(f"[compute_metrics] Mercado: {market} | Días: {days} | Umbral: {threshold}")

        from predictions.monitoring import compute_model_metrics

        result = compute_model_metrics(
            market=market,
            days_back=days,
            alert_threshold=threshold,
            stdout=self.stdout,
        )

        if "error" in result:
            self.stderr.write(self.style.ERROR(f"❌ {result['error']}"))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"✅ {market}: n={result.get('n')} | acc={result.get('accuracy')} | "
                f"ll={result.get('log_loss')} | roi={result.get('roi_pct')}%"
            ))
