# **GENERATOR_PROMPT.md**

## **Sistema SIA-R – Redacción Automática con Integración a WordPress**

### **Especificación completa para generación del proyecto**

---

# 1. **Nombre del Proyecto**

**sia-r-news-engine**

---

# 2. **Objetivo General**

Construir un sistema automatizado de redacción, optimización, auditoría, verificación y publicación de noticias para **eldiademichoacan.com**, con:

* Backend en **Flask**
* Pipeline **SIA-R**
* Taxonomía inteligente (moderada + completamente adaptativa)
* Publicación en **WordPress**
* Autenticación JWT y API-Key
* Documentación completa (manual técnico + manual del usuario final)
* Docker y docker-compose
* Tests unitarios
* Scripts de soporte y herramientas internas

El proyecto debe generarse **completo**, con **código funcional**, **carpetas**, **archivos**, **manuales**, **configuraciones**, **scripts** y **documentación PDF**.

---

# 3. **Estructura del Proyecto**

Crear exactamente la siguiente estructura:

```
sia-r-news-engine/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── README.md
│
├── services/
│   ├── cleaner.py
│   ├── tagger_llm.py
│   ├── auditor_llm.py
│   ├── fact_checker.py
│   ├── verifier.py
│   ├── humanizer.py
│   ├── seo_optimizer.py
│   ├── planner.py
│   ├── taxonomy_normalizer.py
│   ├── taxonomy_autolearn.py
│   ├── wp_client.py
│   ├── wp_taxonomy_manager.py
│   ├── jwt_auth.py
│   ├── api_key_auth.py
│   ├── metrics_collector.py
│   ├── llm_client.py
│
├── pipeline/
│   ├── run_pipeline.py
│   ├── schema.py
│
├── routes/
│   ├── main.py
│   ├── auth.py
│   ├── pipeline_routes.py
│   ├── wp_routes.py
│
├── storage/
│   ├── models.py
│   ├── database.py
│   ├── migrations/
│
├── docs/
│   ├── manual_tecnico.md
│   ├── manual_usuario.md
│   ├── imagenes/
│   ├── generar_pdf.py
│
└── tests/
    ├── test_cleaner.py
    ├── test_tagger.py
    ├── test_wp_client.py
    ├── test_pipeline.py
```

---

# 4. **Detalles de Implementación**

El sistema debe generar *todo el código y archivos* descritos en este documento.

---

## 4.1. **app.py**

* Crear instancia de Flask.
* Registrar Blueprints:

  * main
  * auth
  * pipeline
  * wp
* Cargar variables desde `.env`.
* Configurar CORS.
* Configurar logging estructurado.
* Inicializar JWT.
* Cargar autenticación por API-Key.

---

## 4.2. **config.py**

Debe contener:

* OPENAI_API_KEY
* JWT_SECRET
* API_KEY_MASTER
* WP_BASE_URL
* WP_USERNAME / WP_PASSWORD
* DB_URL
* CONFIG DEL PIPELINE SIA-R
* CONFIG DEL TAXONOMY AUTO-LEARN

---

# 5. **Servicios (services/)**

Generar **código real** para cada módulo, no pseudo-código.

---

## 5.1. cleaner.py

Funciones:

* eliminación de ruido
* normalización unicode
* limpieza de HTML innecesario
* eliminación de duplicados
* corrección básica de estilo

---

## 5.2. tagger_llm.py

Uso de LLM:

* extracción de categorías sugeridas
* etiquetas sugeridas
* entidades
* tono periodístico

Debe devolver JSON estructurado.

---

## 5.3. auditor_llm.py

Auditoría:

* calidad narrativa
* factualidad preliminar
* agresividad
* neutralidad
* mejoras sugeridas

---

## 5.4. fact_checker.py

Incluye:

* heurísticas básicas
* detección de inconsistencias
* comparación con bases públicas
* indicadores de riesgo

---

## 5.5. verifier.py

Valida:

* coherencia final
* duplicación de ideas
* detección de contradicciones

---

## 5.6. humanizer.py

* humanización del texto
* ritmo periodístico
* tono neutral profesional
* evita estilo robótico

---

## 5.7. seo_optimizer.py

Optimiza:

* H1, H2, H3
* metadescripción
* densidad
* entidad principal
* extractos SEO

---

## 5.8. planner.py

* determina fecha de publicación
* determina categorías WP finales
* modo “auto-publicar”
* estrategia de distribución

---

## 5.9. taxonomy_normalizer.py

**Taxonomía moderada**

* corregir acentos
* unificar duplicados
* aplicar sinónimos base
* mapear 1:1 a categorías del WP existente

---

## 5.10. taxonomy_autolearn.py

**Taxonomía completamente adaptativa**

Debe implementar:

* carga de estadísticas de tráfico real
* aprendizaje diario automático
* generación de nuevas relaciones:

  * sinónimos
  * asociaciones
  * fusión de categorías
* actualización de archivo `profile.json`
* sistema de puntuación por relevancia

---

## 5.11. wp_client.py

Funciones:

* obtener token WP
* crear post
* actualizar post
* subir imágenes destacadas

---

## 5.12. wp_taxonomy_manager.py

Crear categorías y tags en WP si no existen:

* `ensure_category(name)`
* `ensure_tag(name)`
* devuelve ID válido para WP

---

## 5.13. jwt_auth.py

## 5.14. api_key_auth.py

Crear autenticación completa:

* acceso por JWT
* login y refresh
* API-Key rotables almacenadas en SQLite

---

## 5.15. metrics_collector.py

