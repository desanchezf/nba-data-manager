"""
Vista índice para ejecutar los management commands de project_commands.
Solo accesible para staff (mismo criterio que el admin).
La salida del comando se duplica al stderr real para que aparezca en los logs del contenedor.
Soporte SSE para streaming en tiempo real.
"""

import contextlib
import io
import json as _json
import queue
import re
import sys
import threading

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


def _admin_ctx(request):
    """Contexto base del admin (sidebar, permisos, etc.) para vistas custom."""
    return admin.site.each_context(request)


class _TeeStream(io.TextIOBase):
    """Escribe en un StringIO y además en el stream real para logs del contenedor."""

    def __init__(self, buffer, real_stream):
        self._buffer = buffer
        self._real = real_stream

    def write(self, s):
        if s:
            self._buffer.write(s)
            try:
                self._real.write(s)
                self._real.flush()
            except (OSError, AttributeError):
                pass
        return len(s)

    def getvalue(self):
        return self._buffer.getvalue()


_TQDM_RE = re.compile(r"(\d+(?:\.\d+)?)%")


class _QueueStream(io.TextIOBase):
    """Duplica escrituras al stream real y pone líneas parseadas en una Queue para SSE.

    Líneas de tqdm (contienen '%|') se emiten como eventos 'progress'.
    El resto como eventos 'output'.
    """

    def __init__(self, real_stream, q):
        self._real = real_stream
        self._q = q
        self._buf = ""

    def write(self, s):
        if s:
            try:
                self._real.write(s)
                self._real.flush()
            except (OSError, AttributeError):
                pass
            self._buf += s
            self._flush_lines()
        return len(s)

    def flush(self):
        try:
            self._real.flush()
        except (OSError, AttributeError):
            pass

    def _flush_lines(self):
        while True:
            cr = self._buf.find("\r")
            nl = self._buf.find("\n")
            if cr == -1 and nl == -1:
                break
            if nl == -1 or (cr != -1 and cr < nl):
                idx = cr
            else:
                idx = nl
            line = self._buf[:idx]
            self._buf = self._buf[idx + 1:]
            if line.strip():
                self._emit(line)

    def _emit(self, line):
        stripped = line.strip()
        if "%|" in stripped:
            m = _TQDM_RE.search(stripped)
            if m:
                pct = float(m.group(1))
                desc_m = re.match(r"^([^:]+):", stripped)
                desc = desc_m.group(1).strip() if desc_m else ""
                self._q.put({"type": "progress", "pct": pct, "desc": desc})
                return
        self._q.put({"type": "output", "text": stripped})


def _build_args_list(command_name, request_post):
    """Construye la lista de argumentos para call_command desde el POST."""
    args_list = []
    for group in COMMAND_GROUPS:
        for cmd in group["commands"]:
            if cmd["name"] != command_name:
                continue
            for arg_spec in cmd["args"]:
                arg_name = arg_spec[0]
                arg_type = arg_spec[1]
                if arg_type == "checkbox":
                    if request_post.get(arg_name) in ("on", "1", "true"):
                        args_list.append(arg_name)
                else:
                    val = request_post.get(arg_name, "").strip()
                    if val:
                        args_list.extend([arg_name, val])
            break
    return args_list


# ---------------------------------------------------------------------------
# Opciones de choices para los formularios de comandos
# ---------------------------------------------------------------------------

