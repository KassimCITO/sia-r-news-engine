
# 🚀 GUÍA DE CONFIGURACIÓN DE INTEGRACIONES DE TENDENCIAS

## Resumen de Fuentes Disponibles

El sistema SIA-R ahora integra **5 fuentes de tendencias en tiempo real**:

| Fuente | Tipo | Costo | Requiere API | Límite |
|--------|------|-------|--------------|--------|
| **Google Trends** | Búsquedas globales | Gratuito | ❌ No | Rate-limited por Google |
| **Twitter/X API** | Social Media | Gratuito (tier básico) | ✅ Sí | 300 requests/15min |
| **News API** | Noticias | Gratuito | ✅ Sí | 100 requests/día |
| **RSS Feeds** | Feeds personalizados | Gratuito | ❌ No | Sin límite |
| **SerpAPI** | Google Search Results | Gratuito (100/mes) | ✅ Sí | 100 búsquedas/mes |

---

## 1️⃣ GOOGLE TRENDS (Recomendado - Sin Configuración)

**Estado:** ✅ Habilitado por defecto  
**Costo:** Gratuito  
**Configuración:** NINGUNA (usa `pytrends`)

```bash
# Ya está instalado en requirements.txt
# Simplemente funciona: GOOGLE_TRENDS_ENABLED=True
```

**Cómo usa:** Busca términos más populares en Google globalmente

**Limitaciones:** 
- Google puede bloquearlo ocasionalmente con HTTP 404
- Intentos con backoff exponencial mitigan esto

---

## 2️⃣ TWITTER/X API v2 (Social Media)

### Paso 1: Crear Cuenta de Developer

1. Ve a https://developer.twitter.com/en/portal/dashboard
2. Haz click en **"Create new app"** o selecciona uno existente
3. Completa el formulario de solicitud (sin costo)

### Paso 2: Obtener Credenciales

1. Ve a **"Keys and tokens"** en tu app
2. En la sección **"Bearer Token"**, genera o copia el token
3. Es el único que necesitas para API v2

### Paso 3: Configurar en .env

```env
TWITTER_API_ENABLED=True
TWITTER_BEARER_TOKEN=your-bearer-token-aqui
```

**Ejemplo de Bearer Token:**
```
AAAAAAAAAAAAAAAAAAAAAA...lTuwPKA
```

### Paso 4: Verificar Funcionamiento

```bash
curl -s "http://localhost:8000/api/ui/trends?sources=twitter" | jq '.trends.twitter'
```

---

## 3️⃣ NEWS API (Noticias en Tiempo Real)

### Paso 1: Registrarse

1. Ve a https://newsapi.org/register
2. Completa el formulario de registro (GRATIS)

### Paso 2: Obtener API Key

1. Una vez registrado, ve a https://newsapi.org/account
2. Verás tu **API Key** en la parte superior
3. Cópialo

### Paso 3: Configurar en .env

```env
NEWS_API_ENABLED=True
NEWS_API_KEY=your-api-key-aqui
NEWS_API_COUNTRY=mx    # Cambia según tu país
NEWS_API_CATEGORY=general
```

