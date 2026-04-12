"""
Formularios para el Prediction Hub NBA.
"""

from django import forms

# Mercados binarios disponibles (moneyline/spread)
BINARY_MARKETS = [
    ("moneyline", "Moneyline (Ganador)"),
    ("spread", "Hándicap / Spread"),
    ("winner_match", "Ganador del encuentro"),
    ("totals", "O/U Totales"),
    ("home_team_total", "Total equipo local"),
    ("away_team_total", "Total equipo visitante"),
    ("first_half_winner", "1.a mitad - Ganador"),
    ("first_half_total", "1.a mitad - Total"),
    ("q1_total", "1.er cuarto - Total"),
    ("q1_winner", "1.er cuarto - Ganador"),
    ("all", "Todos los mercados"),
]

RISK_CHOICES = [
    ("conservative", "Conservador (≥65%)"),
    ("moderate", "Moderado (≥58%)"),
    ("aggressive", "Arriesgado (≥52%)"),
]

N_PREDICTIONS = [
    ("3", "3"),
    ("5", "5"),
    ("10", "10"),
    ("20", "20"),
]

N_SELECTIONS = [
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
]

N_TOP = [
    ("5", "5"),
    ("10", "10"),
    ("20", "20"),
    ("50", "50"),
]


class PreMatchForm(forms.Form):
    """Formulario pre-partido (local vs visitante)."""
    home_team = forms.ChoiceField(label="Equipo local*", choices=[])
    away_team = forms.ChoiceField(label="Equipo visitante*", choices=[])
    market = forms.ChoiceField(label="Mercado", choices=BINARY_MARKETS, initial="moneyline")
    risk_level = forms.ChoiceField(label="Nivel de riesgo", choices=RISK_CHOICES, initial="moderate")
    n_predictions = forms.ChoiceField(label="Nº predicciones", choices=N_PREDICTIONS, initial="5")
    odds_home = forms.FloatField(label="Cuota local (opt.)", required=False)
    odds_away = forms.FloatField(label="Cuota visitante (opt.)", required=False)
    match_date = forms.DateField(label="Fecha partido (opt.)", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    save_bet = forms.BooleanField(label="Guardar apuesta", required=False)
    stake_euros = forms.FloatField(label="Stake (€)", required=False)


class LivePredictionForm(forms.Form):
    """Formulario predicción en directo."""
    game_id = forms.CharField(label="GAME_ID (opt.)", required=False, max_length=64)
    home_team = forms.ChoiceField(label="Equipo local*", choices=[])
    away_team = forms.ChoiceField(label="Equipo visitante*", choices=[])
    market = forms.ChoiceField(label="Mercado", choices=BINARY_MARKETS)
    risk_level = forms.ChoiceField(label="Nivel de riesgo", choices=RISK_CHOICES)
    live_data_json = forms.CharField(
        label="Datos en directo (JSON)",
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": '{"period": 3, "home_score": 78, "away_score": 72, "win_probability_home": 0.62}'}),
        help_text="Objeto JSON con estado del partido. Campos: period, home_score, away_score, win_probability_home (opt.).",
    )


class DiscoveryForm(forms.Form):
    """Formulario para Prediction Discovery (jornada completa)."""
    matchday_json = forms.CharField(
        label="Jornada (JSON)",
        widget=forms.Textarea(attrs={"rows": 8, "placeholder": '[{"home_team_id": "LAL", "away_team_id": "GSW", "date": "2026-01-15", "odds_home": 1.9, "odds_away": 2.1}]'}),
        help_text="Array JSON con encuentros. Campos: home_team_id, away_team_id, date (opt.), odds_home (opt.), odds_away (opt.).",
    )
    market = forms.ChoiceField(label="Mercado", choices=BINARY_MARKETS)
    n_top = forms.ChoiceField(label="Top N resultados", choices=N_TOP, initial="10")
    risk_level = forms.ChoiceField(label="Nivel de riesgo", choices=RISK_CHOICES)


class CombinedBetForm(forms.Form):
    """Formulario apuesta combinada (acumulador)."""
    matches_json = forms.CharField(
        label="Encuentros (JSON)",
        widget=forms.Textarea(attrs={"rows": 8, "placeholder": '[{"home_team_id": "LAL", "away_team_id": "GSW"}, {"home_team_id": "BOS", "away_team_id": "MIA"}]'}),
        help_text="Array JSON con encuentros para construir la combinada.",
    )
    market = forms.ChoiceField(label="Mercado", choices=BINARY_MARKETS)
    n_selections = forms.ChoiceField(label="Nº selecciones", choices=N_SELECTIONS, initial="3")
    risk_level = forms.ChoiceField(label="Nivel de riesgo", choices=RISK_CHOICES)
    stake_euros = forms.FloatField(label="Stake (€)", required=False)
    save_bet = forms.BooleanField(label="Guardar apuesta", required=False)
