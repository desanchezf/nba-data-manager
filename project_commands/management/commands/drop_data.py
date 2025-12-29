import logging

from django.core.management.base import BaseCommand

from data.models import (
    GameBoxscoreTraditional,
    GamePlayByPlay,
    TeamBoxscoreTraditional,
    GameSummary,
)
from roster.models import Teams, Players

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Elimina todos los datos importados mediante import_data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirma que quieres eliminar todos los datos',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR(
                    "⚠️  ADVERTENCIA: Este comando eliminará TODOS los datos importados."
                )
            )
            self.stdout.write(
                "Para confirmar, ejecuta: python manage.py drop_data --confirm"
            )
            return

        self.stdout.write(self.style.WARNING("Iniciando eliminación de datos..."))
        self.stdout.write("=" * 60)
        
        # Eliminar en orden inverso al de importación
        self.drop_team_boxscore_traditional()
        self.drop_game_summary()
        self.drop_game_play_by_play()
        self.drop_game_boxscore_traditional()
        self.drop_players()
        self.drop_teams()
        
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("Eliminación completada exitosamente"))

    def drop_team_boxscore_traditional(self):
        """Elimina todos los registros de TeamBoxscoreTraditional"""
        self.stdout.write(self.style.WARNING("\n[6/6] Eliminando Team Boxscore Traditional..."))
        count = TeamBoxscoreTraditional.objects.count()
        if count > 0:
            TeamBoxscoreTraditional.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Eliminados {count} registros de Team Boxscore Traditional")
            )
            logger.info(f"Eliminados {count} registros de TeamBoxscoreTraditional")
        else:
            self.stdout.write("  ⊘ No hay registros para eliminar")

    def drop_game_summary(self):
        """Elimina todos los registros de GameSummary"""
        self.stdout.write(self.style.WARNING("\n[5/6] Eliminando Game Summary..."))
        count = GameSummary.objects.count()
        if count > 0:
            GameSummary.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Eliminados {count} registros de Game Summary")
            )
            logger.info(f"Eliminados {count} registros de GameSummary")
        else:
            self.stdout.write("  ⊘ No hay registros para eliminar")

    def drop_game_play_by_play(self):
        """Elimina todos los registros de GamePlayByPlay"""
        self.stdout.write(self.style.WARNING("\n[4/6] Eliminando Game Play By Play..."))
        count = GamePlayByPlay.objects.count()
        if count > 0:
            GamePlayByPlay.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Eliminados {count} registros de Game Play By Play")
            )
            logger.info(f"Eliminados {count} registros de GamePlayByPlay")
        else:
            self.stdout.write("  ⊘ No hay registros para eliminar")

    def drop_game_boxscore_traditional(self):
        """Elimina todos los registros de GameBoxscoreTraditional"""
        self.stdout.write(self.style.WARNING("\n[3/6] Eliminando Game Boxscore Traditional..."))
        count = GameBoxscoreTraditional.objects.count()
        if count > 0:
            GameBoxscoreTraditional.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Eliminados {count} registros de Game Boxscore Traditional")
            )
            logger.info(f"Eliminados {count} registros de GameBoxscoreTraditional")
        else:
            self.stdout.write("  ⊘ No hay registros para eliminar")

    def drop_players(self):
        """Elimina todos los registros de Players"""
        self.stdout.write(self.style.WARNING("\n[2/6] Eliminando jugadores..."))
        count = Players.objects.count()
        if count > 0:
            Players.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Eliminados {count} jugadores")
            )
            logger.info(f"Eliminados {count} jugadores")
        else:
            self.stdout.write("  ⊘ No hay registros para eliminar")

    def drop_teams(self):
        """Elimina todos los registros de Teams"""
        self.stdout.write(self.style.WARNING("\n[1/6] Eliminando equipos..."))
        count = Teams.objects.count()
        if count > 0:
            Teams.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"  ✓ Eliminados {count} equipos")
            )
            logger.info(f"Eliminados {count} equipos")
        else:
            self.stdout.write("  ⊘ No hay registros para eliminar")

