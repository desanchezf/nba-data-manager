from django.utils.translation import gettext_lazy as _


class TeamChoices(str):
    teams = (
        ("ATL", _("Atlanta Hawks")),
        ("BOS", _("Boston Celtics")),
        ("BKN", _("Brooklyn Nets")),
        ("CHA", _("Charlotte Hornets")),
        ("CHI", _("Chicago Bulls")),
        ("CLE", _("Cleveland Cavaliers")),
        ("DAL", _("Dallas Mavericks")),
        ("DEN", _("Denver Nuggets")),
        ("DET", _("Detroit Pistons")),
        ("GSW", _("Golden State Warriors")),
        ("HOU", _("Houston Rockets")),
        ("IND", _("Indiana Pacers")),
        ("LAC", _("Los Angeles Clippers")),
        ("LAL", _("Los Angeles Lakers")),
        ("MEM", _("Memphis Grizzlies")),
        ("MIA", _("Miami Heat")),
        ("MIL", _("Milwaukee Bucks")),
        ("MIN", _("Minnesota Timberwolves")),
        ("NOP", _("New Orleans Pelicans")),
        ("NYK", _("New York Knicks")),
        ("OKC", _("Oklahoma City Thunder")),
        ("ORL", _("Orlando Magic")),
        ("PHI", _("Philadelphia 76ers")),
        ("PHX", _("Phoenix Suns")),
        ("POR", _("Portland Trail Blazers")),
        ("SAC", _("Sacramento Kings")),
        ("SAS", _("San Antonio Spurs")),
        ("TOR", _("Toronto Raptors")),
        ("UTA", _("Utah Jazz")),
        ("WAS", _("Washington Wizards")),
    )

    @classmethod
    def choices(cls):
        return TeamChoices.teams
