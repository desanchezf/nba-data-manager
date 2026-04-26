"""
Pipeline completo NBA sin opciones:
ETL → sync_normalized → compute_features (todos los feature markets)
→ train_models (todos los PRIMARY markets) para Regular Season y Playoffs.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

SEASON_TYPES = ["Regular Season", "Playoffs"]


def _primary_markets():
    from predictions.registry import MARKET_REGISTRY, PRIMARY
    return [
        m for m, cfg in MARKET_REGISTRY.items()
        if cfg.get("kind") == PRIMARY
    ]


def _feature_markets():
    """Unique feature_market values across all PRIMARY markets."""
    from predictions.registry import MARKET_REGISTRY, PRIMARY
    seen, result = set(), []
    for cfg in MARKET_REGISTRY.values():
        if cfg.get("kind") == PRIMARY:
            fm = cfg.get("feature_market")
            if fm and fm not in seen:
                seen.add(fm)
                result.append(fm)
    return result


class Command(BaseCommand):
    help = "Pipeline NBA completo: ETL→features→entrenamiento"

    def _step(self, label, command, *args, **kwargs):
        try:
            call_command(
                command, *args,
                stdout=self.stdout, stderr=self.stderr,
                **kwargs
            )
            self.stdout.write(self.style.SUCCESS(f"  ✅ {label}"))
            return True
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"  ❌ {label}: {exc}"))
            return False

    def handle(self, *args, **options):
        sep = "=" * 60
        self.stdout.write(f"\n{sep}")
        self.stdout.write("  NBA Full Pipeline — Regular Season + Playoffs")
        self.stdout.write(f"{sep}\n")

        # 1. ETL
        self.stdout.write("\n[1/4] Importando datos...")
        if not self._step("import_data", "import_data"):
            return

        # 2. Sync
        self.stdout.write("\n[2/4] Sincronizando modelos normalizados...")
        self._step("sync_normalized", "sync_normalized")

        # 3. Compute features por feature_market × season_type
        fm_list = _feature_markets()
        total = len(fm_list) * len(SEASON_TYPES)
        self.stdout.write(
            f"\n[3/4] Calculando features "
            f"({len(fm_list)} markets × {len(SEASON_TYPES)} tipos"
            f" = {total})..."
        )
        done = 0
        for stype in SEASON_TYPES:
            for fm in fm_list:
                ok = self._step(
                    f"features {fm}/{stype}",
                    "compute_features",
                    "--market", fm,
                    "--season-type", stype,
                )
                done += 1
                if ok:
                    self.stdout.write(f"    [{done}/{total}] {fm} / {stype}")

        # 4. Train models por PRIMARY market × season_type
        pm_list = _primary_markets()
        total = len(pm_list) * len(SEASON_TYPES)
        self.stdout.write(
            f"\n[4/4] Entrenando modelos "
            f"({len(pm_list)} markets × {len(SEASON_TYPES)} tipos"
            f" = {total})..."
        )
        done = 0
        for stype in SEASON_TYPES:
            for market in pm_list:
                ok = self._step(
                    f"{market}/{stype}",
                    "train_models",
                    "--market", market,
                    "--season-type", stype,
                )
                done += 1
                if ok:
                    self.stdout.write(f"    [{done}/{total}] {market}")

        self.stdout.write(
            self.style.SUCCESS(f"\n{sep}\n  ✅ Pipeline completado\n{sep}")
        )