SEASONS = [("", "(todas)")] + [(str(y), str(y)) for y in range(2015, 2027)]
SEASON_TYPES = [
    ("", "(todas)"),
    ("Regular Season", "Regular Season"),
    ("Playoffs", "Playoffs"),
]
MARKETS_FEATURES = [
    ("base", "Base"),
    ("moneyline", "Money Line"),
    ("spread", "Spread / Hándicap"),
    ("totals", "Totales (O/U)"),
    ("player_props", "Props de Jugador"),
    ("quarter_ml", "Moneyline por Cuarto"),
    ("quarter_totals", "Totales por Cuarto"),
    ("half_ml", "Moneyline 1.ª Parte"),
    ("half_totals", "Totales 1.ª Parte"),
    ("race_to_points", "Carrera a N Puntos"),
    ("both_teams_over", "Ambos Equipos >N"),
    ("winning_margin", "Margen de Victoria"),
    ("in_game", "In Game"),
]
MARKETS_ML = [
    ("moneyline", "Money Line"),
    ("spread", "Spread / Hándicap"),
    ("totals", "Totales (O/U)"),
    ("quarter_ml", "Moneyline por Cuarto"),
    ("quarter_totals", "Totales por Cuarto"),
    ("half_ml", "Moneyline 1.ª Parte"),
    ("half_totals", "Totales 1.ª Parte"),
    ("race_to_points", "Carrera a N Puntos"),
    ("both_teams_over", "Ambos Equipos >N"),
    ("winning_margin", "Margen de Victoria"),
    ("player_props", "Props de Jugador"),
]
LIMITS = [
    ("", "(default)"),
    ("50", "50"),
    ("100", "100"),
    ("500", "500"),
    ("1000", "1000"),
    ("2000", "2000"),
]
BATCH_SIZES = [
    ("", "(default)"),
    ("1000", "1000"),
    ("2000", "2000"),
    ("5000", "5000"),
]
DAYS_OPTIONS = [
    ("", "(default)"),
    ("7", "7"),
    ("14", "14"),
    ("30", "30"),
    ("60", "60"),
]
ALERT_THRESHOLDS = [
    ("", "(default)"),
    ("0.50", "0.50"),
    ("0.55", "0.55"),
    ("0.60", "0.60"),
]
# ---------------------------------------------------------------------------
# Definición de grupos de comandos y sus argumentos
# ---------------------------------------------------------------------------

