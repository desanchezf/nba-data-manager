"""Comprobar si los modelos Ollama están instalados y alineados con registry.ollama.ai."""

from __future__ import annotations

import logging
from typing import Any

import requests
from django.utils import timezone

from .ollama_utils import resolve_ollama_base_url

logger = logging.getLogger(__name__)

REGISTRY_MANIFEST_URL = "https://registry.ollama.ai/v2/library/{library}/manifests/{tag}"


def parse_library_tag(model_name: str) -> tuple[str, str]:
    s = (model_name or "").strip()
    if not s:
        return "", "latest"
    if ":" in s:
        base, tag = s.rsplit(":", 1)
        return base.strip(), (tag.strip() or "latest")
    return s, "latest"


def normalize_digest_hex(d: str | None) -> str | None:
    if not d:
        return None
    x = d.strip().lower()
    if x.startswith("sha256:"):
        x = x[7:]
    return x or None


def fetch_tags_json(base_url: str, timeout: int = 45) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/tags"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def find_installed_model(tags_payload: dict[str, Any], wanted: str) -> dict[str, Any] | None:
    models = tags_payload.get("models") or []
    w_base, w_tag = parse_library_tag(wanted)
    if not w_base:
        return None
    candidates = []
    for m in models:
        name = (m.get("name") or m.get("model") or "").strip()
        if not name:
            continue
        m_base, m_tag = parse_library_tag(name)
        if m_base.lower() != w_base.lower():
            continue
        candidates.append((m, m_tag))
    if not candidates:
        return None
    if w_tag.lower() == "latest":
        for m, m_tag in candidates:
            if m_tag.lower() == "latest":
                return m
        return candidates[0][0]
    for m, m_tag in candidates:
        if m_tag.lower() == w_tag.lower():
            return m
    return None


def sync_ollama_model_config(config) -> None:
    """Actualiza campos de sincronización en una instancia de OllamaModelConfig."""
    server = config.server
    now = timezone.now()
    fields = [
        "ollama_sync_at", "ollama_installed", "ollama_local_digest",
        "ollama_registry_digest", "ollama_up_to_date", "ollama_sync_detail", "updated_at",
    ]

    if not server.enabled:
        config.ollama_sync_at = now
        config.ollama_installed = None
        config.ollama_local_digest = ""
        config.ollama_registry_digest = ""
        config.ollama_up_to_date = None
        config.ollama_sync_detail = "Servidor deshabilitado; no se comprobó."
        config.save(update_fields=fields)
        return

    base = resolve_ollama_base_url(server.base_url)
    try:
        tags = fetch_tags_json(base)
    except requests.RequestException as e:
        config.ollama_sync_at = now
        config.ollama_installed = None
        config.ollama_local_digest = ""
        config.ollama_registry_digest = ""
        config.ollama_up_to_date = None
        config.ollama_sync_detail = f"Error al consultar /api/tags: {e}"
        config.save(update_fields=fields)
        return

    match = find_installed_model(tags, config.model_name)
    if not match:
        config.ollama_sync_at = now
        config.ollama_installed = False
        config.ollama_local_digest = ""
        config.ollama_registry_digest = ""
        config.ollama_up_to_date = None
        config.ollama_sync_detail = "Modelo no instalado en el servidor Ollama."
        config.save(update_fields=fields)
        return

    raw_local = (match.get("digest") or "").strip()
    config.ollama_installed = True
    config.ollama_local_digest = raw_local[:128]

    lib, tag = parse_library_tag(config.model_name)
    try:
        url = REGISTRY_MANIFEST_URL.format(library=lib, tag=tag)
        r = requests.head(url, timeout=45, allow_redirects=True)
        raw = (r.headers.get("ollama-content-digest") or r.headers.get("Docker-Content-Digest") or "")
        reg_d = normalize_digest_hex(raw)
        reg_err = None if reg_d else "Sin digest en registry."
    except requests.RequestException as e:
        reg_d = None
        reg_err = str(e)

    if reg_err or not reg_d:
        config.ollama_registry_digest = ""
        config.ollama_up_to_date = None
        config.ollama_sync_detail = f"Instalado. {reg_err or 'Sin digest de registry.'}"[:500]
        config.ollama_sync_at = now
        config.save(update_fields=fields)
        return

    config.ollama_registry_digest = reg_d[:128]
    loc_n = normalize_digest_hex(raw_local)
    if loc_n and reg_d and loc_n == reg_d.lower():
        config.ollama_up_to_date = True
        config.ollama_sync_detail = "Al día con registry.ollama.ai."
    else:
        config.ollama_up_to_date = False
        config.ollama_sync_detail = "El digest local difiere del registro público; ejecute pull para actualizar."
    config.ollama_sync_at = now
    config.save(update_fields=fields)
