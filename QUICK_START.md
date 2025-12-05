# 🚀 Guía Rápida de Inicio - SIA-R News Engine

## 1️⃣ Instalación (5 minutos)

### Opción A: Windows

```cmd
# Descargar y extraer el repositorio
# Luego ejecutar:
run.bat
```

### Opción B: Linux / macOS

```bash
# Clonar repositorio
git clone https://github.com/usuario/sia-r-news-engine.git
cd sia-r-news-engine

# Ejecutar script de inicio
chmod +x run.sh
./run.sh
```

### Opción C: Docker

```bash
docker-compose up --build
```

## 2️⃣ Ejecutar Tests (Recomendado - Verificar que todo funciona)

### Instalación de pytest (incluida en requirements.txt)

```bash
# Ejecutar todos los tests
python -m pytest tests/ -v

# O solo tests sin problemas de SQLAlchemy Python 3.13:
python -m pytest tests/test_cleaner.py tests/test_tagger.py tests/test_wp_client.py -v
```

**Resultado esperado:** 15/15 tests PASSED (2.81 segundos)

**Detalles de tests:**
- `test_cleaner.py` — 7 tests de limpieza de texto (HTML, Unicode, whitespace, ruido)
- `test_tagger.py` — 4 tests de extracción de tags y análisis de tono
- `test_wp_client.py` — 4 tests de cliente WordPress

### ⚠️ Nota: Python 3.13 y SQLAlchemy

Si usas **Python 3.13** y ejecutas `pytest tests/` completo verás errores en:
- `test_pipeline.py` — `AssertionError: Class SQLCoreOperations directly inherits TypingOnly...`
- `test_ui.py` — Mismo error

**Causa:** Issue de SQLAlchemy 2.0.x con Python 3.13.

**Soluciones:**
1. **Recomendado:** Usar Python 3.12 (estable)
   ```bash
   # Cambiar a Python 3.12 en tu sistema
   python3.12 -m venv venv  # O usar pyenv, conda, etc.
   ```
2. Esperar a SQLAlchemy 2.2.0+ (próximas versiones)

### Verificar tu versión de Python

```bash
python --version
# Esperado: Python 3.10.x, 3.11.x, o 3.12.x
```

## 3️⃣ Configuración Básica (2 minutos)

Editar el archivo `.env` con tus credenciales:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-... # Obtén tu clave en https://platform.openai.com

# JWT Configuration
JWT_SECRET=tu-secreto-muy-seguro

# WordPress Configuration
WP_BASE_URL=https://tudominio.com
WP_USERNAME=usuario_wordpress
WP_PASSWORD=contrasena_wordpress

# Database
DATABASE_URL=sqlite:///./app.db  # O postgresql://user:pass@localhost/dbname

# Flask Configuration
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## 3️⃣ Primer Acceso (1 minuto)

1. Abre tu navegador en: **http://localhost:8000/login**
2. Las credenciales son las del administrador de WordPress
3. Haz clic en "Ingresar"
4. ¡Serás redirigido al Dashboard!

## 4️⃣ Primeros Pasos

### Paso 1: Explorar el Dashboard

**URL**: http://localhost:8000/dashboard

- Ver estadísticas generales
- Verificar artículos en revisión
- Observar gráficos de rendimiento

### Paso 2: Ejecutar el Pipeline Manualmente

**URL**: http://localhost:8000/pipeline/run

1. Copiar un artículo de tu sitio
2. Pegar en el formulario
3. Hacer clic en "Ejecutar Pipeline"
4. Ver los resultados en tiempo real

### Paso 3: Revisar Artículos

1. En el Dashboard, ir a "Artículos en Revisión"
2. Hacer clic en un artículo
3. Revisar calidad, categorías y tags
4. Tomar decisión: Aprobar o Rechazar

### Paso 4: Configurar Auto-publicación

**URL**: http://localhost:8000/settings

1. Ir a "Auto-publicación"
2. Ajustar umbrales:
   - Calidad mínima: 75%
   - Riesgo máximo: 30%
   - SEO mínimo: 60%
3. Seleccionar categorías permitidas
4. Hacer clic en "Guardar"

## 🎯 Casos de Uso Comunes

### Caso 1: Procesar un Artículo Existente

```
1. Ir a /pipeline/run
2. Copiar contenido de tu blog o fuente
3. Pegar en el formulario
4. Configurar opciones
5. Hacer clic en "Ejecutar Pipeline"
6. Revisar resultados
7. Guardar si está satisfecho
```

### Caso 2: Aprobar Artículo para Publicación

