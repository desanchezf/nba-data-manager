from source.models import Links


class LinksService:
    def __init__(self, category: str = None):
        self.category = category

    def get_links(self):
        """
        Obtiene solo las URLs de los links no scrapeados
        """
        return Links.objects.filter(scraped=False, category=self.category).values_list(
            "url", flat=True
        )

