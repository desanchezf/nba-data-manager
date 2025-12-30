# 🏀 NBA Data Manager - Contexto del Proyecto

## Descripción General

NBA Data Manager es un sistema completo de gestión, análisis y predicción de datos de la NBA construido con Django, Machine Learning y RAG (Retrieval-Augmented Generation). El sistema almacena datos históricos de la NBA y utiliza modelos de ML para realizar predicciones sobre encuentros futuros y partidos en curso, cubriendo una amplia gama de mercados de apuestas deportivas.

## Objetivo Principal

El proyecto tiene como objetivo:
- **Almacenar datos históricos** de la NBA de forma estructurada y eficiente
- **Entrenar modelos de Machine Learning** para realizar predicciones precisas
- **Generar predicciones prepartido** sobre encuentros futuros
- **Realizar predicciones en tiempo real** sobre partidos en curso
- **Almacenar modelos entrenados** para su reutilización y versionado
- **Responder preguntas sobre los datos** mediante un sistema RAG (Retrieval-Augmented Generation)
- **Cubrir múltiples mercados de apuestas** desde ganador del partido hasta estadísticas específicas de jugadores

## Arquitectura del Sistema

### Arquitectura ML + RAG

El sistema utiliza una **arquitectura híbrida** que combina modelos predictivos estadísticos con RAG y LLM:

```
Usuario
  ↓
LLM (interpreta la pregunta)
  ↓
Modelo estadístico (calcula probabilidades)
  ↓
RAG (recupera contexto histórico, datos, métricas)
  ↓
LLM (explica el resultado en lenguaje natural)
```

### Componentes Principales

1. **Modelo Predictivo (Core del Sistema)**
   - Modelos: Regresión Logística, Random Forest, XGBoost, Redes Neuronales, ELO/Glicko
   - Features: Puntos promedio, Pace, Offensive/Defensive rating, Home/Away, Back-to-back, Lesiones, Head-to-head, Estadísticas recientes, Momentum

2. **Sistema RAG (Capa de Contexto)**
   - NO predice, pero enriquece y explica las predicciones
   - Recupera información histórica relevante
   - Proporciona contexto estadístico

3. **LLM (Capa de Lenguaje Natural)**
   - Interpreta preguntas en lenguaje natural
   - Sintetiza predicciones + contexto
   - Genera respuestas comprensibles

## Stack Tecnológico

### Backend
- Django 5.2
- Django REST Framework 3.16.1
- PostgreSQL 16
- Redis 7.0.0
- Celery 5.5.3
- Django Unfold 0.68.0
- Django Prometheus 2.3.1
- Django Redis 5.4.0

### Machine Learning
- Scikit-learn
- XGBoost
- TensorFlow/PyTorch
- Pandas, NumPy
- Joblib/Pickle

### RAG y NLP
- LangChain
- Vector Databases (FAISS, Pinecone, etc.)
- OpenAI/Anthropic
- Sentence Transformers

### Infraestructura
- Docker & Docker Compose
- Prometheus
- Grafana
- Nginx

## Estructura del Proyecto

```
nba-data-manager/
├── dashboard/              # App del dashboard principal
├── data/                   # Modelos de datos NBA
├── roster/                 # Modelos de equipos y jugadores
├── project/                # Configuración principal
│   └── admin.py            # AdminSite personalizado
├── project_commands/        # Comandos de management
├── predictions/            # Modelos de predicciones
├── ia/                     # Modelos de IA
├── ml/                     # Módulo de Machine Learning
├── rag/                    # Sistema RAG
├── prometheus/             # Configuración Prometheus
├── grafana/               # Dashboards Grafana
└── prompt/                # Prompts y contexto
```

## Tipos de Datos Almacenados

El sistema almacena datos extraídos mediante scrappers de NBA.com, organizados en dos categorías principales:

### Datos de Partidos Individuales (GAME_HEADERS)

