from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lineups", "0002_lineupsadvanced_group_name_and_more"),
    ]
    operations = [
        migrations.RunSQL(
            sql=(
                "DROP TABLE IF EXISTS lineups_lineupstraditional; "
                "DROP TABLE IF EXISTS lineups_lineupsadvanced; "
                "DROP TABLE IF EXISTS lineups_lineupsmiscs; "
                "DROP TABLE IF EXISTS lineups_lineupsfourfactors; "
                "DROP TABLE IF EXISTS lineups_lineupsscoring; "
                "DROP TABLE IF EXISTS lineups_lineupsopponent;"
            ),
            reverse_sql="",
        ),
    ]
