# Guía de Instalación y Primeros Pasos

## Instalación Rápida

### Opción 1: Con Docker (Recomendado)

```bash
# 1. Clonar el proyecto
git clone https://github.com/usuario/sia-r-news-engine.git
cd sia-r-news-engine

# 2. Copiar y configurar .env
cp .env.example .env
# Editar .env con tus credenciales (nano .env o tu editor preferido)

# 3. Iniciar con Docker
docker-compose up --build

# 4. Verificar que está funcionando
curl http://localhost:8000/api/status
```

### Opción 2: Instalación Local

```bash
# 1. Requisitos
# Asegurar que tienes Python 3.10+
python --version

# 2. Clonar el proyecto
git clone https://github.com/usuario/sia-r-news-engine.git
cd sia-r-news-engine

# 3. Crear entorno virtual
python -m venv venv

# 4. Activar entorno
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Configurar variables de entorno
cp .env.example .env
# Editar .env (nano, vi, o cualquier editor)

# 7. Inicializar base de datos
python -c "from storage.database import init_db; init_db()"

# 8. Ejecutar
python app.py
```

## Configuración de .env

Edita el archivo `.env` con tus valores reales:

```env
# === OPENAI ===
OPENAI_API_KEY=sk-... (obtén de https://platform.openai.com/api-keys)
OPENAI_MODEL=gpt-4 (o gpt-3.5-turbo)

# === JWT (genera uno seguro) ===
JWT_SECRET=genera-una-clave-segura-aqui-minimo-32-caracteres

# === WORDPRESS ===
WP_BASE_URL=https://tudominio.com
WP_USERNAME=tu_usuario_wordpress
WP_PASSWORD=tu_contraseña_wordpress

# === BASE DE DATOS ===
# SQLite (desarrollo):
DB_URL=sqlite:///./sia_r.db

# PostgreSQL (producción):
# DB_URL=postgresql://user:password@localhost/sia_r

# === LOG ===
LOG_LEVEL=INFO (DEBUG para más detalles)
FLASK_ENV=production (development para debugging)
```

## Verificar Instalación

```bash
# 1. Revisar que el API está corriendo
curl http://localhost:8000/api/status

# Respuesta esperada:
# {
#   "status": "online",
#   "message": "SIA-R News Engine API is running",
#   "version": "1.0.0",
#   "uptime_seconds": 23.45
# }

# 2. Revisar que la BD está inicializada
ls -la sia_r.db  # Si usas SQLite

# 3. Ejecutar tests
pytest tests/ -v
```

## Primer Uso

### 1. Obtener Token JWT

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@test.com",
    "password": "contraseña"
  }'

# Guardar el token obtenido:
TOKEN="eyJhbGc..."
```

### 2. Procesar tu primer artículo

```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Mi primer artículo",
    "content": "Este es el contenido del artículo que quiero procesar con SIA-R..."
  }'
```

### 3. Ver el resultado

La respuesta incluye:
- Texto mejorado
- Categorías y tags sugeridos
- Puntuación de calidad (0-1)
- H1 y meta descripción optimizados
- Avisos si hay algún problema

### 4. Publicar en WordPress

Una vez satisfecho con el resultado:

```bash
curl -X POST http://localhost:8000/api/wp/post \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Mi primer artículo",
    "content": "<p>Contenido procesado...</p>",
    "categories": ["Política"],
    "tags": ["gobierno"],
    "status": "draft"
  }'
```

## Troubleshooting

### Error: "Connection refused"
- Asegurar que Docker está corriendo (si uses Docker)
- Asegurar que el puerto 8000 no está en uso
- Verificar que .env está configurado correctamente

### Error: "Invalid OpenAI API key"
- Verificar que la clave es válida en https://platform.openai.com/account/api-keys
- Asegurar que tienes cuota disponible
- Probar con curl:
  ```bash
  curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"
  ```

### Error: "WordPress connection failed"
- Verificar que WP_BASE_URL es correcto (sin barra final)
- Verificar credenciales de WordPress
- Asegurar que REST API está habilitado en WordPress
- Probar:
  ```bash
  curl https://tudominio.com/wp-json/wp/v2/posts
  ```

### La base de datos no se inicializa
- Asegurar que tienes permisos de escritura en el directorio
- Verificar que el DB_URL es válido
- Reintentar:
  ```bash
  python -c "from storage.database import init_db; init_db()"
  ```

## Generar PDFs de Manuales

```bash
python docs/generar_pdf.py

# Esto generará:
# - docs/manual_tecnico.pdf
# - docs/manual_usuario.pdf
```

## Próximos Pasos

1. **Leer documentación**
   - Manual técnico: `docs/manual_tecnico.md`
   - Manual usuario: `docs/manual_usuario.md`

2. **Explorar endpoints**
   - Ver README.md para lista completa
   - Probar con Postman o curl

3. **Configurar webhooks de WordPress**
   - Opcional: integrar con eventos de WordPress

4. **Monitorear estadísticas**
   - `GET /api/wp/stats`

## Deployment en Producción

### Con Docker

```bash
# Construir imagen
docker build -t sia-r:latest .

# Ejecutar en producción
docker run -d \
  --name sia-r-prod \
  -p 8000:8000 \
  -e FLASK_ENV=production \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ... otras variables ...
  sia-r:latest
```

### Con Gunicorn (sin Docker)

```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app

# Con Nginx como proxy
# Ver documentación de Nginx + Gunicorn
```

## Obtener Ayuda

- **Docs**: Ver `docs/` folder
- **Tests**: `pytest tests/ -v`
- **Logs**: Ver stdout/stderr del proceso
- **Issues**: GitHub issues

---

¡Listo! El sistema debe estar funcionando. Comienza a procesar artículos. 🚀