```
1. Ir a Dashboard
2. Ver "Artículos en Revisión"
3. Hacer clic en artículo
4. Revisar contenido y métricas
5. Hacer clic en "Aprobar"
6. Artículo se publica automáticamente en WordPress
```

### Caso 3: Analizar Rendimiento

```
1. Ir a /metrics
2. Seleccionar período (7d, 30d, 90d, all)
3. Ver gráficos de:
   - Artículos procesados
   - Calidad promedio
   - Tasa de éxito
   - Top categorías
```

## 🔑 Roles y Permisos

Tu acceso depende de tu rol en WordPress:

| Rol | Puede | No Puede |
|-----|------|---------|
| **Editor** | Ver dashboard, Revisar artículos | Publicar, Ejecutar manual, Config. |
| **Publicador** | ^ + Publicar, Ejecutar manual | Gestionar configuración |
| **Administrador** | Todo | - |

⚠️ **Nota**: Los permisos se sincronizan automáticamente desde WordPress.

## 📊 Interfaz Web - Ubicación Rápida

| Página | URL | Función |
|--------|-----|---------|
| Login | `/login` | Acceder al sistema |
| Dashboard | `/dashboard` | Vista general |
| Ejecutar Pipeline | `/pipeline/run` | Procesar artículos |
| Revisor | `/review/view/<id>` | Revisar artículo |
| Publicados | `/published` | Ver en WordPress |
| Logs | `/logs` | Historial |
| Métricas | `/metrics` | Estadísticas |
| Configuración | `/settings` | Parámetros del sistema |

## 🐛 Solucionar Problemas

### "Error: No puedo acceder a la UI"

**Solución**:
```bash
# Verificar que el servidor está corriendo
# Ir a: http://localhost:8000

# Si no funciona, reiniciar:
# Windows: Cerrar terminal y ejecutar run.bat
# Linux/Mac: Presionar Ctrl+C y ejecutar ./run.sh
```

### "Error: No estoy autenticado"

**Solución**:
1. Borrar cookies del navegador
2. Ir a `http://localhost:8000/login`
3. Ingresar credenciales nuevamente

### "Error: Permisos insuficientes"

**Solución**:
1. Contactar al administrador
2. Solicitar cambio de rol en WordPress
3. Los cambios se sincronizan automáticamente

### "Error: No puedo conectar a WordPress"

**Solución**:
1. Verificar que `WP_BASE_URL` es correcto en `.env`
2. Verificar que REST API está habilitada en WordPress
3. Verificar credenciales en `.env`

```bash
# Test de conexión (ejecutar en terminal):
python -c "from services.wp_client import WPClient; WPClient.test_connection()"
```

### "Error: OpenAI API Key inválida"

**Solución**:
1. Obtener nueva clave en https://platform.openai.com/account/api-keys
2. Actualizar en `.env`
3. Reiniciar aplicación

## 🔐 Seguridad Básica

- ✅ Cambiar `JWT_SECRET` a un valor único y seguro
- ✅ Usar contraseñas fuertes en WordPress
- ✅ Mantener `.env` en `.gitignore`
- ✅ No compartir `OPENAI_API_KEY`
- ✅ Cerrar sesión al terminar

## 📚 Próximos Pasos

1. **Leer documentación completa**: Ver [UI_GUIDE.md](./UI_GUIDE.md)
2. **Entender el pipeline**: Ver [manual_tecnico.md](./docs/manual_tecnico.md)
3. **Configurar auto-publicación**: Ver sección de Settings
4. **Monitorear métricas**: Revisar regularmente en `/metrics`

## 💬 Preguntas Frecuentes

**P: ¿Dónde se guarda la base de datos?**
R: En `app.db` (SQLite) o en la base de datos PostgreSQL configurada.

**P: ¿Puedo cambiar el puerto 8000?**
R: Sí, editar `PORT=8000` en `.env`

**P: ¿Necesito tener Django instalado?**
R: No, SIA-R usa Flask.

**P: ¿Los artículos se publican automáticamente?**
R: Sólo si cumple los criterios de auto-publicación configurados en Settings.

**P: ¿Puedo deshacer una publicación?**
R: Sí, puedes desapublicar desde `/published`

## 🆘 Soporte

- 📖 Documentación: Ver archivos `.md` en el proyecto
- 🐛 Bugs: Reportar en Issues
- 💡 Sugerencias: Crear Discussion
- 📧 Email: soporte@ejemplo.com

---

**¡Estás listo para comenzar! 🎉**

Ejecuta `run.sh` (o `run.bat` en Windows) y accede a `http://localhost:8000/login`
