import logging
import os

from django.core.management.base import BaseCommand
from django.conf import settings

import csv
from tqdm import tqdm
from data.models import (
    GameBoxscoreTraditional,
    GamePlayByPlay,
    TeamBoxscoreTraditional,
    GameSummary,
)
from roster.models import Teams, Players
from data.enums import (
    SeasonChoices,
    SeasonTypeChoices,
    GameBoxscorePeriodChoices,
    GamePlayByPlayPeriodChoices,
)

logger = logging.getLogger(__name__)


def safe_int(value, default=0):
    """Convierte un valor a int de forma segura, manejando valores vacíos, '-' y errores."""
    if value is None:
        return default
    value_str = str(value).strip()
    if not value_str or value_str == '-':
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
    if not value_str or value_str == '-':
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
            for p in Players.objects.select_related('team').all()
        }
        self.stdout.write(f"  Cargados {len(existing_players)} jugadores existentes en memoria")
        logger.info(f"Cargados {len(existing_players)} jugadores existentes en memoria")
        
        players_seen = set()  # Evita duplicados: (player_id, season, team_abb)
        players_to_create = []  # Lista para bulk_create
        skipped_count = 0
        
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(total=total_lines, desc="  Procesando jugadores", unit=" filas", ncols=100)
            try:
                for row in reader:
                    progress_bar.update(1)
                    if len(row) < 9:
                        continue

                    player_id = row[5]  # PLAYER_ID
                    player_name = row[6]  # PLAYER_NAME
                    player_name_abb = row[7]  # PLAYER_NAME_ABB
                    player_team_abb = row[8].strip() if row[8] else ""  # PLAYER_TEAM_ABB
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
                    progress_bar.set_postfix({
                        'únicos': len(players_seen),
                        'omitidos': skipped_count
                    })
            finally:
                progress_bar.close()

        # Insertar todos los jugadores de una vez (más eficiente)
        if players_to_create:
            self.stdout.write(f"  Insertando {len(players_to_create)} jugadores nuevos en la base de datos...")
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
        self.stdout.write(self.style.WARNING("\n[3/6] Importando Game Boxscore Traditional..."))
        
        csv_path = "./csv/game_boxscore_traditional.csv"
        total_lines = count_csv_lines(csv_path)
        
        # Cargar registros existentes en memoria (clave única: game_id, season, season_type, home_team_abb, away_team_abb, player_id)
        existing_records = {
            tuple(r)
            for r in GameBoxscoreTraditional.objects.values_list(
                'game_id', 'season', 'season_type', 'home_team_abb', 'away_team_abb', 'player_id'
            )
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(total=total_lines, desc="  Procesando boxscores", unit=" filas", ncols=100)
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
                        GameBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
                        created_count += len(batch)
                        batch = []
                    
                    # Actualizar descripción de la barra
                    progress_bar.set_postfix({
                        'nuevos': created_count + len(batch),
                        'existentes': skipped_count
                    })
            finally:
                progress_bar.close()
            
            # Insertar el lote final
            if batch:
                GameBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
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
                'season', 'season_type', 'game_id', 'team_abb', 'period', 'min', 'score', 'player', 'action'
            )
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(total=total_lines, desc="  Procesando play-by-play", unit=" filas", ncols=100)
            try:
                for row in reader:
                    progress_bar.update(1)
                    if len(row) < 9:
                        continue

                    # Clave única para verificar si ya existe
                    record_key = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    
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
                    progress_bar.set_postfix({
                        'nuevos': created_count + len(batch),
                        'existentes': skipped_count
                    })
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
            for r in GameSummary.objects.values_list('season', 'season_type', 'game_id', 'team_abb')
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(total=total_lines, desc="  Procesando summaries", unit=" filas", ncols=100)
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
                    progress_bar.set_postfix({
                        'nuevos': created_count + len(batch),
                        'existentes': skipped_count
                    })
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
        self.stdout.write(self.style.WARNING("\n[6/6] Importando Team Boxscore Traditional..."))
        
        csv_path = "./csv/teams_box_scores.csv"
        total_lines = count_csv_lines(csv_path)
        
        # Cargar registros existentes en memoria (clave única: season, season_type, team_id, team_abb, game_id)
        existing_records = {
            tuple(r)
            for r in TeamBoxscoreTraditional.objects.values_list('season', 'season_type', 'team_id', 'team_abb', 'game_id')
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            progress_bar = tqdm(total=total_lines, desc="  Procesando team boxscores", unit=" filas", ncols=100)
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
                        TeamBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
                        created_count += len(batch)
                        batch = []
                    
                    # Actualizar descripción de la barra
                    progress_bar.set_postfix({
                        'nuevos': created_count + len(batch),
                        'existentes': skipped_count
                    })
            finally:
                progress_bar.close()
            
            # Insertar el lote final
            if batch:
                TeamBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
                created_count += len(batch)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"  Team Boxscore Traditional: {created_count} nuevos, {skipped_count} existentes, {total_lines} filas procesadas"
            )
        )
