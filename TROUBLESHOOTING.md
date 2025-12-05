# 🔧 Guía de Solución de Problemas - SIA-R News Engine

## Problemas Comunes y Soluciones

### 1. Error: `ModuleNotFoundError: No module named 'bs4'` (o cualquier otro módulo)

**Síntoma:**
```
ModuleNotFoundError: No module named 'bs4'
ModuleNotFoundError: No module named 'openai'
ModuleNotFoundError: No module named 'flask'
```

**Causa:** Las dependencias no están instaladas en el entorno virtual.

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate  # Linux/Mac
# O: venv\Scripts\activate  # Windows

# Instala todas las dependencias
pip install -r requirements.txt

# Si siguen faltando, instala de forma específica:
pip install Flask==2.3.3 openai==1.0.0 beautifulsoup4==4.12.2
```

---

### 2. Error: `pytest: command not found`

**Síntoma:**
```
bash: pytest: command not found
```

**Causa:** pytest no está instalado en el entorno virtual.

**Solución:**
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# O: venv\Scripts\activate  # Windows

# Opción A: Instalar pytest
pip install pytest

# Opción B: Ejecutar a través del módulo Python (más confiable)
python -m pytest tests/ -v
```

---

### 3. Error: `AssertionError: Class SQLCoreOperations directly inherits TypingOnly...`

**Síntoma:**
```
E   AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> 
    directly inherits TypingOnly but has additional attributes...
```

**Ocurre durante:** `pytest tests/` con Python 3.13

**Causa:** Incompatibilidad entre SQLAlchemy 2.0.x y Python 3.13 (issue de herencia de `TypingOnly`).

**Soluciones (en orden de recomendación):**

#### Opción 1: Usar Python 3.12 ✅ RECOMENDADO

```bash
# Verificar versión actual
python --version

# Instalar Python 3.12 (si no lo tienes)
# Windows: Descargar de https://www.python.org/downloads/
# Linux: sudo apt-get install python3.12
# Mac: brew install python@3.12

# Crear nuevo entorno virtual con Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# O: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python -m pytest tests/ -v
# Resultado: ✅ 15/15 tests PASSED
```

#### Opción 2: Actualizar SQLAlchemy (parcial)

```bash
# Se ha actualizado requirements.txt a SQLAlchemy 2.1.1
# Ejecutar solo los tests que funcionan con Python 3.13:
python -m pytest tests/test_cleaner.py tests/test_tagger.py tests/test_wp_client.py -v
# Resultado: ✅ 15/15 tests PASSED
# (test_pipeline.py y test_ui.py aún tienen error)
```

#### Opción 3: Esperar a SQLAlchemy 2.2.0+

```bash
# Cuando SQLAlchemy 2.2.0 se lance, actualizar:
pip install --upgrade SQLAlchemy
```

---

### 4. Error: Docker container "unhealthy"

**Síntoma:**
```
STATUS: Up X minutes (unhealthy)
```

**Comando para verificar:**
```bash
docker-compose ps
docker-compose logs --tail=200 backend
```

**Causas posibles:**
1. Falta de variables de entorno (`.env` no configurado)
2. OpenAI API Key inválida o expirada
3. Puertos en uso (8000, 5432)
4. Problemas de conectividad a OpenAI

**Soluciones:**

```bash
# 1. Verificar archivo .env existe y está correcto
cat .env
# Debe incluir: OPENAI_API_KEY, JWT_SECRET, WP_BASE_URL, DATABASE_URL

# 2. Reiniciar contenedores
docker-compose down
docker-compose up --build

# 3. Ver logs en tiempo real
docker-compose logs -f backend

# 4. Si el problema persiste, verificar puertos
# Windows
netstat -ano | findstr :8000
# Linux/Mac
lsof -i :8000

# 5. Si el puerto 8000 está en uso, libéralo o cambiar puerto en docker-compose.yml
```

---

### 5. Error: `git push origin main` - "Repository not found"

**Síntoma:**
```
fatal: repository 'https://github.com/usuario/sia-r-news-engine.git/' not found
```

**Causa:** El repositorio no existe en GitHub o no tienes permisos.

**Soluciones:**

#### Opción A: Crear repositorio en GitHub primero
1. Ve a https://github.com/new
2. Crea un nuevo repositorio llamado `sia-r-news-engine`
3. No inicialices con README (ya tienes contenido local)
4. Luego ejecuta:
```bash
git remote add origin https://github.com/usuario/sia-r-news-engine.git
git add .
git commit -m "Initial commit: SIA-R News Engine con Dashboard UI"
git push -u origin main
```

#### Opción B: Usar GitHub CLI (si está instalado)
```bash
# Verificar que gh está instalado
gh --version
gh auth status

# Crear repositorio automáticamente
gh repo create sia-r-news-engine --public --source=. --remote=origin --push
```

---

### 6. Error: `flask` o `app` no importa correctamente

