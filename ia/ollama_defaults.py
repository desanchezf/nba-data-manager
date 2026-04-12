"""Modelos Ollama por defecto para NBA Data Manager."""

from __future__ import annotations

import os
from typing import List, Tuple


def get_default_ollama_model_specs() -> List[Tuple[str, str, bool]]:
    """Devuelve lista (model_name, alias_en_ui, is_default)."""
    m1 = os.getenv("OLLAMA_DEFAULT_MODEL", "qwen2.5-coder").strip()
    a1 = os.getenv("OLLAMA_DEFAULT_ALIAS", "Qwen 2.5 Coder").strip()
    m2 = os.getenv("OLLAMA_SECOND_MODEL", "llama3.2").strip()
    a2 = os.getenv("OLLAMA_SECOND_ALIAS", "Llama 3.2").strip()
    return [
        (m1, a1, True),
        (m2, a2, False),
    ]


def get_default_model_names_for_pull() -> List[str]:
    """Nombres únicos para ollama pull."""
    seen: set[str] = set()
    out: List[str] = []
    for name, _, _ in get_default_ollama_model_specs():
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out