Archivos CSV con estadísticas detalladas de cada partido:
- `game_boxscore_traditional.csv`: Estadísticas tradicionales (FGM, FGA, PTS, REB, AST, etc.)
- `game_boxscore_advanced.csv`: Estadísticas avanzadas (OFFRTG, DEFRTG, NETRTG, PACE, PIE, etc.)
- `game_boxscore_misc.csv`: Estadísticas misceláneas (PTS_OFF_TO, FBPS, PITP, etc.)
- `game_boxscore_scoring.csv`: Análisis de anotación (porcentajes de puntos por tipo)
- `game_boxscore_usage.csv`: Estadísticas de uso del jugador
- `game_boxscore_four_factors.csv`: Four factors (EFG_PERC, FTA_RATE, TO_PERC, OREB_PERC)
- `game_boxscore_tracking.csv`: Estadísticas de tracking (SPD, DIST, TCHS, PASS, etc.)
- `game_boxscore_hustle.csv`: Estadísticas de esfuerzo (SCREEN_AST, DEFLECTIONS, BOX_OUTS, etc.)
- `game_boxscore_defense.csv`: Estadísticas defensivas (DFGM, DFGA, DFG_PERC, etc.)
- `game_play_by_play.csv`: Datos jugada por jugada
- `game_summary.csv`: Resumen del partido por equipo (Q1-Q4, OT, PITP, FB_PTS, etc.)

Cada archivo incluye headers comunes: `GAME_ID, SEASON, SEASON_TYPE, HOME_TEAM_ABB, AWAY_TEAM_ABB, PLAYER_ID, PLAYER_NAME, PLAYER_NAME_ABB, PLAYER_TEAM_ABB, PLAYER_POS, PLAYER_DNP, PERIOD, MIN` más estadísticas específicas.

### Datos Agregados por Temporada (STATS_HEADERS)

Archivos CSV con estadísticas agregadas de temporadas completas:
- **Lineups**: Traditional, Advanced, Misc, Four Factors, Scoring, Opponent
- **Teams**: General (Traditional, Advanced, Four Factors, Misc, Scoring, Opponent, Defense, Violations, Estimated Advanced), Clutch, Playtype, Tracking, Defense Dashboard, Shot Dashboard, Box Scores, Advanced Box Scores, Shooting, Opponent Shooting, Hustle, Box Outs
- **Players**: General, Clutch, Playtype, Tracking, Defense Dashboard, Shot Dashboard, Box Scores, Advanced Box Scores, Shooting, Dunk Scores, Opponent Shooting, Hustle, Box Outs, Bios

**Nota**: Los datos se extraen mediante scrappers de NBA.com y se almacenan en archivos CSV con headers específicos definidos en el sistema de scrapping.

## Mercados de Apuestas Soportados

El sistema genera predicciones para múltiples mercados:

### Mercados Principales
- **Ganador**: Ganador del encuentro
- **Hándicap**: Handicaps principales y alternativos
- **Total de Puntos**: Totales principales y alternativos
- **Apuestas Combinadas**: Línea/Total, Doble resultado, etc.

### Mercados por Períodos
- **Mitades**: Primera y segunda mitad (ganador, handicap, totales, márgenes)
- **Cuartos**: Cada cuarto individual (ganador, handicap, totales, márgenes, carreras)

### Mercados de Equipos
- **Totales por Equipo**: Puntos del equipo local/visitante, alternativos, par/impar

### Mercados de Jugadores
- **Puntos**: Anota X+ puntos, puntos específicos, alternativos
- **Asistencias**: Consigue X+ asistencias, asistencias específicas
- **Rebotes**: Registra X+ rebotes, rebotes específicos
- **Triples**: X+ triples anotados, triples específicos
- **Otras Estadísticas**: Tapones, robos
- **Combinaciones**: Puntos + asistencias, puntos + rebotes, triple combinación
- **Rendimiento por Cuarto**: Puntos por cuarto
- **Logros**: Doble doble, triple doble
- **Comparaciones**: Cara a cara, máximo anotador, dúos/tríos anotadores