**Síntoma:**
```
ModuleNotFoundError: No module named 'app'
ImportError: cannot import name 'app' from 'app'
```

**Causa:** El entorno virtual no está activado o la estructura de módulos es incorrecta.

**Solución:**
```bash
# 1. Asegúrate que estás en la raíz del proyecto
pwd  # Linux/Mac: debe mostrar algo con sia-r-news-engine
cd   # Windows: debe mostrar D:\Prj\sia-r-news-engine

# 2. Verifica que app.py existe
ls app.py  # Linux/Mac
dir app.py  # Windows

# 3. Activa el entorno virtual
source venv/bin/activate  # Linux/Mac
# O: venv\Scripts\activate  # Windows

# 4. Ejecuta tests correctamente
python -m pytest tests/ -v
```

---

### 7. Error: `No module named 'storage'` en tests

**Síntoma:**
```
ModuleNotFoundError: No module named 'storage'
```

**Causa:** pytest se ejecuta desde la carpeta equivocada o el `__init__.py` falta.

**Solución:**
```bash
# 1. Verifica que __init__.py existe en storage/
ls storage/__init__.py  # Linux/Mac
dir storage\__init__.py  # Windows

# 2. Ejecuta pytest desde la raíz del proyecto
cd /ruta/a/sia-r-news-engine
python -m pytest tests/ -v

# 3. Si aún falta, crea los __init__.py
touch storage/__init__.py routes/__init__.py services/__init__.py pipeline/__init__.py
```

---

### 8. Error: JWT Token inválido o expirado

**Síntoma:**
```json
{
  "msg": "Token has expired",
  "status": "error"
}
```

**Solución:**
1. Ejecuta login nuevamente para obtener un token nuevo
2. Verifica que `JWT_SECRET` en `.env` coincide en cliente y servidor
3. Aumenta `JWT_ACCESS_TOKEN_EXPIRES` en `config.py` si necesitas tokens más duraderos

```bash
# En .env
JWT_SECRET=tu-secreto-muy-largo-y-seguro

# En config.py (si necesitas ajustar)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Por defecto
```

---

### 9. Error: WordPress REST API no responde

**Síntoma:**
```
requests.exceptions.ConnectionError: Failed to connect to WordPress API
```

**Causa:** URL de WordPress incorrecta, REST API deshabilitada, o conexión rechazada.

**Solución:**
```bash
# 1. Verifica que WP_BASE_URL en .env es correcto
cat .env | grep WP_BASE_URL

# 2. Prueba la conexión manualmente
curl -X GET "https://tudominio.com/wp-json/wp/v2/categories"

# 3. Si no funciona, verifica en tu WordPress:
#    - Configuración > Enlaces permanentes > Asegúrate que no esté "Plain"
#    - Plugins > REST API habilitada (si está restringida)
#    - Firewall/WAF permitiendo /wp-json/

# 4. Cambia WP_BASE_URL en .env
WP_BASE_URL=https://tudominio.com  # Sin trailing slash
```

---

### 10. Error: `OpenAI API Key` inválida

**Síntoma:**
```
openai.error.AuthenticationError: Invalid API key
```

**Solución:**
1. Ve a https://platform.openai.com/api-keys
2. Obtén una nueva API Key
3. Edita `.env` y reemplaza:
   ```bash
   OPENAI_API_KEY=sk-...tu-nueva-clave...
   ```
4. Reinicia el servidor:
   ```bash
   # Si está corriendo en Docker
   docker-compose down
   docker-compose up --build
   
   # Si está corriendo localmente
   # Presiona Ctrl+C y ejecuta de nuevo
   python app.py
   ```

---

## Comandos Útiles de Diagnóstico

### Verificar dependencias instaladas
```bash
pip list | grep -E "Flask|openai|pytest|SQLAlchemy"
```

### Verificar estructura de carpetas
```bash
# Linux/Mac
tree -L 2 -I '__pycache__'

# Windows
tree /L
```

### Limpiar caché de Python y reinstalar dependencias
```bash
# Limpiar caché
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
rm -rf .pytest_cache .eggs *.egg-info

# Reinstalar todo
pip install --force-reinstall -r requirements.txt
```

### Ver logs de Docker en tiempo real
```bash
docker-compose logs -f --tail=100 backend
```

### Ejecutar tests con cobertura
```bash
python -m pytest tests/ --cov=services --cov=routes --cov-report=html
# Abre htmlcov/index.html para ver reporte
```

---

## Contacto y Soporte

Si encuentras un problema no listado aquí:

1. Verifica los logs:
   ```bash
   # Local
   tail -f logs/app.log
   
   # Docker
   docker-compose logs -f backend
   ```

2. Crea un issue en GitHub con:
   - Versión de Python (`python --version`)
   - Comando exacto que ejecutaste
   - Error completo (stack trace)
   - Sistema operativo

3. Revisa la documentación técnica en `docs/manual_tecnico.md`

---

**Última actualización:** 4 de Diciembre de 2025
**Versión:** 1.0.0
