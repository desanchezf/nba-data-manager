"""
Pipeline completo NBA:
ETL → sync_normalized → compute_features → train_models

Equivale a ejecutar todos los pasos de forma secuencial.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Pipeline completo NBA: ETL → features → entrenamiento"

    def add_arguments(self, parser):
        parser.add_argument("--season-type", type=str, default="Regular Season", help="Tipo temporada")
        parser.add_argument("--skip-etl", action="store_true", help="Omitir paso ETL (import_data)")
        parser.add_argument("--skip-sync", action="store_true", help="Omitir sync_normalized")
        parser.add_argument("--skip-features", action="store_true", help="Omitir compute_features")
        parser.add_argument("--skip-train", action="store_true", help="Omitir entrenamiento")
        parser.add_argument("--market", type=str, default="moneyline", help="Mercado a entrenar")
        parser.add_argument("--to-redis", action="store_true", help="Escribir features en Redis")

    def handle(self, *args, **options):
        season_type = options["season_type"]
        skip_etl = options["skip_etl"]
        skip_sync = options["skip_sync"]
        skip_features = options["skip_features"]
        skip_train = options["skip_train"]
        market = options["market"]
        to_redis = options["to_redis"]

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"  NBA Pipeline - {season_type}")
        self.stdout.write(f"{'='*60}\n")

        # Paso 1: Import data
        if not skip_etl:
            self.stdout.write("\n[1/4] Importando datos (import_data)...")
            try:
                call_command("import_data", stdout=self.stdout, stderr=self.stderr)
                self.stdout.write(self.style.SUCCESS("  ✅ import_data completado"))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"  ❌ import_data falló: {exc}"))
                return
        else:
            self.stdout.write("[1/4] Omitiendo import_data (--skip-etl)")

        # Paso 2: Sync normalized
        if not skip_sync:
            self.stdout.write("\n[2/4] Sincronizando modelos normalizados (sync_normalized)...")
            try:
                call_command("sync_normalized", stdout=self.stdout, stderr=self.stderr)
                self.stdout.write(self.style.SUCCESS("  ✅ sync_normalized completado"))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"  ❌ sync_normalized falló: {exc}"))
        else:
            self.stdout.write("[2/4] Omitiendo sync_normalized (--skip-sync)")

        # Paso 3: Compute features
        if not skip_features:
            self.stdout.write(f"\n[3/4] Calculando features (mercado: {market})...")
            try:
                args = ["--market", market, "--season-type", season_type]
                if to_redis:
                    args.append("--to-redis")
                call_command("compute_features", *args, stdout=self.stdout, stderr=self.stderr)
                self.stdout.write(self.style.SUCCESS("  ✅ compute_features completado"))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"  ❌ compute_features falló: {exc}"))
        else:
            self.stdout.write("[3/4] Omitiendo compute_features (--skip-features)")

        # Paso 4: Train models
        if not skip_train:
            self.stdout.write(f"\n[4/4] Entrenando modelo (mercado: {market})...")
            try:
                call_command(
                    "train_models",
                    "--market", market,
                    "--season-type", season_type,
                    stdout=self.stdout, stderr=self.stderr,
                )
                self.stdout.write(self.style.SUCCESS("  ✅ train_models completado"))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"  ❌ train_models falló: {exc}"))
        else:
            self.stdout.write("[4/4] Omitiendo train_models (--skip-train)")

        self.stdout.write(self.style.SUCCESS(
            f"\n{'='*60}\n  ✅ Pipeline NBA completado\n{'='*60}"
        ))
