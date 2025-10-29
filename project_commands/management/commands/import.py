import os
import logging

from django.core.management.base import BaseCommand
from source.models import Links
from urllib.parse import urlparse, parse_qs
from django.conf import settings
from scrapper.models import ScrapperStatus
from scrapper.enums import ScrapperName

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import initial data from links directory"

    def handle(self, *args, **options):
        # Importar links
        if self.import_links():
            self.stdout.write(self.style.SUCCESS("Links imported correctly"))
        else:
            self.stdout.write(self.style.ERROR("Error importing links"))

        # Importar estado del scraper
        if self.import_scrapper_status():
            self.stdout.write(self.style.SUCCESS("Scrapper status imported correctly"))
        else:
            self.stdout.write(self.style.ERROR("Error importing scrapper status"))

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

    def import_scrapper_status(self):
        """
        Importar estado del scraper
        """
        # Mapear nombres bonitos a valores del enum
        name_mapping = {display: value for value, display in ScrapperName.choices()}

        for scrapper_display_name in settings.SCRAPPER_NAMES:
            # Obtener el valor del enum correspondiente
            scrapper_value = name_mapping.get(scrapper_display_name)

            if not scrapper_value:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠️  No se encontró valor del enum para: {scrapper_display_name}"
                    )
                )
                continue

            _, created = ScrapperStatus.objects.get_or_create(
                scrapper_name=scrapper_value,
                defaults={
                    "last_execution": None,
                    "last_link_scraped": None,
                    "is_running": False,
                },
            )
            if created:
                self.stdout.write(f"  ✓ Created: {scrapper_display_name}")
            else:
                self.stdout.write(f"  - Already exists: {scrapper_display_name}")
        return True