COMMAND_GROUPS = [
    {
        "title": "Full Pipeline",
        "commands": [
            {
                "name": "full_pipeline",
                "display_name": "Full Pipeline NBA",
                "help": (
                    "ETL → sync_normalized → compute_features → train_models. "
                    "Cubre Regular Season + Playoffs para todos los mercados."
                ),
                "help_detail": [
                    "Paso 1 — import_data: importa los datos a modelos crudos.",
                    "Paso 2 — sync_normalized: normaliza los datos al modelo core.",
                    "Paso 3 — compute_features: features para todos los mercados × 2 tipos de temporada.",
                    "Paso 4 — train_models: entrena todos los mercados × 2 tipos de temporada.",
                ],
                "args": [],
            },
        ],
    },
    {
        "title": "ETL y sincronización",
        "commands": [
            {
                "name": "import_data",
                "help": "Importa datos NBA → modelos crudos (boxscores, play-by-play, …)",
                "args": [
                    ("--clear", "checkbox", "Vaciar tablas antes"),
                    ("--batch-size", "choice", "Tamaño lote", BATCH_SIZES),
                ],
            },
            {
                "name": "sync_normalized",
                "help": "Sincroniza modelos crudos → core (normalizados)",
                "args": [
                    ("--clear", "checkbox", "Vaciar normalizados antes"),
                    ("--season", "choice", "Temporada", SEASONS),
                    ("--season-type", "choice", "Tipo temporada", SEASON_TYPES),
                    ("--batch", "choice", "Tamaño lote", BATCH_SIZES),
                ],
            },
        ],
    },
    {
        "title": "Features",
        "commands": [
            {
                "name": "compute_features",
                "help": "Calcula features por juego/mercado (rolling PTS/REB/AST, H2H, …)",
                "args": [
                    ("--season", "choice", "Temporada", SEASONS),
                    ("--market", "choice", "Mercado", MARKETS_FEATURES),
                    ("--game-id", "text", "Solo un juego (opcional)"),
                    ("--limit", "choice", "Límite juegos", LIMITS),
                    ("--to-redis", "checkbox", "Escribir también en Redis"),
                ],
            },
        ],
    },
    {
        "title": "ML y predicción",
        "commands": [
            {
                "name": "train_models",
                "help": "Entrena modelos XGBoost/Poisson por mercado",
                "help_detail": [
                    "Clasificadores (XGBoost): moneyline, spread, quarter_ml, half_ml, both_teams_over.",
                    "Regresores Poisson: totals, quarter_totals, half_totals, race_to_points.",
                    "Regresor XGBoost: winning_margin, player_props.",
                    "El target se determina automáticamente según el mercado elegido.",
                ],
                "args": [
                    ("--season-type", "choice", "Tipo temporada", SEASON_TYPES),
                    ("--market", "choice", "Mercado", MARKETS_ML),
                    ("--model-dir", "text", "Carpeta modelos (opcional)"),
                ],
            },
            {
                "name": "batch_predict_futures",
                "help": "Predicciones futuros (log en PredictionLog)",
                "args": [
                    ("--season", "choice", "Temporada", SEASONS),
                    ("--market", "choice", "Mercado", MARKETS_ML),
                    ("--limit", "choice", "Límite", LIMITS),
                ],
            },
            {
                "name": "compute_metrics",
                "help": "Métricas: accuracy, log-loss, ROI simulado",
                "args": [
                    ("--market", "choice", "Mercado", MARKETS_ML),
                    ("--days", "choice", "Días atrás", DAYS_OPTIONS),
                    ("--alert-threshold", "choice", "Umbral", ALERT_THRESHOLDS),
                ],
            },
            {
                "name": "run_backtesting",
                "help": "Backtesting walk-forward: Sharpe, max drawdown y ROI por temporada",
                "help_detail": [
                    "Evalúa el modelo en cada temporada usando datos históricos anteriores.",
                    "Calcula accuracy, log-loss y ROI simulado por año.",
                    "Métricas globales: Sharpe ratio y max drawdown.",
                    "Con --retrain re-entrena el modelo antes de cada fold.",
                ],
                "args": [
                    ("--market", "choice", "Mercado", MARKETS_ML),
                    ("--season-type", "choice", "Tipo temporada", SEASON_TYPES),
                    ("--start-year", "text", "Año inicio eval."),
                    ("--end-year", "text", "Año fin eval."),
                    ("--retrain", "checkbox", "Re-entrenar por fold"),
                ],
            },
        ],
    },
    {
        "title": "Setup",
        "commands": [
            {
                "name": "initsetup",
                "help": "Configuración inicial del proyecto",
                "help_detail": [
                    "Paso 1: crear el superusuario «admin» si no existe.",
                    "Paso 2: registrar o actualizar Ollama «Local Ollama» (OLLAMA_BASE_URL).",
                    "Paso 3: definir los modelos por defecto del chat en ese servidor.",
                    "Paso 4: crear el prompt de sistema NBA si no hay ninguno activo.",
                ],
                "args": [],
            },
        ],
    },
    {
        "title": "IA / LLM",
        "commands": [
            {
                "name": "pull_ollama_models",
                "help": "Descarga en Ollama los modelos por defecto configurados",
                "args": [
                    ("--skip-wait", "checkbox", "Omitir espera al servidor"),
                ],
            },
        ],
    },
]

# Máximo número de columnas de argumentos para alinear todos los comandos en grid
MAX_ARG_COLUMNS = 7

