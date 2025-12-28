# 🏀 NBA Data Manager

Sistema completo de gestión y análisis de datos de la NBA construido con Django, Django REST Framework y Unfold Admin Theme.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API](#-api)
- [Comandos de Management](#-comandos-de-management)
- [Docker](#-docker)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🎯 Funcionalidades Principales
- **Dashboard Interactivo**: Panel de administración moderno con tema Unfold
- **API REST**: Endpoints para integración con aplicaciones externas
- **Gestión de Datos**: Almacenamiento y organización de múltiples tipos de estadísticas
- **Tareas Asíncronas**: Procesamiento en background con Celery
- **Monitoreo**: Sistema de logs y seguimiento

### 📊 Tipos de Datos Soportados
- **Box Scores**: Estadísticas básicas y avanzadas de partidos
- **Shooting**: Análisis de tiros por distancia
- **Defense**: Métricas defensivas y de impacto
- **Rebounding**: Estadísticas de rebotes ofensivos y defensivos
- **Passing**: Análisis de pases y asistencias
- **Touches**: Métricas de posesión y contacto con el balón
- **Clutch**: Estadísticas en situaciones clave
- **Hustle**: Métricas de esfuerzo y actividad
- **Speed & Distance**: Análisis de movimiento y velocidad

## 🛠 Tecnologías

### Backend
- **Django 5.1.5** - Framework web principal
- **Django REST Framework 3.16.1** - API REST
- **PostgreSQL** - Base de datos principal
- **Redis** - Cache y broker de mensajes
- **Celery 5.5.3** - Tareas asíncronas
- **Django Unfold 0.68.0** - Tema moderno para admin

### Infraestructura
- **Docker & Docker Compose** - Containerización
- **Nginx** - Servidor web (producción)
- **Redis** - Cache y cola de tareas
- **PostgreSQL 16** - Base de datos

## 📁 Estructura del Proyecto

```
nba-data-manager/
├── 📁 dashboard/              # App del dashboard principal
├── 📁 data/                   # Modelos de datos NBA
├── 📁 source/                 # Fuentes de datos
├── 📁 project/                # Configuración principal
├── 📁 project_commands/        # Comandos de management
│   └── 📁 management/commands/
│       ├── import.py          # Importar datos
│       ├── import_data.py     # Importar datos desde CSV
│       └── initsetup.py       # Configuración inicial
├── 📁 templates/              # Plantillas personalizadas
├── 📁 static/                 # Archivos estáticos
├── 📄 docker-compose.yml      # Configuración Docker
├── 📄 Dockerfile             # Imagen Docker
└── 📄 requirements.txt       # Dependencias Python
```

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
```

### Configuración de Unfold

El proyecto incluye configuración personalizada de Unfold con:
- Tema NBA personalizado
- Colores azules vibrantes
- Iconos y branding personalizado
- Dashboard optimizado para datos deportivos

## 📖 Uso

### Acceso al Admin
- **URL**: `http://localhost:8000/admin/`
- **Usuario**: Configurado en `initsetup`
- **Contraseña**: Configurada en `initsetup`

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

## 🔌 API

### Endpoints Principales

```bash
# Estadísticas de equipos
GET /api/teams/
GET /api/teams/{team_id}/stats/

# Box Scores
GET /api/boxscores/
GET /api/boxscores/{game_id}/

# Shooting
GET /api/shooting/
GET /api/shooting/{team_id}/

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
# Configuración inicial
python manage.py initsetup

# Importar datos desde CSV
python manage.py import_data

# Importar links desde directorio
python manage.py import
```

## 🐳 Docker

### Servicios Incluidos

- **backend**: Aplicación Django
- **postgres**: Base de datos PostgreSQL
- **redis**: Cache y broker Redis
- **celery**: Worker de tareas asíncronas
- **celery-beat**: Scheduler de tareas

### Comandos Docker Útiles

```bash
# Ver logs
docker-compose logs -f backend

# Ejecutar comando en contenedor
docker-compose exec backend python manage.py shell

# Reiniciar servicios
docker-compose restart backend

# Backup de base de datos
docker-compose exec postgres pg_dump -U postgres nba_data > backup.sql
```

## 📊 Monitoreo y Logs

### Sistema de Logs
- **Status Tracking**: Seguimiento del estado de ejecución
- **Error Handling**: Manejo robusto de errores

### Métricas Disponibles
- Tiempo de procesamiento
- Volumen de datos procesados
- Errores y excepciones

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

### Próximas Funcionalidades
- [ ] API GraphQL
- [ ] Dashboard de analytics avanzado
- [ ] Notificaciones en tiempo real
- [ ] Exportación a múltiples formatos
- [ ] Integración con APIs externas
- [ ] Machine Learning para predicciones

### Mejoras Planificadas
- [ ] Optimización de consultas
- [ ] Cache inteligente
- [ ] Monitoreo avanzado
- [ ] Documentación API interactiva

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

🏀 **¡Disfruta analizando datos de la NBA!**