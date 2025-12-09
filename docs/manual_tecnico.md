# Manual Técnico - SIA-R News Engine

## Índice

1. [Arquitectura](#arquitectura)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Pipeline Detallado](#pipeline-detallado)
5. [Modelos de Datos](#modelos-de-datos)
6. [API Endpoints](#api-endpoints)
7. [Taxonomía Adaptativa](#taxonomía-adaptativa)
8. [Seguridad](#seguridad)
9. [Troubleshooting](#troubleshooting)

## Arquitectura

### Diagrama General

```
┌─────────────────────────────────────────────────────────────┐
│                       Cliente/Frontend                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask API Gateway                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Routes: main.py, auth.py, pipeline_routes.py, wp..  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                 ▼
    ┌────────┐    ┌─────────────┐   ┌──────────┐
    │Pipeline│    │Services     │   │WordPress │
    │Engine  │    │Collection   │   │Client    │
    └────────┘    └─────────────┘   └──────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Storage Layer      │
              │  - SQLAlchemy        │
              │  - SQLite/PostgreSQL │
              │  - Models            │
              └──────────────────────┘
```

### Componentes Principales

#### 1. Pipeline (`pipeline/`)
- **run_pipeline.py**: Orquestador del flujo de procesamiento
- **schema.py**: Validación de entrada/salida con Pydantic

#### 2. Services (`services/`)
- **cleaner.py**: Limpieza y normalización de texto
- **tagger_llm.py**: Extracción de metadatos con IA
- **auditor_llm.py**: Auditoría de calidad narrativa
- **fact_checker.py**: Verificación de hechos
- **verifier.py**: Coherencia y contradicciones
- **humanizer.py**: Humanización de texto
- **seo_optimizer.py**: Optimización SEO
- **planner.py**: Planificación de publicación
- **taxonomy_normalizer.py**: Taxonomía moderada
- **taxonomy_autolearn.py**: Aprendizaje automático
- **wp_client.py**: Cliente de WordPress
- **wp_taxonomy_manager.py**: Gestión de categorías/tags
- **jwt_auth.py**: Autenticación JWT
- **api_key_auth.py**: Autenticación por API Key
- **trend_harvester.py**: Orquestador de obtención de tendencias (Google, Twitter, NewsAPI)
- **article_generator.py**: Orquestador de generación contenido automatizado
- **topic_expander.py**: Expansión de temas y ángulos con LLM
- **headline_forge.py**: Generación de titulares virales/SEO
- **sensitivity_guard.py**: Filtro de contenido sensible y seguridad de marca
- **scheduler.py**: Sistema de tareas programadas (news cron)
- **metrics_collector.py**: Recolección de métricas
- **llm_client.py**: Wrapper de OpenAI

#### 3. Routes (`routes/`)
- **main.py**: Endpoints de status
- **auth.py**: Autenticación
- **pipeline_routes.py**: Pipeline execution
- **wp_routes.py**: Endpoints de WordPress

#### 4. Storage (`storage/`)
- **database.py**: Conexión SQLAlchemy
- **models.py**: Modelos ORM (User, ApiKey, PipelineLog, Taxonomy_*, Settings)
- **migrations/**: Migraciones de BD

## Instalación

### Requisitos Previos

```bash
- Python 3.10+
- pip (gestor de paquetes Python)
- git
- (Opcional) Docker & Docker Compose
```

### Pasos de Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/usuario/sia-r-news-engine.git
cd sia-r-news-engine

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear archivo .env
cp .env.example .env

# 6. Editar configuración
nano .env  # o tu editor preferido

# 7. Inicializar BD
python -c "from storage.database import init_db; init_db()"

# 8. Ejecutar
python app.py
```

### Instalación con Docker

```bash
# 1. Crear .env con credenciales
cp .env.example .env
# Editar .env

# 2. Construir e iniciar
docker-compose up --build

# 3. La aplicación estará en http://localhost:8000
```

## Configuración

### Variables de Entorno

```env
# === OpenAI ===
OPENAI_API_KEY=sk-...          # Tu clave de OpenAI
OPENAI_MODEL=gpt-4             # Modelo a usar
OPENAI_TEMPERATURE=0.7         # Creatividad (0-2)
OPENAI_MAX_TOKENS=2000         # Máximo de tokens

# === JWT ===
JWT_SECRET=tu-secreto-super-largo-123
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hora

# === API Key ===
API_KEY_MASTER=tu-clave-maestra

# === WordPress ===
WP_BASE_URL=https://tudominio.com
WP_USERNAME=admin
WP_PASSWORD=contraseña

# === BD ===
DB_URL=sqlite:///./sia_r.db
# O para PostgreSQL:
# DB_URL=postgresql://user:pass@localhost/sia_r

# === Aplicación ===
FLASK_ENV=production  # development o production
LOG_LEVEL=INFO        # DEBUG, INFO, WARNING, ERROR
```

## Pipeline Detallado

### Flujo de Ejecución

```
Entrada (título + contenido)
    │
    ▼
[1] CLEANER: Limpieza de texto
    ├─ Remover HTML
    ├─ Normalizar Unicode
    ├─ Remover ruido (URLs, emails)
    ├─ Remover duplicados
    └─ Corregir estilo
    │
    ▼
[2] TAGGER: Extracción de metadatos (LLM)
    ├─ Categorías sugeridas
    ├─ Tags sugeridos
    ├─ Entidades (personas, lugares)
    └─ Tono periodístico
    │
    ▼
[3] AUDITOR: Auditoría de calidad (LLM)
    ├─ Calidad narrativa (score 0-10)
    ├─ Factualidad preliminar
    ├─ Nivel de agresividad
    ├─ Neutralidad periodística
    └─ Mejoras sugeridas
    │
    ▼
[4] FACT_CHECKER: Verificación de hechos
    ├─ Detectar red flags (afirmaciones absolutas)
    ├─ Verificar fechas
    ├─ Verificar números
    ├─ Contar citas
    └─ Calcular risk_score (0-1)
    │
    ▼
[5] VERIFIER: Verificación de coherencia
    ├─ Puntuación de coherencia
    ├─ Detectar contradicciones
    ├─ Encontrar ideas duplicadas
    ├─ Analizar flujo de oraciones
    └─ Determinar validez general
    │
    ▼
[6] HUMANIZER: Humanización de texto
    ├─ Reducir pasiva
    ├─ Agregar contracciones
    ├─ Reducir repeticiones
    └─ Mejorar fluidez con LLM
    │
    ▼
[7] SEO_OPTIMIZER: Optimización SEO
    ├─ Generar H1 atractivo
    ├─ Sugerir H2s
    ├─ Meta descripción
    ├─ Densidad de palabras clave
    └─ Recomendaciones SEO
    │
    ▼
[8] TAXONOMY_NORMALIZER: Normalización
    ├─ Remover acentos
    ├─ Unificar duplicados
    ├─ Aplicar sinónimos base
    └─ Mapear a WP categories
    │
    ▼
[9] PLANNER: Planificación
    ├─ Fecha de publicación
    ├─ Hora óptima
    ├─ Categorías finales
    ├─ Tags finales
    ├─ Estrategia de distribución
    └─ Estimación de alcance
    │
    ▼
[10] AUTOLEARN: Aprendizaje
    ├─ Actualizar estadísticas
    ├─ Descubrir sinónimos
    ├─ Crear asociaciones
    └─ Actualizar perfil
    │
    ▼
Salida: JSON con todo el procesamiento
```

### Puntuación de Calidad

```
Quality_Score = 
    (Coherencia × 0.30) +
    (1 - FactCheckRisk × 0.30) +
    (NarrativeQuality/10 × 0.20) +
    (Neutrality/10 × 0.20)
```

Rango: 0-1 (1 = perfecto)

### Ready for Publication

Se considera listo para publicar si:
- `overall_valid` = true
- `risk_score` < 0.6
- `quality_score` > 0.5

## Modelos de Datos

### User
```python
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "password_hash": "...",
    "is_active": true,
    "created_at": "2025-12-04T10:30:00Z"
}
```

### ApiKey
```python
{
    "id": 1,
    "user_id": 1,
    "key_hash": "...",
    "key_prefix": "abc123",
    "is_active": true,
    "last_used": "2025-12-04T10:30:00Z",
    "expires_at": "2026-03-04T10:30:00Z"
}
```

### PipelineLog
```python
{
    "id": 1,
    "user_id": 1,
    "input_text": "...",
    "output_json": {...},
    "status": "success",
    "error_message": null,
    "execution_time": 45.23,
    "model_used": "gpt-4",
    "created_at": "2025-12-04T10:30:00Z",
    "wp_post_id": 123
}
```

### TaxonomyStats
```python
{
    "id": 1,
    "category_name": "Política",
    "tag_name": "elecciones",
    "usage_count": 42,
    "traffic_score": 850.0,
    "relevance_score": 0.87,
    "last_updated": "2025-12-04T10:30:00Z"
}
```

### AutoLearnProfile
```python
{
    "id": 1,
    "category_id": 5,
    "category_name": "Política",
    "synonyms": ["politica", "política", "politics"],
    "related_categories": [
        {"name": "Gobierno", "weight": 0.92},
        {"name": "Nacional", "weight": 0.78}
    ],
    "patterns": ["elecciones", "voto", "diputados"],
    "weight": 1.2,
    "confidence": 0.95,
    "last_updated": "2025-12-04T10:30:00Z"
}
```

## API Endpoints

### Autenticación

#### POST /api/auth/login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "status": "success",
  "user_id": 12345,
  "email": "user@example.com",
  "access_token": "eyJhbGc...",
  "api_key": "key_...",
  "token_type": "Bearer"
}
```

#### POST /api/auth/refresh
```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"access_token": "eyJhbGc..."}'
```

### Pipeline

#### POST /api/pipeline/run
```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "title": "Últimas noticias de política",
    "content": "El gobierno anunció nuevas medidas económicas...",
    "auto_publish": false
  }'
```

Response:
```json
{
  "status": "success",
  "execution_time_ms": 23450.5,
  "final_text": "Texto procesado y humanizado...",
  "final_h1": "Gobierno anuncia medidas económicas",
  "final_meta_description": "El gobierno presentó un nuevo...",
  "final_categories": ["Política", "Economía"],
  "final_tags": ["gobierno", "medidas", "economía"],
  "quality_score": 0.87,
  "ready_for_publication": true,
  "warnings": [],
  "stages": {...}
}
```

### WordPress

#### POST /api/wp/post
```bash
curl -X POST http://localhost:8000/api/wp/post \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token" \
  -d '{
    "title": "Título del Post",
    "content": "<p>Contenido...</p>",
    "categories": [5, 8],
    "tags": [12, 45],
    "status": "publish"
  }'
```

Response:
```json
{
  "status": "success",
  "post_id": 1234,
  "message": "Post created successfully"
}
```

#### GET /api/wp/taxonomies
```bash
curl -X GET http://localhost:8000/api/wp/taxonomies
```

Response:
```json
{
  "status": "success",
  "categories": [
    {"id": 1, "name": "Política"},
    {"id": 2, "name": "Deporte"}
  ],
  "tags": [
    {"id": 1, "name": "elecciones"},
    {"id": 2, "name": "futbol"}
  ]
}
```

## Taxonomía Adaptativa

### Cómo Funciona

1. **Recopilación**: Cada artículo registra sus categorías y tags
2. **Análisis**: Se analizan patrones de co-ocurrencia
3. **Descubrimiento**: Se encuentran sinónimos y asociaciones
4. **Fusión**: Las categorías muy similares se fusionan
5. **Aprendizaje**: El perfil se actualiza automáticamente

### Archivo de Perfil

```json
{
  "last_update": "2025-12-04T10:30:00",
  "categories": {
    "politica": {
      "count": 156,
      "traffic_total": 5420.0,
      "last_used": "2025-12-04T09:15:00"
    }
  },
  "synonyms": {
    "politica": [
      {"candidate": "gobierno", "confidence": 0.82}
    ]
  },
  "associations": {
    "politica": {
      "elecciones": 45.0,
      "voto": 38.0
    }
  },
  "statistics": {
    "total_articles": 345,
    "total_categories": 18,
    "learning_cycles": 3
  }
}
```

## Seguridad

### Autenticación

- **JWT**: Token expire en 1 hora (configurable)
- **API Keys**: Con fecha de expiración
- **Refresh**: Renovar tokens sin re-autenticar

### Autorización

- Cada usuario solo ve sus propios logs
- Acceso a recursos mediante roles (futuro)

### CORS

Configurado para aceptar solicitudes de múltiples orígenes:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Variables Sensibles

- Nunca commitear `.env` con valores reales
- Usar `.env.example` como template
- En producción, usar secrets manager

## Troubleshooting

### Error: "Invalid API Key"
```
Solución:
1. Verificar OPENAI_API_KEY en .env
2. Verificar que la clave no haya expirado
3. Probar con curl:
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Error: "Connection refused: WordPress"
```
Solución:
1. Verificar WP_BASE_URL es correcto
2. Verificar WP_USERNAME y WP_PASSWORD
3. Verificar que REST API está habilitado
4. Probar:
   curl https://tudominio.com/wp-json/wp/v2/
```

### Error: "Database locked"
```
Solución:
1. Si usa SQLite: solo 1 escritor a la vez
2. Cambiar a PostgreSQL en producción
3. Aumentar timeout:
   DB_URL=sqlite:///./sia_r.db?timeout=10
```

### Pipeline muy lento
```
Solución:
1. Verificar latencia de OpenAI (típicamente 2-5s)
2. Verificar conexión a WordPress
3. Reducir OPENAI_MAX_TOKENS si es grande
4. Usar GPT-3.5 en lugar de GPT-4 si disponible
```

---

**Versión**: 1.0.0
**Última actualización**: 4 de diciembre de 2025