# Mercados para pronóstico por rivales
FORECAST_MARKETS = [
    {"slug": "moneyline", "label": "Pronóstico Moneyline"},
    {"slug": "spread", "label": "Pronóstico Spread"},
    {"slug": "totals", "label": "Pronóstico Totales (O/U)"},
    {"slug": "quarter_ml", "label": "Pronóstico Moneyline por Cuarto"},
    {"slug": "quarter_totals", "label": "Pronóstico Totales por Cuarto"},
    {"slug": "half_ml", "label": "Pronóstico Moneyline 1.ª Parte"},
    {"slug": "half_totals", "label": "Pronóstico Totales 1.ª Parte"},
    {"slug": "race_to_points", "label": "Pronóstico Carrera a N Puntos"},
    {"slug": "both_teams_over", "label": "Pronóstico Ambos >N"},
    {"slug": "winning_margin", "label": "Pronóstico Margen de Victoria"},
]

VISUALIZATION_SEASONS = [("", "(actual)")] + [
    (str(y), str(y)) for y in range(2026, 2014, -1)
]


# ---------------------------------------------------------------------------
# Helpers de datos para visualizaciones (NBA)
# ---------------------------------------------------------------------------

def _get_team_comparison_data(home_team_id, away_team_id, as_of_date=None):
    """
    Devuelve datos para gráficos comparativos: labels y valores home/away.
    Usa compute_features_for_matchup con métricas NBA (PTS, REB, AST).
    """
    from datetime import date

    from django.utils.dateparse import parse_date

    from features.engine.matchup import compute_features_for_matchup

    if as_of_date is None:
        as_of_date = date.today()
    if isinstance(as_of_date, str):
        as_of_date = parse_date(as_of_date) or date.today()

    feats = compute_features_for_matchup(
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        as_of_date=as_of_date,
        market="base",
    )
    if not feats:
        return {"labels": [], "home": [], "away": []}

    # (etiqueta español, key home, key away)
    metrics = [
        ("PTS prom. (5)", "team_home_pts_avg_5", "team_away_pts_avg_5"),
        ("PTS prom. (10)", "team_home_pts_avg_10", "team_away_pts_avg_10"),
        ("REB prom. (5)", "team_home_reb_avg_5", "team_away_reb_avg_5"),
        ("REB prom. (10)", "team_home_reb_avg_10", "team_away_reb_avg_10"),
        ("AST prom. (5)", "team_home_ast_avg_5", "team_away_ast_avg_5"),
        ("AST prom. (10)", "team_home_ast_avg_10", "team_away_ast_avg_10"),
        ("Win% (10)", "win_pct_home_10", "win_pct_away_10"),
        ("PTS concedidos (10)", "team_home_pts_allowed_avg_10", "team_away_pts_allowed_avg_10"),
    ]
    labels = []
    home_vals = []
    away_vals = []
    for label, hk, ak in metrics:
        h = feats.get(hk)
        a = feats.get(ak)
        if h is None and a is None:
            continue
        labels.append(label)
        home_vals.append(round(float(h or 0), 2))
        away_vals.append(round(float(a or 0), 2))
    return {"labels": labels, "home": home_vals, "away": away_vals}


def _get_single_team_data(team_id, as_of_date=None):
    """
    Devuelve datos estadísticos de un solo equipo para visualización NBA.
    """
    from datetime import date

    from django.utils.dateparse import parse_date

    from features.engine.matchup import compute_features_for_matchup

    if as_of_date is None:
        as_of_date = date.today()
    if isinstance(as_of_date, str):
        as_of_date = parse_date(as_of_date) or date.today()

    feats = compute_features_for_matchup(
        home_team_id=team_id,
        away_team_id=team_id,
        as_of_date=as_of_date,
        market="base",
    )
    if not feats:
        return {"labels": [], "values": []}

    metrics = [
        ("PTS prom. (5)", "team_home_pts_avg_5"),
        ("PTS prom. (10)", "team_home_pts_avg_10"),
        ("REB prom. (5)", "team_home_reb_avg_5"),
        ("REB prom. (10)", "team_home_reb_avg_10"),
        ("AST prom. (5)", "team_home_ast_avg_5"),
        ("AST prom. (10)", "team_home_ast_avg_10"),
        ("Win% (10)", "win_pct_home_10"),
        ("PTS concedidos (10)", "team_home_pts_allowed_avg_10"),
    ]
    labels = []
    values = []
    for label, key in metrics:
        v = feats.get(key)
        if v is None:
            continue
        labels.append(label)
        values.append(round(float(v or 0), 2))
    return {"labels": labels, "values": values}


