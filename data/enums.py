from django.utils.translation import gettext_lazy as _


class SeasonChoices(str):
    seasons = (
        ("2015-16", _("2015-16")),
        ("2016-17", _("2016-17")),
        ("2017-18", _("2017-18")),
        ("2018-19", _("2018-19")),
        ("2019-20", _("2019-20")),
        ("2020-21", _("2020-21")),
        ("2021-22", _("2021-22")),
        ("2022-23", _("2022-23")),
        ("2023-24", _("2023-24")),
        ("2024-25", _("2024-25")),
        ("2025-26", _("2025-26")),
    )

    @classmethod
    def choices(cls):
        return SeasonChoices.seasons


class SeasonTypeChoices(str):
    season_types = (
        ("pre-season", _("Pre-Temporada")),
        ("regular-season", _("Temporada Regular")),
        ("playoffs", _("Playoffs")),
        ("all-star", _("All-Star")),
        ("play-in", _("Play-In")),
        ("ist", _("IST")),
    )

    @classmethod
    def choices(cls):
        return SeasonTypeChoices.season_types


class GameBoxscorePeriodChoices(str):
    boxscore_periods = (
        ("All", _("Todo el juego")),
        ("Q1", _("1er Cuarto")),
        ("Q2", _("2do Cuarto")),
        ("Q3", _("3er Cuarto")),
        ("Q4", _("4to Cuarto")),
        ("OT1", _("Tiempo Extra 1")),
        ("OT2", _("Tiempo Extra 2")),
        ("OT3", _("Tiempo Extra 3")),
        ("OT4", _("Tiempo Extra 4")),
        ("1stHalf", _("1ra Mitad")),
        ("2ndHalf", _("2da Mitad")),
        ("AllOT", _("Todos los Tiempos Extra")),
    )

    @classmethod
    def choices(cls):
        return GameBoxscorePeriodChoices.boxscore_periods


class GamePlayByPlayPeriodChoices(str):
    play_by_play_periods = (
        ("All", _("Todo el juego")),
        ("Q1", _("1er Cuarto")),
        ("Q2", _("2do Cuarto")),
        ("Q3", _("3er Cuarto")),
        ("Q4", _("4to Cuarto")),
        ("OT1", _("Tiempo Extra 1")),
        ("OT2", _("Tiempo Extra 2")),
        ("OT3", _("Tiempo Extra 3")),
        ("OT4", _("Tiempo Extra 4")),
    )

    @classmethod
    def choices(cls):
        return GamePlayByPlayPeriodChoices.play_by_play_periods
