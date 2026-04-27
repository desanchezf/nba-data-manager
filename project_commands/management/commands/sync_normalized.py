"""
Sincroniza los modelos crudos NBA (game, game_boxscore, teams, players, roster)
hacia los modelos normalizados de core (Game, Team, Player, GamePlayerLine, GameTeamLine).
"""

from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    help = "Sincroniza datos crudos → modelos normalizados core"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Vaciar modelos core antes")
        parser.add_argument("--season", type=str, default="", help="Filtrar por temporada (ej. 2025)")
        parser.add_argument("--season-type", type=str, default="", help="Tipo temporada (Regular Season, Playoffs)")
        parser.add_argument("--batch", type=int, default=1000, help="Tamaño de lote")

    def handle(self, *args, **options):
        clear = options["clear"]
        season = options["season"]
        season_type = options["season_type"]
        batch_size = options["batch"]

        if clear:
            self.stdout.write("Vaciando modelos core...")
            from core.models import (
                Game, Player, Team,
                GamePlayerLine, GameTeamLine, WinProbabilitySnapshot,
            )
            WinProbabilitySnapshot.objects.all().delete()
            GameTeamLine.objects.all().delete()
            GamePlayerLine.objects.all().delete()
            Game.objects.all().delete()
            Player.objects.all().delete()
            Team.objects.all().delete()
            self.stdout.write(self.style.WARNING("Modelos core vaciados."))

        self._sync_teams()
        self._sync_players()
        self._sync_games(season, season_type, batch_size)
        self._sync_player_lines(season, season_type, batch_size)
        self._sync_team_lines(season, season_type, batch_size)

        self.stdout.write(self.style.SUCCESS("✅ Sincronización core completada."))

    def _sync_teams(self):
        self.stdout.write("Sincronizando equipos...")
        try:
            from roster.models import Teams as RosterTeam
            from core.models import Team

            qs = list(RosterTeam.objects.all())
            count = 0
            for rt in tqdm(qs, desc="  Equipos", unit=" eq", ncols=80, file=self.stdout):
                team_id = str(rt.team_id) if hasattr(rt, "team_id") else str(rt.pk)
                Team.objects.update_or_create(
                    team_id=team_id,
                    defaults={
                        "name": getattr(rt, "name", "") or "",
                        "abbreviation": getattr(rt, "abb", "") or "",
                        "conference": getattr(rt, "conference", "") or "",
                        "division": getattr(rt, "division", "") or "",
                    },
                )
                count += 1
            self.stdout.write(f"  Equipos sincronizados: {count}")
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"  Equipos: {exc}"))

    def _sync_players(self):
        self.stdout.write("Sincronizando jugadores...")
        try:
            from roster.models import Players as RosterPlayer
            from core.models import Player, Team

            qs = list(RosterPlayer.objects.select_related().all())
            count = 0
            for rp in tqdm(qs, desc="  Jugadores", unit=" jug", ncols=80, file=self.stdout):
                player_id = str(rp.player_id) if hasattr(rp, "player_id") else str(rp.pk)
                team_obj = None
                if hasattr(rp, "team_id") and rp.team_id:
                    team_obj = Team.objects.filter(team_id=str(rp.team_id)).first()
                Player.objects.update_or_create(
                    player_id=player_id,
                    defaults={
                        "name": getattr(rp, "full_name", getattr(rp, "name", "")) or "",
                        "team": team_obj,
                    },
                )
                count += 1
            self.stdout.write(f"  Jugadores sincronizados: {count}")
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"  Jugadores: {exc}"))

    def _sync_games(self, season, season_type, batch_size):
        self.stdout.write("Sincronizando partidos...")
        try:
            from game.models import GameBoxscoreTraditional, GameSummary
            from core.models import Game, Team

            qs = GameBoxscoreTraditional.objects.all()
            if season:
                qs = qs.filter(season=season)
            if season_type:
                qs = qs.filter(season_type__icontains=season_type)

            total = qs.values("game_id").distinct().count()
            game_ids_seen = set()
            count = 0

            bar = tqdm(
                total=total, desc="  Partidos", unit=" part",
                ncols=80, file=self.stdout,
            )
            for row in qs.iterator(chunk_size=batch_size):
                gid = str(getattr(row, "game_id", ""))
                if not gid or gid in game_ids_seen:
                    continue
                game_ids_seen.add(gid)
                bar.update(1)

                home_abb = str(getattr(row, "home_team_abb", "") or "")
                away_abb = str(getattr(row, "away_team_abb", "") or "")
                home_team = Team.objects.filter(abbreviation=home_abb).first() if home_abb else None
                away_team = Team.objects.filter(abbreviation=away_abb).first() if away_abb else None

                home_score = None
                away_score = None
                if home_abb and away_abb:
                    hs = GameSummary.objects.filter(game_id=gid, team_abb=home_abb).first()
                    as_ = GameSummary.objects.filter(game_id=gid, team_abb=away_abb).first()
                    if hs:
                        home_score = hs.final or None
                    if as_:
                        away_score = as_.final or None

                Game.objects.update_or_create(
                    game_id=gid,
                    defaults={
                        "league": "NBA",
                        "season": str(getattr(row, "season", "") or ""),
                        "season_type": str(getattr(row, "season_type", "") or ""),
                        "date": getattr(row, "game_date", None),
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_score": home_score,
                        "away_score": away_score,
                        "n_result": (
                            f"{home_score}-{away_score}"
                            if home_score is not None and away_score is not None
                            else ""
                        ),
                    },
                )
                count += 1
            bar.close()
            self.stdout.write(f"  Partidos sincronizados: {count}")
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"  Partidos: {exc}"))

    def _sync_team_lines(self, season, season_type, batch_size):
        self.stdout.write("Sincronizando estadísticas de equipo...")
        try:
            from game.models import TeamBoxscoreTraditional, GameSummary
            from core.models import Game, Team, GameTeamLine

            qs = TeamBoxscoreTraditional.objects.all()
            if season:
                qs = qs.filter(season=season)
            if season_type:
                qs = qs.filter(season_type__icontains=season_type)

            total = qs.count()
            count_all = 0
            count_q = 0

            bar = tqdm(
                total=total, desc="  Team lines", unit=" filas",
                ncols=80, file=self.stdout,
            )
            for row in qs.iterator(chunk_size=batch_size):
                bar.update(1)
                gid = str(getattr(row, "game_id", "") or "")
                if not gid:
                    continue

                game = Game.objects.filter(game_id=gid).first()
                if not game:
                    continue

                team_abb = str(getattr(row, "team_abb", "") or "")
                team = Team.objects.filter(abbreviation=team_abb).first() if team_abb else None
                home_away = str(getattr(row, "home_away", "") or "")

                GameTeamLine.objects.update_or_create(
                    game=game,
                    team=team,
                    period="ALL",
                    defaults={
                        "home_away": home_away,
                        "fgm": _safe_int(getattr(row, "fgm", 0)),
                        "fga": _safe_int(getattr(row, "fga", 0)),
                        "fg_pct": _safe_float(getattr(row, "fg_pct", None)),
                        "fg3m": _safe_int(getattr(row, "fg3m", 0)),
                        "fg3a": _safe_int(getattr(row, "fg3a", 0)),
                        "fg3_pct": _safe_float(getattr(row, "fg3_pct", None)),
                        "ftm": _safe_int(getattr(row, "ftm", 0)),
                        "fta": _safe_int(getattr(row, "fta", 0)),
                        "ft_pct": _safe_float(getattr(row, "ft_pct", None)),
                        "oreb": _safe_int(getattr(row, "oreb", 0)),
                        "dreb": _safe_int(getattr(row, "dreb", 0)),
                        "reb": _safe_int(getattr(row, "reb", 0)),
                        "ast": _safe_int(getattr(row, "ast", 0)),
                        "stl": _safe_int(getattr(row, "stl", 0)),
                        "blk": _safe_int(getattr(row, "blk", 0)),
                        "tov": _safe_int(getattr(row, "tov", 0)),
                        "pf": _safe_int(getattr(row, "pf", 0)),
                        "pts": _safe_int(getattr(row, "pts", 0)),
                    },
                )
                count_all += 1

                summary = GameSummary.objects.filter(
                    game_id=gid, team_abb=team_abb
                ).first()
                if summary and team:
                    for qtr, field in (
                        ("Q1", "q1"), ("Q2", "q2"), ("Q3", "q3"), ("Q4", "q4"),
                    ):
                        pts_q = getattr(summary, field, 0) or 0
                        GameTeamLine.objects.update_or_create(
                            game=game,
                            team=team,
                            period=qtr,
                            defaults={"home_away": home_away, "pts": pts_q},
                        )
                        count_q += 1
            bar.close()
            self.stdout.write(
                f"  Team lines ALL: {count_all} | Cuartos: {count_q}"
            )
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"  Team lines: {exc}"))

    def _sync_player_lines(self, season, season_type, batch_size):
        self.stdout.write("Sincronizando estadísticas de jugadores...")
        try:
            from game_boxscore.models import GameBoxscoreTraditional
            from core.models import Game, Player, Team, GamePlayerLine

            qs = GameBoxscoreTraditional.objects.all()
            if season:
                qs = qs.filter(season=season)
            if season_type:
                qs = qs.filter(season_type__icontains=season_type)

            total = qs.count()
            count = 0

            bar = tqdm(
                total=total, desc="  Player lines", unit=" filas",
                ncols=80, file=self.stdout,
            )
            for row in qs.iterator(chunk_size=batch_size):
                bar.update(1)
                gid = str(getattr(row, "game_id", ""))
                pid = str(getattr(row, "player_id", "") or "")
                if not gid or not pid:
                    continue

                game = Game.objects.filter(game_id=gid).first()
                if not game:
                    continue

                player = Player.objects.filter(player_id=pid).first()
                team_id = str(getattr(row, "team_id", "") or "")
                team = Team.objects.filter(team_id=team_id).first() if team_id else None

                GamePlayerLine.objects.update_or_create(
                    game=game,
                    player=player,
                    team=team,
                    period=str(getattr(row, "period", "ALL") or "ALL"),
                    defaults={
                        "home_away": str(getattr(row, "home_away", "") or ""),
                        "position": str(getattr(row, "position", "") or ""),
                        "min_played": _safe_float(getattr(row, "min", None)),
                        "fgm": _safe_int(getattr(row, "fgm", 0)),
                        "fga": _safe_int(getattr(row, "fga", 0)),
                        "fg_pct": _safe_float(getattr(row, "fg_pct", None)),
                        "fg3m": _safe_int(getattr(row, "fg3m", 0)),
                        "fg3a": _safe_int(getattr(row, "fg3a", 0)),
                        "fg3_pct": _safe_float(getattr(row, "fg3_pct", None)),
                        "ftm": _safe_int(getattr(row, "ftm", 0)),
                        "fta": _safe_int(getattr(row, "fta", 0)),
                        "ft_pct": _safe_float(getattr(row, "ft_pct", None)),
                        "oreb": _safe_int(getattr(row, "oreb", 0)),
                        "dreb": _safe_int(getattr(row, "dreb", 0)),
                        "reb": _safe_int(getattr(row, "reb", 0)),
                        "ast": _safe_int(getattr(row, "ast", 0)),
                        "stl": _safe_int(getattr(row, "stl", 0)),
                        "blk": _safe_int(getattr(row, "blk", 0)),
                        "tov": _safe_int(getattr(row, "tov", 0)),
                        "pf": _safe_int(getattr(row, "pf", 0)),
                        "pts": _safe_int(getattr(row, "pts", 0)),
                        "plus_minus": _safe_int(getattr(row, "plus_minus", None)),
                    },
                )
                count += 1
            bar.close()
            self.stdout.write(f"  Estadísticas jugadores: {count}")
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"  Estadísticas jugadores: {exc}"))


def _safe_int(v, default=0):
    try:
        return int(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _safe_float(v, default=None):
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default
