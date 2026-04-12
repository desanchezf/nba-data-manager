"""
Almacén de features agregadas por juego/jugador y por mercado NBA.
Persistencia en DB y en Redis (key: GAME_ID+market) para inferencia rápida.
"""

from django.db import models


class GameFeatureSet(models.Model):
    """
    Features agregadas por partido (y opcionalmente por mercado).
    key Redis: features:{game_id}:{market}
    """

    game_id = models.CharField("GAME_ID", max_length=64, db_index=True)
    market = models.CharField(
        "Mercado (moneyline, totals, spread, props, in_game)",
        max_length=32,
        default="base",
        db_index=True,
    )
    features = models.JSONField("Features (dict)", default=dict)
    computed_at = models.DateTimeField("Fecha de cómputo", auto_now=True)
    season = models.CharField("SEASON", max_length=10, blank=True, db_index=True)
    season_type = models.CharField("SEASON_TYPE", max_length=20, blank=True, db_index=True)

    class Meta:
        verbose_name = "Game feature set"
        verbose_name_plural = "Game feature sets"
        ordering = ["-computed_at", "game_id"]
        unique_together = [["game_id", "market"]]
        indexes = [
            models.Index(fields=["game_id", "market"]),
            models.Index(fields=["season", "season_type"]),
        ]

    def __str__(self):
        return f"{self.game_id} ({self.market})"


class PlayerFeatureSet(models.Model):
    """
    Features agregadas por jugador (rolling, matchup) hasta una fecha.
    """

    player_id = models.CharField("PLAYER_ID", max_length=40, db_index=True)
    as_of_date = models.DateField("Fecha de referencia", null=True, blank=True, db_index=True)
    context = models.CharField(
        "Contexto (scoring/rebounding/playmaking/defense)",
        max_length=32,
        default="all",
    )
    features = models.JSONField("Features (dict)", default=dict)
    computed_at = models.DateTimeField("Fecha de cómputo", auto_now=True)
    season = models.CharField("SEASON", max_length=10, blank=True, db_index=True)

    class Meta:
        verbose_name = "Player feature set"
        verbose_name_plural = "Player feature sets"
        ordering = ["-as_of_date", "player_id"]
        indexes = [
            models.Index(fields=["player_id", "as_of_date"]),
            models.Index(fields=["season", "context"]),
        ]

    def __str__(self):
        return f"{self.player_id} @ {self.as_of_date} ({self.context})"
