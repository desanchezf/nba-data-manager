# 🏀 NBA Data Manager

Sistema completo de gestión, análisis y predicción de datos de la NBA construido con Django, Machine Learning y RAG (Retrieval-Augmented Generation). El sistema almacena datos históricos de la NBA y utiliza modelos de ML para realizar predicciones sobre encuentros futuros y partidos en curso, cubriendo una amplia gama de mercados de apuestas deportivas.

## TO-DO
- Descripción de los datos almacenados
- En base a la descripción determinar que datos son necesarios para cada algoritmo

## 📋 Tabla de Contenidos

### Parte Técnica
- [Visión General](#-visión-general)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Docker](#-docker)
- [Monitoreo](#-monitoreo)
- [API](#-api)
- [Comandos de Management](#-comandos-de-management)
- [Desarrollo](#-desarrollo)
- [Uso](#-uso)

### Parte de Dominio
- [Características y Datos](#-características-y-datos)
- [Predicciones con Machine Learning](#-predicciones-con-machine-learning)
- [Sistema RAG](#-sistema-rag)
- [Arquitectura ML + RAG](#-arquitectura-ml--rag)
- [Mercados de Apuestas](#-mercados-de-apuestas)

### Final
- [Contribución](#-contribución)
- [Roadmap](#-roadmap)
- [Troubleshooting](#-troubleshooting)
- [Licencia](#-licencia)

## 🎯 Visión General

NBA Data Manager es una plataforma integral diseñada para almacenar datos históricos de la NBA y utilizar modelos de Machine Learning para realizar predicciones sobre encuentros futuros y partidos en curso, cubriendo una amplia gama de mercados de apuestas deportivas.

## 📁 Estructura del Proyecto

```
nba-data-manager/
├── 📁 dashboard/              # App del dashboard principal
├── 📁 data/                   # Modelos de datos NBA
├── 📁 game/                   # Partidos: play-by-play, summary, boxscore traditional
├── 📁 game_boxscore/          # Box scores por partido (advanced, traditional)
├── 📁 lineups/                # Estadísticas por alineación (traditional, advanced, misc, etc.)
├── 📁 players/                # Estadísticas por jugador (general, clutch, playtype, tracking, etc.)
├── 📁 roster/                 # Modelos de equipos y jugadores
├── 📁 teams/                   # Estadísticas por equipo (general, clutch, tracking, etc.)
├── 📁 project/                # Configuración principal
│   └── 📁 admin.py            # AdminSite personalizado
├── 📁 project_commands/        # Comandos de management
│   └── 📁 management/commands/
│       ├── import.py          # Importar datos
│       ├── import_data.py     # Importar datos desde CSV
│       └── initsetup.py       # Configuración inicial (crea admin y manager)
├── 📁 ml/                     # Módulo de Machine Learning
│   ├── 📁 models/             # Modelos entrenados
│   ├── 📁 training/           # Scripts de entrenamiento
│   └── 📁 prediction/         # Scripts de predicción
├── 📁 rag/                    # Sistema RAG
│   ├── 📁 embeddings/         # Generación de embeddings
│   ├── 📁 retrieval/         # Sistema de recuperación
│   └── 📁 generation/         # Generación de respuestas
├── 📁 templates/              # Plantillas personalizadas
├── 📁 static/                # Archivos estáticos
├── 📁 prometheus/             # Configuración Prometheus
├── 📁 grafana/               # Dashboards Grafana
├── 📄 docker-compose.yml      # Configuración Docker
├── 📄 Dockerfile             # Imagen Docker
└── 📄 requirements.txt       # Dependencias Python
```

### Descripción de Directorios

- **`dashboard/`**: Aplicación principal del dashboard con vistas y templates
- **`data/`**: Modelos Django para almacenar estadísticas de partidos (box scores, shooting, defense, etc.)
- **`game/`**: Modelos de partidos (play-by-play, summary por equipo, boxscore traditional por jugador)
- **`game_boxscore/`**: Box scores por partido (traditional, advanced)
- **`lineups/`**: Estadísticas por alineación (traditional, advanced, four factors, misc, scoring, opponent)
- **`players/`**: Estadísticas por jugador (general, clutch, playtype, tracking, defense dashboard, shot dashboard, etc.)
- **`roster/`**: Modelos para equipos y jugadores de la NBA
- **`teams/`**: Estadísticas por equipo (general, clutch, tracking, defense dashboard, opponent shots, etc.)
- **`project/`**: Configuración principal de Django (settings, urls, admin personalizado)
- **`project_commands/`**: Comandos de management personalizados para importación y setup
- **`ml/`**: Módulo de Machine Learning con modelos entrenados, scripts de entrenamiento y predicción
- **`rag/`**: Sistema RAG con generación de embeddings, recuperación de información y generación de respuestas
- **`prometheus/`**: Configuración de Prometheus para métricas
- **`grafana/`**: Dashboards y configuración de Grafana

## 🛠 Tecnologías

### Backend
- **Django 5.2** - Framework web principal
- **Django REST Framework 3.16.1** - API REST
- **PostgreSQL 16** - Base de datos principal
- **Redis 7.0.0** - Cache y broker de mensajes
- **Celery 5.5.3** - Tareas asíncronas
- **Django Unfold 0.68.0** - Tema moderno para admin
- **Django Prometheus 2.3.1** - Métricas y monitoreo
- **Django Redis 5.4.0** - Cache backend

### Machine Learning
- **Scikit-learn** - Modelos de ML tradicionales
- **XGBoost** - Modelos de boosting
- **TensorFlow/PyTorch** - Deep Learning (según implementación)
- **Pandas** - Procesamiento de datos
- **NumPy** - Cálculos numéricos
- **Joblib/Pickle** - Serialización de modelos

### RAG y NLP
- **LangChain** - Framework para aplicaciones LLM
- **Vector Databases** - Almacenamiento de embeddings (FAISS, Pinecone, etc.)
- **OpenAI/Anthropic** - Modelos de lenguaje (según implementación)
- **Sentence Transformers** - Generación de embeddings

### Infraestructura
- **Docker & Docker Compose** - Containerización
- **Prometheus** - Métricas y monitoreo
- **Grafana** - Visualización de métricas
- **Nginx** - Servidor web (producción)
- **Redis** - Cache y cola de tareas

## 🚀 Instalación

### Prerrequisitos
- Python 3.9+
- Docker & Docker Compose
- Git

### Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd nba-data-manager
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Construir y ejecutar**
```bash
docker-compose up --build
```

4. **Configuración inicial**
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py initsetup
```

El comando `initsetup` crea:
- **Superuser**: `admin` / `admin` (acceso completo)
- **Manager**: `manager` / `manager123` (acceso completo excepto Celery)

### Instalación Local

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**
```bash
# Instalar PostgreSQL y Redis
# Configurar en settings.py
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
python manage.py initsetup
```

## ⚙️ Configuración

### Variables de Entorno

```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/nba_data
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# ML Configuration
ML_MODELS_PATH=/path/to/models
ML_CACHE_ENABLED=True

# RAG Configuration
RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_VECTOR_DB_PATH=/path/to/vector_db
OPENAI_API_KEY=your-openai-key  # Si usas OpenAI
```

### Configuración de Unfold

El proyecto incluye configuración personalizada de Unfold con:
- Tema NBA personalizado
- Colores azules vibrantes
- Iconos y branding personalizado
- Dashboard optimizado para datos deportivos

### Usuarios del Sistema

- **Superuser (admin)**: Acceso completo a todas las funcionalidades, incluyendo Celery
- **Manager (manager)**: Acceso completo a datos y predicciones, sin acceso a configuración de Celery

## 🐳 Docker

### Servicios Incluidos

- **backend**: Aplicación Django
- **postgres**: Base de datos PostgreSQL
- **redis**: Cache y broker Redis
- **celery**: Worker de tareas asíncronas
- **celery-beat**: Scheduler de tareas
- **prometheus**: Métricas y monitoreo
- **grafana**: Visualización de métricas

### Comandos Docker Útiles

```bash
# Ver logs
docker-compose logs -f backend

# Ejecutar comando en contenedor
docker-compose exec backend python manage.py shell

# Reiniciar servicios
docker-compose restart backend

# Backup de base de datos
docker-compose exec postgres pg_dump -U postgres postgres > backup.sql
```

## 📊 Monitoreo

### Prometheus y Grafana

El sistema incluye monitoreo completo con:
- **Prometheus**: Recopilación de métricas
- **Grafana**: Dashboards de visualización

**Acceso:**
- Grafana: `http://localhost:3000` (admin/admin)
- Prometheus: `http://localhost:9090`

### Métricas Disponibles
- Request rate y latencia
- Error rates
- Database query performance
- Cache hit ratios
- Celery task metrics
- ML model performance
- RAG query metrics

## 🔌 API

### Endpoints Principales

```bash
# Estadísticas de equipos
GET /api/teams/
GET /api/teams/{team_id}/stats/

# Box Scores
GET /api/boxscores/
GET /api/boxscores/{game_id}/

# Predicciones
GET /api/predictions/prematch/{game_id}/
GET /api/predictions/realtime/{game_id}/
POST /api/predictions/batch/

# Modelos
GET /api/models/
GET /api/models/{model_id}/
POST /api/models/train/

# RAG
POST /api/rag/query
GET /api/rag/history/

# Filtros disponibles
?season=2024-25
?season_type=Regular+Season
?team=Lakers
?date_from=2024-01-01
?date_to=2024-12-31
```

### Autenticación
```bash
# Token de autenticación
POST /api/auth/token/
Authorization: Token your-token-here
```

## 🎮 Comandos de Management

### Comandos Disponibles

```bash
# Configuración inicial (crea admin y manager)
python manage.py initsetup

# Importar datos desde CSV
python manage.py import_data

# Importar links desde directorio
python manage.py import

# Entrenar modelos
python manage.py train_model --market=winner
python manage.py train_all_models

# Generar predicciones
python manage.py predict --game_id=12345 --type=prematch
```

## 🔧 Desarrollo

### Estructura de Datos

Cada modelo de datos incluye:
- **Metadatos**: Temporada, tipo de temporada, fecha
- **Estadísticas específicas**: Campos relevantes para cada tipo
- **Índices optimizados**: Para consultas rápidas
- **Validaciones**: Integridad de datos

### Agregar Nuevos Tipos de Datos

1. Crear modelo en `data/models.py`
2. Configurar admin en `data/admin.py`
3. Crear comandos de importación en `project_commands/management/commands/`

### Agregar Nuevos Modelos ML

1. Crear script de entrenamiento en `ml/training/`
2. Implementar lógica de predicción en `ml/prediction/`
3. Registrar modelo en el sistema de versionado

## 📖 Uso

### Acceso al Admin
- **URL**: `http://localhost:8000/admin/`
- **Superuser**: `admin` / `admin`
- **Manager**: `manager` / `manager123`

### Dashboard Principal
- **URL**: `http://localhost:8000/dashboard/`
- Vista general de estadísticas y métricas

### Importar Datos

```bash
# Importar datos desde CSV
python manage.py import_data

# Importar links desde directorio
python manage.py import
```

**Importación desde CSV en el Admin**: Cada modelo de las apps **Game**, **Game Boxscore**, **Lineups**, **Players** y **Teams** dispone en el admin de Django de un botón *Importar CSV* que permite subir los archivos desde `csv/`. La importación normaliza las cabeceras del CSV a minúsculas (p. ej. `SEASON` → `season`), aplica mapeos de columnas cuando el CSV usa nombres distintos (p. ej. `MATCH_UP` → `matchup`) y, en modelos con `unique_together`, actualiza registros existentes en lugar de duplicarlos al reimportar.

### Entrenar Modelos

```bash
# Entrenar modelo para un mercado específico
python manage.py train_model --market=winner --season=2024-25

# Entrenar todos los modelos
python manage.py train_all_models
```

### Generar Predicciones

```bash
# Predicción prepartido
python manage.py predict --game_id=12345 --type=prematch

# Predicción en tiempo real
python manage.py predict --game_id=12345 --type=realtime
```

### Consultas RAG

```bash
# Consulta mediante API
POST /api/rag/query
{
  "question": "¿Cuál es el promedio de puntos de LeBron James?"
}
```

---

## ✨ Características y Datos

### 🎯 Funcionalidades Principales
- **Dashboard Interactivo**: Panel de administración moderno con tema Unfold
- **API REST**: Endpoints para integración con aplicaciones externas
- **Gestión de Datos**: Almacenamiento y organización de múltiples tipos de estadísticas
- **Machine Learning**: Modelos entrenados para predicciones de múltiples mercados
- **Predicciones en Tiempo Real**: Análisis y predicciones durante partidos en curso
- **Sistema RAG**: Preguntas y respuestas inteligentes sobre los datos almacenados
- **Tareas Asíncronas**: Procesamiento en background con Celery
- **Monitoreo**: Sistema de logs, métricas y seguimiento con Prometheus y Grafana

### 📊 Tipos de Datos Soportados

El sistema almacena datos extraídos mediante scrappers de NBA.com, organizados en dos categorías principales:

#### Datos de Partidos Individuales (GAME_HEADERS)

Estos archivos CSV contienen estadísticas detalladas de cada partido:

- **`game_boxscore_traditional.csv`**: Estadísticas tradicionales por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `FGM`: Field Goals Made (tiros de campo anotados)
  - `FGA`: Field Goals Attempted (tiros de campo intentados)
  - `FG_PERC`: Porcentaje de tiros de campo
  - `3PM`: Three Pointers Made (triples anotados)
  - `3PA`: Three Pointers Attempted (triples intentados)
  - `3P_PERC`: Porcentaje de triples
  - `FTM`: Free Throws Made (tiros libres anotados)
  - `FTA`: Free Throws Attempted (tiros libres intentados)
  - `FT_PERC`: Porcentaje de tiros libres
  - `OREB`: Offensive Rebounds (rebotes ofensivos)
  - `DREB`: Defensive Rebounds (rebotes defensivos)
  - `REB`: Total Rebounds (rebotes totales)
  - `AST`: Assists (asistencias)
  - `STL`: Steals (robos)
  - `BLK`: Blocks (tapones)
  - `TO`: Turnovers (pérdidas)
  - `PF`: Personal Fouls (faltas personales)
  - `PTS`: Points (puntos)
  - `PLUS_MINUS`: Diferencia de puntos cuando el jugador está en cancha

- **`game_boxscore_advanced.csv`**: Estadísticas avanzadas por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `OFFRTG`: Offensive Rating (puntos por 100 posesiones ofensivas)
  - `DEFRTG`: Defensive Rating (puntos permitidos por 100 posesiones defensivas)
  - `NETRTG`: Net Rating (diferencia entre offensive y defensive rating)
  - `AST_PERC`: Porcentaje de asistencias
  - `AST_TO`: Ratio de asistencias por pérdidas
  - `AST_RATIO`: Ratio de asistencias
  - `OREB_PERC`: Porcentaje de rebotes ofensivos
  - `DREB_PERC`: Porcentaje de rebotes defensivos
  - `REB_PERC`: Porcentaje de rebotes totales
  - `TO_RATIO`: Ratio de pérdidas
  - `EFG_PERC`: Effective Field Goal Percentage (porcentaje efectivo de tiros)
  - `TS_PERC`: True Shooting Percentage (porcentaje real de tiro)
  - `USG_PERC`: Usage Percentage (porcentaje de uso del jugador)
  - `PACE`: Posesiones por 48 minutos
  - `PIE`: Player Impact Estimate (estimación del impacto del jugador)

- **`game_boxscore_misc.csv`**: Estadísticas misceláneas por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `PTS_OFF_TO`: Puntos anotados tras pérdidas del equipo
  - `ND_PTS`: Puntos en segunda oportunidad
  - `FBPS`: Fast Break Points (puntos en contraataque)
  - `PITP`: Points in the Paint (puntos en la pintura)
  - `OPP_PTS_OFF_TO`: Puntos del oponente tras pérdidas
  - `OPP_ND_PTS`: Puntos del oponente en segunda oportunidad
  - `OPP_FBPS`: Fast Break Points del oponente
  - `OPP_PITP`: Points in the Paint del oponente
  - `BLK`: Blocks (tapones)
  - `BLKA`: Blocked Attempts (intentos bloqueados)
  - `PF`: Personal Fouls (faltas personales)
  - `FD`: Fouls Drawn (faltas recibidas)

- **`game_boxscore_scoring.csv`**: Análisis de anotación por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `PERC_FGA_2PT`: Porcentaje de intentos de tiro de 2 puntos
  - `PERC_FGA_3PT`: Porcentaje de intentos de tiro de 3 puntos
  - `PERC_PTS_2PT`: Porcentaje de puntos de 2 puntos
  - `PERC_PTS_2PT_MR`: Porcentaje de puntos de 2 puntos desde media distancia
  - `PERC_PTS_3PT`: Porcentaje de puntos de 3 puntos
  - `PERC_PTS_FBPS`: Porcentaje de puntos en contraataque
  - `PERC_PTS_FT`: Porcentaje de puntos desde la línea de tiros libres
  - `PERC_PTS_OFFTO`: Porcentaje de puntos tras pérdidas
  - `PERC_PTS_PITP`: Porcentaje de puntos en la pintura
  - `FGM2_PERC_AST`: Porcentaje de tiros de 2 puntos anotados con asistencia
  - `FGM2_PERC_UAST`: Porcentaje de tiros de 2 puntos anotados sin asistencia
  - `FGM3_PERC_AST`: Porcentaje de triples anotados con asistencia
  - `FGM3_PERC_UAST`: Porcentaje de triples anotados sin asistencia
  - `FGM_PERC_AST`: Porcentaje de tiros anotados con asistencia
  - `FGM_PERC_UAST`: Porcentaje de tiros anotados sin asistencia

- **`game_boxscore_usage.csv`**: Estadísticas de uso por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `USG_PERC`: Usage Percentage (porcentaje de uso del jugador)
  - `PERC_FGM`: Porcentaje de tiros anotados del equipo
  - `PERC_FGA`: Porcentaje de intentos de tiro del equipo
  - `PERC_3PM`: Porcentaje de triples anotados del equipo
  - `PERC_3PA`: Porcentaje de intentos de triple del equipo
  - `PERC_FTM`: Porcentaje de tiros libres anotados del equipo
  - `PERC_FTA`: Porcentaje de intentos de tiro libre del equipo
  - `PERC_OREB`: Porcentaje de rebotes ofensivos del equipo
  - `PERC_DREB`: Porcentaje de rebotes defensivos del equipo
  - `PERC_REB`: Porcentaje de rebotes totales del equipo
  - `PERC_AST`: Porcentaje de asistencias del equipo
  - `PERC_TO`: Porcentaje de pérdidas del equipo
  - `PERC_STL`: Porcentaje de robos del equipo
  - `PERC_BLK`: Porcentaje de tapones del equipo
  - `PERC_BLKA`: Porcentaje de intentos bloqueados del equipo
  - `PERC_PF`: Porcentaje de faltas personales del equipo
  - `PERC_PFD`: Porcentaje de faltas recibidas del equipo
  - `PERC_PTS`: Porcentaje de puntos del equipo

- **`game_boxscore_four_factors.csv`**: Four factors por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `EFG_PERC`: Effective Field Goal Percentage (porcentaje efectivo de tiros)
  - `FTA_RATE`: Free Throw Attempt Rate (tasa de intentos de tiros libres)
  - `TM_TO_PERC`: Team Turnover Percentage (porcentaje de pérdidas del equipo)
  - `OREB_PERC`: Offensive Rebound Percentage (porcentaje de rebotes ofensivos)
  - `OPP_EFG_PERC`: Effective Field Goal Percentage del oponente
  - `OPP_FTA_RATE`: Free Throw Attempt Rate del oponente
  - `OPP_TO_PERC`: Team Turnover Percentage del oponente
  - `OPP_OREB_PERC`: Offensive Rebound Percentage del oponente

- **`game_boxscore_tracking.csv`**: Estadísticas de tracking por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `SPD`: Speed (velocidad promedio en millas por hora)
  - `DIST`: Distance (distancia recorrida en millas)
  - `ORBC`: Offensive Rebound Chances (oportunidades de rebote ofensivo)
  - `DRBC`: Defensive Rebound Chances (oportunidades de rebote defensivo)
  - `RBC`: Rebound Chances (oportunidades de rebote totales)
  - `TCHS`: Touches (toques del balón)
  - `SAST`: Secondary Assists (asistencias secundarias)
  - `FT_AST`: Free Throw Assists (asistencias que resultaron en tiros libres)
  - `PASS`: Passes (pases realizados)
  - `AST`: Assists (asistencias)
  - `CFGM`: Close Field Goals Made (tiros anotados con defensor cerca)
  - `CFGA`: Close Field Goals Attempted (tiros intentados con defensor cerca)
  - `CFG_PERC`: Close Field Goal Percentage (porcentaje de tiros con defensor cerca)
  - `UFGM`: Uncontested Field Goals Made (tiros anotados sin defensor)
  - `UFGA`: Uncontested Field Goals Attempted (tiros intentados sin defensor)
  - `UFG_PERC`: Uncontested Field Goal Percentage (porcentaje de tiros sin defensor)
  - `FG_PERC`: Field Goal Percentage (porcentaje de tiros de campo)
  - `DFGM`: Defended Field Goals Made (tiros anotados defendidos)
  - `DFGA`: Defended Field Goals Attempted (tiros intentados defendidos)
  - `DFG_PERC`: Defended Field Goal Percentage (porcentaje de tiros defendidos)

- **`game_boxscore_hustle.csv`**: Estadísticas de esfuerzo por jugador y período
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `MIN`: Minutos jugados
  - `SCREEN_AST`: Screen Assists (asistencias por bloqueos)
  - `SCREEN_AST_PTS`: Screen Assist Points (puntos por asistencias de bloqueos)
  - `DEFLECTIONS`: Deflections (desviaciones del balón)
  - `OFF_LOOSE_BALLS_RECOVERED`: Offensive Loose Balls Recovered (balones sueltos recuperados ofensivamente)
  - `DEF_LOOSE_BALLS_RECOVERED`: Defensive Loose Balls Recovered (balones sueltos recuperados defensivamente)
  - `LOOSE_BALLS_RECOVERED`: Total Loose Balls Recovered (balones sueltos recuperados totales)
  - `CHARGES_DRAWN`: Charges Drawn (cargas ofensivas recibidas)
  - `CONTESTED_2PT_SHOTS`: Contestados de 2 puntos (tiros de 2 puntos contestados)
  - `CONTESTED_3PT_SHOTS`: Contestados de 3 puntos (tiros de 3 puntos contestados)
  - `CONTESTED_SHOTS`: Total Contestados (tiros contestados totales)
  - `OFF_BOX_OUTS`: Offensive Box Outs (bloqueos de rebote ofensivos)
  - `DEF_BOX_OUTS`: Defensive Box Outs (bloqueos de rebote defensivos)
  - `BOX_OUTS`: Total Box Outs (bloqueos de rebote totales)

- **`game_boxscore_defense.csv`**: Estadísticas defensivas por jugador
  - `GAME_ID`: Identificador único del juego/encuentro
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `HOME_TEAM_ABB`: Abreviatura del equipo local (3 letras)
  - `AWAY_TEAM_ABB`: Abreviatura del equipo visitante (3 letras)
  - `PLAYER_ID`: Identificador único del jugador
  - `PLAYER_NAME`: Nombre completo del jugador
  - `PLAYER_NAME_ABB`: Slug del nombre del jugador (para URLs)
  - `PLAYER_TEAM_ABB`: Abreviatura del equipo del jugador
  - `PLAYER_POS`: Posición del jugador (C, F, G)
  - `PLAYER_DNP`: Indica si el jugador no jugó (DNP - Did Not Play)
  - `MIN`: Minutos jugados
  - `DEF_MIN`: Defensive Minutes (minutos jugados en defensa)
  - `PARTIAL_POSS`: Partial Possessions (posesiones parciales)
  - `PTS`: Points (puntos permitidos)
  - `DREB`: Defensive Rebounds (rebotes defensivos)
  - `AST`: Assists (asistencias permitidas)
  - `TOV`: Turnovers (pérdidas forzadas)
  - `STL`: Steals (robos)
  - `BLK`: Blocks (tapones)
  - `DFGM`: Defended Field Goals Made (tiros anotados defendidos)
  - `DFGA`: Defended Field Goals Attempted (tiros intentados defendidos)
  - `DFG_PERC`: Defended Field Goal Percentage (porcentaje de tiros defendidos)
  - `D3PM`: Defended 3 Pointers Made (triples anotados defendidos)
  - `D3PA`: Defended 3 Pointers Attempted (triples intentados defendidos)
  - `D3P_PERC`: Defended 3 Point Percentage (porcentaje de triples defendidos)

- **`game_play_by_play.csv`**: Datos jugada por jugada de cada partido
  - `PERIOD`: Período del juego (Q1, Q2, Q3, Q4, OT1, OT2, etc.)
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `GAME_ID`: Identificador único del juego/encuentro
  - `TEAM_ABB`: Abreviatura del equipo (3 letras)
  - `MIN`: Tiempo del reloj (ej: "11:23")
  - `SCORE`: Marcador en el momento del evento (ej: "12-10") o "-" si no está disponible
  - `PLAYER`: Nombre del jugador involucrado en la acción
  - `ACTION`: Descripción de la acción/jugada realizada

- **`game_summary.csv`**: Resumen del partido por equipo
  - `SEASON`: Temporada de la NBA (ej: "2024-25")
  - `SEASON_TYPE`: Tipo de temporada (Regular Season, Playoffs, Pre-Season)
  - `GAME_ID`: Identificador único del juego/encuentro
  - `TEAM_ABB`: Abreviatura del equipo (3 letras)
  - `Q1`: Puntos anotados en el primer cuarto
  - `Q2`: Puntos anotados en el segundo cuarto
  - `Q3`: Puntos anotados en el tercer cuarto
  - `Q4`: Puntos anotados en el cuarto cuarto
  - `OT1`: Puntos anotados en la primera prórroga (0 si no hay overtime)
  - `OT2`: Puntos anotados en la segunda prórroga (0 si no hay overtime)
  - `OT3`: Puntos anotados en la tercera prórroga (0 si no hay overtime)
  - `OT4`: Puntos anotados en la cuarta prórroga (0 si no hay overtime)
  - `FINAL`: Puntos finales del equipo
  - `PITP`: Points in the Paint (puntos en la pintura)
  - `FB_PTS`: Fast Break Points (puntos en contraataque)
  - `BIG_LD`: Biggest Lead (mayor ventaja del partido)
  - `BPTS`: Bench Points (puntos del banquillo)
  - `TREB`: Team Rebounds (rebotes del equipo)
  - `TOV`: Turnovers (pérdidas)
  - `TTOV`: Team Turnovers (pérdidas del equipo)
  - `POT`: Points Off Turnovers (puntos tras pérdidas)
  - `LEAD_CHANGES`: Cambios de ventaja durante el partido
  - `TIMES_TIED`: Veces que el partido estuvo empatado

**Nota**: Cada archivo CSV contiene headers específicos definidos en el sistema de scrapping. Los headers completos están disponibles en la configuración del scrapper y se importan automáticamente al sistema.


#### Distribución de los csv por apps

- **Game**
  - Game Play by Play (`game_play_by_play.csv`)
  - Game Summary (`game_summary.csv`)
- **Game Boxscore**
  - Game Boxscore Advanced (`game_boxscore_advanced.csv`)
  - Game Boxscore Traditional (`game_boxscore_traditional.csv`)
- **Lineups**
  - Lineups Advanced (`lineups_advanced.csv`)
  - Lineups Four Factors (`lineups_four_factors.csv`)
  - Lineups Misc (`lineups_misc.csv`)
  - Lineups Opponent (`lineups_opponent.csv`)
  - Lineups Scoring (`lineups_scoring.csv`)
  - Lineups Traditional (`lineups_traditional.csv`)
- **Players**
  - Players Advanced Box Scores Advanced (`players_advanced_box_scores_advanced.csv`)
  - Players Advanced Box Scores Misc (`players_advanced_box_scores_misc.csv`)
  - Players Advanced Box Scores Scoring (`players_advanced_box_scores_scoring.csv`)
  - Players Advanced Box Scores Traditional (`players_advanced_box_scores_traditional.csv`)
  - Players Advanced Box Scores Usage (`players_advanced_box_scores_usage.csv`)
  - Players Bios (`players_bios.csv`)
  - Players Box Outs (`players_box_outs.csv`)
  - Players Box Scores (`players_box_scores.csv`)
  - Players Clutch Advanced (`players_clutch_advanced.csv`)
  - Players Clutch Misc (`players_clutch_misc.csv`)
  - Players Clutch Scoring (`players_clutch_scoring.csv`)
  - Players Clutch Traditional (`players_clutch_traditional.csv`)
  - Players Clutch Usage (`players_clutch_usage.csv`)
  - Players Defense Dashboard 2PT (`players_defense_dashboard_2pt.csv`)
  - Players Defense Dashboard 3PT (`players_defense_dashboard_3pt.csv`)
  - Players Defense Dashboard &gt;15FT (`players_defense_dashboard_gt15.csv`)
  - Players Defense Dashboard &lt;10FT (`players_defense_dashboard_lt10.csv`)
  - Players Defense Dashboard &lt;6FT (`players_defense_dashboard_lt6.csv`)
  - Players Defense Dashboard Overall (`players_defense_dashboard_overall.csv`)
  - Players Dunk Scores (`players_dunk_scores.csv`)
  - Players General Advanced (`players_general_advanced.csv`)
  - Players General Defense (`players_general_defense.csv`)
  - Players General Estimated Advanced (`players_general_estimated_advanced.csv`)
  - Players General Misc (`players_general_misc.csv`)
  - Players General Opponent (`players_general_opponent.csv`)
  - Players General Scoring (`players_general_scoring.csv`)
  - Players General Usage (`players_general_usage.csv`)
  - Players General Violations (`players_general_violations.csv`)
  - Players Hustle (`players_hustle.csv`)
  - Players Opponent Shooting Overall (`players_opponent_shooting_overall.csv`)
  - Players Playtype Ball Handler (`players_playtype_ball_handler.csv`)
  - Players Playtype Cut (`players_playtype_cut.csv`)
  - Players Playtype Hand Off (`players_playtype_hand_off.csv`)
  - Players Playtype Isolation (`players_playtype_isolation.csv`)
  - Players Playtype Misc (`players_playtype_misc.csv`)
  - Players Playtype Off Screen (`players_playtype_off_screen.csv`)
  - Players Playtype Putbacks (`players_playtype_putbacks.csv`)
  - Players Playtype Roll Man (`players_playtype_roll_man.csv`)
  - Players Playtype Spot Up (`players_playtype_spot_up.csv`)
  - Players Playtype Transition (`players_playtype_transition.csv`)
  - Players Shooting (`players_shooting.csv`)
  - Players Shot Dashboard Closest Defender (`players_shot_dashboard_closest_defender.csv`)
  - Players Shot Dashboard Closest Defender 10 (`players_shot_dashboard_closest_defender_10.csv`)
  - Players Shot Dashboard Dribbles (`players_shot_dashboard_dribbles.csv`)
  - Players Shot Dashboard General (`players_shot_dashboard_general.csv`)
  - Players Shot Dashboard Shot Clock (`players_shot_dashboard_shot_clock.csv`)
  - Players Shot Dashboard Touch Time (`players_shot_dashboard_touch_time.csv`)
  - Players Tracking Catch Shoot (`players_tracking_catch_shoot.csv`)
  - Players Tracking Defensive Impact (`players_tracking_defensive_impact.csv`)
  - Players Tracking Defensive Rebounding (`players_tracking_defensive_rebounding.csv`)
  - Players Tracking Drives (`players_tracking_drives.csv`)
  - Players Tracking Elbow Touch (`players_tracking_elbow_touch.csv`)
  - Players Tracking Offensive Rebounding (`players_tracking_offensive_rebounding.csv`)
  - Players Tracking Paint Touch (`players_tracking_paint_touch.csv`)
  - Players Tracking Passing (`players_tracking_passing.csv`)
  - Players Tracking Post Ups (`players_tracking_post_ups.csv`)
  - Players Tracking Pullup (`players_tracking_pullup.csv`)
  - Players Tracking Rebounding (`players_tracking_rebounding.csv`)
  - Players Tracking Shooting Efficiency (`players_tracking_shooting_efficiency.csv`)
  - Players Tracking Speed Distance (`players_tracking_speed_distance.csv`)
  - Players Tracking Touches (`players_tracking_touches.csv`)
- **Teams**
  - Teams Box Outs (`teams_box_outs.csv`)
  - Teams Box Scores (`teams_box_scores.csv`) — una fila por equipo por partido (incl. `game_id`, `home_away`)
  - Teams Clutch Advanced (`teams_clutch_advanced.csv`)
  - Teams Clutch Four Factors (`teams_clutch_four_factors.csv`)
  - Teams Clutch Misc (`teams_clutch_misc.csv`)
  - Teams Clutch Opponent (`teams_clutch_opponent.csv`)
  - Teams Clutch Scoring (`teams_clutch_scoring.csv`)
  - Teams Clutch Traditional (`teams_clutch_traditional.csv`)
  - Teams Defense Dashboard 2PT (`teams_defense_dashboard_2pt.csv`)
  - Teams Defense Dashboard 3PT (`teams_defense_dashboard_3pt.csv`)
  - Teams Defense Dashboard >15FT (`teams_defense_dashboard_gt15.csv`)
  - Teams Defense Dashboard <10FT (`teams_defense_dashboard_lt10.csv`)
  - Teams Defense Dashboard <6FT (`teams_defense_dashboard_lt6.csv`)
  - Teams Defense Dashboard Overall (`teams_defense_dashboard_overall.csv`)
  - Teams General Advanced (`teams_general_advanced.csv`)
  - Teams General Defense (`teams_general_defense.csv`)
  - Teams General Estimated Advanced (`teams_general_estimated_advanced.csv`)
  - Teams General Four Factors (`teams_general_four_factors.csv`)
  - Teams General Misc (`teams_general_misc.csv`)
  - Teams General Opponent (`teams_general_opponent.csv`)
  - Teams General Scoring (`teams_general_scoring.csv`)
  - Teams General Traditional (`teams_general_traditional.csv`)
  - Teams General Violations (`teams_general_violations.csv`)
  - Teams Hustle (`teams_hustle.csv`)
  - Teams Opponent Shooting Overall (`teams_opponent_shooting_overall.csv`)
  - Teams Opponent Shots Closest Defender (`teams_opponent_shots_closest_defender.csv`)
  - Teams Opponent Shots Closest Defender 10 (`teams_opponent_shots_closest_defender_10.csv`)
  - Teams Opponent Shots Dribbles (`teams_opponent_shots_dribbles.csv`)
  - Teams Opponent Shots General (`teams_opponent_shots_general.csv`)
  - Teams Opponent Shots Shot Clock (`teams_opponent_shots_shotclock.csv`)
  - Teams Opponent Shots Touch Time (`teams_opponent_shots_touch_time.csv`)
  - Teams Playtype Ball Handler (`teams_playtype_ball_handler.csv`)
  - Teams Playtype Cut (`teams_playtype_cut.csv`)
  - Teams Playtype Hand Off (`teams_playtype_hand_off.csv`)
  - Teams Playtype Isolation (`teams_playtype_isolation.csv`)
  - Teams Playtype Misc (`teams_playtype_misc.csv`)
  - Teams Playtype Off Screen (`teams_playtype_off_screen.csv`)
  - Teams Playtype Post Up (`teams_playtype_post_up.csv`)
  - Teams Playtype Putbacks (`teams_playtype_putbacks.csv`)
  - Teams Playtype Roll Man (`teams_playtype_roll_man.csv`)
  - Teams Playtype Spot Up (`teams_playtype_spot_up.csv`)
  - Teams Playtype Transition (`teams_playtype_transition.csv`)
  - Teams Shooting (`teams_shooting.csv`)
  - Teams Shot Dashboard Closest Defender (`teams_shot_dashboard_closest_defender.csv`)
  - Teams Shot Dashboard Closest Defender 10 (`teams_shot_dashboard_closest_defender_10.csv`)
  - Teams Shot Dashboard Dribbles (`teams_shot_dashboard_dribbles.csv`)
  - Teams Shot Dashboard General (`teams_shot_dashboard_general.csv`)
  - Teams Shot Dashboard Shot Clock (`teams_shot_dashboard_shot_clock.csv`)
  - Teams Shot Dashboard Touch Time (`teams_shot_dashboard_touch_time.csv`)
  - Teams Tracking Catch & Shoot (`teams_tracking_catch_shoot.csv`)
  - Teams Tracking Defensive Impact (`teams_tracking_defensive_impact.csv`)
  - Teams Tracking Defensive Rebounding (`teams_tracking_defensive_rebounding.csv`)
  - Teams Tracking Drives (`teams_tracking_drives.csv`)
  - Teams Tracking Elbow Touch (`teams_tracking_elbow_touch.csv`)
  - Teams Tracking Offensive Rebounding (`teams_tracking_offensive_rebounding.csv`)
  - Teams Tracking Paint Touch (`teams_tracking_paint_touch.csv`)
  - Teams Tracking Passing (`teams_tracking_passing.csv`)
  - Teams Tracking Post Ups (`teams_tracking_post_ups.csv`)
  - Teams Tracking Pullup (`teams_tracking_pullup.csv`)
  - Teams Tracking Rebounding (`teams_tracking_rebounding.csv`)
  - Teams Tracking Shooting Efficiency (`teams_tracking_shooting_efficiency.csv`)
  - Teams Tracking Speed & Distance (`teams_tracking_speed_distance.csv`)
  - Teams Tracking Touches (`teams_tracking_touches.csv`)


#### Distribución de modelos por app

Las siguientes apps definen modelos Django. **dashboard**, **grafana**, **prometheus**, **prompt**, **static**, **templates**, **project_commands** y **project** no definen modelos (son configuración, UI, comandos o estáticos).

- **game**
  - `GameBoxscoreTraditional` — Box score tradicional por jugador y período
  - `GamePlayByPlay` — Jugada a jugada del partido
  - `GameSummary` — Resumen por equipo (cuartos, PITP, FB_PTS, etc.)
  - `TeamBoxscoreTraditional` — Box score tradicional por equipo

- **game_boxscore**
  - `GameBoxscoreTraditional` — Box score tradicional por partido
  - `GameBoxscoreAdvanced` — Box score avanzado por partido

- **lineups**
  - `LineupsTraditional`
  - `LineupsAdvanced`
  - `LineupsMisc`
  - `LineupsFourFactors`
  - `LineupsScoring`
  - `LineupsOpponent`

- **players**
  - General
    - `PlayersGeneralTraditional`
    - `PlayersGeneralAdvanced`
    - `PlayersGeneralMisc`
    - `PlayersGeneralScoring`
    - `PlayersGeneralUsage`
    - `PlayersGeneralOpponent`
    - `PlayersGeneralDefense`
    - `PlayersGeneralViolations`
    - `PlayersGeneralEstimatedAdvanced`
  - Clutch
    - `PlayersClutchTraditional`
    - `PlayersClutchAdvanced`
    - `PlayersClutchMisc`
    - `PlayersClutchScoring`
    - `PlayersClutchUsage`
  - Playtype
    - `PlayersPlaytypeIsolation`
    - `PlayersPlaytypeTransition`
    - `PlayersPlaytypeBallHandler`
    - `PlayersPlaytypeRollMan`
    - `PlayersPlaytypePostUp`
    - `PlayersPlaytypeSpotUp`
    - `PlayersPlaytypeHandOff`
    - `PlayersPlaytypeCut`
    - `PlayersPlaytypeOffScreen`
    - `PlayersPlaytypePutbacks`
    - `PlayersPlaytypeMisc`
  - Tracking
    - `PlayersTrackingDrives`
    - `PlayersTrackingDefensiveImpact`
    - `PlayersTrackingCatchShoot`
    - `PlayersTrackingPassing`
    - `PlayersTrackingTouches`
    - `PlayersTrackingPullup`
    - `PlayersTrackingRebounding`
    - `PlayersTrackingOffensiveRebounding`
    - `PlayersTrackingDefensiveRebounding`
    - `PlayersTrackingShootingEfficiency`
    - `PlayersTrackingSpeedDistance`
    - `PlayersTrackingElbowTouch`
    - `PlayersTrackingPostUps`
    - `PlayersTrackingPaintTouch`
  - Defense dashboard
    - `PlayersDefenseDashboardOverall`
    - `PlayersDefenseDashboard3pt`
    - `PlayersDefenseDashboard2pt`
    - `PlayersDefenseDashboardLt6`
    - `PlayersDefenseDashboardLt10`
    - `PlayersDefenseDashboardGt15`
  - Shot dashboard
    - `PlayersShotDashboardGeneral`
    - `PlayersShotDashboardShotClock`
    - `PlayersShotDashboardDribbles`
    - `PlayersShotDashboardTouchTime`
    - `PlayersShotDashboardClosestDefender`
    - `PlayersShotDashboardClosestDefender10`
  - Otros
    - `PlayersBoxScores`
    - `PlayersAdvancedBoxScoresTraditional`
    - `PlayersAdvancedBoxScoresAdvanced`
    - `PlayersAdvancedBoxScoresMisc`
    - `PlayersAdvancedBoxScoresScoring`
    - `PlayersAdvancedBoxScoresUsage`
    - `PlayersShooting`
    - `PlayersDunkScores`
    - `PlayersOpponentShootingOverall`
    - `PlayersHustle`
    - `PlayersBoxOuts`
    - `PlayersBios`

- **roster**
  - `Teams` — Equipos NBA
  - `Players` — Jugadores NBA

- **teams**
  - General
    - `TeamsGeneralTraditional`
    - `TeamsGeneralAdvanced`
    - `TeamsGeneralFourFactors`
    - `TeamsGeneralMisc`
    - `TeamsGeneralScoring`
    - `TeamsGeneralOpponent`
    - `TeamsGeneralDefense`
    - `TeamsGeneralViolations`
    - `TeamsGeneralEstimatedAdvanced`
  - Clutch
    - `TeamsClutchTraditional`
    - `TeamsClutchAdvanced`
    - `TeamsClutchFourFactors`
    - `TeamsClutchMisc`
    - `TeamsClutchScoring`
    - `TeamsClutchOpponent`
  - Playtype
    - `TeamsPlaytypeIsolation`
    - `TeamsPlaytypeTransition`
    - `TeamsPlaytypeBallHandler`
    - `TeamsPlaytypeRollMan`
    - `TeamsPlaytypePostUp`
    - `TeamsPlaytypeSpotUp`
    - `TeamsPlaytypeHandOff`
    - `TeamsPlaytypeCut`
    - `TeamsPlaytypeOffScreen`
    - `TeamsPlaytypePutbacks`
    - `TeamsPlaytypeMisc`
  - Tracking
    - `TeamsTrackingDrives`
    - `TeamsTrackingDefensiveImpact`
    - `TeamsTrackingCatchShoot`
    - `TeamsTrackingPassing`
    - `TeamsTrackingTouches`
    - `TeamsTrackingPullup`
    - `TeamsTrackingRebounding`
    - `TeamsTrackingOffensiveRebounding`
    - `TeamsTrackingDefensiveRebounding`
    - `TeamsTrackingShootingEfficiency`
    - `TeamsTrackingSpeedDistance`
    - `TeamsTrackingElbowTouch`
    - `TeamsTrackingPostUps`
    - `TeamsTrackingPaintTouch`
  - Defense dashboard
    - `TeamsDefenseDashboardOverall`
    - `TeamsDefenseDashboard3pt`
    - `TeamsDefenseDashboard2pt`
    - `TeamsDefenseDashboardLt6`
    - `TeamsDefenseDashboardLt10`
    - `TeamsDefenseDashboardGt15`
  - Shot dashboard
    - `TeamsShotDashboardGeneral`
    - `TeamsShotDashboardShotClock`
    - `TeamsShotDashboardDribbles`
    - `TeamsShotDashboardTouchTime`
    - `TeamsShotDashboardClosestDefender`
    - `TeamsShotDashboardClosestDefender10`
  - Opponent
    - `TeamsOpponentShootingOverall`
    - `TeamsOpponentShotsGeneral`
    - `TeamsOpponentShotsShotclock`
    - `TeamsOpponentShotsDribbles`
    - `TeamsOpponentShotsTouchTime`
    - `TeamsOpponentShotsClosestDefender`
    - `TeamsOpponentShotsClosestDefender10`
  - Otros
    - `TeamsAdvancedBoxScores`
    - `TeamsAdvancedBoxScoresAdvanced`
    - `TeamsAdvancedBoxScoresFourFactors`
    - `TeamsAdvancedBoxScoresMisc`
    - `TeamsAdvancedBoxScoresScoring`
    - `TeamsShooting`
    - `TeamsHustle`
    - `TeamsBoxOuts`
    - `TeamsBoxScores`

- **ia**
  - `PredictionModel` — Modelos de predicción (ML)

- **predictions**
  - `Prediction` — Predicciones generadas
  - `PredictionsHistory` — Historial de predicciones


## 🤖 Predicciones con Machine Learning

### Tipos de Predicciones

#### Predicciones Prepartido
El sistema puede generar predicciones antes de que comience un partido, analizando:
- Estadísticas históricas de los equipos
- Rendimiento reciente
- Enfrentamientos previos
- Lesiones y ausencias
- Factores contextuales (local/visitante, descanso, etc.)

#### Predicciones en Tiempo Real
Durante partidos en curso, el sistema actualiza predicciones considerando:
- Puntuación actual
- Ritmo del partido
- Rendimiento en tiempo real
- Momentum y tendencias del juego
- Estadísticas del partido en curso

### Almacenamiento de Modelos
- **Versionado de Modelos**: Almacenamiento de diferentes versiones de modelos entrenados
- **Metadata de Modelos**: Información sobre rendimiento, fecha de entrenamiento, métricas
- **Modelos Especializados**: Modelos específicos para diferentes tipos de mercados
- **Reutilización**: Carga y uso de modelos previamente entrenados

### Mercados Cubiertos
El sistema puede generar predicciones para todos los mercados listados en la sección [Mercados de Apuestas](#-mercados-de-apuestas), incluyendo:
- Ganador del partido
- Hándicaps y totales
- Estadísticas de jugadores
- Mercados por cuartos y mitades
- Apuestas especiales y combinadas

## 💬 Sistema RAG

### Preguntas a los Datos
El sistema implementa un sistema RAG (Retrieval-Augmented Generation) que permite:

- **Consultas en Lenguaje Natural**: Hacer preguntas sobre los datos almacenados
- **Búsqueda Semántica**: Encontrar información relevante en el histórico de datos
- **Respuestas Contextualizadas**: Generar respuestas basadas en los datos reales
- **Análisis Inteligente**: Interpretar tendencias y patrones en los datos

### Ejemplos de Consultas
- "¿Cuál es el promedio de puntos de LeBron James en partidos de playoffs?"
- "¿Qué equipo tiene mejor porcentaje de victorias como visitante esta temporada?"
- "¿Cuántos partidos han superado los 250 puntos esta temporada?"
- "¿Qué jugador tiene más triples anotados en los últimos 10 partidos?"

## 🏗️ Arquitectura ML + RAG

### Visión General

El sistema utiliza una **arquitectura híbrida** que combina modelos predictivos estadísticos con RAG y LLM para proporcionar predicciones precisas y explicaciones en lenguaje natural.

### Componentes del Sistema

#### 1. Modelo Predictivo (Core del Sistema)

El **motor de predicción** utiliza modelos estadísticos y de Machine Learning:

**Modelos Disponibles:**
- **Regresión Logística**: Para clasificación binaria (ganador/perdedor)
- **Random Forest**: Para predicciones robustas con múltiples features
- **XGBoost**: Para modelos de alto rendimiento
- **Redes Neuronales**: Para patrones complejos
- **Modelos de Rating**: ELO, Glicko para rankings de equipos

**Features Principales:**
- Puntos promedio (ofensivos y defensivos)
- Pace (ritmo de juego)
- Offensive/Defensive rating
- Home/Away (local/visitante)
- Back-to-back games (partidos consecutivos)
- Lesiones y ausencias
- Head-to-head (enfrentamientos previos)
- Estadísticas recientes (últimos 5, 10 partidos)
- Momentum y tendencias

#### 2. Sistema RAG (Capa de Contexto)

El RAG actúa como **capa de lenguaje y contexto**, NO como motor de predicción:

- **Recuperación de Contexto**: Busca información histórica relevante
- **Enriquecimiento de Datos**: Añade contexto estadístico a las predicciones
- **Explicaciones**: Proporciona razonamiento basado en datos históricos

#### 3. LLM (Capa de Lenguaje Natural)

El LLM interpreta preguntas y genera respuestas en lenguaje natural:

- **Interpretación**: Entiende la intención de la pregunta del usuario
- **Síntesis**: Combina predicciones del modelo con contexto del RAG
- **Explicación**: Genera respuestas comprensibles en lenguaje natural

### Flujo de Arquitectura

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

### Ejemplo Concreto

**Pregunta del Usuario:**
> "¿El equipo X anotará más de 100 puntos?"

**Flujo de Procesamiento:**

1. **LLM interpreta la pregunta**
   - Identifica: Equipo X, predicción de puntos, umbral 100

2. **Modelo estadístico calcula probabilidad**
   ```
   P(puntos > 100) = 0.67 (67%)
   ```

3. **RAG recupera contexto histórico**
   - Promedio de puntos del equipo X: 108 pts
   - Ritmo de juego: Alto (102 posesiones/game)
   - Defensa del rival: Débil (112 pts permitidos promedio)
   - Últimos 10 partidos: 8 de 10 superaron 100 puntos
   - Head-to-head: Promedio 105 pts en últimos enfrentamientos

4. **LLM genera respuesta en lenguaje natural**
   > "Basado en los últimos 10 partidos (promedio 108 pts), el ritmo alto del equipo X y la defensa débil del rival, el modelo estima un **67% de probabilidad** de superar los 100 puntos. En los últimos enfrentamientos, el equipo X promedió 105 puntos, y considerando que el rival permite 112 puntos por partido, la predicción favorece claramente el 'Más de 100 puntos'."

### Dónde Encaja Cada Componente

✅ **Modelo Predictivo**:
- Calcula probabilidades y predicciones numéricas
- Es el **core del sistema** de predicción
- Requiere features estadísticas bien diseñadas

✅ **RAG**:
- Excelente como **capa de contexto y explicación**
- NO predice, pero **enriquece y explica** las predicciones
- Proporciona datos históricos relevantes

✅ **LLM**:
- Interpreta preguntas en lenguaje natural
- Sintetiza predicciones + contexto en respuestas comprensibles
- Genera explicaciones detalladas

### Ventajas de esta Arquitectura

1. **Precisión**: Los modelos estadísticos son más precisos que LLMs puros para predicciones numéricas
2. **Explicabilidad**: El RAG proporciona contexto histórico que justifica las predicciones
3. **Naturalidad**: El LLM hace que las respuestas sean comprensibles y naturales
4. **Flexibilidad**: Puede responder tanto preguntas de predicción como consultas históricas
5. **Escalabilidad**: Los modelos estadísticos son más eficientes que LLMs para cálculos masivos

## 📈 Mercados de Apuestas

El sistema genera predicciones para los siguientes mercados:

### Ganador
- **Ganador del encuentro**: Selección del equipo ganador del partido

### Hándicap
- **Hándicap**: Mercado principal de handicap donde se aplica un valor de handicap a cada equipo
  - Ejemplo: Phoenix Suns +14,5 vs Oklahoma City Thunder -14,5
- **Hándicaps alternativos**: Múltiples opciones de handicap con diferentes valores (desde +39,5 hasta -10,5)

### Total de Puntos
- **Total de puntos**: Apuesta sobre el total de puntos combinados de ambos equipos
  - Más de X puntos / Menos de X puntos
- **Total de puntos - Alternativo**: Múltiples opciones de totales alternativos (desde 199,5 hasta 249,5)

### Apuestas Combinadas
- **Línea / Total - Apuesta doble**: Combinación de handicap y total de puntos
  - Ejemplo: Phoenix Suns +14,5/Más de 224,5
- **Doble a partido/total de puntos**: Combinación de ganador del partido y total de puntos
  - Ejemplo: Phoenix Suns / Más de 224,5
- **Doble resultado**: Resultado al descanso y resultado final
  - Ejemplo: Phoenix Suns / Phoenix Suns (gana primera mitad y partido)

### Margen de Victoria

#### Margen de Victoria Simple
- **Margen de victoria**: Bandas simples de margen de victoria
  - Ejemplo: Phoenix Suns 1 - 10, Phoenix Suns 11+

#### Margen de Victoria (Bandas)
- **Margen de victoria (Bandas)**: Múltiples bandas de margen de victoria
  - Bandas de 1-5, 6-10, 11-15, 16-20, 21-25, 26-30, 31+ puntos
  - Disponible para ambos equipos

#### Margen de Victoria (Cuatro bandas)
- **Margen de victoria (Cuatro bandas)**: Cuatro bandas de margen
  - Bandas de 1-5, 6-10, 11-15, 16+ puntos

#### Margen de Victoria (10 pt)
- **Margen de victoria (10 pt)**: Bandas de 10 puntos
  - Bandas de 1-10, 11-20, 21-30, 31+ puntos

#### Margen de Victoria (Exacto)
- **Margen de victoria (Exacto)**: Margen exacto de victoria
  - Opciones desde 1 hasta 30+ puntos para cada equipo

#### Margen de Victoria 12
- **Margen de victoria 12**: Doce bandas de margen de victoria
  - Bandas de 1-5, 6-10, 11-15, 16-20, 21-25, 26+ puntos

### Mercados de Mitades

#### Primera Mitad
- **1.a mitad - Ganador**: Ganador de la primera mitad
- **1.a mitad - Ganador sin empate**: Ganador de la primera mitad sin opción de empate
- **1ª mitad - Resultado**: Resultado de la primera mitad (ganador o empate)
- **1.a mitad - Hándicap**: Handicap de la primera mitad
- **1.a mitad - Total de puntos**: Total de puntos en la primera mitad
- **1ª mitad - Total de puntos - Par/Impar**: Paridad del total de puntos de la primera mitad
- **1.a mitad - Total de puntos alternativo**: Totales alternativos para la primera mitad
- **1.a mitad - Total del equipo visitante**: Total de puntos del equipo visitante en primera mitad
- **1.a mitad - Total del equipo local**: Total de puntos del equipo local en primera mitad
- **1.ª mitad: Línea/Total - Apuesta doble**: Combinación de handicap y total primera mitad
- **1.a mitad - Doble a ganador/total**: Combinación de ganador y total primera mitad
- **1.ª mitad - Apuesta a ganador (3 opciones)**: Ganador primera mitad incluyendo empate
- **Hándicap alternativo en la 1.a mitad**: Handicaps alternativos para primera mitad
- **1ª parte - Margen**: Margen de victoria en la primera mitad
- **Margen de la 1ª Parte (Exacto)**: Margen exacto en primera mitad

#### Segunda Mitad
- **2.a mitad - Ganador**: Ganador de la segunda mitad
- **2.a mitad - Hándicap**: Handicap de la segunda mitad
- **2.a mitad - Total de puntos**: Total de puntos en la segunda mitad
- **2.o cuarto - Doble a hándicap/total**: Combinación de handicap y total segunda mitad
- **2.o cuarto - Doble a ganador/total**: Combinación de ganador y total segunda mitad
- **2.o cuarto - Apuesta a ganador (3 opciones)**: Ganador segunda mitad incluyendo empate

### Mercados por Cuartos

#### Primer Cuarto
- **1.er cuarto - Ganador**: Ganador del primer cuarto
- **1.er cuarto - Ganador sin empate**: Ganador del primer cuarto sin opción de empate
- **1.er cuarto - Hándicap**: Handicap del primer cuarto
- **1.er cuarto - Total de puntos**: Total de puntos en el primer cuarto
- **1.er cuarto - Total de puntos - Par/Impar**: Paridad del total de puntos del primer cuarto
- **1.er cuarto - Total del equipo visitante**: Total visitante en primer cuarto
- **1.er cuarto - Total del equipo local**: Total local en primer cuarto
- **1.er cuarto: Línea/Total - Apuesta doble**: Combinación de handicap y total primer cuarto
- **1.er cuarto - Doble a ganador/total**: Combinación de ganador y total primer cuarto
- **1.er cuarto - Apuesta a ganador (3 opciones)**: Ganador primer cuarto incluyendo empate
- **1.er cuarto - Carrera a X**: Primer equipo en alcanzar X puntos en el primer cuarto
- **Hándicap Alternativo en el 1er Cuarto**: Handicaps alternativos para primer cuarto
- **1.er cuarto - Total de puntos alternativo**: Totales alternativos para primer cuarto
- **Margen del 1er Cuarto**: Margen de victoria en primer cuarto
- **Margen del 1er Cuarto (Exacto)**: Margen exacto en primer cuarto
- **Ganador del 1. er cuarto/Ganador del partido**: Combinación de ganador primer cuarto y partido
- **1.er cuarto - Primer equipo en anotar**: Primer equipo en anotar en primer cuarto

#### Segundo Cuarto
- **2.o cuarto - Ganador**: Ganador del segundo cuarto
- **2.o cuarto - Hándicap**: Handicap del segundo cuarto
- **2.o cuarto - Total de puntos**: Total de puntos en el segundo cuarto
- **2.o cuarto - Total del equipo visitante**: Total visitante en segundo cuarto
- **2.o cuarto - Total del equipo local**: Total local en segundo cuarto
- **2.o cuarto - Carrera a X**: Primer equipo en alcanzar X puntos en el segundo cuarto
- **Hándicap Alternativo en el 2º Cuarto**: Handicaps alternativos para segundo cuarto
- **Puntos Totales del 2º Cuarto - Apuesta Alternativa**: Totales alternativos para segundo cuarto
- **Margen del 2º Cuarto**: Margen de victoria en segundo cuarto
- **Margen del 2º Cuarto (Exacto)**: Margen exacto en segundo cuarto
- **2.o cuarto - Primer equipo en anotar**: Primer equipo en anotar en segundo cuarto
- **2.o cuarto - Último equipo en anotar**: Último equipo en anotar en segundo cuarto

#### Tercer Cuarto
- **3.er cuarto - Ganador**: Ganador del tercer cuarto
- **3.er cuarto - Hándicap**: Handicap del tercer cuarto
- **3.er cuarto - Total de puntos**: Total de puntos en el tercer cuarto
- **3.er cuarto - Total del equipo visitante**: Total visitante en tercer cuarto
- **3.er cuarto - Total del equipo local**: Total local en tercer cuarto
- **3.er cuarto - Doble a hándicap/total**: Combinación de handicap y total tercer cuarto
- **3.er cuarto - Doble a ganador/total**: Combinación de ganador y total tercer cuarto
- **3.er cuarto - Apuesta a ganador (3 opciones)**: Ganador tercer cuarto incluyendo empate
- **3.er cuarto - Carrera a X**: Primer equipo en alcanzar X puntos en el tercer cuarto
- **Hándicap Alternativo en el 3er Cuarto**: Handicaps alternativos para tercer cuarto
- **Puntos Totales del 3er Cuarto - Apuesta Alternativa**: Totales alternativos para tercer cuarto
- **Margen del 3er Cuarto**: Margen de victoria en tercer cuarto
- **Margen del 3er Cuarto (Exacto)**: Margen exacto en tercer cuarto
- **3.er cuarto - Primer equipo en anotar**: Primer equipo en anotar en tercer cuarto

#### Cuarto Cuarto
- **4.o cuarto - Ganador**: Ganador del cuarto cuarto
- **4.o cuarto - Hándicap**: Handicap del cuarto cuarto
- **4.o cuarto -Total de puntos**: Total de puntos en el cuarto cuarto
- **4.o cuarto - Total del equipo visitante**: Total visitante en cuarto cuarto
- **4.o cuarto - Total del equipo local**: Total local en cuarto cuarto
- **4.o cuarto - Doble a hándicap/total**: Combinación de handicap y total cuarto cuarto
- **4.o cuarto - Doble a ganador/total**: Combinación de ganador y total cuarto cuarto
- **4.o cuarto - Apuesta a ganador (3 opciones)**: Ganador cuarto cuarto incluyendo empate
- **4.o cuarto - Carrera a X**: Primer equipo en alcanzar X puntos en el cuarto cuarto
- **Hándicap Alternativo en el 4º Cuarto**: Handicaps alternativos para cuarto cuarto
- **Puntos Totales del 4º Cuarto - Apuesta Alternativa**: Totales alternativos para cuarto cuarto
- **Margen del 4º Cuarto**: Margen de victoria en cuarto cuarto
- **Margen del 4º Cuarto (Exacto)**: Margen exacto en cuarto cuarto
- **4.o cuarto - Primer equipo en anotar**: Primer equipo en anotar en cuarto cuarto

### Mercados de Equipos

#### Totales por Equipo
- **Equipo visitante - Total de puntos**: Total de puntos del equipo visitante
- **Equipo local - Total de puntos**: Total de puntos del equipo local
- **Equipo visitante - Total de puntos alternativo**: Totales alternativos del equipo visitante
- **Equipo local - Total de puntos adicional**: Totales alternativos del equipo local
- **Equipo visitante - Total de puntos impar/par**: Paridad del total del equipo visitante
- **Equipo local - Total de puntos impar/par**: Paridad del total del equipo local

### Mercados de Jugadores

#### Puntos de Jugadores
- **Anota X+ puntos**: Apuestas sobre puntos mínimos de jugadores
  - Opciones: 5+, 10+, 15+, 20+, 25+, 30+, 35+, 40+, 45+, 50+ puntos
- **[Jugador] - Puntos**: Apuestas sobre/abajo de un total específico de puntos
  - Ejemplo: Shai Gilgeous-Alexander Más/Menos de 30,5 puntos
- **[Jugador] - Puntos alternativos**: Múltiples opciones de totales de puntos

#### Asistencias de Jugadores
- **Consigue X+ asistencias**: Apuestas sobre asistencias mínimas
  - Opciones: 2+, 4+, 6+, 8+, 10+, 12+ asistencias
- **[Jugador] - Asistencias**: Apuestas sobre/abajo de un total específico de asistencias

#### Rebotes de Jugadores
- **Registra X+ rebotes**: Apuestas sobre rebotes mínimos
  - Opciones: 4+, 6+, 8+, 10+, 12+, 14+, 16+ rebotes
- **[Jugador] - Rebotes**: Apuestas sobre/abajo de un total específico de rebotes

#### Triples de Jugadores
- **X+ triples anotados**: Apuestas sobre triples mínimos
  - Opciones: 1+, 2+, 3+ triples
- **[Jugador] - Triples anotados**: Apuestas sobre/abajo de un total específico de triples

#### Otras Estadísticas de Jugadores
- **Consigue X+ tapones**: Apuestas sobre tapones mínimos
  - Opciones: 1+, 2+, 3+ tapones
- **Consigue X+ robos**: Apuestas sobre robos mínimos
  - Opciones: 1+, 2+, 3+, 4+ robos
- **[Jugador] - Tapones**: Apuestas sobre/abajo de un total específico de tapones
- **[Jugador] - Robos**: Apuestas sobre/abajo de un total específico de robos

#### Combinaciones de Estadísticas de Jugadores
- **[Jugador] - Puntos + asistencias**: Combinación de puntos y asistencias
- **[Jugador] - Puntos + rebotes**: Combinación de puntos y rebotes
- **[Jugador] - Puntos + rebotes + asistencias**: Triple combinación
- **[Jugador] - Rebotes + asistencias**: Combinación de rebotes y asistencias
- **[Jugador] - Puntos alternativos + Rebotes + Asistencias**: Combinación con totales alternativos
- **[Jugador] - Puntos alternativos + Asistencias**: Puntos alternativos y asistencias
- **[Jugador] - Puntos alternativos + Rebotes + Asistencias**: Triple combinación con alternativos

#### Rendimiento por Cuarto
- **Jugador que anota X+ puntos en cada cuarto**: Puntos mínimos en cada cuarto
  - Opciones: 3+, 5+, 8+ puntos en cada cuarto
- **[Jugador] - Puntos en el 1er cuarto**: Puntos en el primer cuarto
- **1st Quarter - To Score X+ Points**: Puntos mínimos en primer cuarto
  - Opciones: 2+, 4+, 6+, 8+, 10+, 12+, 15+, 20+ puntos

#### Logros Especiales
- **Consigue un doble doble**: Doble doble (10+ en dos categorías)
- **Consigue un triple doble**: Triple doble (10+ en tres categorías)

#### Comparaciones y Rankings de Jugadores
- **Doble posibilidad anotadores**: Apuesta sobre cuál de dos jugadores anotará más puntos
  - Ejemplo: S. Gilgeous-Alexander o D. Booker
- **Dúo anotadores**: Apuesta sobre la suma de puntos de dos jugadores
  - Ejemplo: S. Gilgeous-Alexander + D. Booker
- **Trío anotadores**: Apuesta sobre la suma de puntos de tres jugadores
  - Ejemplo: S. Gilgeous-Alexander + Jal. Williams + D. Booker
- **Máximo anotador**: Apuesta sobre qué jugador será el máximo anotador del partido
- **Máximo anotador y victoria de su equipo**: Combinación de máximo anotador y victoria de su equipo
- **Número de puntos (Cara a cara)**: Comparación directa de puntos entre dos jugadores

### Mercados Especiales

#### Primera Canasta
- **Primer equipo en anotar**: Primer equipo que anota en el partido
- **Primera canasta**: Jugador que anota la primera canasta
- **Método de la primera canasta**: Tipo de primera canasta (Mate, Tiro libre, Bandeja, Tiro de 3 puntos, Otro)
- **Jugador que anota la primera canasta del equipo**: Primer anotador de cada equipo
- **Primera Canasta/Ganador Partido (Apuesta Doble)**: Combinación de primera canasta y ganador
- **Primera Canasta/Ganador Primer Cuarto (Apuesta Doble)**: Combinación de primera canasta y ganador primer cuarto

#### Carreras de Puntos
- **Carrera a X puntos**: Primer equipo en alcanzar X puntos en el partido
  - Opciones: 8, 10, 15, 20, 25, 30, 35, 40 puntos

#### Eventos Especiales
- **Lidera de principio a fin**: Equipo que lidera durante todo el partido
- **Ambos equipos anotan en el primer minuto**: Si ambos equipos anotan en el primer minuto
- **2 o más tiros de 3 puntos anotados en los primeros 3 minutos**: Triples en primeros 3 minutos
- **¿Habrá prórroga?**: Si el partido va a prórroga
- **Mitad con más puntos**: Qué mitad (primera o segunda) tendrá más puntos
- **Cuarto con mayor puntuación**: Qué cuarto (1º, 2º, 3º, 4º) tendrá más puntos

#### Apuestas Especiales
- **Crear Apuesta - Especiales**: Combinaciones especiales de jugadores y estadísticas
- **Apuesta triple**: Combinación de tres resultados

#### Ganar Todos los Cuartos/Mitades
- **[Equipo] gana todos los cuartos**: Apuesta sobre si un equipo gana todos los cuartos del partido
- **[Equipo] gana ambas mitades**: Apuesta sobre si un equipo gana ambas mitades del partido

### Mercados Alternativos

#### Totales Alternativos
- **Total de puntos - Alternativo**: Múltiples opciones de totales (desde 199,5 hasta 249,5)
- **Equipo visitante - Total de puntos alternativo**: Totales alternativos del visitante
- **Equipo local - Total de puntos adicional**: Totales alternativos del local
- **1.a mitad - Total de puntos alternativo**: Totales alternativos primera mitad

#### Handicaps Alternativos
- **Hándicaps alternativos**: Handicaps alternativos del partido completo
- **Hándicap alternativo en la 1.a mitad**: Handicaps alternativos primera mitad
- **Hándicap Alternativo en el 1er Cuarto**: Handicaps alternativos primer cuarto
- **Hándicap Alternativo en el 2º Cuarto**: Handicaps alternativos segundo cuarto
- **Hándicap Alternativo en el 3er Cuarto**: Handicaps alternativos tercer cuarto
- **Hándicap Alternativo en el 4º Cuarto**: Handicaps alternativos cuarto cuarto

---

## 🤝 Contribución

### Cómo Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

### Estándares de Código

- **PEP 8**: Estilo de código Python
- **Type Hints**: Tipado estático cuando sea posible
- **Docstrings**: Documentación de funciones y clases
- **Tests**: Cobertura de pruebas adecuada

## 📈 Roadmap

### Funcionalidades en Desarrollo
- [x] Almacenamiento de datos NBA
- [x] Sistema de monitoreo (Prometheus/Grafana)
- [x] Usuarios con permisos diferenciados
- [ ] Sistema de predicciones ML
- [ ] Predicciones en tiempo real
- [ ] Sistema RAG completo
- [ ] Almacenamiento de modelos entrenados
- [ ] API de predicciones
- [ ] Dashboard de predicciones

### Mejoras Planificadas
- [ ] Optimización de consultas
- [ ] Cache inteligente
- [ ] Modelos de deep learning
- [ ] Fine-tuning de modelos LLM
- [ ] Documentación API interactiva
- [ ] Sistema de alertas

## 🐛 Troubleshooting

### Problemas Comunes

**Error de conexión a base de datos**
```bash
# Verificar que PostgreSQL esté ejecutándose
docker-compose ps postgres
```

**Problemas con Celery**
```bash
# Reiniciar workers
docker-compose restart celery celery-beat
```

**Errores de importación**
```bash
# Verificar logs
docker-compose logs backend
```

**Problemas con modelos ML**
```bash
# Verificar que los modelos estén en la ruta correcta
docker-compose exec backend python manage.py check_models
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Equipo

- **Desarrollador Principal**: [Tu Nombre]
- **Contribuidores**: [Lista de contribuidores]

## 📞 Soporte

- **Issues**: [GitHub Issues](link-to-issues)
- **Documentación**: [Wiki del proyecto](link-to-wiki)
- **Email**: [tu-email@ejemplo.com]

---

⭐ **¡Dale una estrella al proyecto si te resulta útil!**

🏀 **¡Disfruta analizando y prediciendo datos de la NBA!**
