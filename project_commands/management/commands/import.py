import os
import logging

from django.core.management.base import BaseCommand

from source.models import Links
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Addind inittial data"

    def handle(self, *args, **options):
        # Importar links
        if self.import_links():
            logger.info("Links importados correctamente")
        else:
            logger.error("Error al importar links")

    # Importar links
    def import_links(self):
        """
        Importar links desde el directorio de links
        """
        try:
            links_dir = "project_commands/management/commands/links"
            if not os.path.isdir(links_dir):
                raise ValueError(f"No existe el directorio de links: {links_dir}")

            for file_name in os.listdir(links_dir):
                file_path = os.path.join(links_dir, file_name)
                if not os.path.isfile(file_path):
                    continue  # skip subdirs etc

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        url = line.strip()
                        if not url or not url.startswith("https://"):
                            continue

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
        except Exception as e:
            logger.error(f"Error al importar links: {e}")
            return False
        return True
