# SYSACAD

Integrantes:
- Bravo, Carolina Noelia
- Chang Yang, Gabriela


# Proyecto SysAcad - Microservicio de Gestión Académica

Este repositorio contiene el microservicio **SysAcad**, un sistema para gestión académica de universidades, levantado con **Flask** y Docker, incluyendo pruebas de carga y documentación de patrones de microservicios.

---

## 1️⃣ Levantar el proyecto con Docker

### Requisitos

- Docker y Docker Compose instalados
- `.env` con configuración de base de datos y Redis (no incluido en el repositorio, usar `.env.example`)

### Pasos para levantar

1. Copiar `.env.example` a `.env` y configurar tus credenciales de PostgreSQL y Redis.
2. Levantar los servicios:

```bash
docker-compose up -d --build
````

3. Verificar que el microservicio funcione:

```bash
curl http://localhost:5000/api/v1/universidad
```

> Debe devolver los datos de universidades desde la base de datos.

---

## 2️⃣ Pruebas de carga con Locust

### Instalación

Si trabajas en Python local:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install locust
```

### Archivo de prueba (`locust_tests/locustfile.py`)

* Simula peticiones a la URL del microservicio.
* Ejemplo básico para GET/POST:

```python
from locust import HttpUser, task, between

class SysAcadUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_universidad(self):
        self.client.get("/api/v1/universidad")
```

### Ejecutar pruebas

```bash
locust -f locust_tests/locustfile.py --users 100 --spawn-rate 10 --run-time 40s --headless --host=http://localhost:5000 --html reporte.html
```

* Esto genera un **reporte HTML** `reporte.html` con tiempos de respuesta, requests por segundo, errores, etc.
* Adjuntar este reporte a la entrega.

---

## 3️⃣ Patrones de microservicios implementados

### Balanceo de carga

* Usando **Traefik** como reverse proxy en `docker-compose.yml`.
* Distribuye peticiones entre contenedores del mismo servicio.
* Configuración ejemplo:

```yaml
services:
  web:
    image: sysacad:latest
    deploy:
      replicas: 3
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.sysacad.rule=Host(`ecommerce.universidad.localhost`)"
```

---

### Retry / Circuit breaker

* Patrón conceptual usando **requests + Retry**:

```python
import requests
from requests.adapters import HTTPAdapter, Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=0.5)
session.mount("http://", HTTPAdapter(max_retries=retries))

response = session.get("http://otro-servicio/api/v1/data")
```

* Permite reintentos ante fallos temporales y reduce errores de comunicación.

---

### Rate Limit

* Evita sobrecarga del servicio con **Flask-Limiter**:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"])
```

* Limita 100 requests por minuto por cliente/IP.

---

### Cache (Redis)

* Mejora rendimiento y reduce consultas a base de datos con **Flask-Caching + Redis**:

```python
from flask_caching import Cache

cache = Cache(config={
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "redis",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_REDIS_PASSWORD": "tu_password"
})
cache.init_app(app)

@app.route("/api/v1/universidad")
@cache.cached(timeout=60)
def get_universidad():
    return jsonify(Universidad.query.all())
```
