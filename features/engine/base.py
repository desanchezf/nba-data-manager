"""
Funciones base para acceso a features desde Redis o DB.
"""

import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

CACHE_PREFIX = getattr(settings, "FEATURES_CACHE_PREFIX", "nba_features")
CACHE_TTL = getattr(settings, "FEATURES_CACHE_TTL", 86400 * 7)


def _redis_client():
    """Devuelve un cliente Redis o None si no está disponible."""
    try:
        import redis
        url = getattr(settings, "CELERY_BROKER_URL", "redis://redis:6379/0")
        return redis.Redis.from_url(url, decode_responses=True)
    except Exception:
        return None


def _redis_key(game_id: str, market: str) -> str:
    return f"{CACHE_PREFIX}:{game_id}:{market}"


def get_game_features(game_id: str, market: str = "base") -> dict:
    """Carga features desde Redis (preferido) o DB."""
    # Intentar Redis primero
    r = _redis_client()
    if r:
        try:
            raw = r.get(_redis_key(game_id, market))
            if raw:
                return json.loads(raw)
        except Exception as exc:
            logger.debug("Redis get error: %s", exc)

    # Fallback a DB
    try:
        from features.models import GameFeatureSet
        fs = GameFeatureSet.objects.filter(game_id=game_id, market=market).first()
        return fs.features if fs else {}
    except Exception as exc:
        logger.warning("DB features error: %s", exc)
        return {}


def save_game_features(game_id: str, market: str, features: dict,
                       season: str = "", season_type: str = "",
                       to_redis: bool = False) -> None:
    """Guarda features en DB y opcionalmente en Redis."""
    try:
        from features.models import GameFeatureSet
        GameFeatureSet.objects.update_or_create(
            game_id=game_id,
            market=market,
            defaults={
                "features": features,
                "season": season,
                "season_type": season_type,
            },
        )
    except Exception as exc:
        logger.error("save_game_features DB error: %s", exc)

    if to_redis:
        r = _redis_client()
        if r:
            try:
                r.setex(_redis_key(game_id, market), CACHE_TTL, json.dumps(features))
            except Exception as exc:
                logger.warning("Redis set error: %s", exc)
