"""
Pipeline completo NBA sin opciones:
ETL → sync_normalized → compute_features (todos los feature markets)
→ train_models (todos los PRIMARY markets) para Regular Season y Playoffs.
"""

import time
from datetime import datetime

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


def _fmt(seconds):
    """Human-readable duration."""
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s}s" if m else f"{s}s"


class Command(BaseCommand):
    help = "Pipeline NBA completo: ETL→features→entrenamiento"

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.stdout.write(f"[{ts}] {msg}")

    def _step(self, label, command, *args, **kwargs):
        self._log(f"▶ {label}...")
        t0 = time.time()
        try:
            call_command(
                command, *args,
                stdout=self.stdout, stderr=self.stderr,
                **kwargs
            )
            elapsed = _fmt(time.time() - t0)
            self.stdout.write(
                self.style.SUCCESS(f"  ✅ {label} ({elapsed})")
            )
            return True
        except Exception as exc:
            elapsed = _fmt(time.time() - t0)
            self.stderr.write(
                self.style.ERROR(f"  ❌ {label} ({elapsed}): {exc}")
            )
            return False

    def handle(self, *args, **options):
        sep = "=" * 60
        t_total = time.time()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.stdout.write(f"\n{sep}")
        self.stdout.write(f"  NBA Full Pipeline — {now}")
        self.stdout.write(
            "  Regular Season + Playoffs · todos los mercados"
        )
        self.stdout.write(f"{sep}\n")

        # 1. ETL
        self.stdout.write("\n[1/4] ── Import data ─────────────────────────")
        if not self._step("import_data", "import_data"):
            self.stderr.write(
                self.style.ERROR("Pipeline abortado: ETL falló.")
            )
            return

        # 2. Sync
        self.stdout.write(
            "\n[2/4] ── Sync normalized ──────────────────────"
        )
        self._step("sync_normalized", "sync_normalized")

        # 3. Compute features
        fm_list = _feature_markets()
        total_f = len(fm_list) * len(SEASON_TYPES)
        self.stdout.write(
            f"\n[3/4] ── Compute features "
            f"({len(fm_list)} markets × {len(SEASON_TYPES)} tipos"
            f" = {total_f}) ──────"
        )
        done_f = 0
        ok_f = 0
        for stype in SEASON_TYPES:
            for fm in fm_list:
                done_f += 1
                label = f"features {fm}/{stype} [{done_f}/{total_f}]"
                ok = self._step(
                    label, "compute_features",
                    "--market", fm, "--season-type", stype,
                )
                if ok:
                    ok_f += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"  Features: {ok_f}/{total_f} completados"
            )
        )

        # 4. Train models
        pm_list = _primary_markets()
        total_t = len(pm_list) * len(SEASON_TYPES)
        self.stdout.write(
            f"\n[4/4] ── Train models "
            f"({len(pm_list)} markets × {len(SEASON_TYPES)} tipos"
            f" = {total_t}) ──────────"
        )
        done_t = 0
        ok_t = 0
        for stype in SEASON_TYPES:
            for market in pm_list:
                done_t += 1
                label = f"train {market}/{stype} [{done_t}/{total_t}]"
                ok = self._step(
                    label, "train_models",
                    "--market", market, "--season-type", stype,
                )
                if ok:
                    ok_t += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"  Modelos: {ok_t}/{total_t} entrenados"
            )
        )

        elapsed_total = _fmt(time.time() - t_total)
        self.stdout.write(
            self.style.SUCCESS(
                f"\n{sep}\n"
                f"  ✅ Pipeline completado en {elapsed_total}\n"
                f"{sep}"
            )
        )