def _get_global_stats(as_of_date=None):
    """
    Devuelve, para cada métrica NBA, el equipo que más destaca (valor máximo).
    """
    from datetime import date

    from django.utils.dateparse import parse_date

    from core.models import Team
    from features.engine.matchup import compute_features_for_matchup

    if as_of_date is None:
        as_of_date = date.today()
    if isinstance(as_of_date, str):
        as_of_date = parse_date(as_of_date) or date.today()

    metrics = [
        ("PTS prom. (5)", "team_home_pts_avg_5"),
        ("PTS prom. (10)", "team_home_pts_avg_10"),
        ("REB prom. (10)", "team_home_reb_avg_10"),
        ("AST prom. (10)", "team_home_ast_avg_10"),
        ("Win% (10)", "win_pct_home_10"),
        ("FG% prom. (10)", "team_home_fg_pct_avg_10"),
        ("3P% prom. (10)", "team_home_fg3_pct_avg_10"),
        ("PTS concedidos (10)", "team_home_pts_allowed_avg_10"),
    ]

    best = {
        key: {"team": None, "value": None, "label": label} for label, key in metrics
    }
    teams = Team.objects.all()
    for t in teams:
        feats = compute_features_for_matchup(
            home_team_id=t.team_id,
            away_team_id=t.team_id,
            as_of_date=as_of_date,
            market="base",
        )
        if not feats:
            continue
        for label, key in metrics:
            v = feats.get(key)
            if v is None:
                continue
            v = float(v or 0)
            cur = best[key]["value"]
            if cur is None or v > cur:
                best[key]["value"] = v
                best[key]["team"] = getattr(t, "name", None) or t.team_id

    labels = []
    values = []
    teams_out = []
    for label, key in metrics:
        info = best[key]
        if info["team"] is None:
            continue
        labels.append(label)
        values.append(round(info["value"], 2))
        teams_out.append(info["team"])
    return {"metrics": labels, "values": values, "teams": teams_out}


def _run_command(command_name, request_post):
    """Ejecuta el comando y devuelve (success, output). Duplica stdout/stderr a los streams reales."""
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    out_tee = _TeeStream(out_buf, sys.stdout)
    err_tee = _TeeStream(err_buf, sys.stderr)
    try:
        args_list = _build_args_list(command_name, request_post)
        call_command(command_name, *args_list, stdout=out_tee, stderr=err_tee)
        return True, out_tee.getvalue() + (err_tee.getvalue() or "")
    except Exception as e:
        return False, str(e) + "\n" + (err_tee.getvalue() or "")


# ---------------------------------------------------------------------------
# Vistas
# ---------------------------------------------------------------------------

