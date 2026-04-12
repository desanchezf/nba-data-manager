"""
Descarga en Ollama los modelos por defecto definidos en ia.ollama_defaults.
"""

import time

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Descarga modelos Ollama por defecto (OLLAMA_DEFAULT_MODEL / OLLAMA_SECOND_MODEL)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-wait",
            action="store_true",
            help="Omitir espera al servidor Ollama",
        )

    def handle(self, *args, **options):
        skip_wait = options["skip_wait"]

        from django.conf import settings
        from ia.models import OllamaServer
        from ia.ollama_defaults import get_default_model_names_for_pull
        from ia.ollama_utils import ollama_pull, resolve_ollama_base_url

        base_url_cfg = getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434")

        # Esperar a que Ollama esté disponible
        if not skip_wait:
            self.stdout.write("Esperando al servidor Ollama...")
            import requests
            for attempt in range(10):
                try:
                    r = requests.get(f"{base_url_cfg.rstrip('/')}/api/tags", timeout=5)
                    if r.ok:
                        self.stdout.write(self.style.SUCCESS("  Servidor Ollama disponible."))
                        break
                except Exception:
                    pass
                self.stdout.write(f"  Intento {attempt+1}/10, esperando 5s...")
                time.sleep(5)

        models = get_default_model_names_for_pull()
        self.stdout.write(f"Modelos a descargar: {models}")

        # Obtener servidor del admin o usar URL base
        server = OllamaServer.objects.filter(enabled=True).first()
        if server:
            base = resolve_ollama_base_url(server.base_url)
        else:
            base = base_url_cfg

        for model_name in models:
            self.stdout.write(f"  Descargando: {model_name}...")
            ok, msg = ollama_pull(base, model_name)
            if ok:
                self.stdout.write(self.style.SUCCESS(f"  ✅ {model_name}: {msg}"))
            else:
                self.stderr.write(self.style.WARNING(f"  ⚠️  {model_name}: {msg}"))
