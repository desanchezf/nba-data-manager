from django.utils.translation import gettext_lazy as _


class PredictionTypeChoices:
    """Tipos de predicción"""

    PREMATCH = "prematch"
    LIVE = "live"

    CHOICES = (
        (PREMATCH, _("Prepartido")),
        (LIVE, _("Live/En directo")),
    )

    @classmethod
    def choices(cls):
        return cls.CHOICES


class PredictionCategoryChoices:
    """Categorías principales de predicciones"""

    WINNER = "winner"
    HANDICAP = "handicap"
    TOTAL_POINTS = "total_points"
    COMBINED_BETS = "combined_bets"
    MARGIN_OF_VICTORY = "margin_of_victory"
    HALVES = "halves"
    QUARTERS = "quarters"
    TEAM_TOTALS = "team_totals"
    PLAYER_STATS = "player_stats"
    SPECIAL_MARKETS = "special_markets"
    ALTERNATIVE_MARKETS = "alternative_markets"

    CHOICES = (
        (WINNER, _("Ganador")),
        (HANDICAP, _("Hándicap")),
        (TOTAL_POINTS, _("Total de Puntos")),
        (COMBINED_BETS, _("Apuestas Combinadas")),
        (MARGIN_OF_VICTORY, _("Margen de Victoria")),
        (HALVES, _("Mercados de Mitades")),
        (QUARTERS, _("Mercados por Cuartos")),
        (TEAM_TOTALS, _("Mercados de Equipos")),
        (PLAYER_STATS, _("Mercados de Jugadores")),
        (SPECIAL_MARKETS, _("Mercados Especiales")),
        (ALTERNATIVE_MARKETS, _("Mercados Alternativos")),
    )

    @classmethod
    def choices(cls):
        return cls.CHOICES