@staff_member_required
@require_http_methods(["POST"])
@csrf_protect
def tools_run_stream(request):
    """SSE endpoint: ejecuta un comando en un hilo y emite eventos en tiempo real.

    Eventos emitidos (formato SSE, text/event-stream):
      {type: 'progress', pct: 45.0, desc: 'Sync'}  — progreso real de tqdm
      {type: 'output',   text: 'Línea de salida'}   — salida normal del comando
      {type: 'done',     success: bool, output: str} — fin de ejecución
    """
    command_name = request.POST.get("command", "").strip()

    def _err_stream(msg):
        yield f"data: {_json.dumps({'type': 'done', 'success': False, 'output': msg})}\n\n"

    if not command_name:
        return StreamingHttpResponse(
            _err_stream("No command specified."), content_type="text/event-stream"
        )

    args_list = _build_args_list(command_name, request.POST)
    q = queue.Queue()

    def _run():
        out_stream = _QueueStream(sys.stdout, q)
        err_stream = _QueueStream(sys.stderr, q)
        try:
            with (
                contextlib.redirect_stdout(out_stream),
                contextlib.redirect_stderr(err_stream),
            ):
                call_command(
                    command_name, *args_list, stdout=out_stream, stderr=err_stream
                )
            q.put({"type": "done", "success": True})
        except Exception as exc:
            q.put({"type": "done", "success": False, "error": str(exc)})

    threading.Thread(target=_run, daemon=True).start()

    def _event_stream():
        output_parts = []
        while True:
            try:
                event = q.get(timeout=300)
            except queue.Empty:
                yield 'data: {"type":"ping"}\n\n'
                continue
            if event["type"] == "output":
                output_parts.append(event["text"])
                yield f"data: {_json.dumps(event)}\n\n"
            elif event["type"] == "progress":
                yield f"data: {_json.dumps(event)}\n\n"
            elif event["type"] == "done":
                event["output"] = "\n".join(output_parts)
                if "error" in event and event["error"]:
                    event["output"] = event["error"] + (
                        "\n" + event["output"] if event["output"] else ""
                    )
                yield f"data: {_json.dumps(event)}\n\n"
                break

    response = StreamingHttpResponse(_event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


def _is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


@staff_member_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def tools_index(request):
    """Lista los comandos y ejecuta el que se envíe por POST (Herramientas / Tools)."""
    result = None
    if request.method == "POST":
        command_name = request.POST.get("command")
        if command_name:
            success, output = _run_command(command_name, request.POST)
            result = {
                "command": command_name,
                "success": success,
                "output": output,
            }
            if _is_ajax(request):
                return JsonResponse(result)
            config_list = []
            for k in sorted(request.POST.keys()):
                if k in ("csrfmiddlewaretoken", "command"):
                    continue
                v = request.POST.get(k, "")
                if v in ("on", "1", "true"):
                    v = "Sí"
                elif v in ("", "0", "false") and k.startswith("--"):
                    v = "No"
                config_list.append((k, v))
            result["config"] = config_list

    def snake_to_title(s):
        if not s:
            return s
        t = str(s).replace("_", " ")
        return t[:1].upper() + t[1:].lower()

    # Rellenar argumentos hasta MAX_ARG_COLUMNS para grid alineado
    groups_for_template = []
    for group in COMMAND_GROUPS:
        commands_padded = []
        for cmd in group["commands"]:
            args = list(cmd["args"])
            padded = args + [None] * max(0, MAX_ARG_COLUMNS - len(args))
            commands_padded.append(
                {
                    **cmd,
                    "args_padded": padded,
                    "display_name": cmd.get("display_name")
                    or snake_to_title(cmd.get("name", "")),
                }
            )
        groups_for_template.append({**group, "commands": commands_padded})

    try:
        from core.models import Team
        teams = list(Team.objects.order_by("name").values("team_id", "name"))
    except Exception:
        teams = []

    return render(
        request,
        "tools/index.html",
        {
            **_admin_ctx(request),
            "title": "Herramientas",
            "command_groups": groups_for_template,
            "result": result,
            "max_arg_columns": MAX_ARG_COLUMNS,
            "teams": teams,
        },
    )


@staff_member_required
@require_http_methods(["GET"])
def ml_forecast_index(request):
    """Página ML: Pronóstico por mercado (equipos local/visitante)."""
    try:
        from core.models import Team
        teams = list(Team.objects.order_by("name").values("team_id", "name"))
    except Exception:
        teams = []
    return render(
        request,
        "ml/index.html",
        {
            **_admin_ctx(request),
            "title": "ML",
            "forecast_markets": FORECAST_MARKETS,
            "teams": teams,
        },
    )


@staff_member_required
@require_http_methods(["GET"])
def ia_index(request):
    """Página IA: conversación con el LLM (chat) y almacenamiento en sesión."""
    from ia.models import ChatSession, OllamaModelConfig

    models_list = []
    try:
        for cfg in (
            OllamaModelConfig.objects.select_related("server")
            .filter(
                server__enabled=True,
                deprecated=False,
                deprecated_at__isnull=True,
            )
            .order_by("-is_default", "alias")
        ):
            models_list.append(
                {
                    "value": f"{cfg.server.name}|{cfg.model_name}",
                    "label": f"{cfg.alias} ({cfg.model_name})",
                }
            )
    except Exception:
        pass

    session_id = None
    messages_json = "[]"
    try:
        import json

        last_session = (
            ChatSession.objects.filter(user=request.user)
            .order_by("-updated_at")
            .first()
        )
        if last_session:
            session_id = last_session.pk
            messages = list(
                last_session.messages.values("role", "content").order_by("created_at")
            )
            messages_json = json.dumps(messages)
    except Exception:
        pass

    return render(
        request,
        "ia/index.html",
        {
            **_admin_ctx(request),
            "title": "IA",
            "ollama_models": models_list,
            "session_id": session_id,
            "messages_json": messages_json,
        },
    )


@staff_member_required
@require_http_methods(["POST"])
@csrf_protect
def ia_ask(request):
    """Recibe una pregunta, guarda en sesión, llama al LLM y devuelve respuesta + session_id."""
    import requests as _requests

    from ia.models import ChatMessage, ChatSession, OllamaModelConfig, OllamaServer

    question = (request.POST.get("question") or "").strip()
    if not question:
        return JsonResponse({"error": "Escriba una pregunta."}, status=400)
    model_key = (request.POST.get("model") or "").strip()
    session_id_param = request.POST.get("session_id", "").strip()
    session = None
    if session_id_param and session_id_param.isdigit():
        try:
            session = ChatSession.objects.get(
                pk=int(session_id_param), user=request.user
            )
        except ChatSession.DoesNotExist:
            pass
    if not session:
        session = ChatSession.objects.create(
            user=request.user,
            model_key=model_key or "",
        )
    ChatMessage.objects.create(
        session=session, role=ChatMessage.ROLE_USER, content=question
    )

    server = None
    model_name = None
    if model_key and "|" in model_key:
        parts = model_key.split("|", 1)
        server_name, model_name = parts[0], parts[1]
        try:
            server = OllamaServer.objects.get(name=server_name, enabled=True)
        except OllamaServer.DoesNotExist:
            pass
    if not server:
        try:
            cfg = (
                OllamaModelConfig.objects.select_related("server")
                .filter(
                    server__enabled=True,
                    deprecated=False,
                    deprecated_at__isnull=True,
                    is_default=True,
                )
                .first()
            )
            if not cfg:
                cfg = (
                    OllamaModelConfig.objects.select_related("server")
                    .filter(
                        server__enabled=True,
                        deprecated=False,
                        deprecated_at__isnull=True,
                    )
                    .first()
                )
            if cfg:
                server = cfg.server
                model_name = cfg.model_name
        except Exception:
            pass

    if not server or not model_name:
        return JsonResponse(
            {"error": "No hay modelo Ollama configurado o habilitado."},
            status=503,
        )

    from ia.ollama_utils import resolve_ollama_base_url

    base_url = resolve_ollama_base_url(server.base_url)

    # Construir historial de la sesión para contexto
    history = list(session.messages.values("role", "content").order_by("created_at"))

    from ia.models import SystemPrompt

    system_prompt = SystemPrompt.get_active()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt.content})
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": question})

    url = f"{base_url}/api/chat"
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False,
    }
    try:
        resp = _requests.post(
            url,
            json=payload,
            timeout=120,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code >= 400:
            err_detail = resp.text[:800]
            try:
                body = resp.json()
                if isinstance(body, dict) and body.get("error"):
                    err_detail = str(body["error"])
            except Exception:
                pass
            hint = ""
            if resp.status_code == 404:
                hint = (
                    " Suele indicar que el modelo no está instalado en Ollama o el "
                    f"nombre no coincide (solicitado: «{model_name}»). "
                    "Ejecute pull del mismo nombre o ajuste IA → Configuraciones de modelo Ollama."
                )
            return JsonResponse(
                {
                    "error": f"Ollama HTTP {resp.status_code}: {err_detail}.{hint}",
                    "session_id": session.pk,
                },
                status=502,
            )
        data = resp.json()
        answer = ((data.get("message") or {}).get("content") or "").strip()
        ChatMessage.objects.create(
            session=session,
            role=ChatMessage.ROLE_ASSISTANT,
            content=answer,
        )
        return JsonResponse(
            {
                "answer": answer,
                "session_id": session.pk,
                "error": None,
            }
        )
    except _requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": f"No se pudo conectar con Ollama: {e!s}"},
            status=502,
        )


