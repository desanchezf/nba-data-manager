from django.utils.translation import gettext_lazy as _


class ScrapperName(str):
    scrapper_name = (
        ("advanced_boxscore_scraper", _("Advanced Boxscore Scraper")),
        ("box_outs_scraper", _("Box Outs Scraper")),
        ("boxscore_scraper", _("Boxscore Scraper")),
        ("catch_shoot_scraper", _("Catch & Shoot Scraper")),
        ("clutch_scraper", _("Clutch Scraper")),
        ("defense_dashboard_scraper", _("Defense Dashboard Scraper")),
        ("defensive_impact_scraper", _("Defensive Impact Scraper")),
        ("defensive_rebounding_scraper", _("Defensive Rebounding Scraper")),
        ("drives_scraper", _("Drives Scraper")),
        ("elbow_touch_scraper", _("Elbow Touch Scraper")),
        ("hustle_scraper", _("Hustle Scraper")),
        ("offensive_rebounding_scraper", _("Offensive Rebounding Scraper")),
        ("opponent_shooting_scraper", _("Opponent Shooting Scraper")),
        ("paint_touch_scraper", _("Paint Touch Scraper")),
        ("passing_scraper", _("Passing Scraper")),
        ("playtipe_scraper", _("Playtipe Scraper")),
        ("post_ups_scraper", _("Post Ups Scraper")),
        ("pull_up_shooting_scraper", _("Pull Up Shooting Scraper")),
        ("rebounding_scraper", _("Rebounding Scraper")),
        ("shooting_efficiency_scraper", _("Shooting Efficiency Scraper")),
        ("shooting_scraper", _("Shooting Scraper")),
        ("shot_dashboard_scraper", _("Shot Dashboard Scraper")),
        ("speed_distance_scraper", _("Speed & Distance Scraper")),
        ("touches_scraper", _("Touches Scraper")),
    )

    @classmethod
    def choices(cls):
        return ScrapperName.scrapper_name
