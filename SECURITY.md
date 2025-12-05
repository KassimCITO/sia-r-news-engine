# 🔒 Reporte de Seguridad y Vulnerabilidades - 4 de Diciembre de 2025

## ⚠️ Vulnerabilidades Detectadas

GitHub Dependabot ha detectado **11 vulnerabilidades** en el repositorio:
- 1 crítica
- 4 altas
- 6 moderadas

**URL:** https://github.com/KassimCITO/sia-r-news-engine/security/dependabot

---

## 🛠️ Recomendaciones de Seguridad

### 1. Actualizar Dependencias Vulnerables

```bash
# Ver dependencias con vulnerabilidades conocidas
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# Ver reporte de seguridad
pip audit
# o: safety check
```

### 2. Dependencias Recomendadas para Actualizar

Las vulnerabilidades típicas en proyectos similares afectan a:
- `Pillow` (problema de procesamiento de imágenes)
- `reportlab` (PDF generation issues)
- `Flask` extensiones

**Comando para actualizar a versiones seguras:**
```bash
pip install --upgrade \
    Pillow==10.1.0 \
    reportlab==4.0.9 \
    Flask==3.0.0 \
    Flask-JWT-Extended==4.6.0 \
    requests==2.32.0
```

### 3. Actualizar requirements.txt

**Generar requirements.txt actualizado:**
```bash
# Con tu venv activado
pip freeze > requirements.txt.new

# Revisar cambios
diff requirements.txt requirements.txt.new

# Reemplazar
mv requirements.txt.new requirements.txt
```

### 4. Ejecutar Tests Después de Actualizaciones

```bash
# Tras actualizar dependencias, verificar que todo sigue funcionando
python -m pytest tests/test_cleaner.py tests/test_tagger.py tests/test_wp_client.py -v

# Resultado esperado: 15/15 tests PASSED
```

### 5. Configurar Dependabot en GitHub

**Archivos necesarios** (crear en `.github/dependabot.yml`):

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "kassimcito"
    assignees:
      - "kassimcito"
    labels:
      - "dependencies"
      - "python"
```

---

## 🔐 Mejores Prácticas de Seguridad

### 1. Gestionar Secretos de Forma Segura

**❌ NO hacer:**
```bash
# Nunca guardes secrets en archivos versionados
OPENAI_API_KEY=sk-1234567890abcdef
JWT_SECRET=my-secret-key
```

**✅ SÍ hacer:**
```bash
# Usar archivo .env (gitignore)
# Crear .env.example con placeholders
OPENAI_API_KEY=your-openai-api-key-here
JWT_SECRET=your-jwt-secret-here

# En .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

**Verificar que `.env` no está en el repo:**
```bash
git ls-files | grep -E "\.env|secrets|credentials"
# No debe retornar nada
```

### 2. Usar Variables de Entorno en Producción

**Docker:**
```dockerfile
# En Dockerfile NO incluir secrets
# Pasar como variables de entorno en docker-compose.yml o docker run

# docker-compose.yml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - JWT_SECRET=${JWT_SECRET}

# Ejecutar con:
OPENAI_API_KEY=sk-... docker-compose up
```

**Kubernetes (si usas):**
```bash
kubectl create secret generic sia-r-secrets \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  --from-literal=jwt-secret=$JWT_SECRET
```

### 3. Validar Entrada de Usuarios

**Ejemplo en `app.py` o blueprints:**

```python
from flask import request
from pydantic import ValidationError, BaseModel

class ArticleInput(BaseModel):
    title: str
    content: str
    author: str
    category: str

@app.route('/api/pipeline/run', methods=['POST'])
def run_pipeline():
    try:
        data = ArticleInput(**request.json)
        # Procesar datos validados
    except ValidationError as e:
        return {"error": str(e)}, 400
```

### 4. Habilitar HTTPS en Producción

**En `config.py`:**
```python
# Forzar HTTPS
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CORS restrictivo
CORS_ORIGINS = ["https://yourdomain.com"]
```

