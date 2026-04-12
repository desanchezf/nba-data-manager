"""Helpers para hablar con el servidor Ollama."""

from __future__ import annotations

import json
from typing import Tuple

import requests
from django.conf import settings


def resolve_ollama_base_url(server_base_url: str) -> str:
    """Aplica OLLAMA_BASE_URL sobre URLs locales cuando corresponde."""
    base = (server_base_url or "").rstrip("/")
    override = (getattr(settings, "OLLAMA_BASE_URL", "") or "").rstrip("/")
    if override and any(
        h in base for h in ("localhost", "127.0.0.1", "host.docker.internal")
    ):
        return override
    return base


def ollama_pull(base_url: str, model_name: str, timeout: int = 3600) -> Tuple[bool, str]:
    """
    POST /api/pull (stream). Devuelve (éxito, mensaje).
    """
    name = (model_name or "").strip()
    if not name:
        return False, "Indique un nombre de modelo."

    url = f"{base_url.rstrip('/')}/api/pull"
    lines: list[str] = []
    try:
        resp = requests.post(
            url,
            json={"name": name},
            stream=True,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        for raw in resp.iter_lines(decode_unicode=True):
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            err = data.get("error")
            if err:
                return False, str(err)
            st = data.get("status")
            if st:
                lines.append(str(st))
        tail = lines[-1] if lines else "pull completado"
        return True, tail
    except requests.RequestException as e:
        return False, str(e)