### Mercados Especiales
- **Primera Canasta**: Primer equipo/jugador en anotar, método
- **Carreras de Puntos**: Primer equipo en alcanzar X puntos
- **Eventos Especiales**: Lidera de principio a fin, prórroga, mitad/cuarto con más puntos
- **Apuestas Especiales**: Combinaciones personalizadas
- **Ganar Todos los Cuartos/Mitades**: Equipo gana todos los cuartos/mitades

### Mercados Alternativos
- **Totales Alternativos**: Múltiples opciones de totales
- **Handicaps Alternativos**: Múltiples opciones de handicaps

## Tipos de Predicciones

### Predicciones Prepartido
- Analiza estadísticas históricas, rendimiento reciente, enfrentamientos previos, lesiones, factores contextuales

### Predicciones en Tiempo Real
- Considera puntuación actual, ritmo del partido, rendimiento en tiempo real, momentum, estadísticas del partido en curso

## Sistema RAG

### Funcionalidad
- **Consultas en Lenguaje Natural**: Preguntas sobre los datos almacenados
- **Búsqueda Semántica**: Encuentra información relevante en el histórico
- **Respuestas Contextualizadas**: Genera respuestas basadas en datos reales
- **Análisis Inteligente**: Interpreta tendencias y patrones

### Ejemplos de Consultas
- "¿Cuál es el promedio de puntos de LeBron James en partidos de playoffs?"
- "¿Qué equipo tiene mejor porcentaje de victorias como visitante esta temporada?"
- "¿Cuántos partidos han superado los 250 puntos esta temporada?"
- "¿Qué jugador tiene más triples anotados en los últimos 10 partidos?"

## Usuarios del Sistema

- **Superuser (admin)**: Acceso completo a todas las funcionalidades, incluyendo Celery
- **Manager (manager)**: Acceso completo a datos y predicciones, sin acceso a configuración de Celery

## Modelos de Datos Principales

### Predictions
- `PrePrediction`: Predicciones prepartido
- `LivePredictions`: Predicciones en tiempo real
- `PredictionsHistory`: Historial de predicciones

### IA
- `PredictionModel`: Modelos entrenados almacenados

### Data
- Modelos para box scores, shooting, defense, rebounding, passing, touches, clutch, hustle, speed & distance, play by play

### Roster
- `Teams`: Equipos de la NBA
- `Players`: Jugadores de la NBA

## Comandos de Management

- `initsetup`: Configuración inicial (crea admin y manager)
- `import_data`: Importar datos desde CSV
- `import`: Importar links desde directorio
- `train_model`: Entrenar modelo para un mercado específico
- `train_all_models`: Entrenar todos los modelos
- `predict`: Generar predicciones (prematch o realtime)

## API Endpoints

- `/api/teams/`: Estadísticas de equipos
- `/api/boxscores/`: Box scores
- `/api/predictions/prematch/{game_id}/`: Predicciones prepartido
- `/api/predictions/realtime/{game_id}/`: Predicciones en tiempo real
- `/api/models/`: Gestión de modelos
- `/api/rag/query`: Consultas RAG

## Monitoreo

- **Prometheus**: Recopilación de métricas (puerto 9090)
- **Grafana**: Visualización de métricas (puerto 3000)
- Métricas: Request rate, latencia, error rates, database performance, cache ratios, Celery tasks, ML performance, RAG queries

## Principios de Diseño

1. **Precisión**: Modelos estadísticos más precisos que LLMs puros para predicciones numéricas
2. **Explicabilidad**: RAG proporciona contexto histórico que justifica las predicciones
3. **Naturalidad**: LLM hace que las respuestas sean comprensibles
4. **Flexibilidad**: Responde tanto preguntas de predicción como consultas históricas
5. **Escalabilidad**: Modelos estadísticos más eficientes que LLMs para cálculos masivos

## Notas Importantes

- El RAG NO predice, solo enriquece y explica las predicciones
- Los modelos estadísticos son el core del sistema de predicción
- El LLM sintetiza predicciones + contexto en respuestas comprensibles
- El sistema cubre más de 100 tipos diferentes de mercados de apuestas
- Los modelos se almacenan con versionado y metadata
- El sistema soporta tanto predicciones prepartido como en tiempo real
