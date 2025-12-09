# GENERATOR_PROMPT.md

# Especificación completa del Sistema SIA‑R (Redacción Automática, Revisión, Publicación, UI, Tendencias en Tiempo Real)

Este documento instruye a VS Code / Copilot / Code para **generar el proyecto completo**, asegurando que:

* La página principal **funciona desde el primer build**.
* Los módulos previos permanecen intactos.
* Los nuevos campos de configuración (palabras clave + URL de WordPress + categorías dinámicas) están integrados y operativos.
* Las fuentes de tendencias se actualizan **en tiempo real al entrar a la app** y también **de forma periódica**.

Incluye todas las funciones existentes más las ampliaciones solicitadas.

---

# 1. Arquitectura Completa del Proyecto

```
/ (root)
│── app.py
│── config.py
│── requirements.txt
│── generator_prompt.md
│
├── services/
│   ├── trend_harvester.py
│   ├── trend_sources/
│   │     ├── google_trends.py
│   │     ├── twitter_x.py
│   │     ├── reddit_hot.py
│   │     ├── news_api.py
│   │     └── youtube_trending.py
│   ├── topic_expander.py
│   ├── headline_forge.py
│   ├── article_generator.py
│   ├── sensitivity_guard.py
│   ├── veracity_score.py
│   ├── quality_improver.py
│   ├── taxonomy_normalizer.py
│   ├── content_pipeline.py
│   └── scheduler.py
│
├── routes/
│   ├── ui.py
│   ├── api.py
│   └── auth.py
│
├── database/
│   ├── models.py
│   └── db.sqlite3
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── review.html
│   ├── published.html
│   ├── settings.html
│   ├── logs.html
│   └── metrics.html
│
├── static/
│   ├── css/
│   └── js/
│
└── docs/
    ├── manual_usuario.md
    └── manual_tecnico.md
```

Incluye nueva carpeta **trend_sources** para consultas a múltiples proveedores de tendencias, con actualización en tiempo real.

---

# 2. Página principal `/` operativa desde el primer build

En `app.py`:

```
from routes.ui import ui_bp
app.register_blueprint(ui_bp)
```

En `routes/ui.py`:

```
@ui_bp.route("/")
def home():
    return render_template(
        "index.html",
        status=get_pipeline_status(),
        keywords=get_current_keywords(),
        wp_site=get_wp_site_url(),
        wp_categories=get_wp_categories(),
        last_trends=get_recent_trends()
    )
```

La página `index.html` DEBE incluir:

* Estado general del sistema
* **Panel con palabras clave activas**
* **Sitio WordPress configurado**
* **Categorias cargadas en vivo desde WP**
* Tendencias recogidas automáticamente al entrar
* Botón para ejecutar el pipeline manualmente

---

# 3. Dashboard `/dashboard`

Tecnologías:

* Flask
* Jinja2
* Bootstrap 5
* JWT + Cookies seguras
* CSRF Protection

Páginas:

1. `/` – Dashboard general
2. `/login`
3. `/dashboard`
4. `/review/view/<id>`
5. `/pipeline/run`
6. `/published`
7. `/settings`
8. `/logs`
9. `/metrics`

Endpoints REST obligatorios:

* `GET /api/ui/status`
* `GET /api/ui/reviews`
* `POST /api/ui/review/<id>/approve`
* `POST /api/ui/review/<id>/reject`
* `POST /api/ui/run`
* `GET /api/wp/categories`
* `POST /api/settings/keywords`
* `POST /api/settings/wp`

---

# 4. NUEVA Configuración avanzada en el Dashboard

## 4.1. Cuadro de texto para palabras o frases clave

Debe aparecer en el Dashboard principal, no en Settings.

Campo:

```
<textarea name="trend_keywords"></textarea>
```

Almacena en la tabla `settings`:

* `id`
* `trend_keywords` (texto plano)
* `wp_url`
* `selected_categories`

Uso:

* Es insumo directo para `trend_harvester.py`.
* Se actualiza cada vez que el usuario guarda cambios.

## 4.2. Configuración directa del sitio WordPress

```
<input name="site_url" value="https://eldiademichoacan.com" />
```

