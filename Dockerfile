# Versión de linux que se va a utilizar dentro del container
FROM python:3.12-bookworm
# FROM python:3.14-bookworm -> Por ahora incomplatible con el tema

# Evita la generación de archivos de bytecode (.pyc)
ENV PYTHONDONTWRITEBYTECODE 1
# Evita el almacenamiento en búfer de la salida y el error estándar
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema y herramientas de compilación
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    gettext \
    curl \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chromium y ChromeDriver para Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Verificar rutas de Chromium y ChromeDriver
RUN which chromium || echo "Chromium no encontrado en PATH" && \
    which chromedriver || echo "ChromeDriver no encontrado en PATH" && \
    ls -la /usr/bin/chromium* /usr/bin/chromedriver* 2>/dev/null || true && \
    ls -la /usr/lib/chromium* 2>/dev/null || true

# Configurar variables de entorno para Chrome/Chromium
ENV CHROMIUM_FLAGS="--no-sandbox --disable-dev-shm-usage"

# Instalar UV usando pip (más confiable en contenedores)
RUN pip install uv

RUN mkdir /code
WORKDIR /code

# Copiar solo requirements.txt primero para aprovechar cache de Docker
COPY requirements.txt /code/

# Usar UV para instalar dependencias (mucho más rápido que pip)
# --system: instala en el sistema Python
# --no-cache: evita cache local para builds más limpios
RUN uv pip install --system --no-cache -r requirements.txt

# Instalar herramientas adicionales
RUN apt-get update && apt-get install -y htop && rm -rf /var/lib/apt/lists/*

# Memory management
ENV PYTHONMALLOC=malloc
ENV MALLOC_ARENA_MAX=2
ENV PYTHONHASHSEED=random

# Optimizar garbage collection
ENV PYTHONGC=1

COPY . /code/

# Dar permisos de ejecución al entrypoint
RUN chmod +x /code/entrypoint.sh