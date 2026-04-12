"""Tareas Celery para IA / Ollama."""

from celery import shared_task


@shared_task(name="ia.check_ollama_models_registry_sync")
def check_ollama_models_registry_sync():
    """
    Comprueba cada OllamaModelConfig:
    presencia en /api/tags y comparación de digest con registry.ollama.ai.
    """
    from .models import OllamaModelConfig
    from .ollama_sync import sync_ollama_model_config

    qs = OllamaModelConfig.objects.select_related("server").filter(server__enabled=True)
    n = 0
    for cfg in qs.iterator():
        sync_ollama_model_config(cfg)
        n += 1
    return {"status": "ok", "checked": n}
