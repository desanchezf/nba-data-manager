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

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import initial data from links directory"

    def handle(self, *args, **options):
        self.import_teams()
        self.import_players()
        self.import_game_boxscore_traditional()
        self.import_game_play_by_play()
        self.import_game_summary()
        self.import_team_boxscore_traditional()

    def import_teams(self):
        # Importa equipos desde NBA_TEAMS_INFO definido en settings.py
        # Estructura: {"Nombre Equipo": [abreviatura, team_id, conferencia,
        # división]}
        teams_created = 0
        teams_updated = 0

        for team_name, team_info in settings.NBA_TEAMS_INFO.items():
            team_abb = team_info[0]
            team_id = team_info[1]
            team_conference = team_info[2]
            team_division = team_info[3]

            team, created = Teams.objects.get_or_create(
                team_id=team_id,
                defaults={
                    "team_name": team_name,
                    "team_abb": team_abb,
                    "team_conference": team_conference,
                    "team_division": team_division,
                },
            )

            if not created:
                # Actualizar si ya existe
                team.team_name = team_name
                team.team_abb = team_abb
                team.team_conference = team_conference
                team.team_division = team_division
                team.save()
                teams_updated += 1
            else:
                teams_created += 1

        logger.info(
            "Importados %d equipos nuevos y %d actualizados",
            teams_created,
            teams_updated,
        )

    def import_players(self):
        # Extrae jugadores únicos del archivo game_boxscore_traditional.csv
        # Columnas: GAME_ID,SEASON,SEASON_TYPE,HOME_TEAM_ABB,AWAY_TEAM_ABB,
        # PLAYER_ID,PLAYER_NAME,PLAYER_NAME_ABB,PLAYER_TEAM_ABB,...
        players_seen = set()  # Evita duplicados: (player_id, season, team_abb)

        with open("./csv/game_boxscore_traditional.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                if len(row) < 9:
                    continue

                player_id = row[5]  # PLAYER_ID
                player_name = row[6]  # PLAYER_NAME
                player_name_abb = row[7]  # PLAYER_NAME_ABB
                player_team_abb = row[8]  # PLAYER_TEAM_ABB
                season = row[1]  # SEASON

                # Crear clave única para evitar duplicados
                player_key = (player_id, season, player_team_abb)

                if player_key not in players_seen:
                    players_seen.add(player_key)

                    # Obtener el equipo por su abreviatura
                    try:
                        team = Teams.objects.get(team_abb=player_team_abb)
                    except Teams.DoesNotExist:
                        logger.warning(
                            "Equipo %s no encontrado para jugador %s",
                            player_team_abb,
                            player_name,
                        )
                        continue

                    # Crear o actualizar el jugador
                    # La combinación única es (season, player_id, team)
                    # para permitir guardar diferentes equipos del jugador
                    Players.objects.get_or_create(
                        player_id=player_id,
                        season=season,
                        team=team,
                        defaults={
                            "player_name": player_name,
                            "player_abb": player_name_abb,
                        },
                    )

        logger.info("Importados %d jugadores únicos", len(players_seen))

    def import_game_boxscore_traditional(self):
        # Lee el archivo CSV y crea registros para cada fila
        with open("./csv/game_boxscore_traditional.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                if len(row) < 31:
                    continue

                GameBoxscoreTraditional.objects.get_or_create(
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

    def import_game_play_by_play(self):
        with open("./csv/game_play_by_play.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                if len(row) < 9:
                    continue

                GamePlayByPlay.objects.get_or_create(
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

    def import_game_summary(self):
        with open("./csv/game_summary.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                if len(row) < 23:
                    continue

                GameSummary.objects.get_or_create(
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

    def import_team_boxscore_traditional(self):
        with open("./csv/teams_box_scores.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera

            for row in reader:
                if len(row) < 28:
                    continue

                TeamBoxscoreTraditional.objects.get_or_create(
                    season=row[0],
                    season_type=row[1],
                    team_id=int(row[2]) if row[2] else 0,
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
