from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ejecuta el scraper de NBA"

    def handle(self, *args, **options):
        pass
