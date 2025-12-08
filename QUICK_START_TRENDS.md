# ⚡ GUÍA RÁPIDA - PRIMEROS PASOS

## En 5 minutos: Activar RSS Feeds (ya funciona)

```bash
# 1. Abrir dashboard
http://localhost:8000/dashboard

# 2. Click en "Actualizar" en la sección Tendencias
# → Verás noticias reales de El País, BBC, Bloomberg

# 3. Click en una noticia → "Seleccionar"
# → Va al pipeline con ese trend
```

**Resultado:** ✅ Funcionando ahora mismo

---

## En 15 minutos: Agregar Twitter

```bash
# 1. Ve a: https://developer.twitter.com/en/portal/dashboard

# 2. Crea app (si no tienes)
# → "Create new app" → Completa datos → Env: Production

# 3. Ve a "Keys and tokens"
# → Copia "Bearer Token"

# 4. Edita .env en tu PC
nano .env

# Agrega:
TWITTER_API_ENABLED=True
TWITTER_BEARER_TOKEN=AAAA...

# 5. Reinicia contenedor
docker-compose restart

# 6. Probar
curl "http://localhost:8000/api/ui/trends?sources=twitter"
```

**Resultado:** ✅ Trending topics de Twitter en México

---

## En 20 minutos: Agregar News API

```bash
# 1. Ve a: https://newsapi.org/register

# 2. Regístrate (GRATIS)

# 3. Ve a: https://newsapi.org/account
# → Copia API Key

# 4. Edita .env
nano .env

# Agrega:
NEWS_API_ENABLED=True
NEWS_API_KEY=a1b2c3d4e5f6g7h8i9j0

# 5. Reinicia
docker-compose restart

# 6. Probar
curl "http://localhost:8000/api/ui/trends?sources=newsapi"
```

**Resultado:** ✅ Top headlines en tiempo real

---

## Probar Todas Las Fuentes

```bash
# Ver todas combinadas y ordenadas
curl "http://localhost:8000/api/ui/trends?flatten=1&limit=10"

# Ver por fuente individual
curl "http://localhost:8000/api/ui/trends?flatten=0"

# Solo una fuente específica
curl "http://localhost:8000/api/ui/trends?sources=google_trends"

# Forzar actualización (sin caché)
curl "http://localhost:8000/api/ui/trends?force=1"
```

---

## Ver Logs en Tiempo Real

```bash
# Terminal 1: Ver logs
docker-compose logs -f

# Terminal 2: Hacer request
curl "http://localhost:8000/api/ui/trends?force=1"

# Verás en logs qué fuentes se activaron, cuáles fallaron, etc.
```

---

## Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `.env` | Tus API keys aquí |
| `.env.example` | Template con explicaciones |
| `config.py` | Todas las variables leídas de .env |
| `services/multi_trends_service.py` | Lógica de integraciones |
| `routes/ui_routes.py` | Endpoint `/api/ui/trends` |
| `TRENDS_SETUP.md` | Guía completa paso a paso |
| `BEFORE_AFTER_COMPARISON.md` | Qué cambió |

---

## Checklist

- [ ] Dashboard carga y muestra "Actualizar"
- [ ] RSS Feeds funcionan (verás noticias de El País)
- [ ] Clickeé "Actualizar" y se actualizó
- [ ] Leí TRENDS_SETUP.md
- [ ] Agregué Twitter Bearer Token a .env
- [ ] Agregué News API Key a .env
- [ ] Reinicié contenedor: `docker-compose restart`
- [ ] Probé `/api/ui/trends?flatten=1` en curl
- [ ] Todos los trends aparecen en dashboard

---

## URLs de Configuración Rápida

**Paso 1: Twitter**  
https://developer.twitter.com/en/portal/dashboard  
→ Copiar Bearer Token

**Paso 2: News API**  
https://newsapi.org/register  
→ Registrarse → Copiar API Key

**Paso 3: SerpAPI (opcional)**  
https://serpapi.com/  
→ Sign up → Copiar API Key

---

## Troubleshooting Rápido

**Q: No veo tendencias**  
A: Verifica logs → `docker-compose logs | grep -i trends`

**Q: "Google Trends HTTP 404"**  
A: Normal, Google lo bloquea. Sistema reintenta 3 veces automáticamente.

**Q: Twitter no funciona**  
A: Bearer Token inválido. Verifica en https://developer.twitter.com/en/portal/dashboard

**Q: News API no funciona**  
A: API Key expirada o alcanzó límite diario. Verifica en https://newsapi.org/account

**Q: RSS feeds lentos**  
A: Algunos feeds son lentos. Cámbia URLs en .env por feeds más rápidos.

---

## Performance

| Operación | Tiempo |
|-----------|--------|
| Dashboard carga | <1s (caché) |
| Click "Actualizar" | 5-10s (APIs reales) |
| Siguiente click | <1s (caché 1h) |
| Fuerza refresh | 5-10s (bypass caché) |

---

## Siguiente Paso: Documentación Completa

Lee `TRENDS_SETUP.md` para:
- Explicación detallada de cada API
- URLs de RSS feeds útiles
- Comandos de testing completos
- Troubleshooting avanzado

**Ruta recomendada:**
1. Prueba RSS (funciona ahora)
2. Lee TRENDS_SETUP.md (15 min)
3. Agrega Twitter (5 min)
4. Agrega News API (5 min)
5. Personaliza RSS feeds (10 min)
6. ¡Listo!

---

**Última actualización:** 8 de Diciembre de 2025  
**Preguntas?** Consulta `TRENDS_SETUP.md` o `MULTI_TRENDS_IMPLEMENTATION.md`