@staff_member_required
@require_http_methods(["GET"])
def visualization_index(request):
    """
    Visualización: datos estadísticos de un solo equipo NBA (gráficos por equipo).
    Si la petición es AJAX con team y season, devuelve JSON para el gráfico.
    """
    from datetime import date

    if _is_ajax(request):
        team = request.GET.get("team", "").strip()
        season = request.GET.get("season", "").strip()
        if not team:
            return JsonResponse({"error": "Seleccione un equipo"}, status=400)
        as_of_date = None
        if season and season.isdigit():
            as_of_date = date(int(season), 12, 31)
        data = _get_single_team_data(team, as_of_date=as_of_date)
        return JsonResponse(data)

    try:
        from core.models import Team
        teams = list(Team.objects.order_by("name").values("team_id", "name"))
    except Exception:
        teams = []

    return render(
        request,
        "visualization/index.html",
        {
            **_admin_ctx(request),
            "title": "Visualización",
            "teams": teams,
            "season_choices": VISUALIZATION_SEASONS,
        },
    )


@staff_member_required
@require_http_methods(["GET"])
def comparison_index(request):
    """
    Comparación: equipo local vs visitante (gráficos comparativos NBA).
    Si la petición es AJAX con home_team, away_team y season, devuelve JSON para el gráfico.
    """
    from datetime import date

    if _is_ajax(request):
        home = request.GET.get("home_team", "").strip()
        away = request.GET.get("away_team", "").strip()
        season = request.GET.get("season", "").strip()
        if not home or not away:
            return JsonResponse(
                {"error": "Faltan equipo local o visitante"}, status=400
            )
        as_of_date = None
        if season and season.isdigit():
            as_of_date = date(int(season), 12, 31)
        data = _get_team_comparison_data(home, away, as_of_date=as_of_date)
        return JsonResponse(data)

    try:
        from core.models import Team
        teams = list(Team.objects.order_by("name").values("team_id", "name"))
    except Exception:
        teams = []

    return render(
        request,
        "comparison/index.html",
        {
            **_admin_ctx(request),
            "title": "Comparación",
            "teams": teams,
            "season_choices": VISUALIZATION_SEASONS,
        },
    )


@staff_member_required
@require_http_methods(["GET"])
def global_index(request):
    """
    Global: para cada métrica NBA muestra el equipo que más destaca.
    Selector por temporada (choices); respuesta JSON para gráfico/tablas.
    """
    from datetime import date

    if _is_ajax(request):
        season = request.GET.get("season", "").strip()
        as_of_date = None
        if season and season.isdigit():
            as_of_date = date(int(season), 12, 31)
        data = _get_global_stats(as_of_date=as_of_date)
        return JsonResponse(data)

    return render(
        request,
        "global/index.html",
        {
            **_admin_ctx(request),
            "title": "Global",
            "season_choices": VISUALIZATION_SEASONS,
        },
    )