a) Controla la API base
b) Controla extracción de categorías
c) Se usa para publicar artículos

## 4.3. Carga automática de categorías desde WordPress

Al ingresar al Dashboard o al guardar nueva URL:

1. Llamar: `/wp-json/wp/v2/categories?per_page=100`.
2. Guardar resultado en DB.
3. Mostrar Multi‑Select:

```
<select multiple name="wp_categories[]">
   <option value="ID">Nombre</option>
</select>
```

Se elimina duplicidad en Settings → Integraciones.
Toda la configuración vive ahora en el Dashboard.

---

# 5. Sistema de Tendencias en Tiempo Real

## 5.0. Gestión de claves y valores para actualizaciones en tiempo real

Todas las credenciales necesarias para consultar fuentes externas (por ejemplo, API Keys de Twitter/X, NewsAPI, YouTube, etc.) **deben almacenarse obligatoriamente en el archivo `.env`**, y nunca en el código fuente.

El sistema debe:

* Cargar automáticamente las variables desde `.env` mediante `python-dotenv`.
* Validar en tiempo de ejecución si alguna clave falta.
* Registrar advertencias en el log si alguna API Key está caducada o ausente.
* Permitir que el usuario final pueda actualizar sus claves desde el **Manual de Usuario**, donde deben incluirse:

  * Pasos para generar cada API Key.
  * Pasos para agregar o actualizar los valores dentro del archivo `.env`.
  * Qué hacer si una clave expira.

Ejemplos de claves esperadas:

```
TWITTER_API_KEY=
TWITTER_API_SECRET=
NEWSAPI_KEY=
YOUTUBE_API_KEY=
```

Estas claves se usan en la recolección de tendencias y en cualquier endpoint que requiera autenticación externa.
(Actualización inmediata + periódica)

## 5.1. Al cargar la app (Dashboard o `/`):

Debe ejecutarse automáticamente:

```
fetch_trends_realtime()
```

## 5.2. Fuentes incluidas obligatorias

* Google Trends
* Twitter/X tendencias
* Noticias recientes (NewsAPI o RSS)
* Videos populares (YouTube Trending)
* Reddit Hot / Top
* Búsquedas locales basadas en palabras clave personalizadas

## 5.3. Algoritmo consolidado

`trend_harvester.py` debe combinar todas las fuentes y generar una lista de tendencias normalizadas.

---

# 6. Pipeline de generación masiva de contenido

Secuencia obligatoria:

1. `fetch_trends()` usando las palabras clave
2. `expand_topics()`
3. `generate_headlines()`
4. `generate_articles()`
5. `check_sensitivity()`
6. `check_veracity()`
7. `rewrite_quality()`
8. `normalize_taxonomy()`
9. Guardar en DB

Tabla `articles`:

* id
* headline
* content
* category_list
* tag_list
* risk_score
* veracity_score
* status (pending, approved, rejected, published)
* created_at
* updated_at

---

# 7. Auto‑Publicación en WordPress

Condiciones:

* `risk_score <= max_risk_to_auto_publish`
* `veracity_score >= min_veracity_to_auto_publish`
* Categoría seleccionada por el usuario
* No contener palabras prohibidas

Publicación vía:
`POST /wp-json/wp/v2/posts`

Debe soportar:

* imágenes destacadas (media upload)
* categorías
* tags

---

# 8. Cron Jobs

En `scheduler.py`:

* Cada 10 minutos → generar artículos
* Cada hora → actualizar tendencias
* Cada día → mantenimiento
* Al cargar la UI → ejecutar actualización rápida de tendencias

---

# 9. Manuales

Generar automáticamente:

* `docs/manual_usuario.md`
* `docs/manual_tecnico.md`

Exportables a PDF.

---

# 10. Resultado esperado

VS Code debe generar un sistema completo que incluya:

* Página principal funcional con tendencias en tiempo real
* Dashboard con campos expandido (keywords + WP URL + categorías)
* Módulos históricos intactos
* Integración WordPress completa
* Multi‑fuente de tendencias
* Auto‑publicación confiable
* Cron jobs operativos
* UI lista para uso profesional

**Todo debe estar funcionando desde el primer build, sin errores y sin páginas vacías.**
