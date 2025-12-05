# SIA-R News Engine

**Sistema Automatizado de Redacción, Auditoría y Publicación de Noticias**

## Descripción

SIA-R es un sistema completo de inteligencia artificial para procesar, optimizar, auditar y publicar noticias automáticamente en WordPress. Utiliza el modelo GPT-4 de OpenAI para análisis avanzados de contenido y proporciona un pipeline completo de procesamiento de textos con:

- ✅ Limpieza y normalización de textos
- ✅ Extracción de categorías y etiquetas con IA
- ✅ Auditoría de calidad narrativa
- ✅ Verificación de hechos automática
- ✅ Humanización de textos
- ✅ Optimización SEO
- ✅ Publicación automática en WordPress
- ✅ Taxonomía adaptativa con aprendizaje automático
- ✅ Autenticación JWT y API Key
- ✅ Métricas y estadísticas

## Requisitos

- **Python 3.10 - 3.12** (Python 3.13 en desarrollo; ver nota sobre SQLAlchemy)
- OpenAI API Key
- WordPress con REST API habilitada
- Docker y Docker Compose (opcional)

### ⚠️ Nota: Python 3.13 y SQLAlchemy

**Estado Actual:** Sistema compatible con Python 3.10-3.12. Python 3.13 requiere SQLAlchemy >= 2.1.1.

**Problema:** SQLAlchemy 2.0.x tiene incompatibilidad con Python 3.13 (`TypingOnly` inheritance issue). Se ha actualizado `requirements.txt` a `SQLAlchemy==2.1.1` para soporte parcial.

**Solución recomendada:**
- Usar Python 3.12 (estable, sin problemas)
- O esperar a SQLAlchemy 2.2.0+ (próximas versiones)

**Verificar tu versión:**
```bash
python --version
```

## Instalación

### Opción 1: Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/usuario/sia-r-news-engine.git
cd sia-r-news-engine

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests (asegurar que todo funciona)
python -m pytest tests/ -v  # Ver QUICK_START.md para notas sobre Python 3.13
cp .env.example .env
# Editar .env con tus valores

# Inicializar base de datos
python -c "from storage.database import init_db; init_db()"

# Ejecutar aplicación
python app.py
```

### Opción 2: Docker

```bash
docker-compose up --build
```

La aplicación estará disponible en `http://localhost:8000`

## Configuración

Editar el archivo `.env` con tus credenciales:

```env
OPENAI_API_KEY=tu-clave-openai
JWT_SECRET=tu-secreto-jwt
WP_BASE_URL=https://tudominio.com
WP_USERNAME=usuario_wordpress
WP_PASSWORD=contrasena_wordpress
```

## Uso

### 1. Autenticación

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "contraseña"
  }'
```

Respuesta:
```json
{
  "status": "success",
  "access_token": "eyJhbGc...",
  "api_key": "eyJhbGc..."
}
```

### 2. Ejecutar Pipeline

```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu_token" \
  -d '{
    "title": "Título del Artículo",
    "content": "Contenido del artículo...",
    "auto_publish": false
  }'
```

### 3. Publicar en WordPress

```bash
curl -X POST http://localhost:8000/api/wp/post \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu_token" \
  -d '{
    "title": "Título",
    "content": "<p>Contenido...</p>",
    "categories": ["Política", "Nacional"],
    "tags": ["elecciones", "gobierno"],
    "status": "publish"
  }'
