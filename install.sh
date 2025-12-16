#!/bin/bash

# ejecutar solo una vez en Git Bash: 
# Convertir formato Windows → Unix:     sed -i 's/\r$//' install.sh
# Da permisos al script:                chmod +x install.sh
# Ejecuta:                             ./install.sh

set -e  # detener si algo falla

echo "========================================"
echo " Instalación - Sistema Gestión Académica "
echo "========================================"

# 1️⃣ Verificar Docker
if ! command -v docker &> /dev/null
then
    echo "❌ Docker no está instalado"
    exit 1
fi

if ! docker info &> /dev/null
then
    echo "❌ Docker no está corriendo"
    exit 1
fi

echo "✅ Docker OK"
echo ""

# 2️⃣ Build de imágenes
echo "▶️ Construyendo imágenes..."
docker compose -f docker-compose.install.yml build

echo "✅ Build completado"
echo ""

# 3️⃣ Levantar servicios
echo "▶️ Levantando servicios..."
docker compose up -d

# 4️⃣ Cargar variables del .env
echo "📖 Cargando configuración..."
if [ -f .env ]; then
    # Cargar solo líneas que no sean comentarios y exportarlas
    export $(grep -v '^#' .env | xargs) 2>/dev/null || true
    echo "✅ .env cargado"
else
    echo "⚠️  No se encontró .env"
fi
echo ""

# 5️⃣ Esperar PostgreSQL
echo "⏳ Esperando PostgreSQL..."
until docker compose exec -T postgres pg_isready -U "$POSTGRES_USER" &> /dev/null; do
    sleep 2
done
echo "✅ PostgreSQL listo"
echo ""

# 6️⃣ Crear bases de datos
echo "🗄️  Creando bases de datos..."

docker compose exec -T postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -q << 'EOF' 2>/dev/null
DO $$
BEGIN
    -- DEV_SYSACAD
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'DEV_SYSACAD') THEN
        CREATE DATABASE "DEV_SYSACAD";
        RAISE NOTICE 'Base DEV_SYSACAD creada';
    END IF;
    
    -- TEST_SYSACAD
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'TEST_SYSACAD') THEN
        CREATE DATABASE "TEST_SYSACAD";
        RAISE NOTICE 'Base TEST_SYSACAD creada';
    END IF;
    
    -- PROD_SYSACAD
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'PROD_SYSACAD') THEN
        CREATE DATABASE "PROD_SYSACAD";
        RAISE NOTICE 'Base PROD_SYSACAD creada';
    END IF;
END $$;

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE "DEV_SYSACAD" TO CURRENT_USER;
GRANT ALL PRIVILEGES ON DATABASE "TEST_SYSACAD" TO CURRENT_USER;
GRANT ALL PRIVILEGES ON DATABASE "PROD_SYSACAD" TO CURRENT_USER;
EOF

echo "✅ Bases creadas"
echo ""


# 7. (OPCIONAL) Ejecutar migraciones Flask si las tienes
# echo "🔄 Ejecutando migraciones..."
# docker compose exec flask flask db upgrade
# o
# docker compose exec flask python manage.py migrate

echo "========================================"
echo " 🚀 Sistema instalado y configurado "
echo "========================================"
echo ""
echo "📊 Bases de datos disponibles:"
echo "   • DEV_SYSACAD    (Desarrollo)"
echo "   • TEST_SYSACAD   (Testing)"
echo "   • PROD_SYSACAD   (Producción)"
echo ""
echo "🌐 Accesos:"
echo "   • PostgreSQL: localhost:5433"
echo "   • Usuario: $POSTGRES_USER"
echo "   • Contraseña: $POSTGRES_PASSWORD"
echo ""
echo "🔧 Comandos útiles:"
echo "   • Ver logs: docker compose logs"
echo "   • Detener: docker compose down"
echo "   • Reiniciar: ./install.sh"
echo "========================================"