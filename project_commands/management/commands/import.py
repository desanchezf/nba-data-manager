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
            self.stdout.write(self.style.SUCCESS("Links imported correctly"))
        else:
            self.stdout.write(self.style.ERROR("Error importing links"))

    # Importar links
    def import_links(self):
        """
        Importar links desde el directorio de links
        """
        try:
            links_dir = "project_commands/management/commands/links"
            if not os.path.isdir(links_dir):
                raise ValueError(f"No existe el directorio de links: {links_dir}")

            self.stdout.write(f"Processing directory: {links_dir}")
            total_links = 0
            created_links = 0
            existing_links = 0

            for file_name in os.listdir(links_dir):
                file_path = os.path.join(links_dir, file_name)
                if not os.path.isfile(file_path):
                    continue  # skip subdirs etc

                self.stdout.write(f"Processing file: {file_name}")
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
                                f"  ✓ Created: {category} - {season} - {season_type}"
                            )
                        else:
                            existing_links += 1
                            self.stdout.write(
                                f"  - Already exists: {category} - {season} - {season_type}"
                            )

                self.stdout.write(
                    f"  Archivo {file_name}: {file_links} links procesados"
                )

            # Resumen final
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write("SUMMARY OF IMPORTATION:")
            self.stdout.write(f"Total links processed: {total_links}")
            self.stdout.write(f"Links created: {created_links}")
            self.stdout.write(f"Links already exist: {existing_links}")
            self.stdout.write("=" * 50)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing links: {e}"))
            return False
        return True