### 5. Rate Limiting

**Instalar extensión:**
```bash
pip install Flask-Limiter
```

**Implementar:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/pipeline/run', methods=['POST'])
@limiter.limit("10 per minute")
def run_pipeline():
    pass
```

### 6. Logging de Seguridad

**En `config.py`:**
```python
import logging

# Log accesos fallidos
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/security.log'),
        logging.StreamHandler()
    ]
)
```

### 7. Monitoreo de Dependencias

**Habilitar GitHub Security Tab:**
1. Ve a Settings > Security & analysis
2. Habilita "Dependabot alerts" ✅
3. Habilita "Dependabot security updates" ✅

### 8. Auditoría de Código

**Usar herramientas estáticas:**
```bash
# Instalar herramientas de análisis
pip install bandit pylint safety

# Ejecutar análisis
bandit -r . -ll  # Detecta vulnerabilidades comunes
pylint services/ routes/  # Calidad de código
safety check  # Vulnerabilidades conocidas en dependencias
```

---

## 📋 Checklist de Seguridad

- [ ] `.env` añadido a `.gitignore`
- [ ] `.env.example` creado sin valores reales
- [ ] Todos los secrets pasan como variables de entorno
- [ ] CORS configurado de forma restrictiva
- [ ] HTTPS forzado en producción
- [ ] Rate limiting habilitado en endpoints críticos
- [ ] Validación de entrada en todos los endpoints
- [ ] Logging de eventos de seguridad
- [ ] Dependabot configurado y monitoreado
- [ ] Tests de seguridad en CI/CD
- [ ] JWT tokens con expiración corta
- [ ] Contraseñas hasheadas (bcrypt, scrypt)

---

## 🚀 Pasos Inmediatos

### Paso 1: Crear .env.example
```bash
# Copiar .env a .env.example sin valores reales
cp .env .env.example

# Editar .env.example
cat > .env.example << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# JWT Configuration
JWT_SECRET=your-jwt-secret-here

# WordPress Configuration
WP_BASE_URL=https://tudominio.com
WP_USERNAME=wordpress_user
WP_PASSWORD=wordpress_password

# Database
DATABASE_URL=sqlite:///./app.db

# Flask Configuration
FLASK_ENV=production
DEBUG=False
EOF

# Añadir a git
git add .env.example
git commit -m "chore: Añadir .env.example para referencia (sin secretos reales)"
```

### Paso 2: Actualizar .gitignore
```bash
# Asegurar que .env está ignorado
cat >> .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.*.local
secrets/

# Credentials
*.pem
*.key
credentials.json

# Sensitive files
config/secrets.yml
docker-compose.override.yml
EOF

git add .gitignore
git commit -m "chore: Actualizar .gitignore con archivos sensibles"
```

### Paso 3: Verificar que no hay secretos en el historial
```bash
# Buscar API keys en el historio
git log -p -S "sk-" | head -20

# Si encuentra algo, usar BFG Repo-Cleaner
# git clone --mirror https://github.com/user/sia-r-news-engine.git
# bfg --replace-text passwords.txt --no-blob-protection sia-r-news-engine.git
# cd sia-r-news-engine.git && git push --mirror
```

### Paso 4: Ejecutar auditoría
```bash
pip install pip-audit
pip-audit

# Resultado esperado: vulnerabilidades listadas
# Actualizar requirements.txt con versiones seguras
```

---

## 📞 Referencias

- **GitHub Security:** https://github.com/KassimCITO/sia-r-news-engine/security
- **Dependabot Docs:** https://docs.github.com/en/code-security/dependabot
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **Python Security:** https://python.readthedocs.io/en/latest/library/security_warnings.html
- **Flask Security:** https://flask.palletsprojects.com/security/

---

**Documento creado:** 4 de Diciembre de 2025
**Prioridad:** ALTA
**Acción recomendada:** Implementar checkpoints de seguridad antes de deployment a producción
