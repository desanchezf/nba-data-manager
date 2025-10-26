from django.contrib import admin

# Register your models here.
from source.models import Links, Games


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ("category", "season", "season_type", "url", "scraped")
    search_fields = ("category", "season", "season_type", "url")
    list_filter = ("category", "season", "season_type", "scraped")
    ordering = ("-created_at",)


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ("date", "home_team", "away_team", "scraped")
    search_fields = ("date", "home_team", "away_team")
    list_filter = ("date", "home_team", "away_team", "scraped")
    ordering = ("-date", "home_team")