**Códigos de país válidos:**
- `mx` = México
- `us` = USA
- `br` = Brasil
- `ar` = Argentina
- [Ver lista completa en docs](https://newsapi.org/docs/endpoints/top-headlines)

**Categorías disponibles:**
```
general, business, entertainment, health, science, sports, technology
```

### Paso 4: Verificar Funcionamiento

```bash
curl -s "http://localhost:8000/api/ui/trends?sources=newsapi" | jq '.trends.newsapi'
```

---

## 4️⃣ RSS FEEDS (Feeds Personalizados - Sin API)

**Estado:** ✅ Habilitado por defecto  
**Costo:** Gratuito  
**Configuración:** Agregar URLs de RSS

### URLs de RSS Populares

```env
RSS_FEEDS_ENABLED=True
RSS_FEED_URLS=https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada,https://www.bbc.com/mundo/feed.xml,https://feeds.bloomberg.com/markets/news.rss,http://rss.cnn.com/rss/edition.rss
```

**Otros feeds útiles:**
- **Reuters:** `https://www.reutersagency.com/feed/`
- **TechCrunch:** `http://feeds.feedburner.com/TechCrunch/`
- **Hacker News:** `https://news.ycombinator.com/rss`
- **Medium:** `https://medium.com/feed/tag/[topic]`

### Paso de Configuración

1. Edita `.env`
2. Modifica `RSS_FEED_URLS` con tus URLs favoritas (separadas por coma)
3. Reinicia contenedor: `docker-compose restart`

### Verificar Funcionamiento

```bash
curl -s "http://localhost:8000/api/ui/trends?sources=rss_feeds" | jq '.trends.rss_feeds'
```

---

## 5️⃣ SERPAPI (Google Search Results)

### Paso 1: Registrarse

1. Ve a https://serpapi.com/
2. Haz click en **"Sign up"** (GRATIS - 100 búsquedas/mes)

### Paso 2: Obtener API Key

1. Login a tu dashboard: https://serpapi.com/dashboard
2. Verás tu **API Key** en la parte superior
3. Cópialo

### Paso 3: Configurar en .env

```env
SERPAPI_ENABLED=True
SERPAPI_API_KEY=your-api-key-aqui
```

### Paso 4: Verificar Funcionamiento

```bash
curl -s "http://localhost:8000/api/ui/trends?sources=serpapi" | jq '.trends.serpapi'
```

---

## ⚙️ CONFIGURACIÓN COMPLETA DE .env

```env
# ============================================================================
# GOOGLE TRENDS (Sin configuración - habilitado por defecto)
# ============================================================================
GOOGLE_TRENDS_ENABLED=True

# ============================================================================
# TWITTER/X API v2
# ============================================================================
TWITTER_API_ENABLED=True
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAA...lTuwPKA

# ============================================================================
# NEWS API
# ============================================================================
NEWS_API_ENABLED=True
NEWS_API_KEY=a1b2c3d4e5f6g7h8i9j0
NEWS_API_COUNTRY=mx
NEWS_API_CATEGORY=general

# ============================================================================
# RSS FEEDS
# ============================================================================
RSS_FEEDS_ENABLED=True
RSS_FEED_URLS=https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada,https://www.bbc.com/mundo/feed.xml

# ============================================================================
# SERPAPI
# ============================================================================
SERPAPI_ENABLED=True
SERPAPI_API_KEY=xyz123abc456def789

# ============================================================================
# CACHE
# ============================================================================
TRENDS_CACHE_TTL=3600
TRENDS_MAX_RESULTS=20
```

---

## 🧪 TESTING DEL SISTEMA

### 1. Ver todas las fuentes (combinadas)

```bash
curl "http://localhost:8000/api/ui/trends?flatten=1"
```

**Respuesta:**
```json
{
  "status": "success",
  "trends": [
    {"title": "...", "source": "Google Trends", "score": 100, ...},
    {"title": "...", "source": "Twitter/X", "score": 95, ...},
    ...
  ],
  "total": 15,
  "sources": ["google_trends", "twitter", "newsapi", "rss_feeds"],
  "from_sources": "combined"
}
```

### 2. Ver fuentes individuales

```bash
curl "http://localhost:8000/api/ui/trends?flatten=0"
```

**Respuesta:**
```json
{
  "status": "success",
  "trends": {
    "google_trends": [{...}, {...}],
    "twitter": [{...}],
    "newsapi": [{...}, {...}],
    "rss_feeds": [{...}, {...}, {...}]
  },
  "sources": ["google_trends", "twitter", "newsapi", "rss_feeds"]
}
```

### 3. Forzar refresh (bypass cache)

```bash
curl "http://localhost:8000/api/ui/trends?force=1&flatten=1"
```

### 4. Solo una fuente específica

```bash
curl "http://localhost:8000/api/ui/trends?sources=twitter,newsapi"
```

---

## 🔄 REINICIAR CON NUEVAS CONFIGURACIONES

Después de cambiar `.env`:

```bash
# Opción 1: Reiniciar contenedor
docker-compose restart

# Opción 2: Reconstruir completamente
docker-compose down
docker-compose up -d --build

# Verificar que está corriendo
docker-compose ps
```

---

## ✅ CHECKLIST DE CONFIGURACIÓN

- [ ] Copié `.env.example` a `.env`
- [ ] Habilitué Google Trends (`GOOGLE_TRENDS_ENABLED=True`)
- [ ] Agregué mi **Twitter Bearer Token** (OPTIONAL)
- [ ] Agregué mi **News API Key** (OPTIONAL)
- [ ] Configuré URLs de **RSS Feeds** (OPTIONAL)
- [ ] Agregué **SerpAPI Key** (OPTIONAL)
- [ ] Reinicié el contenedor
- [ ] Probé `/api/ui/trends` en el navegador
- [ ] Clickeé "Actualizar" en el dashboard para probar

---

## 🐛 TROUBLESHOOTING

### Error: "Google Trends HTTP 404"
**Causa:** Google bloqueó la solicitud temporalmente  
**Solución:** El sistema reintenta 3 veces con backoff automático. Es normal ocasionalmente.

### Error: "Twitter API unauthorized"
**Causa:** Bearer Token inválido o expirado  
**Verificar:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.twitter.com/2/tweets/search/recent?query=test
```

### Error: "News API key invalid"
**Causa:** API key incorrecto o alcanzó límite diario  
**Verificar:** Ve a https://newsapi.org/account y copia la key nuevamente

### Trends no aparecen
**Verificar:**
1. Contenedor está corriendo: `docker-compose ps`
2. Logs del contenedor: `docker-compose logs`
3. Configuración en `.env` es correcta
4. Reiniciaste después de cambiar `.env`

---

## 📊 MONITOREO DE FUENTES

### Ver logs en tiempo real

```bash
docker-compose logs -f app
```

**Buscar errores de trends:**
```bash
docker-compose logs | grep -i trends
docker-compose logs | grep -i "Google Trends"
docker-compose logs | grep -i "Twitter"
```

### Estadísticas de uso

Endpoint: `/api/ui/metrics` (si está habilitado)

---

## 💡 RECOMENDACIONES

1. **Comienza con:** Google Trends + RSS Feeds (sin API keys)
2. **Luego agrega:** Twitter Bearer Token (fácil de obtener)
3. **Finalmente:** News API + SerpAPI (opcionales)

---

## 📝 NOTAS IMPORTANTES

- Todas las integraciones tienen **cache de 1 hora** por defecto
- El botón "Actualizar" en dashboard fuerza refresh: `?force=1`
- Las fuentes se intentan en paralelo, fallos no afectan otras fuentes
- Respuestas se combinan y ordenan por score

---

**Última actualización:** 8 de Diciembre de 2025  
**Versión:** 2.0 (Multi-source Trends)
