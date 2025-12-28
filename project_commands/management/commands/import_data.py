import logging

from django.core.management.base import BaseCommand
from django.conf import settings

import csv
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
        processed_rows = 0
        
        with open("./csv/game_boxscore_traditional.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                processed_rows += 1
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
                
                # Mostrar progreso cada 10000 filas
                if processed_rows % 10000 == 0:
                    self.stdout.write(f"  Procesadas {processed_rows} filas, {len(players_seen)} jugadores únicos encontrados...")

        # Insertar todos los jugadores de una vez (más eficiente)
        if players_to_create:
            self.stdout.write(f"  Insertando {len(players_to_create)} jugadores nuevos en la base de datos...")
            Players.objects.bulk_create(players_to_create, ignore_conflicts=True)
            logger.info(f"Creados {len(players_to_create)} jugadores nuevos")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"  Jugadores: {len(players_seen)} únicos importados, {skipped_count} omitidos (equipos no válidos), {processed_rows} filas procesadas"
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
        
        # Cargar registros existentes en memoria (clave única: game_id, season, season_type, home_team_abb, away_team_abb, player_id)
        existing_records = {
            (r.game_id, r.season, r.season_type, r.home_team_abb, r.away_team_abb, r.player_id)
            for r in GameBoxscoreTraditional.objects.values_list(
                'game_id', 'season', 'season_type', 'home_team_abb', 'away_team_abb', 'player_id'
            )
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        processed_rows = 0
        
        with open("./csv/game_boxscore_traditional.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                processed_rows += 1
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
                        fgm=int(row[13]) if row[13] else 0,
                        fga=int(row[14]) if row[14] else 0,
                        fg_perc=float(row[15]) if row[15] else 0.0,
                        threepm=int(row[16]) if row[16] else 0,
                        threepa=int(row[17]) if row[17] else 0,
                        threep_perc=float(row[18]) if row[18] else 0.0,
                        ftm=int(row[19]) if row[19] else 0,
                        fta=int(row[20]) if row[20] else 0,
                        ft_perc=float(row[21]) if row[21] else 0.0,
                        oreb=int(row[22]) if row[22] else 0,
                        dreb=int(row[23]) if row[23] else 0,
                        reb=int(row[24]) if row[24] else 0,
                        ast=int(row[25]) if row[25] else 0,
                        stl=int(row[26]) if row[26] else 0,
                        blk=int(row[27]) if row[27] else 0,
                        to=int(row[28]) if row[28] else 0,
                        pf=int(row[29]) if row[29] else 0,
                        pts=int(row[30]) if row[30] else 0,
                        plus_minus=int(row[31]) if len(row) > 31 and row[31] else 0,
                    )
                )
                
                # Insertar por lotes
                if len(batch) >= batch_size:
                    GameBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
                    created_count += len(batch)
                    self.stdout.write(f"  Procesadas {processed_rows} filas, {created_count} nuevos insertados, {skipped_count} existentes...")
                    batch = []
            
            # Insertar el lote final
            if batch:
                GameBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
                created_count += len(batch)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"  Game Boxscore Traditional: {created_count} nuevos, {skipped_count} existentes, {processed_rows} filas procesadas"
            )
        )

    def import_game_play_by_play(self):
        self.stdout.write(self.style.WARNING("\n[4/6] Importando Game Play By Play..."))
        
        # Cargar registros existentes en memoria (clave única basada en los campos únicos)
        existing_records = {
            (r.season, r.season_type, r.game_id, r.team_abb, r.period, r.min, r.score, r.player, r.action)
            for r in GamePlayByPlay.objects.values_list(
                'season', 'season_type', 'game_id', 'team_abb', 'period', 'min', 'score', 'player', 'action'
            )
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        processed_rows = 0
        
        with open("./csv/game_play_by_play.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                processed_rows += 1
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
                    self.stdout.write(f"  Procesadas {processed_rows} filas, {created_count} nuevos insertados, {skipped_count} existentes...")
                    batch = []
            
            # Insertar el lote final
            if batch:
                GamePlayByPlay.objects.bulk_create(batch, ignore_conflicts=True)
                created_count += len(batch)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"  Game Play By Play: {created_count} nuevos, {skipped_count} existentes, {processed_rows} filas procesadas"
            )
        )

    def import_game_summary(self):
        self.stdout.write(self.style.WARNING("\n[5/6] Importando Game Summary..."))
        
        # Cargar registros existentes en memoria (clave única: season, season_type, game_id, team_abb)
        existing_records = {
            (r.season, r.season_type, r.game_id, r.team_abb)
            for r in GameSummary.objects.values_list('season', 'season_type', 'game_id', 'team_abb')
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        processed_rows = 0
        
        with open("./csv/game_summary.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                processed_rows += 1
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
                        q1=int(row[4]) if row[4] else 0,
                        q2=int(row[5]) if row[5] else 0,
                        q3=int(row[6]) if row[6] else 0,
                        q4=int(row[7]) if row[7] else 0,
                        ot1=int(row[8]) if row[8] else 0,
                        ot2=int(row[9]) if row[9] else 0,
                        ot3=int(row[10]) if row[10] else 0,
                        ot4=int(row[11]) if row[11] else 0,
                        final=int(row[12]) if row[12] else 0,
                        pitp=int(row[13]) if row[13] else 0,
                        fb_pts=int(row[14]) if row[14] else 0,
                        big_ld=int(row[15]) if row[15] else 0,
                        bpts=int(row[16]) if row[16] else 0,
                        treb=int(row[17]) if row[17] else 0,
                        tov=int(row[18]) if row[18] else 0,
                        ttov=int(row[19]) if row[19] else 0,
                        pot=int(row[20]) if row[20] else 0,
                        lead_changes=int(row[21]) if row[21] else 0,
                        times_tied=int(row[22]) if row[22] else 0,
                    )
                )
                
                # Insertar por lotes
                if len(batch) >= batch_size:
                    GameSummary.objects.bulk_create(batch, ignore_conflicts=True)
                    created_count += len(batch)
                    self.stdout.write(f"  Procesadas {processed_rows} filas, {created_count} nuevos insertados, {skipped_count} existentes...")
                    batch = []
            
            # Insertar el lote final
            if batch:
                GameSummary.objects.bulk_create(batch, ignore_conflicts=True)
                created_count += len(batch)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"  Game Summary: {created_count} nuevos, {skipped_count} existentes, {processed_rows} filas procesadas"
            )
        )

    def import_team_boxscore_traditional(self):
        self.stdout.write(self.style.WARNING("\n[6/6] Importando Team Boxscore Traditional..."))
        
        # Cargar registros existentes en memoria (clave única: season, season_type, team_id, team_abb, game_id)
        existing_records = {
            (r.season, r.season_type, r.team_id, r.team_abb, r.game_id)
            for r in TeamBoxscoreTraditional.objects.values_list('season', 'season_type', 'team_id', 'team_abb', 'game_id')
        }
        self.stdout.write(f"  Cargados {len(existing_records)} registros existentes en memoria")
        
        batch_size = 5000
        batch = []
        created_count = 0
        skipped_count = 0
        processed_rows = 0
        
        with open("./csv/teams_box_scores.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                processed_rows += 1
                if len(row) < 28:
                    continue

                team_id = int(row[2]) if row[2] else 0
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
                        min=int(row[9]) if row[9] else 0,
                        pts=int(row[10]) if row[10] else 0,
                        fgm=int(row[11]) if row[11] else 0,
                        fga=int(row[12]) if row[12] else 0,
                        fg_pct=float(row[13]) if row[13] else 0.0,
                        fg3m=int(row[14]) if row[14] else 0,
                        fg3a=int(row[15]) if row[15] else 0,
                        fg3_pct=float(row[16]) if row[16] else 0.0,
                        ftm=int(row[17]) if row[17] else 0,
                        fta=int(row[18]) if row[18] else 0,
                        ft_pct=float(row[19]) if row[19] else 0.0,
                        oreb=int(row[20]) if row[20] else 0,
                        dreb=int(row[21]) if row[21] else 0,
                        reb=int(row[22]) if row[22] else 0,
                        ast=int(row[23]) if row[23] else 0,
                        stl=int(row[24]) if row[24] else 0,
                        blk=int(row[25]) if row[25] else 0,
                        tov=int(row[26]) if row[26] else 0,
                        pf=int(row[27]) if row[27] else 0,
                        plus_minus=int(row[28]) if len(row) > 28 and row[28] else 0,
                    )
                )
                
                # Insertar por lotes
                if len(batch) >= batch_size:
                    TeamBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
                    created_count += len(batch)
                    self.stdout.write(f"  Procesadas {processed_rows} filas, {created_count} nuevos insertados, {skipped_count} existentes...")
                    batch = []
            
            # Insertar el lote final
            if batch:
                TeamBoxscoreTraditional.objects.bulk_create(batch, ignore_conflicts=True)
                created_count += len(batch)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"  Team Boxscore Traditional: {created_count} nuevos, {skipped_count} existentes, {processed_rows} filas procesadas"
            )
        )
