# Dockerfile final para gestion_academica con UV y Gunicorn

FROM python:3.10-slim-bullseye

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV FLASK_CONTEXT=production
ENV FLASK_APP=app

# Crear usuario no root
RUN useradd --create-home --home-dir /home/sysacad sysacad
WORKDIR /home/sysacad

# Dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar uv (gestor de paquetes moderno)
RUN pip install --no-cache-dir uv

# Copiar pyproject.toml
COPY pyproject.toml ./

# Crear virtualenv y activar para instalar dependencias
RUN uv venv .venv

RUN uv sync

# Copiar el proyecto completo
COPY . .

# Ajustar permisos del usuario
RUN chown -R sysacad:sysacad /home/sysacad
USER sysacad

# Ejecutar Gunicorn (WSGI server para Flask)
CMD [".venv/bin/gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]