```

## Endpoints Principales

### Pipeline
- `POST /api/pipeline/run` - Ejecutar pipeline completo
- `POST /api/pipeline/simulate` - Simular pipeline sin publicar
- `GET /api/pipeline/status` - Estado del pipeline

### WordPress
- `POST /api/wp/post` - Crear/actualizar post
- `GET /api/wp/taxonomies` - Obtener categorías y tags
- `POST /api/wp/rebuild-taxonomy-profiles` - Reconstruir perfiles de taxonomía
- `GET /api/wp/stats` - Estadísticas

### Autenticación
- `POST /api/auth/login` - Login con email/password
- `POST /api/auth/refresh` - Renovar token JWT
- `POST /api/auth/verify` - Verificar token

### Status
- `GET /api/status` - Estado general del API
- `GET /api/health` - Health check

### UI / Dashboard (NUEVO)
- `GET /api/ui/status` - Estado del dashboard
- `GET /api/ui/reviews` - Artículos en revisión
- `GET /api/ui/review/<id>` - Detalles de revisión
- `POST /api/ui/review/<id>/approve` - Aprobar artículo
- `POST /api/ui/review/<id>/reject` - Rechazar artículo
- `GET /api/ui/published` - Artículos publicados
- `GET /api/ui/settings` - Configuración del sistema
- `POST /api/ui/settings` - Actualizar configuración
- `GET /api/ui/metrics` - Métricas y estadísticas
- `GET /api/ui/logs` - Logs de ejecución
- `DELETE /api/ui/logs/<id>` - Eliminar log
- `POST /api/ui/logs/clear` - Limpiar todos los logs
- `POST /api/ui/run` - Ejecutar pipeline desde UI

## Interfaz Web (Dashboard)

SIA-R incluye una interfaz web completa para gestionar, monitorear y controlar el sistema:

### Acceso

```
http://localhost:8000/login
```

### Páginas Disponibles

1. **Login** (`/login`)
   - Autenticación con JWT
   - Soporte para modo oscuro
   - Redirección automática

2. **Dashboard** (`/dashboard`)
   - Estadísticas en tiempo real
   - Artículos pendientes de revisión
   - Gráficos de rendimiento
   - Acciones rápidas

3. **Revisor de Artículos** (`/review/view/<id>`)
   - Visualización completa del contenido
   - Métricas de calidad y riesgo
   - Categorías y tags detectados
   - Aprobar/Rechazar con motivo

4. **Ejecutor de Pipeline** (`/pipeline/run`)
   - Procesar artículos manualmente
   - Ingreso de título, contenido, autor
   - Vista previa de resultados
   - Opciones de procesamiento avanzadas

5. **Artículos Publicados** (`/published`)
   - Listado de todos los artículos en WordPress
   - Búsqueda y filtros
   - Enlace directo a WordPress
   - Gestión de publicaciones

6. **Logs de Ejecución** (`/logs`)
   - Historial completo de procesamiento
   - Filtros por estado, fecha, artículo
   - Detalles de cada ejecución
   - Eliminación de logs

7. **Métricas** (`/metrics`)
   - Análisis de desempeño del pipeline
   - Gráficos de distribución y tendencias
   - Top categorías y problemas comunes
   - Períodos personalizables

8. **Configuración** (`/settings`)
   - Parámetros de auto-publicación (umbrales de calidad, riesgo, SEO)
   - Gestión de permisos y roles
   - Configuración de notificaciones
   - Integraciones (WordPress, OpenAI)

### Características de la Interfaz

✨ **Tema Oscuro/Claro** - Toggle disponible en navbar
🔐 **Autenticación JWT** - Tokens seguros con expiración
📱 **Responsive Design** - Adaptable a móvil, tablet, desktop
⚡ **Real-time Updates** - Sincronización de datos en vivo
📊 **Gráficos Interactivos** - Chart.js integrado
🔔 **Notificaciones Toast** - Feedback visual de acciones

### Roles y Permisos

| Acción | Editor | Publicador | Administrador |
|--------|--------|-----------|---------------|
| Ver Dashboard | ✓ | ✓ | ✓ |
| Revisar Artículos | ✓ | ✓ | ✓ |
| Publicar Automático | ✗ | ✓ | ✓ |
| Ejecutar Pipeline Manual | ✗ | ✓ | ✓ |
| Gestionar Configuración | ✗ | ✗ | ✓ |
| Eliminar Logs | ✗ | ✗ | ✓ |

**Nota**: Los roles se asignan automáticamente desde WordPress.

### Guía de Uso

Para una guía completa de la interfaz, ver [UI_GUIDE.md](./UI_GUIDE.md)



```
sia-r-news-engine/
├── services/          # Módulos de procesamiento
├── pipeline/          # Orquestador del pipeline
├── routes/            # Endpoints Flask
├── storage/           # Modelos y BD
├── tests/             # Tests unitarios
├── docs/              # Documentación
├── app.py             # Aplicación principal
├── config.py          # Configuración
└── requirements.txt   # Dependencias
```

## Documentación

Ver documentos detallados:
- [Manual Técnico](./docs/manual_tecnico.md)
- [Manual del Usuario](./docs/manual_usuario.md)

## Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=.

# Tests específicos
pytest tests/test_cleaner.py
pytest tests/test_pipeline.py
```

## Seguridad

- Todas las contraseñas y claves se almacenan en variables de entorno
- JWT para autenticación segura
- API Keys rotables para acceso programático
- CORS configurado

## Logs

Los logs se escriben en:
- Consola (desarrollo)
- Archivos (producción, configurar en config.py)

Nivel de log: `LOG_LEVEL=INFO` (configurable en .env)

## Troubleshooting

### Error de conexión a OpenAI
- Verificar que `OPENAI_API_KEY` sea válido
- Verificar que el modelo `gpt-4` esté disponible en tu cuenta
- Verificar cuota de API

### Error de conexión a WordPress
- Verificar que `WP_BASE_URL` sea correcto
- Verificar credenciales de WordPress
- Asegurar que REST API esté habilitada en WordPress

### Error de base de datos
- Verificar que `DB_URL` sea válida
- En SQLite, verificar permisos de carpeta
- Ejecutar `python -c "from storage.database import init_db; init_db()"`

## Licencia

MIT License - Ver LICENSE.md

## Soporte

Para reportar bugs o sugerencias, crear un issue en el repositorio.

## Roadmap

- [ ] Integración con Cloudflare Cache Purge
- [ ] Detección automática de viralidad
- [ ] Dashboard web
- [ ] Soporte para múltiples blogs
- [ ] Análisis de sentimiento avanzado
- [ ] Integración con redes sociales

---

**Versión:** 1.0.0  
**Último update:** 2025-12-04