* almacenar logs de pipeline
* almacenar éxito/fallas
* almacenar tráfico de cada categoría

---

## 5.16. llm_client.py

Wrapper:

* OpenAI GPT
* adjustable model
* retries
* timeout

---

# 6. **Pipeline**

## run_pipeline.py

Debe:

1. Recibir entrada (texto inicial)
2. Ejecutar:

   * cleaner
   * tagger
   * auditor
   * fact-check
   * verifier
   * humanizer
   * seo optimizer
   * planner
3. Crear JSON final
4. Registrar logs en DB
5. Retornar respuesta final completa

---

## schema.py

* Definir modelos de entrada/salida del pipeline
* Validación con Pydantic

---

# 7. **Rutas Flask**

## main.py

* `/api/status`

## auth.py

* `/api/auth/login`
* `/api/auth/refresh`

## pipeline_routes.py

* `/api/pipeline/run`
* `/api/pipeline/simulate`

## wp_routes.py

* `/api/wp/post`
* `/api/wp/taxonomies`
* `/api/wp/rebuild-taxonomy-profiles`

## Interfaz visual local — UI / Dashboard (localhost:8000)

### Resumen

El sistema debe exponer una interfaz web en `http://localhost:8000` (puerto configurable) que permita a editores y administradores operar el pipeline, revisar artículos y controlar la publicación automática. Usar Flask + templates Jinja2 + Bootstrap 5. La UI debe integrarse con autenticación y API Key.

### Páginas / Vistas necesarias

1. `/` — Página de estado (mini dashboard)
2. `/login` — Login
3. `/dashboard` — Lista de items en revisión
4. `/review/view/<id>` — Vista de revisión con comparador
5. `/pipeline/run` — Ejecutar pipeline manualmente
6. `/published` — Artículos publicados vía SIA-R
7. `/settings` — Configuración (admin)
8. `/logs` — Logs del pipeline
9. `/metrics` — Gráficos estadísticos

### Endpoints REST adicionales

* `GET /api/ui/status`
* `GET /api/ui/reviews?status=pending`
* `GET /api/ui/review/<id>`
* `POST /api/ui/review/<id>/approve`
* `POST /api/ui/review/<id>/reject`
* `POST /api/ui/run`
* `GET /api/ui/published`
* `GET /api/ui/settings`
* `POST /api/ui/settings`

### Controles de Auto-Publicación

Parámetros clave:

* `min_veracity_to_auto_publish`
* `max_risk_to_auto_publish`
* `allow_auto_publish_categories`
* `require_editor_for_sensitive_topics`

### Previsualización

Generar vista HTML local y opción de draft en WordPress.

### Seguridad / Roles

* `editor`: revisar y aprobar
* `admin`: manejar configuración y API keys

### Notas técnicas

* Templates en `templates/`
* CSS en `static/css/`
* JS en `static/js/`
* Protección CSRF

### Workflow UI + pipeline

1. Se ejecuta pipeline
2. Auto-publish o envío a revisión
3. Editor revisa y aprueba/rechaza
4. Publicación final en WordPress

### Requisitos UX

* Modo oscuro
* Tabla paginada
* Filtros y búsqueda

### Pruebas UI

* Tests end-to-end con `pytest` y `requests`

### Salida esperada

* Archivos HTML en `templates/`
* Endpoints para UI
* JS para interacción
* Documentación en `docs/manual_usuario.md`

---

# 8. **Base de Datos**

## database.py

* SQLAlchemy
* conexión y sesión

## models.py

Tablas:

* Users
* ApiKeys
* PipelineLogs
* TaxonomyStats
* AutoLearnProfile (sinónimos, patrones, pesos)

---

# 9. **Docker**

### Dockerfile

* python:3.10
* gunicorn
* dependencias
* puerto 8000

### docker-compose.yml

* backend (Flask + gunicorn)
* volúmenes persistentes

---

# 10. **Tests**

Crear pruebas reales:

* test_cleaner.py
* test_tagger.py
* test_wp_client.py
* test_pipeline.py

---

# 11. **Documentación**

## docs/manual_tecnico.md

Incluir:

* arquitectura
* instalación
* flujo interno
* modelos de datos
* endpoints
* uso del pipeline
* taxonomía adaptativa
* seguridad
* esquemas JSON
* diagramas en ASCII o mermaid

## docs/manual_usuario.md

Incluir:

* cómo iniciar sesión
* cómo usar `/run`
* cómo publicar en WP
* cómo revisar sugerencias
* ejemplos de entradas
* ejemplos de salidas
* capturas (usar placeholders)
* pasos numerados

## docs/generar_pdf.py

Crear script en Python que:

* lea ambos `.md`
* genere PDF con:

  * portada
  * índice
  * estilos básicos
  * imágenes de `/docs/imagenes/`

---

# 12. **Sugerencias de Mejora (Incluir)**

* logging JSON
* modo extremo de SEO
* detección automática de viralidad
* integración con Cloudflare Cache Purge
* endpoint de diagnóstico
* sistema de actualización de modelos
* sistema de autoetiquetado por boost patterns

---

# 13. **Entrega esperada**

El generador debe construir:

* TODO el código
* TODAS las carpetas
* TODOS los archivos
* Documentación técnica
* Manual del usuario
* Scripts PDF
* Proyecto listo para ejecutar con:

  * `docker-compose up --build`
  * `python app.py`
* Proyecto listo para importar a un servidor Linux

---

# Fin del documento

Este archivo define **la especificación íntegra** que debe generar el entorno de IA.
