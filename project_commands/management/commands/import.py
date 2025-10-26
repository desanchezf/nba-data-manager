import os
import logging

from django.core.management.base import BaseCommand

from source.models import Links
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import initial data from links directory"

    def handle(self, *args, **options):
        # Importar links
        if self.import_links():
            self.stdout.write(self.style.SUCCESS("Links importados correctamente"))
        else:
            self.stdout.write(self.style.ERROR("Error al importar links"))

    # Importar links
    def import_links(self):
        """
        Importar links desde el directorio de links
        """
        try:
            links_dir = "project_commands/management/commands/links"
            if not os.path.isdir(links_dir):
                raise ValueError(f"No existe el directorio de links: {links_dir}")

            self.stdout.write(f"Procesando directorio: {links_dir}")
            total_links = 0
            created_links = 0
            existing_links = 0

            for file_name in os.listdir(links_dir):
                file_path = os.path.join(links_dir, file_name)
                if not os.path.isfile(file_path):
                    continue  # skip subdirs etc

                self.stdout.write(f"Procesando archivo: {file_name}")
                file_links = 0

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        url = line.strip()
                        if not url or not url.startswith("https://"):
                            continue

                        total_links += 1
                        file_links += 1

                        # Analizar parámetros de la URL para obtener temporada y season_type
                        parsed = urlparse(url)
                        qs = parse_qs(parsed.query)
                        # Default values por si faltan en la url
                        season_type = qs.get("SeasonType", [""])[0].replace("+", " ")
                        season = qs.get("Season", [""])[0]
                        # category from path, ej: /stats/teams/boxscores-traditional
                        category = parsed.path.split("/")[-1]

                        # Guardar en modelo Links
                        obj, created = Links.objects.get_or_create(
                            category=category,
                            season_type=season_type,
                            season=season,
                            defaults={
                                "url": url,
                                "scraped": False,
                            },
                        )

                        if created:
                            created_links += 1
                            self.stdout.write(
                                f"  ✓ Creado: {category} - {season} - {season_type}"
                            )
                        else:
                            existing_links += 1
                            self.stdout.write(
                                f"  - Ya existía: {category} - {season} - {season_type}"
                            )

                self.stdout.write(
                    f"  Archivo {file_name}: {file_links} links procesados"
                )

            # Resumen final
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write("RESUMEN DE IMPORTACIÓN:")
            self.stdout.write(f"Total de links procesados: {total_links}")
            self.stdout.write(f"Links creados: {created_links}")
            self.stdout.write(f"Links ya existentes: {existing_links}")
            self.stdout.write("=" * 50)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al importar links: {e}"))
            return False
        return True
