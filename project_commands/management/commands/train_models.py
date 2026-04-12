"""
Entrena modelos ML por mercado NBA.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Entrena modelos XGBoost/Poisson por mercado NBA"

    def add_arguments(self, parser):
        parser.add_argument("--season-type", type=str, default="Regular Season", help="Tipo temporada")
        parser.add_argument("--market", type=str, default="moneyline", help="Mercado a entrenar")
        parser.add_argument("--model-dir", type=str, default="", help="Carpeta modelos (opcional)")

    def handle(self, *args, **options):
        season_type = options["season_type"]
        market = options["market"]
        model_dir = options["model_dir"]

        from django.conf import settings
        from pathlib import Path

        if not model_dir:
            model_dir = Path(getattr(settings, "MODEL_STORAGE_PATH", settings.MEDIA_ROOT / "models"))

        self.stdout.write(f"[train_models] Mercado: {market} | Tipo: {season_type}")
        self.stdout.write(f"[train_models] Directorio: {model_dir}")

        from predictions.train import train_and_save

        ok, msg = train_and_save(
            season_type=season_type,
            market=market,
            model_dir=model_dir,
            stdout=self.stdout,
        )

        if ok:
            self.stdout.write(self.style.SUCCESS(f"✅ {msg}"))
        else:
            self.stderr.write(self.style.ERROR(f"❌ {msg}"))
