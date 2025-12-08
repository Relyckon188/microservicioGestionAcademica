
# SYSACAD

Integrantes:

* Bravo, Carolina Noelia
* Chang Yang, Gabriela

---

# Proyecto SysAcad – Microservicio de Gestión Académica

Este repositorio contiene el microservicio **SysAcad**, un sistema de gestión académica desarrollado con **Flask**, con despliegue en **Docker** y **Traefik**, incluyendo pruebas de carga y patrones de microservicios implementados dentro del proyecto.

---

# 1️. Levantar el proyecto con Docker

## Requisitos

* Docker y Docker Compose
* Archivo `.env` configurado (basado en `.env.example`)

## Pasos

1. Crear archivo `.env`, luego modificar los datos correspondientes:

```bash
cp .env.example .env
```

2. Levantar toda la infraestructura:

```bash
docker-compose up -d --build
```

3. Probar el microservicio:

```bash
curl http://localhost:5000/api/v1/universidad
```

Debe devolver los datos de universidades desde la base de datos.

---

# 2️. Pruebas de carga con Locust

El repositorio ya incluye una carpeta **`locust_tests/`** con:

* `locustfile.py` → script de pruebas
* `reporte.html` → reporte HTML generado
* `Locust.pdf` → reporte PDF exportado

Por lo tanto, la configuración ya está lista para reproducir las pruebas.

## Ejecutar pruebas (opcional)

Si se desea volver a correr Locust:

```bash
locust -f locust_tests/locustfile.py --users 100 --spawn-rate 10 --run-time 40s --headless --host=http://localhost:5000 --html reporte.html
```

Esto regenerará un archivo `reporte.html` actualizado.

---

# 3️. Patrones de Microservicios Implementados

A continuación se detallan los patrones ya integrados en el proyecto.

---

## 3.1 Balanceo de carga (Traefik + réplicas)

Implementado en `docker-compose.yml`:

```yaml
services:
  backend:
    image: sysacad:latest
    deploy:
      replicas: 3
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`backend.universidad.localhost`)"
      - "traefik.http.services.backend.loadbalancer.server.port=5000"
```

Traefik distribuye peticiones entre los contenedores del microservicio.

---

## 3.2 Retry & Circuit Breaker (Traefik)

Configurado mediante middlewares:

```yaml
# Retry
- "traefik.http.middlewares.backend-retry.retry.attempts=3"
- "traefik.http.middlewares.backend-retry.retry.initialinterval=100ms"

# Circuit Breaker
- "traefik.http.middlewares.backend-cb.circuitbreaker.expression=LatencyAtQuantileMS(50.0) > 100"
```

* **Retry** → Reintentos automáticos ante fallos temporales.
* **Circuit Breaker** → Abre el circuito si la latencia excede 100 ms.

---

## 3.3 Rate Limit (Flask-Limiter)

No está configurado al proyecto, pero se puede agregar directamente el siguiente codigo al `docker-compose.yml` :

```yaml
# ------------ RATE LIMIT ------------
- "traefik.http.middlewares.backend-rl.ratelimit.average=100"
- "traefik.http.middlewares.backend-rl.ratelimit.burst=50"
```

y tambien agregar 'backend-rl' a mi lista de middlwares:

```yaml
- "traefik.http.routers.backend.middlewares=backend-retry,backend-cb,backend-rl"
```

---

## 3.4 Caché con Redis

El Redis está configurado en el archivo `config.py` de la app:

```python
class Config:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False

    # Cache
    CACHE_TYPE = os.getenv("CACHE_TYPE", "RedisCache")
    CACHE_REDIS_HOST = os.getenv("CACHE_REDIS_HOST", "redis")
    CACHE_REDIS_PORT = int(os.getenv("CACHE_REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(os.getenv("CACHE_REDIS_DB", 0))
    CACHE_REDIS_PASSWORD = os.getenv("CACHE_REDIS_PASSWORD") or None

    @staticmethod
    def init_app(app):
        pass
```

---

# 5️. Tecnologías

* Flask
* PostgreSQL
* Redis
* Traefik
* Docker
* Locust

---

