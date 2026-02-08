import logging
import os

from django.core.management.base import BaseCommand
from django.conf import settings

import csv
from tqdm import tqdm
from game.models import (
    GameBoxscoreTraditional,
    GamePlayByPlay,
    TeamBoxscoreTraditional,
    GameSummary,
)
from roster.models import Teams, Players
from django.utils.dateparse import parse_datetime, parse_date
from django.db import models as django_models

# Importar modelos de teams, lineups y players
from teams.models import (
    TeamsGeneralTraditional,
    TeamsGeneralAdvanced,
    TeamsGeneralFourFactors,
    TeamsGeneralMisc,
    TeamsGeneralScoring,
    TeamsGeneralOpponent,
    TeamsGeneralDefense,
    TeamsGeneralViolations,
    TeamsGeneralEstimatedAdvanced,
    TeamsClutchTraditional,
    TeamsClutchAdvanced,
    TeamsClutchFourFactors,
    TeamsClutchMisc,
    TeamsClutchScoring,
    TeamsClutchOpponent,
    TeamsBoxOuts,
    TeamsHustle,
    TeamsPlaytypeBallHandler,
    TeamsPlaytypeCut,
    TeamsPlaytypeHandOff,
    TeamsPlaytypeIsolation,
    TeamsPlaytypeMisc,
    TeamsPlaytypeOffScreen,
    TeamsPlaytypePostUp,
    TeamsPlaytypePutbacks,
    TeamsPlaytypeRollMan,
    TeamsPlaytypeSpotUp,
    TeamsPlaytypeTransition,
    TeamsTrackingCatchShoot,
    TeamsTrackingDefensiveImpact,
    TeamsTrackingDefensiveRebounding,
    TeamsTrackingDrives,
    TeamsTrackingElbowTouch,
    TeamsTrackingOffensiveRebounding,
    TeamsTrackingPaintTouch,
    TeamsTrackingPassing,
    TeamsTrackingPostUps,
    TeamsTrackingPullup,
    TeamsTrackingRebounding,
    TeamsTrackingShootingEfficiency,
    TeamsTrackingSpeedDistance,
    TeamsTrackingTouches,
    TeamsDefenseDashboardOverall,
    TeamsDefenseDashboard2pt,
    TeamsDefenseDashboard3pt,
    TeamsDefenseDashboardLt6,
    TeamsDefenseDashboardLt10,
    TeamsDefenseDashboardGt15,
    TeamsShotDashboardGeneral,
    TeamsShotDashboardShotClock,
    TeamsShotDashboardDribbles,
    TeamsShotDashboardTouchTime,
    TeamsShotDashboardClosestDefender,
    TeamsShotDashboardClosestDefender10,
    TeamsShooting,
    TeamsOpponentShootingOverall,
    TeamsOpponentShotsGeneral,
    TeamsOpponentShotsShotclock,
    TeamsOpponentShotsDribbles,
    TeamsOpponentShotsTouchTime,
    TeamsOpponentShotsClosestDefender,
    TeamsOpponentShotsClosestDefender10,
)

from lineups.models import (
    LineupsTraditional,
    LineupsAdvanced,
    LineupsMisc,
    LineupsFourFactors,
    LineupsScoring,
    LineupsOpponent,
)

from players.models import (
    PlayersGeneralTraditional,
    PlayersGeneralAdvanced,
    PlayersGeneralMisc,
    PlayersGeneralScoring,
    PlayersGeneralUsage,
    PlayersGeneralOpponent,
    PlayersGeneralDefense,
    PlayersGeneralViolations,
    PlayersGeneralEstimatedAdvanced,
    PlayersClutchTraditional,
    PlayersClutchAdvanced,
    PlayersClutchMisc,
    PlayersClutchScoring,
    PlayersClutchUsage,
    PlayersBios,
    PlayersBoxOuts,
    PlayersHustle,
    PlayersPlaytypeBallHandler,
    PlayersPlaytypeCut,
    PlayersPlaytypeHandOff,
    PlayersPlaytypeIsolation,
    PlayersPlaytypeMisc,
    PlayersPlaytypeOffScreen,
    PlayersPlaytypePostUp,
    PlayersPlaytypePutbacks,
    PlayersPlaytypeRollMan,
    PlayersPlaytypeSpotUp,
    PlayersPlaytypeTransition,
    PlayersTrackingCatchShoot,
    PlayersTrackingDefensiveImpact,
    PlayersTrackingDefensiveRebounding,
    PlayersTrackingDrives,
    PlayersTrackingElbowTouch,
    PlayersTrackingOffensiveRebounding,
    PlayersTrackingPaintTouch,
    PlayersTrackingPassing,
    PlayersTrackingPostUps,
    PlayersTrackingPullup,
    PlayersTrackingRebounding,
    PlayersTrackingShootingEfficiency,
    PlayersTrackingSpeedDistance,
    PlayersTrackingTouches,
    PlayersDefenseDashboardOverall,
    PlayersDefenseDashboard2pt,
    PlayersDefenseDashboard3pt,
    PlayersDefenseDashboardLt6,
    PlayersDefenseDashboardLt10,
    PlayersDefenseDashboardGt15,
    PlayersShotDashboardGeneral,
    PlayersShotDashboardShotClock,
    PlayersShotDashboardDribbles,
    PlayersShotDashboardTouchTime,
    PlayersShotDashboardClosestDefender,
    PlayersShotDashboardClosestDefender10,
    PlayersBoxScores,
    PlayersAdvancedBoxScoresTraditional,
    PlayersAdvancedBoxScoresAdvanced,
    PlayersAdvancedBoxScoresMisc,
    PlayersAdvancedBoxScoresScoring,
    PlayersAdvancedBoxScoresUsage,
    PlayersShooting,
    PlayersDunkScores,
    PlayersOpponentShootingOverall,
)