class PredictionMarketChoices:
    """Mercados específicos de predicciones"""

    # Ganador
    WINNER_MATCH = "winner_match"

    # Hándicap
    HANDICAP_MAIN = "handicap_main"
    HANDICAP_ALTERNATIVE = "handicap_alternative"

    # Total de Puntos
    TOTAL_POINTS_MAIN = "total_points_main"
    TOTAL_POINTS_ALTERNATIVE = "total_points_alternative"

    # Apuestas Combinadas
    LINE_TOTAL_DOUBLE = "line_total_double"
    WINNER_TOTAL_DOUBLE = "winner_total_double"
    DOUBLE_RESULT = "double_result"

    # Margen de Victoria
    MARGIN_SIMPLE = "margin_simple"
    MARGIN_BANDS = "margin_bands"
    MARGIN_FOUR_BANDS = "margin_four_bands"
    MARGIN_10PT = "margin_10pt"
    MARGIN_EXACT = "margin_exact"
    MARGIN_12 = "margin_12"

    # Primera Mitad
    FIRST_HALF_WINNER = "first_half_winner"
    FIRST_HALF_WINNER_NO_DRAW = "first_half_winner_no_draw"
    FIRST_HALF_RESULT = "first_half_result"
    FIRST_HALF_HANDICAP = "first_half_handicap"
    FIRST_HALF_TOTAL = "first_half_total"
    FIRST_HALF_TOTAL_ODD_EVEN = "first_half_total_odd_even"
    FIRST_HALF_TOTAL_ALTERNATIVE = "first_half_total_alternative"
    FIRST_HALF_AWAY_TOTAL = "first_half_away_total"
    FIRST_HALF_HOME_TOTAL = "first_half_home_total"
    FIRST_HALF_LINE_TOTAL_DOUBLE = "first_half_line_total_double"
    FIRST_HALF_WINNER_TOTAL_DOUBLE = "first_half_winner_total_double"
    FIRST_HALF_WINNER_3WAY = "first_half_winner_3way"
    FIRST_HALF_HANDICAP_ALTERNATIVE = "first_half_handicap_alternative"
    FIRST_HALF_MARGIN = "first_half_margin"
    FIRST_HALF_MARGIN_EXACT = "first_half_margin_exact"

    # Segunda Mitad
    SECOND_HALF_WINNER = "second_half_winner"
    SECOND_HALF_HANDICAP = "second_half_handicap"
    SECOND_HALF_TOTAL = "second_half_total"
    SECOND_HALF_LINE_TOTAL_DOUBLE = "second_half_line_total_double"
    SECOND_HALF_WINNER_TOTAL_DOUBLE = "second_half_winner_total_double"
    SECOND_HALF_WINNER_3WAY = "second_half_winner_3way"

    # Primer Cuarto
    Q1_WINNER = "q1_winner"
    Q1_WINNER_NO_DRAW = "q1_winner_no_draw"
    Q1_HANDICAP = "q1_handicap"
    Q1_TOTAL = "q1_total"
    Q1_TOTAL_ODD_EVEN = "q1_total_odd_even"
    Q1_AWAY_TOTAL = "q1_away_total"
    Q1_HOME_TOTAL = "q1_home_total"
    Q1_LINE_TOTAL_DOUBLE = "q1_line_total_double"
    Q1_WINNER_TOTAL_DOUBLE = "q1_winner_total_double"
    Q1_WINNER_3WAY = "q1_winner_3way"
    Q1_RACE_TO_X = "q1_race_to_x"
    Q1_HANDICAP_ALTERNATIVE = "q1_handicap_alternative"
    Q1_TOTAL_ALTERNATIVE = "q1_total_alternative"
    Q1_MARGIN = "q1_margin"
    Q1_MARGIN_EXACT = "q1_margin_exact"
    Q1_WINNER_MATCH_WINNER = "q1_winner_match_winner"
    Q1_FIRST_TEAM_SCORE = "q1_first_team_score"

    # Segundo Cuarto
    Q2_WINNER = "q2_winner"
    Q2_HANDICAP = "q2_handicap"
    Q2_TOTAL = "q2_total"
    Q2_AWAY_TOTAL = "q2_away_total"
    Q2_HOME_TOTAL = "q2_home_total"
    Q2_RACE_TO_X = "q2_race_to_x"
    Q2_HANDICAP_ALTERNATIVE = "q2_handicap_alternative"
    Q2_TOTAL_ALTERNATIVE = "q2_total_alternative"
    Q2_MARGIN = "q2_margin"
    Q2_MARGIN_EXACT = "q2_margin_exact"
    Q2_FIRST_TEAM_SCORE = "q2_first_team_score"
    Q2_LAST_TEAM_SCORE = "q2_last_team_score"

    # Tercer Cuarto
    Q3_WINNER = "q3_winner"
    Q3_HANDICAP = "q3_handicap"
    Q3_TOTAL = "q3_total"
    Q3_AWAY_TOTAL = "q3_away_total"
    Q3_HOME_TOTAL = "q3_home_total"
    Q3_LINE_TOTAL_DOUBLE = "q3_line_total_double"
    Q3_WINNER_TOTAL_DOUBLE = "q3_winner_total_double"
    Q3_WINNER_3WAY = "q3_winner_3way"
    Q3_RACE_TO_X = "q3_race_to_x"
    Q3_HANDICAP_ALTERNATIVE = "q3_handicap_alternative"
    Q3_TOTAL_ALTERNATIVE = "q3_total_alternative"
    Q3_MARGIN = "q3_margin"
    Q3_MARGIN_EXACT = "q3_margin_exact"
    Q3_FIRST_TEAM_SCORE = "q3_first_team_score"

    # Cuarto Cuarto
    Q4_WINNER = "q4_winner"
    Q4_HANDICAP = "q4_handicap"
    Q4_TOTAL = "q4_total"
    Q4_AWAY_TOTAL = "q4_away_total"
    Q4_HOME_TOTAL = "q4_home_total"
    Q4_LINE_TOTAL_DOUBLE = "q4_line_total_double"
    Q4_WINNER_TOTAL_DOUBLE = "q4_winner_total_double"
    Q4_WINNER_3WAY = "q4_winner_3way"
    Q4_RACE_TO_X = "q4_race_to_x"
    Q4_HANDICAP_ALTERNATIVE = "q4_handicap_alternative"
    Q4_TOTAL_ALTERNATIVE = "q4_total_alternative"
    Q4_MARGIN = "q4_margin"
    Q4_MARGIN_EXACT = "q4_margin_exact"
    Q4_FIRST_TEAM_SCORE = "q4_first_team_score"

    # Mercados de Equipos
    AWAY_TEAM_TOTAL = "away_team_total"
    HOME_TEAM_TOTAL = "home_team_total"
    AWAY_TEAM_TOTAL_ALTERNATIVE = "away_team_total_alternative"
    HOME_TEAM_TOTAL_ALTERNATIVE = "home_team_total_alternative"
    AWAY_TEAM_TOTAL_ODD_EVEN = "away_team_total_odd_even"
    HOME_TEAM_TOTAL_ODD_EVEN = "home_team_total_odd_even"

    # Mercados de Jugadores - Puntos
    PLAYER_POINTS_X_PLUS = "player_points_x_plus"
    PLAYER_POINTS_SPECIFIC = "player_points_specific"
    PLAYER_POINTS_ALTERNATIVE = "player_points_alternative"

    # Mercados de Jugadores - Asistencias
    PLAYER_ASSISTS_X_PLUS = "player_assists_x_plus"
    PLAYER_ASSISTS_SPECIFIC = "player_assists_specific"

    # Mercados de Jugadores - Rebotes
    PLAYER_REBOUNDS_X_PLUS = "player_rebounds_x_plus"
    PLAYER_REBOUNDS_SPECIFIC = "player_rebounds_specific"

    # Mercados de Jugadores - Triples
    PLAYER_THREES_X_PLUS = "player_threes_x_plus"
    PLAYER_THREES_SPECIFIC = "player_threes_specific"

    # Mercados de Jugadores - Otras Estadísticas
    PLAYER_BLOCKS_X_PLUS = "player_blocks_x_plus"
    PLAYER_STEALS_X_PLUS = "player_steals_x_plus"
    PLAYER_BLOCKS_SPECIFIC = "player_blocks_specific"
    PLAYER_STEALS_SPECIFIC = "player_steals_specific"

    # Mercados de Jugadores - Combinaciones
    PLAYER_POINTS_ASSISTS = "player_points_assists"
    PLAYER_POINTS_REBOUNDS = "player_points_rebounds"
    PLAYER_POINTS_REBOUNDS_ASSISTS = "player_points_rebounds_assists"
    PLAYER_REBOUNDS_ASSISTS = "player_rebounds_assists"
    PLAYER_POINTS_ALT_REBOUNDS_ASSISTS = "player_points_alt_rebounds_assists"
    PLAYER_POINTS_ALT_ASSISTS = "player_points_alt_assists"
    PLAYER_POINTS_ALT_REBOUNDS_ASSISTS_ALT = "player_points_alt_rebounds_assists_alt"

    # Mercados de Jugadores - Rendimiento por Cuarto
    PLAYER_POINTS_EACH_QUARTER = "player_points_each_quarter"
    PLAYER_POINTS_Q1 = "player_points_q1"
    PLAYER_POINTS_Q1_X_PLUS = "player_points_q1_x_plus"

    # Mercados de Jugadores - Logros
    PLAYER_DOUBLE_DOUBLE = "player_double_double"
    PLAYER_TRIPLE_DOUBLE = "player_triple_double"

    # Mercados de Jugadores - Comparaciones
    PLAYER_POINTS_HEAD_TO_HEAD = "player_points_head_to_head"
    PLAYER_POINTS_DUO = "player_points_duo"
    PLAYER_POINTS_TRIO = "player_points_trio"
    PLAYER_TOP_SCORER = "player_top_scorer"
    PLAYER_TOP_SCORER_TEAM_WIN = "player_top_scorer_team_win"
    PLAYER_POINTS_COMPARISON = "player_points_comparison"

    # Mercados Especiales - Primera Canasta
    FIRST_BASKET_TEAM = "first_basket_team"
    FIRST_BASKET_PLAYER = "first_basket_player"
    FIRST_BASKET_METHOD = "first_basket_method"
    FIRST_BASKET_TEAM_PLAYER = "first_basket_team_player"
    FIRST_BASKET_WINNER_DOUBLE = "first_basket_winner_double"
    FIRST_BASKET_Q1_WINNER_DOUBLE = "first_basket_q1_winner_double"

    # Mercados Especiales - Carreras
    RACE_TO_X_POINTS = "race_to_x_points"

    # Mercados Especiales - Eventos
    LEAD_FROM_START = "lead_from_start"
    BOTH_TEAMS_SCORE_FIRST_MINUTE = "both_teams_score_first_minute"
    THREE_POINTERS_FIRST_3_MIN = "three_pointers_first_3_min"
    OVERTIME = "overtime"
    HALF_WITH_MORE_POINTS = "half_with_more_points"
    QUARTER_WITH_MORE_POINTS = "quarter_with_more_points"

    # Mercados Especiales - Apuestas Especiales
    SPECIAL_BET = "special_bet"
    TRIPLE_BET = "triple_bet"

    # Mercados Especiales - Ganar Todos
    TEAM_WIN_ALL_QUARTERS = "team_win_all_quarters"
    TEAM_WIN_BOTH_HALVES = "team_win_both_halves"

    # Mercados Alternativos - Totales
    TOTAL_POINTS_ALTERNATIVE_MAIN = "total_points_alternative_main"
    AWAY_TEAM_TOTAL_ALTERNATIVE_MAIN = "away_team_total_alternative_main"
    HOME_TEAM_TOTAL_ALTERNATIVE_MAIN = "home_team_total_alternative_main"
    FIRST_HALF_TOTAL_ALTERNATIVE_MAIN = "first_half_total_alternative_main"

    # Mercados Alternativos - Handicaps
    HANDICAP_ALTERNATIVE_MAIN = "handicap_alternative_main"
    FIRST_HALF_HANDICAP_ALTERNATIVE_MAIN = "first_half_handicap_alternative_main"
    Q1_HANDICAP_ALTERNATIVE_MAIN = "q1_handicap_alternative_main"
    Q2_HANDICAP_ALTERNATIVE_MAIN = "q2_handicap_alternative_main"
    Q3_HANDICAP_ALTERNATIVE_MAIN = "q3_handicap_alternative_main"
    Q4_HANDICAP_ALTERNATIVE_MAIN = "q4_handicap_alternative_main"

    CHOICES = (
        # Ganador
        (WINNER_MATCH, _("Ganador del encuentro")),
        # Hándicap
        (HANDICAP_MAIN, _("Hándicap")),
        (HANDICAP_ALTERNATIVE, _("Hándicaps alternativos")),
        # Total de Puntos
        (TOTAL_POINTS_MAIN, _("Total de puntos")),
        (TOTAL_POINTS_ALTERNATIVE, _("Total de puntos - Alternativo")),
        # Apuestas Combinadas
        (LINE_TOTAL_DOUBLE, _("Línea / Total - Apuesta doble")),
        (WINNER_TOTAL_DOUBLE, _("Doble a partido/total de puntos")),
        (DOUBLE_RESULT, _("Doble resultado")),
        # Margen de Victoria
        (MARGIN_SIMPLE, _("Margen de victoria")),
        (MARGIN_BANDS, _("Margen de victoria (Bandas)")),
        (MARGIN_FOUR_BANDS, _("Margen de victoria (Cuatro bandas)")),
        (MARGIN_10PT, _("Margen de victoria (10 pt)")),
        (MARGIN_EXACT, _("Margen de victoria (Exacto)")),
        (MARGIN_12, _("Margen de victoria 12")),
        # Primera Mitad
        (FIRST_HALF_WINNER, _("1.a mitad - Ganador")),
        (FIRST_HALF_WINNER_NO_DRAW, _("1.a mitad - Ganador sin empate")),
        (FIRST_HALF_RESULT, _("1ª mitad - Resultado")),
        (FIRST_HALF_HANDICAP, _("1.a mitad - Hándicap")),
        (FIRST_HALF_TOTAL, _("1.a mitad - Total de puntos")),
        (FIRST_HALF_TOTAL_ODD_EVEN, _("1ª mitad - Total de puntos - Par/Impar")),
        (FIRST_HALF_TOTAL_ALTERNATIVE, _("1.a mitad - Total de puntos alternativo")),
        (FIRST_HALF_AWAY_TOTAL, _("1.a mitad - Total del equipo visitante")),
        (FIRST_HALF_HOME_TOTAL, _("1.a mitad - Total del equipo local")),
        (FIRST_HALF_LINE_TOTAL_DOUBLE, _("1.ª mitad: Línea/Total - Apuesta doble")),
        (FIRST_HALF_WINNER_TOTAL_DOUBLE, _("1.a mitad - Doble a ganador/total")),
        (FIRST_HALF_WINNER_3WAY, _("1.ª mitad - Apuesta a ganador (3 opciones)")),
        (FIRST_HALF_HANDICAP_ALTERNATIVE, _("Hándicap alternativo en la 1.a mitad")),
        (FIRST_HALF_MARGIN, _("1ª parte - Margen")),
        (FIRST_HALF_MARGIN_EXACT, _("Margen de la 1ª Parte (Exacto)")),
        # Segunda Mitad
        (SECOND_HALF_WINNER, _("2.a mitad - Ganador")),
        (SECOND_HALF_HANDICAP, _("2.a mitad - Hándicap")),
        (SECOND_HALF_TOTAL, _("2.a mitad - Total de puntos")),
        (SECOND_HALF_LINE_TOTAL_DOUBLE, _("2.o cuarto - Doble a hándicap/total")),
        (SECOND_HALF_WINNER_TOTAL_DOUBLE, _("2.o cuarto - Doble a ganador/total")),
        (SECOND_HALF_WINNER_3WAY, _("2.o cuarto - Apuesta a ganador (3 opciones)")),
        # Primer Cuarto
        (Q1_WINNER, _("1.er cuarto - Ganador")),
        (Q1_WINNER_NO_DRAW, _("1.er cuarto - Ganador sin empate")),
        (Q1_HANDICAP, _("1.er cuarto - Hándicap")),
        (Q1_TOTAL, _("1.er cuarto - Total de puntos")),
        (Q1_TOTAL_ODD_EVEN, _("1.er cuarto - Total de puntos - Par/Impar")),
        (Q1_AWAY_TOTAL, _("1.er cuarto - Total del equipo visitante")),
        (Q1_HOME_TOTAL, _("1.er cuarto - Total del equipo local")),
        (Q1_LINE_TOTAL_DOUBLE, _("1.er cuarto: Línea/Total - Apuesta doble")),
        (Q1_WINNER_TOTAL_DOUBLE, _("1.er cuarto - Doble a ganador/total")),
        (Q1_WINNER_3WAY, _("1.er cuarto - Apuesta a ganador (3 opciones)")),
        (Q1_RACE_TO_X, _("1.er cuarto - Carrera a X")),
        (Q1_HANDICAP_ALTERNATIVE, _("Hándicap Alternativo en el 1er Cuarto")),
        (Q1_TOTAL_ALTERNATIVE, _("1.er cuarto - Total de puntos alternativo")),
        (Q1_MARGIN, _("Margen del 1er Cuarto")),
        (Q1_MARGIN_EXACT, _("Margen del 1er Cuarto (Exacto)")),
        (Q1_WINNER_MATCH_WINNER, _("Ganador del 1. er cuarto/Ganador del partido")),
        (Q1_FIRST_TEAM_SCORE, _("1.er cuarto - Primer equipo en anotar")),
        # Segundo Cuarto
        (Q2_WINNER, _("2.o cuarto - Ganador")),
        (Q2_HANDICAP, _("2.o cuarto - Hándicap")),
        (Q2_TOTAL, _("2.o cuarto - Total de puntos")),
        (Q2_AWAY_TOTAL, _("2.o cuarto - Total del equipo visitante")),
        (Q2_HOME_TOTAL, _("2.o cuarto - Total del equipo local")),
        (Q2_RACE_TO_X, _("2.o cuarto - Carrera a X")),
        (Q2_HANDICAP_ALTERNATIVE, _("Hándicap Alternativo en el 2º Cuarto")),
        (Q2_TOTAL_ALTERNATIVE, _("Puntos Totales del 2º Cuarto - Apuesta Alternativa")),
        (Q2_MARGIN, _("Margen del 2º Cuarto")),
        (Q2_MARGIN_EXACT, _("Margen del 2º Cuarto (Exacto)")),
        (Q2_FIRST_TEAM_SCORE, _("2.o cuarto - Primer equipo en anotar")),
        (Q2_LAST_TEAM_SCORE, _("2.o cuarto - Último equipo en anotar")),
        # Tercer Cuarto
        (Q3_WINNER, _("3.er cuarto - Ganador")),
        (Q3_HANDICAP, _("3.er cuarto - Hándicap")),
        (Q3_TOTAL, _("3.er cuarto - Total de puntos")),
        (Q3_AWAY_TOTAL, _("3.er cuarto - Total del equipo visitante")),
        (Q3_HOME_TOTAL, _("3.er cuarto - Total del equipo local")),
        (Q3_LINE_TOTAL_DOUBLE, _("3.er cuarto - Doble a hándicap/total")),
        (Q3_WINNER_TOTAL_DOUBLE, _("3.er cuarto - Doble a ganador/total")),
        (Q3_WINNER_3WAY, _("3.er cuarto - Apuesta a ganador (3 opciones)")),
        (Q3_RACE_TO_X, _("3.er cuarto - Carrera a X")),
        (Q3_HANDICAP_ALTERNATIVE, _("Hándicap Alternativo en el 3er Cuarto")),
        (
            Q3_TOTAL_ALTERNATIVE,
            _("Puntos Totales del 3er Cuarto - Apuesta Alternativa"),
        ),
        (Q3_MARGIN, _("Margen del 3er Cuarto")),
        (Q3_MARGIN_EXACT, _("Margen del 3er Cuarto (Exacto)")),
        (Q3_FIRST_TEAM_SCORE, _("3.er cuarto - Primer equipo en anotar")),
        # Cuarto Cuarto
        (Q4_WINNER, _("4.o cuarto - Ganador")),
        (Q4_HANDICAP, _("4.o cuarto - Hándicap")),
        (Q4_TOTAL, _("4.o cuarto -Total de puntos")),
        (Q4_AWAY_TOTAL, _("4.o cuarto - Total del equipo visitante")),
        (Q4_HOME_TOTAL, _("4.o cuarto - Total del equipo local")),
        (Q4_LINE_TOTAL_DOUBLE, _("4.o cuarto - Doble a hándicap/total")),
        (Q4_WINNER_TOTAL_DOUBLE, _("4.o cuarto - Doble a ganador/total")),
        (Q4_WINNER_3WAY, _("4.o cuarto - Apuesta a ganador (3 opciones)")),
        (Q4_RACE_TO_X, _("4.o cuarto - Carrera a X")),
        (Q4_HANDICAP_ALTERNATIVE, _("Hándicap Alternativo en el 4º Cuarto")),
        (Q4_TOTAL_ALTERNATIVE, _("Puntos Totales del 4º Cuarto - Apuesta Alternativa")),
        (Q4_MARGIN, _("Margen del 4º Cuarto")),
        (Q4_MARGIN_EXACT, _("Margen del 4º Cuarto (Exacto)")),
        (Q4_FIRST_TEAM_SCORE, _("4.o cuarto - Primer equipo en anotar")),
        # Mercados de Equipos
        (AWAY_TEAM_TOTAL, _("Equipo visitante - Total de puntos")),
        (HOME_TEAM_TOTAL, _("Equipo local - Total de puntos")),
        (
            AWAY_TEAM_TOTAL_ALTERNATIVE,
            _("Equipo visitante - Total de puntos alternativo"),
        ),
        (HOME_TEAM_TOTAL_ALTERNATIVE, _("Equipo local - Total de puntos adicional")),
        (AWAY_TEAM_TOTAL_ODD_EVEN, _("Equipo visitante - Total de puntos impar/par")),
        (HOME_TEAM_TOTAL_ODD_EVEN, _("Equipo local - Total de puntos impar/par")),
        # Mercados de Jugadores - Puntos
        (PLAYER_POINTS_X_PLUS, _("Anota X+ puntos")),
        (PLAYER_POINTS_SPECIFIC, _("[Jugador] - Puntos")),
        (PLAYER_POINTS_ALTERNATIVE, _("[Jugador] - Puntos alternativos")),
        # Mercados de Jugadores - Asistencias
        (PLAYER_ASSISTS_X_PLUS, _("Consigue X+ asistencias")),
        (PLAYER_ASSISTS_SPECIFIC, _("[Jugador] - Asistencias")),
        # Mercados de Jugadores - Rebotes
        (PLAYER_REBOUNDS_X_PLUS, _("Registra X+ rebotes")),
        (PLAYER_REBOUNDS_SPECIFIC, _("[Jugador] - Rebotes")),
        # Mercados de Jugadores - Triples
        (PLAYER_THREES_X_PLUS, _("X+ triples anotados")),
        (PLAYER_THREES_SPECIFIC, _("[Jugador] - Triples anotados")),
        # Mercados de Jugadores - Otras Estadísticas
        (PLAYER_BLOCKS_X_PLUS, _("Consigue X+ tapones")),
        (PLAYER_STEALS_X_PLUS, _("Consigue X+ robos")),
        (PLAYER_BLOCKS_SPECIFIC, _("[Jugador] - Tapones")),
        (PLAYER_STEALS_SPECIFIC, _("[Jugador] - Robos")),
        # Mercados de Jugadores - Combinaciones
        (PLAYER_POINTS_ASSISTS, _("[Jugador] - Puntos + asistencias")),
        (PLAYER_POINTS_REBOUNDS, _("[Jugador] - Puntos + rebotes")),
        (
            PLAYER_POINTS_REBOUNDS_ASSISTS,
            _("[Jugador] - Puntos + rebotes + asistencias"),
        ),
        (PLAYER_REBOUNDS_ASSISTS, _("[Jugador] - Rebotes + asistencias")),
        (
            PLAYER_POINTS_ALT_REBOUNDS_ASSISTS,
            _("[Jugador] - Puntos alternativos + Rebotes + Asistencias"),
        ),
        (PLAYER_POINTS_ALT_ASSISTS, _("[Jugador] - Puntos alternativos + Asistencias")),
        (
            PLAYER_POINTS_ALT_REBOUNDS_ASSISTS_ALT,
            _("[Jugador] - Puntos alternativos + Rebotes + Asistencias"),
        ),
        # Mercados de Jugadores - Rendimiento por Cuarto
        (PLAYER_POINTS_EACH_QUARTER, _("Jugador que anota X+ puntos en cada cuarto")),
        (PLAYER_POINTS_Q1, _("[Jugador] - Puntos en el 1er cuarto")),
        (PLAYER_POINTS_Q1_X_PLUS, _("1st Quarter - To Score X+ Points")),
        # Mercados de Jugadores - Logros
        (PLAYER_DOUBLE_DOUBLE, _("Consigue un doble doble")),
        (PLAYER_TRIPLE_DOUBLE, _("Consigue un triple doble")),
        # Mercados de Jugadores - Comparaciones
        (PLAYER_POINTS_HEAD_TO_HEAD, _("Doble posibilidad anotadores")),
        (PLAYER_POINTS_DUO, _("Dúo anotadores")),
        (PLAYER_POINTS_TRIO, _("Trío anotadores")),
        (PLAYER_TOP_SCORER, _("Máximo anotador")),
        (PLAYER_TOP_SCORER_TEAM_WIN, _("Máximo anotador y victoria de su equipo")),
        (PLAYER_POINTS_COMPARISON, _("Número de puntos (Cara a cara)")),
        # Mercados Especiales - Primera Canasta
        (FIRST_BASKET_TEAM, _("Primer equipo en anotar")),
        (FIRST_BASKET_PLAYER, _("Primera canasta")),
        (FIRST_BASKET_METHOD, _("Método de la primera canasta")),
        (
            FIRST_BASKET_TEAM_PLAYER,
            _("Jugador que anota la primera canasta del equipo"),
        ),
        (
            FIRST_BASKET_WINNER_DOUBLE,
            _("Primera Canasta/Ganador Partido (Apuesta Doble)"),
        ),
        (
            FIRST_BASKET_Q1_WINNER_DOUBLE,
            _("Primera Canasta/Ganador Primer Cuarto (Apuesta Doble)"),
        ),
        # Mercados Especiales - Carreras
        (RACE_TO_X_POINTS, _("Carrera a X puntos")),
        # Mercados Especiales - Eventos
        (LEAD_FROM_START, _("Lidera de principio a fin")),
        (BOTH_TEAMS_SCORE_FIRST_MINUTE, _("Ambos equipos anotan en el primer minuto")),
        (
            THREE_POINTERS_FIRST_3_MIN,
            _("2 o más tiros de 3 puntos anotados en los primeros 3 minutos"),
        ),
        (OVERTIME, _("¿Habrá prórroga?")),
        (HALF_WITH_MORE_POINTS, _("Mitad con más puntos")),
        (QUARTER_WITH_MORE_POINTS, _("Cuarto con mayor puntuación")),
        # Mercados Especiales - Apuestas Especiales
        (SPECIAL_BET, _("Crear Apuesta - Especiales")),
        (TRIPLE_BET, _("Apuesta triple")),
        # Mercados Especiales - Ganar Todos
        (TEAM_WIN_ALL_QUARTERS, _("[Equipo] gana todos los cuartos")),
        (TEAM_WIN_BOTH_HALVES, _("[Equipo] gana ambas mitades")),
        # Mercados Alternativos - Totales
        (TOTAL_POINTS_ALTERNATIVE_MAIN, _("Total de puntos - Alternativo")),
        (
            AWAY_TEAM_TOTAL_ALTERNATIVE_MAIN,
            _("Equipo visitante - Total de puntos alternativo"),
        ),
        (
            HOME_TEAM_TOTAL_ALTERNATIVE_MAIN,
            _("Equipo local - Total de puntos adicional"),
        ),
        (
            FIRST_HALF_TOTAL_ALTERNATIVE_MAIN,
            _("1.a mitad - Total de puntos alternativo"),
        ),
        # Mercados Alternativos - Handicaps
        (HANDICAP_ALTERNATIVE_MAIN, _("Hándicaps alternativos")),
        (
            FIRST_HALF_HANDICAP_ALTERNATIVE_MAIN,
            _("Hándicap alternativo en la 1.a mitad"),
        ),
        (Q1_HANDICAP_ALTERNATIVE_MAIN, _("Hándicap Alternativo en el 1er Cuarto")),
        (Q2_HANDICAP_ALTERNATIVE_MAIN, _("Hándicap Alternativo en el 2º Cuarto")),
        (Q3_HANDICAP_ALTERNATIVE_MAIN, _("Hándicap Alternativo en el 3er Cuarto")),
        (Q4_HANDICAP_ALTERNATIVE_MAIN, _("Hándicap Alternativo en el 4º Cuarto")),
    )

    @classmethod
    def choices(cls):
        return cls.CHOICES