logger = logging.getLogger(__name__)


def safe_int(value, default=0):
    """Convierte un valor a int de forma segura, manejando valores vacíos, '-' y errores."""
    if value is None:
        return default
    value_str = str(value).strip()
    if not value_str or value_str == "-":
        return default
    try:
        return int(value_str)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """Convierte un valor a float de forma segura, manejando valores vacíos, '-' y errores."""
    if value is None:
        return default
    value_str = str(value).strip()
    if not value_str or value_str == "-":
        return default
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return default


def count_csv_lines(filepath):
    """Cuenta el número de líneas en un archivo CSV (sin incluir la cabecera)."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return max(0, sum(1 for _ in f) - 1)  # Restar 1 por la cabecera
    except (FileNotFoundError, IOError):
        return 0


class Command(BaseCommand):
    help = "Import initial data from links directory"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Iniciando importación de datos..."))
        self.stdout.write("=" * 60)

        self.import_teams()
        self.import_players()
        self.import_game_boxscore_traditional()
        self.import_game_play_by_play()
        self.import_game_summary()
        self.import_team_boxscore_traditional()

        self.stdout.write("=" * 60)

        # Importar datos de CSVs por app
        self.import_teams_csvs()
        self.import_lineups_csvs()
        self.import_players_csvs()

        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("Importación completada exitosamente"))

    def import_teams(self):
        # Importa equipos desde NBA_TEAMS_INFO definido en settings.py
        # Estructura: {"Nombre Equipo": [abreviatura, team_id, conferencia, división]}
        self.stdout.write(self.style.WARNING("\n[1/6] Importando equipos..."))
        teams_created = 0
        teams_updated = 0

        for team_name, team_info in settings.NBA_TEAMS_INFO.items():
            # Estructura: ["ATL", 1610612737, "East", "Southeast"]
            team_abb = team_info[0]  # Abreviación (ej: "ATL")
            team_id = team_info[1]  # ID del equipo
            team_conference = team_info[2]  # Conferencia (ej: "East")
            team_division = team_info[3]  # División (ej: "Southeast")

            team, created = Teams.objects.update_or_create(
                team_id=team_id,
                defaults={
                    "team_name": team_name,  # Nombre completo (ej: "Atlanta Hawks")
                    "team_abb": team_abb,  # Abreviación (ej: "ATL")
                    "team_conference": team_conference,
                    "team_division": team_division,
                },
            )

            if created:
                teams_created += 1
                self.stdout.write(f"  ✓ Creado: {team_name} ({team_abb})")
            else:
                teams_updated += 1
                self.stdout.write(f"  ↻ Actualizado: {team_name} ({team_abb})")

        self.stdout.write(
            self.style.SUCCESS(
                f"  Equipos: {teams_created} creados, {teams_updated} actualizados"
            )
        )
        logger.info(
            "Importados %d equipos nuevos y %d actualizados",
            teams_created,
            teams_updated,
        )

    def import_players(self):
        # Extrae jugadores únicos del archivo game_boxscore_traditional.csv
        # Columnas: GAME_ID,SEASON,SEASON_TYPE,HOME_TEAM_ABB,AWAY_TEAM_ABB,
        # PLAYER_ID,PLAYER_NAME,PLAYER_NAME_ABB,PLAYER_TEAM_ABB,...
        self.stdout.write(self.style.WARNING("\n[2/6] Importando jugadores..."))

        csv_path = "./csv/game_boxscore_traditional.csv"
        total_lines = count_csv_lines(csv_path)

        # Cargar todos los equipos en memoria una vez (optimización)
        teams_dict = {team.team_abb: team for team in Teams.objects.all()}
        self.stdout.write(f"  Cargados {len(teams_dict)} equipos en memoria")
        logger.info(f"Cargados {len(teams_dict)} equipos en memoria")

        # Cargar todos los jugadores existentes en memoria (optimización)
        existing_players = {
            (p.player_id, p.season, p.team_id)
            for p in Players.objects.select_related("team").all()
        }
        self.stdout.write(
            f"  Cargados {len(existing_players)} jugadores existentes en memoria"
        )
        logger.info(f"Cargados {len(existing_players)} jugadores existentes en memoria")

        players_seen = set()  # Evita duplicados: (player_id, season, team_abb)
        players_to_create = []  # Lista para bulk_create
        skipped_count = 0

        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(
                total=total_lines,
                desc="  Procesando jugadores",
                unit=" filas",
                ncols=100,
            )
            try:
                for row in reader:
                    progress_bar.update(1)
                    if len(row) < 9:
                        continue

                    player_id = row[5]  # PLAYER_ID
                    player_name = row[6]  # PLAYER_NAME
                    player_name_abb = row[7]  # PLAYER_NAME_ABB
                    player_team_abb = (
                        row[8].strip() if row[8] else ""
                    )  # PLAYER_TEAM_ABB
                    season = row[1]  # SEASON

                    # Saltar si el equipo está vacío o no existe
                    if not player_team_abb or player_team_abb not in teams_dict:
                        skipped_count += 1
                        continue

                    team = teams_dict[player_team_abb]
                    player_key = (player_id, season, team.id)

                    # Saltar si ya existe
                    if player_key in existing_players:
                        continue

                    # Crear clave única para evitar duplicados en el CSV
                    csv_key = (player_id, season, player_team_abb)
                    if csv_key not in players_seen:
                        players_seen.add(csv_key)
                        players_to_create.append(
                            Players(
                                player_id=player_id,
                                player_name=player_name,
                                player_abb=player_name_abb,
                                team=team,
                                season=season,
                            )
                        )

                    # Actualizar descripción de la barra
                    progress_bar.set_postfix(
                        {"únicos": len(players_seen), "omitidos": skipped_count}
                    )
            finally:
                progress_bar.close()

        # Insertar todos los jugadores de una vez (más eficiente)
        if players_to_create:
            self.stdout.write(
                f"  Insertando {len(players_to_create)} jugadores nuevos en la base de datos..."
            )
            Players.objects.bulk_create(players_to_create, ignore_conflicts=True)
            logger.info(f"Creados {len(players_to_create)} jugadores nuevos")

        self.stdout.write(
            self.style.SUCCESS(
                f"  Jugadores: {len(players_seen)} únicos importados, {skipped_count} omitidos (equipos no válidos), {total_lines} filas procesadas"
            )
        )
        logger.info(
            "Importados %d jugadores únicos, %d omitidos (equipos no válidos)",
            len(players_seen),
            skipped_count,
        )

    def import_game_boxscore_traditional(self):
        # Lee el archivo CSV y crea registros para cada fila (optimizado para CSVs grandes)
        self.stdout.write(
            self.style.WARNING("\n[3/6] Importando Game Boxscore Traditional...")
        )

        csv_path = "./csv/game_boxscore_traditional.csv"
        total_lines = count_csv_lines(csv_path)

        # Cargar registros existentes en memoria (clave única: game_id, season, season_type, home_team_abb, away_team_abb, player_id)
        existing_records = {
            tuple(r)
            for r in GameBoxscoreTraditional.objects.values_list(
                "game_id",
                "season",
                "season_type",
                "home_team_abb",
                "away_team_abb",
                "player_id",
            )
        }
        self.stdout.write(
            f"  Cargados {len(existing_records)} registros existentes en memoria"
        )

        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0

        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(
                total=total_lines,
                desc="  Procesando boxscores",
                unit=" filas",
                ncols=100,
            )
            try:
                for row in reader:
                    progress_bar.update(1)
                    if len(row) < 31:
                        continue

                    # Clave única para verificar si ya existe
                    record_key = (row[0], row[1], row[2], row[3], row[4], row[5])

                    if record_key in existing_records:
                        skipped_count += 1
                        continue

                    # Crear objeto para bulk_create
                    batch.append(
                        GameBoxscoreTraditional(
                            game_id=row[0],
                            season=row[1],
                            season_type=row[2],
                            home_team_abb=row[3],
                            away_team_abb=row[4],
                            player_id=row[5],
                            player_name=row[6],
                            player_name_abb=row[7],
                            player_team_abb=row[8],
                            player_pos=row[9],
                            player_dnp=row[10].lower() == "true",
                            period=row[11],
                            min=row[12],
                            fgm=safe_int(row[13]),
                            fga=safe_int(row[14]),
                            fg_perc=safe_float(row[15]),
                            threepm=safe_int(row[16]),
                            threepa=safe_int(row[17]),
                            threep_perc=safe_float(row[18]),
                            ftm=safe_int(row[19]),
                            fta=safe_int(row[20]),
                            ft_perc=safe_float(row[21]),
                            oreb=safe_int(row[22]),
                            dreb=safe_int(row[23]),
                            reb=safe_int(row[24]),
                            ast=safe_int(row[25]),
                            stl=safe_int(row[26]),
                            blk=safe_int(row[27]),
                            to=safe_int(row[28]),
                            pf=safe_int(row[29]),
                            pts=safe_int(row[30]),
                            plus_minus=safe_int(row[31]) if len(row) > 31 else 0,
                        )
                    )

                    # Insertar por lotes
                    if len(batch) >= batch_size:
                        GameBoxscoreTraditional.objects.bulk_create(
                            batch, ignore_conflicts=True
                        )
                        created_count += len(batch)
                        batch = []

                    # Actualizar descripción de la barra
                    progress_bar.set_postfix(
                        {
                            "nuevos": created_count + len(batch),
                            "existentes": skipped_count,
                        }
                    )
            finally:
                progress_bar.close()

            # Insertar el lote final
            if batch:
                GameBoxscoreTraditional.objects.bulk_create(
                    batch, ignore_conflicts=True
                )
                created_count += len(batch)

        self.stdout.write(
            self.style.SUCCESS(
                f"  Game Boxscore Traditional: {created_count} nuevos, {skipped_count} existentes, {total_lines} filas procesadas"
            )
        )

    def import_game_play_by_play(self):
        self.stdout.write(self.style.WARNING("\n[4/6] Importando Game Play By Play..."))

        csv_path = "./csv/game_play_by_play.csv"
        total_lines = count_csv_lines(csv_path)

        # Cargar registros existentes en memoria (clave única basada en los campos únicos)
        existing_records = {
            tuple(r)
            for r in GamePlayByPlay.objects.values_list(
                "season",
                "season_type",
                "game_id",
                "team_abb",
                "period",
                "min",
                "score",
                "player",
                "action",
            )
        }
        self.stdout.write(
            f"  Cargados {len(existing_records)} registros existentes en memoria"
        )

        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0

        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(
                total=total_lines,
                desc="  Procesando play-by-play",
                unit=" filas",
                ncols=100,
            )
            try:
                for row in reader:
                    progress_bar.update(1)
                    if len(row) < 9:
                        continue

                    # Clave única para verificar si ya existe
                    record_key = (
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                    )

                    if record_key in existing_records:
                        skipped_count += 1
                        continue

                    # Crear objeto para bulk_create
                    batch.append(
                        GamePlayByPlay(
                            season=row[0],
                            season_type=row[1],
                            game_id=row[2],
                            team_abb=row[3],
                            period=row[4],
                            min=row[5],
                            score=row[6],
                            player=row[7],
                            action=row[8],
                        )
                    )

                    # Insertar por lotes
                    if len(batch) >= batch_size:
                        GamePlayByPlay.objects.bulk_create(batch, ignore_conflicts=True)
                        created_count += len(batch)
                        batch = []

                    # Actualizar descripción de la barra
                    progress_bar.set_postfix(
                        {
                            "nuevos": created_count + len(batch),
                            "existentes": skipped_count,
                        }
                    )
            finally:
                progress_bar.close()

            # Insertar el lote final
            if batch:
                GamePlayByPlay.objects.bulk_create(batch, ignore_conflicts=True)
                created_count += len(batch)

        self.stdout.write(
            self.style.SUCCESS(
                f"  Game Play By Play: {created_count} nuevos, {skipped_count} existentes, {total_lines} filas procesadas"
            )
        )

    def import_game_summary(self):
        self.stdout.write(self.style.WARNING("\n[5/6] Importando Game Summary..."))

        csv_path = "./csv/game_summary.csv"
        total_lines = count_csv_lines(csv_path)

        # Cargar registros existentes en memoria (clave única: season, season_type, game_id, team_abb)
        existing_records = {
            tuple(r)
            for r in GameSummary.objects.values_list(
                "season", "season_type", "game_id", "team_abb"
            )
        }
        self.stdout.write(
            f"  Cargados {len(existing_records)} registros existentes en memoria"
        )

        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0

        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(
                total=total_lines,
                desc="  Procesando summaries",
                unit=" filas",
                ncols=100,
            )
            try:
                for row in reader:
                    progress_bar.update(1)
                    if len(row) < 23:
                        continue

                    # Clave única para verificar si ya existe
                    record_key = (row[0], row[1], row[2], row[3])

                    if record_key in existing_records:
                        skipped_count += 1
                        continue

                    # Crear objeto para bulk_create
                    batch.append(
                        GameSummary(
                            season=row[0],
                            season_type=row[1],
                            game_id=row[2],
                            team_abb=row[3],
                            q1=safe_int(row[4]),
                            q2=safe_int(row[5]),
                            q3=safe_int(row[6]),
                            q4=safe_int(row[7]),
                            ot1=safe_int(row[8]),
                            ot2=safe_int(row[9]),
                            ot3=safe_int(row[10]),
                            ot4=safe_int(row[11]),
                            final=safe_int(row[12]),
                            pitp=safe_int(row[13]),
                            fb_pts=safe_int(row[14]),
                            big_ld=safe_int(row[15]),
                            bpts=safe_int(row[16]),
                            treb=safe_int(row[17]),
                            tov=safe_int(row[18]),
                            ttov=safe_int(row[19]),
                            pot=safe_int(row[20]),
                            lead_changes=safe_int(row[21]),
                            times_tied=safe_int(row[22]),
                        )
                    )

                    # Insertar por lotes
                    if len(batch) >= batch_size:
                        GameSummary.objects.bulk_create(batch, ignore_conflicts=True)
                        created_count += len(batch)
                        batch = []

                    # Actualizar descripción de la barra
                    progress_bar.set_postfix(
                        {
                            "nuevos": created_count + len(batch),
                            "existentes": skipped_count,
                        }
                    )
            finally:
                progress_bar.close()

            # Insertar el lote final
            if batch:
                GameSummary.objects.bulk_create(batch, ignore_conflicts=True)
                created_count += len(batch)

        self.stdout.write(
            self.style.SUCCESS(
                f"  Game Summary: {created_count} nuevos, {skipped_count} existentes, {total_lines} filas procesadas"
            )
        )

    def import_team_boxscore_traditional(self):
        self.stdout.write(
            self.style.WARNING("\n[6/6] Importando Team Boxscore Traditional...")
        )

        csv_path = "./csv/teams_box_scores.csv"
        total_lines = count_csv_lines(csv_path)

        # Cargar registros existentes en memoria (clave única: season, season_type, team_id, team_abb, game_id)
        existing_records = {
            tuple(r)
            for r in TeamBoxscoreTraditional.objects.values_list(
                "season", "season_type", "team_id", "team_abb", "game_id"
            )
        }
        self.stdout.write(
            f"  Cargados {len(existing_records)} registros existentes en memoria"
        )

        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0

        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(
                total=total_lines,
                desc="  Procesando team boxscores",
                unit=" filas",
                ncols=100,
            )
            try:
                for row in reader:
                    progress_bar.update(1)
                    if len(row) < 28:
                        continue

                    team_id = safe_int(row[2])
                    # Clave única para verificar si ya existe
                    record_key = (row[0], row[1], team_id, row[3], row[4])

                    if record_key in existing_records:
                        skipped_count += 1
                        continue

                    # Crear objeto para bulk_create
                    batch.append(
                        TeamBoxscoreTraditional(
                            season=row[0],
                            season_type=row[1],
                            team_id=team_id,
                            team_abb=row[3],
                            game_id=row[4],
                            matchup=row[5],
                            home_away=row[6],
                            gdate=row[7],
                            wl=row[8],
                            min=safe_int(row[9]),
                            pts=safe_int(row[10]),
                            fgm=safe_int(row[11]),
                            fga=safe_int(row[12]),
                            fg_pct=safe_float(row[13]),
                            fg3m=safe_int(row[14]),
                            fg3a=safe_int(row[15]),
                            fg3_pct=safe_float(row[16]),
                            ftm=safe_int(row[17]),
                            fta=safe_int(row[18]),
                            ft_pct=safe_float(row[19]),
                            oreb=safe_int(row[20]),
                            dreb=safe_int(row[21]),
                            reb=safe_int(row[22]),
                            ast=safe_int(row[23]),
                            stl=safe_int(row[24]),
                            blk=safe_int(row[25]),
                            tov=safe_int(row[26]),
                            pf=safe_int(row[27]),
                            plus_minus=safe_int(row[28]) if len(row) > 28 else 0,
                        )
                    )

                    # Insertar por lotes
                    if len(batch) >= batch_size:
                        TeamBoxscoreTraditional.objects.bulk_create(
                            batch, ignore_conflicts=True
                        )
                        created_count += len(batch)
                        batch = []

                    # Actualizar descripción de la barra
                    progress_bar.set_postfix(
                        {
                            "nuevos": created_count + len(batch),
                            "existentes": skipped_count,
                        }
                    )
            finally:
                progress_bar.close()

            # Insertar el lote final
            if batch:
                TeamBoxscoreTraditional.objects.bulk_create(
                    batch, ignore_conflicts=True
                )
                created_count += len(batch)

        self.stdout.write(
            self.style.SUCCESS(
                f"  Team Boxscore Traditional: {created_count} nuevos, {skipped_count} existentes, {total_lines} filas procesadas"
            )
        )

    def import_csv_to_model(self, csv_path, model_class, csv_field_map=None):
        """
        Función genérica para importar un CSV a un modelo Django.
        Usa la misma lógica que el código de importación en admin.py
        """
        if not os.path.exists(csv_path):
            self.stdout.write(
                self.style.WARNING(f"  ⚠ Archivo no encontrado: {csv_path}")
            )
            return 0, 0, []

        total_lines = count_csv_lines(csv_path)
        if total_lines == 0:
            return 0, 0, []

        meta = model_class._meta
        field_names = [field.name for field in meta.fields]

        # Campos ignorados (no se importan)
        ignore_fields = {"GROUP_NAME", "TEAM_ABBREVIATION"}

        created_count = 0
        updated_count = 0
        errors = []
        batch_size = 5000
        batch = []

        # Obtener campos únicos del modelo
        unique_fields = [
            f for f in meta.fields if hasattr(f, "unique") and f.unique
        ] or [f for f in meta.fields if f.primary_key]

        # Si el modelo tiene unique_together, usar esos campos
        unique_together = getattr(meta, "unique_together", [])
        unique_field_names = []
        if unique_together:
            unique_field_names = (
                unique_together[0]
                if isinstance(unique_together[0], list)
                else list(unique_together[0])
            )
        elif unique_fields:
            unique_field_names = [unique_fields[0].name]

        self.stdout.write(f"  Importando {os.path.basename(csv_path)}...")

        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            progress_bar = tqdm(
                total=total_lines,
                desc=f"    Procesando {model_class.__name__}",
                unit=" filas",
                ncols=100,
            )
            try:
                for row_num, row in enumerate(reader, start=2):
                    progress_bar.update(1)

                    try:
                        # Normalizar columnas del CSV (aplicar mismo mapeo que en admin)
                        if "teams" in csv_path.lower():
                            # Mapeo para teams
                            row_normalized = {
                                k.lower(): v
                                for k, v in row.items()
                                if not k.upper().endswith("_RANK")
                                and k.upper() not in ignore_fields
                            }
                            csv_field_map_teams = {"w": "win", "l": "lose"}
                            for csv_key, model_key in csv_field_map_teams.items():
                                if (
                                    csv_key in row_normalized
                                    and model_key in field_names
                                ):
                                    row_normalized[model_key] = row_normalized.pop(
                                        csv_key
                                    )
                        elif "players" in csv_path.lower():
                            # Mapeo para players
                            row_normalized = {
                                k.lower(): v
                                for k, v in row.items()
                                if not k.upper().endswith("_RANK")
                                and k.upper() not in ignore_fields
                            }
                            csv_field_map_players = {"l": "lose"}
                            for csv_key, model_key in csv_field_map_players.items():
                                if (
                                    csv_key in row_normalized
                                    and model_key in field_names
                                ):
                                    row_normalized[model_key] = row_normalized.pop(
                                        csv_key
                                    )
                        else:
                            # Lineups - sin mapeo especial
                            row_normalized = {
                                k.lower(): v
                                for k, v in row.items()
                                if not k.upper().endswith("_RANK")
                                and k.upper() not in ignore_fields
                            }

                        # Aplicar mapeo personalizado si existe
                        if csv_field_map:
                            for csv_key, model_key in csv_field_map.items():
                                if (
                                    csv_key in row_normalized
                                    and model_key in field_names
                                ):
                                    row_normalized[model_key] = row_normalized.pop(
                                        csv_key
                                    )

                        # Preparar datos para crear/actualizar
                        data = {}
                        for field_name in field_names:
                            if field_name in row_normalized:
                                value = (
                                    row_normalized[field_name].strip()
                                    if row_normalized[field_name]
                                    else ""
                                )

                                # Obtener el campo del modelo
                                field = meta.get_field(field_name)

                                # Manejar ForeignKey
                                if field.many_to_one:  # ForeignKey
                                    # Para estos modelos normalmente no hay ForeignKeys
                                    # Si hay algún ForeignKey, intentar buscar el objeto relacionado
                                    related_model = field.related_model
                                    try:
                                        if value.isdigit():
                                            related_obj = related_model.objects.get(
                                                pk=int(value)
                                            )
                                            data[field_name] = related_obj
                                        else:
                                            # Intentar buscar por otros campos
                                            continue  # Saltar si no se puede resolver
                                    except Exception:
                                        continue  # Saltar si no se puede resolver
                                    continue

                                # Manejar tipos de datos
                                if isinstance(field, django_models.BooleanField):
                                    data[field_name] = value.lower() in (
                                        "true",
                                        "1",
                                        "yes",
                                        "sí",
                                        "si",
                                    )
                                elif isinstance(field, django_models.IntegerField):
                                    data[field_name] = safe_int(value)
                                elif isinstance(field, django_models.FloatField):
                                    data[field_name] = safe_float(value)
                                elif isinstance(field, django_models.DateTimeField):
                                    parsed = parse_datetime(value)
                                    if parsed:
                                        data[field_name] = parsed
                                elif isinstance(field, django_models.DateField):
                                    parsed = parse_date(value)
                                    if parsed:
                                        data[field_name] = parsed
                                else:
                                    data[field_name] = value if value else ""

                        # Crear o actualizar el objeto usando unique_together
                        if unique_field_names:
                            # Construir filtro con campos únicos
                            filter_kwargs = {
                                name: data.get(name)
                                for name in unique_field_names
                                if name in data
                            }

                            if all(
                                v for v in filter_kwargs.values()
                            ):  # Si todos los valores están presentes
                                obj, created = model_class.objects.update_or_create(
                                    **filter_kwargs, defaults=data
                                )
                                if created:
                                    created_count += 1
                                else:
                                    updated_count += 1
                            else:
                                # Si faltan campos únicos, crear nuevo
                                model_class.objects.create(**data)
                                created_count += 1
                        else:
                            # Si no hay campos únicos, siempre crear nuevo
                            model_class.objects.create(**data)
                            created_count += 1

                        # Agregar a batch para bulk operations si es necesario (opcional)
                        # Por ahora, usamos update_or_create que es más seguro

                    except Exception as e:
                        errors.append(f"Fila {row_num}: {str(e)}")
                        if len(errors) <= 10:  # Limitar errores mostrados
                            logger.error(f"Error en fila {row_num} de {csv_path}: {e}")

                    # Actualizar descripción de la barra
                    if row_num % 100 == 0:
                        progress_bar.set_postfix(
                            {
                                "creados": created_count,
                                "actualizados": updated_count,
                                "errores": len(errors),
                            }
                        )
            finally:
                progress_bar.close()

        return created_count, updated_count, errors

    def import_teams_csvs(self):
        """Importa todos los CSVs que empiezan por teams_"""
        self.stdout.write(self.style.WARNING("\n[7] Importando CSVs de teams..."))

        csv_dir = "./csv"
        csv_to_model = {
            "teams_general_traditional.csv": TeamsGeneralTraditional,
            "teams_general_advanced.csv": TeamsGeneralAdvanced,
            "teams_general_four_factors.csv": TeamsGeneralFourFactors,
            "teams_general_misc.csv": TeamsGeneralMisc,
            "teams_general_scoring.csv": TeamsGeneralScoring,
            "teams_general_opponent.csv": TeamsGeneralOpponent,
            "teams_general_defense.csv": TeamsGeneralDefense,
            "teams_general_violations.csv": TeamsGeneralViolations,
            "teams_general_estimated_advanced.csv": TeamsGeneralEstimatedAdvanced,
            "teams_clutch_traditional.csv": TeamsClutchTraditional,
            "teams_clutch_advanced.csv": TeamsClutchAdvanced,
            "teams_clutch_four_factors.csv": TeamsClutchFourFactors,
            "teams_clutch_misc.csv": TeamsClutchMisc,
            "teams_clutch_scoring.csv": TeamsClutchScoring,
            "teams_clutch_opponent.csv": TeamsClutchOpponent,
            "teams_box_outs.csv": TeamsBoxOuts,
            "teams_hustle.csv": TeamsHustle,
            "teams_playtype_ball_handler.csv": TeamsPlaytypeBallHandler,
            "teams_playtype_cut.csv": TeamsPlaytypeCut,
            "teams_playtype_hand_off.csv": TeamsPlaytypeHandOff,
            "teams_playtype_isolation.csv": TeamsPlaytypeIsolation,
            "teams_playtype_misc.csv": TeamsPlaytypeMisc,
            "teams_playtype_off_screen.csv": TeamsPlaytypeOffScreen,
            "teams_playtype_post_up.csv": TeamsPlaytypePostUp,
            "teams_playtype_putbacks.csv": TeamsPlaytypePutbacks,
            "teams_playtype_roll_man.csv": TeamsPlaytypeRollMan,
            "teams_playtype_spot_up.csv": TeamsPlaytypeSpotUp,
            "teams_playtype_transition.csv": TeamsPlaytypeTransition,
            "teams_tracking_catch_shoot.csv": TeamsTrackingCatchShoot,
            "teams_tracking_defensive_impact.csv": TeamsTrackingDefensiveImpact,
            "teams_tracking_defensive_rebounding.csv": TeamsTrackingDefensiveRebounding,
            "teams_tracking_drives.csv": TeamsTrackingDrives,
            "teams_tracking_elbow_touch.csv": TeamsTrackingElbowTouch,
            "teams_tracking_offensive_rebounding.csv": TeamsTrackingOffensiveRebounding,
            "teams_tracking_paint_touch.csv": TeamsTrackingPaintTouch,
            "teams_tracking_passing.csv": TeamsTrackingPassing,
            "teams_tracking_post_ups.csv": TeamsTrackingPostUps,
            "teams_tracking_pullup.csv": TeamsTrackingPullup,
            "teams_tracking_rebounding.csv": TeamsTrackingRebounding,
            "teams_tracking_shooting_efficiency.csv": TeamsTrackingShootingEfficiency,
            "teams_tracking_speed_distance.csv": TeamsTrackingSpeedDistance,
            "teams_tracking_touches.csv": TeamsTrackingTouches,
            "teams_defense_dashboard_overall.csv": TeamsDefenseDashboardOverall,
            "teams_defense_dashboard_2pt.csv": TeamsDefenseDashboard2pt,
            "teams_defense_dashboard_3pt.csv": TeamsDefenseDashboard3pt,
            "teams_defense_dashboard_lt6.csv": TeamsDefenseDashboardLt6,
            "teams_defense_dashboard_lt10.csv": TeamsDefenseDashboardLt10,
            "teams_defense_dashboard_gt15.csv": TeamsDefenseDashboardGt15,
            "teams_shot_dashboard_general.csv": TeamsShotDashboardGeneral,
            "teams_shot_dashboard_shot_clock.csv": TeamsShotDashboardShotClock,
            "teams_shot_dashboard_dribbles.csv": TeamsShotDashboardDribbles,
            "teams_shot_dashboard_touch_time.csv": TeamsShotDashboardTouchTime,
            "teams_shot_dashboard_closest_defender.csv": TeamsShotDashboardClosestDefender,
            "teams_shot_dashboard_closest_defender_10.csv": TeamsShotDashboardClosestDefender10,
            "teams_shooting.csv": TeamsShooting,
            "teams_opponent_shooting_overall.csv": TeamsOpponentShootingOverall,
            "teams_opponent_shots_general.csv": TeamsOpponentShotsGeneral,
            "teams_opponent_shots_shotclock.csv": TeamsOpponentShotsShotclock,
            "teams_opponent_shots_dribbles.csv": TeamsOpponentShotsDribbles,
            "teams_opponent_shots_touch_time.csv": TeamsOpponentShotsTouchTime,
            "teams_opponent_shots_closest_defender.csv": TeamsOpponentShotsClosestDefender,
            "teams_opponent_shots_closest_defender_10.csv": TeamsOpponentShotsClosestDefender10,
        }

        total_created = 0
        total_updated = 0

        for csv_file, model_class in sorted(csv_to_model.items()):
            csv_path = os.path.join(csv_dir, csv_file)
            created, updated, errors = self.import_csv_to_model(csv_path, model_class)
            total_created += created
            total_updated += updated

            if errors:
                self.stdout.write(
                    self.style.ERROR(f"    ⚠ {csv_file}: {len(errors)} errores")
                )
                if len(errors) <= 5:
                    for error in errors:
                        self.stdout.write(self.style.ERROR(f"      {error}"))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    ✓ {csv_file}: {created} creados, {updated} actualizados"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n  Teams: {total_created} registros creados, {total_updated} actualizados"
            )
        )

    def import_lineups_csvs(self):
        """Importa todos los CSVs que empiezan por lineups_"""
        self.stdout.write(self.style.WARNING("\n[8] Importando CSVs de lineups..."))

        csv_dir = "./csv"
        csv_to_model = {
            "lineups_traditional.csv": LineupsTraditional,
            "lineups_advanced.csv": LineupsAdvanced,
            "lineups_misc.csv": LineupsMisc,
            "lineups_four_factors.csv": LineupsFourFactors,
            "lineups_scoring.csv": LineupsScoring,
            "lineups_opponent.csv": LineupsOpponent,
        }

        total_created = 0
        total_updated = 0

        for csv_file, model_class in sorted(csv_to_model.items()):
            csv_path = os.path.join(csv_dir, csv_file)
            created, updated, errors = self.import_csv_to_model(csv_path, model_class)
            total_created += created
            total_updated += updated

            if errors:
                self.stdout.write(
                    self.style.ERROR(f"    ⚠ {csv_file}: {len(errors)} errores")
                )
                if len(errors) <= 5:
                    for error in errors:
                        self.stdout.write(self.style.ERROR(f"      {error}"))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    ✓ {csv_file}: {created} creados, {updated} actualizados"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n  Lineups: {total_created} registros creados, {total_updated} actualizados"
            )
        )

    def import_players_csvs(self):
        """Importa todos los CSVs que empiezan por players_"""
        self.stdout.write(self.style.WARNING("\n[9] Importando CSVs de players..."))

        csv_dir = "./csv"
        csv_to_model = {
            "players_general_traditional.csv": PlayersGeneralTraditional,
            "players_general_advanced.csv": PlayersGeneralAdvanced,
            "players_general_misc.csv": PlayersGeneralMisc,
            "players_general_scoring.csv": PlayersGeneralScoring,
            "players_general_usage.csv": PlayersGeneralUsage,
            "players_general_opponent.csv": PlayersGeneralOpponent,
            "players_general_defense.csv": PlayersGeneralDefense,
            "players_general_violations.csv": PlayersGeneralViolations,
            "players_general_estimated_advanced.csv": PlayersGeneralEstimatedAdvanced,
            "players_clutch_traditional.csv": PlayersClutchTraditional,
            "players_clutch_advanced.csv": PlayersClutchAdvanced,
            "players_clutch_misc.csv": PlayersClutchMisc,
            "players_clutch_scoring.csv": PlayersClutchScoring,
            "players_clutch_usage.csv": PlayersClutchUsage,
            "players_bios.csv": PlayersBios,
            "players_box_outs.csv": PlayersBoxOuts,
            "players_hustle.csv": PlayersHustle,
            "players_playtype_ball_handler.csv": PlayersPlaytypeBallHandler,
            "players_playtype_cut.csv": PlayersPlaytypeCut,
            "players_playtype_hand_off.csv": PlayersPlaytypeHandOff,
            "players_playtype_isolation.csv": PlayersPlaytypeIsolation,
            "players_playtype_misc.csv": PlayersPlaytypeMisc,
            "players_playtype_off_screen.csv": PlayersPlaytypeOffScreen,
            "players_playtype_post_up.csv": PlayersPlaytypePostUp,
            "players_playtype_putbacks.csv": PlayersPlaytypePutbacks,
            "players_playtype_roll_man.csv": PlayersPlaytypeRollMan,
            "players_playtype_spot_up.csv": PlayersPlaytypeSpotUp,
            "players_playtype_transition.csv": PlayersPlaytypeTransition,
            "players_tracking_catch_shoot.csv": PlayersTrackingCatchShoot,
            "players_tracking_defensive_impact.csv": PlayersTrackingDefensiveImpact,
            "players_tracking_defensive_rebounding.csv": PlayersTrackingDefensiveRebounding,
            "players_tracking_drives.csv": PlayersTrackingDrives,
            "players_tracking_elbow_touch.csv": PlayersTrackingElbowTouch,
            "players_tracking_offensive_rebounding.csv": PlayersTrackingOffensiveRebounding,
            "players_tracking_paint_touch.csv": PlayersTrackingPaintTouch,
            "players_tracking_passing.csv": PlayersTrackingPassing,
            "players_tracking_post_ups.csv": PlayersTrackingPostUps,
            "players_tracking_pullup.csv": PlayersTrackingPullup,
            "players_tracking_rebounding.csv": PlayersTrackingRebounding,
            "players_tracking_shooting_efficiency.csv": PlayersTrackingShootingEfficiency,
            "players_tracking_speed_distance.csv": PlayersTrackingSpeedDistance,
            "players_tracking_touches.csv": PlayersTrackingTouches,
            "players_defense_dashboard_overall.csv": PlayersDefenseDashboardOverall,
            "players_defense_dashboard_2pt.csv": PlayersDefenseDashboard2pt,
            "players_defense_dashboard_3pt.csv": PlayersDefenseDashboard3pt,
            "players_defense_dashboard_lt6.csv": PlayersDefenseDashboardLt6,
            "players_defense_dashboard_lt10.csv": PlayersDefenseDashboardLt10,
            "players_defense_dashboard_gt15.csv": PlayersDefenseDashboardGt15,
            "players_shot_dashboard_general.csv": PlayersShotDashboardGeneral,
            "players_shot_dashboard_shot_clock.csv": PlayersShotDashboardShotClock,
            "players_shot_dashboard_dribbles.csv": PlayersShotDashboardDribbles,
            "players_shot_dashboard_touch_time.csv": PlayersShotDashboardTouchTime,
            "players_shot_dashboard_closest_defender.csv": PlayersShotDashboardClosestDefender,
            "players_shot_dashboard_closest_defender_10.csv": PlayersShotDashboardClosestDefender10,
            "players_box_scores.csv": PlayersBoxScores,
            "players_advanced_box_scores_traditional.csv": PlayersAdvancedBoxScoresTraditional,
            "players_advanced_box_scores_advanced.csv": PlayersAdvancedBoxScoresAdvanced,
            "players_advanced_box_scores_misc.csv": PlayersAdvancedBoxScoresMisc,
            "players_advanced_box_scores_scoring.csv": PlayersAdvancedBoxScoresScoring,
            "players_advanced_box_scores_usage.csv": PlayersAdvancedBoxScoresUsage,
            "players_shooting.csv": PlayersShooting,
            "players_dunk_scores.csv": PlayersDunkScores,
            "players_opponent_shooting_overall.csv": PlayersOpponentShootingOverall,
        }

        total_created = 0
        total_updated = 0

        for csv_file, model_class in sorted(csv_to_model.items()):
            csv_path = os.path.join(csv_dir, csv_file)
            created, updated, errors = self.import_csv_to_model(csv_path, model_class)
            total_created += created
            total_updated += updated

            if errors:
                self.stdout.write(
                    self.style.ERROR(f"    ⚠ {csv_file}: {len(errors)} errores")
                )
                if len(errors) <= 5:
                    for error in errors:
                        self.stdout.write(self.style.ERROR(f"      {error}"))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    ✓ {csv_file}: {created} creados, {updated} actualizados"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n  Players: {total_created} registros creados, {total_updated} actualizados"
            )
        )
