# Manual del Usuario - SIA-R News Engine

## Guía Rápida para Redactores y Publicadores

### ¿Qué es SIA-R?

SIA-R es un asistente inteligente de IA que:
- ✅ Mejora automáticamente la calidad de tus artículos
- ✅ Optimiza para motores de búsqueda (SEO)
- ✅ Verifica hechos automáticamente
- ✅ Publica directamente en WordPress
- ✅ Aprende de tus patrones de publicación

## Inicio Rápido en 5 Pasos

### Paso 1: Acceder al Sistema

1. Abrir navegador: `http://localhost:8000`
2. O usar la API directamente

### Paso 2: Iniciar Sesión

```
URL: POST http://localhost:8000/api/auth/login
Email: tu@email.com
Contraseña: tu_contraseña
```

Recibirás un **token JWT** para futuras solicitudes.

### Paso 3: Preparar tu Artículo

Tener listo:
- **Título**: Máximo 100 caracteres, descriptivo
- **Contenido**: Mínimo 50 caracteres (sin límite superior)

Ejemplo:
```
Título: "Nuevas medidas de seguridad en la capital"
Contenido: "El gobierno anunció hoy un plan integral 
de seguridad que incluye 500 nuevos policías..."
```

### Paso 4: Enviar para Procesamiento

```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN_AQUI" \
  -d '{
    "title": "Tu título",
    "content": "Tu contenido...",
    "auto_publish": false
  }'
```

### Paso 5: Revisar y Publicar

El sistema retorna:
- ✅ Texto mejorado
- ✅ Puntuación de calidad (0-100)
- ✅ Categorías y tags sugeridos
- ✅ Meta descripción para SEO

Si todo se ve bien, publicar en WordPress.

## Flujo Completo de Uso

### 1. Login

```
POST /api/auth/login

Enviar:
{
  "email": "tu@email.com",
  "password": "contraseña"
}

Recibes:
{
  "access_token": "eyJhbGc...",
  "api_key": "key_abc123..."
}
```

**Guardá este token, lo usarás en todas las solicitudes.**

### 2. Procesar Artículo (Simulación)

Para revisar cambios sin publicar:

```bash
curl -X POST http://localhost:8000/api/pipeline/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi artículo",
    "content": "Contenido aquí..."
  }'
```

Respuesta incluye:
- Texto limpiado y mejorado
- Calidad general (0-1)
- Categorías y tags propuestos
- H1 y meta descripción optimizados

### 3. Revisar Resultados

La respuesta contiene:

```json
{
  "status": "success",
  "final_text": "Texto procesado...",
  "final_categories": ["Política", "Nacional"],
  "final_tags": ["gobierno", "seguridad"],
  "quality_score": 0.87,
  "ready_for_publication": true,
  "warnings": []
}
```

**Significado de quality_score:**
- 0.90-1.0 = Excelente ⭐⭐⭐⭐⭐
- 0.75-0.89 = Muy Bueno ⭐⭐⭐⭐
- 0.60-0.74 = Bueno ⭐⭐⭐
- 0.40-0.59 = Aceptable ⭐⭐
- < 0.40 = Necesita mejoras ⭐

### 4. Publicar en WordPress

Una vez aprobado:

```bash
curl -X POST http://localhost:8000/api/wp/post \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "title": "Nuevas medidas de seguridad",
    "content": "<p>Texto procesado...</p>",
    "categories": ["Política"],
    "tags": ["gobierno"],
    "status": "draft"
  }'
```

**Nota:** Usar `"status": "draft"` para revisar antes de publicar.

### 5. Verificar Estadísticas

```bash
curl -X GET http://localhost:8000/api/wp/stats
```

Ver:
- Artículos procesados
- Tasa de éxito
- Categorías más populares
- Desempeño

## Ejemplos de Uso

### Ejemplo 1: Artículo de Política

**Entrada:**
```
Título: elecciones
Contenido: el gobierno va a hacer elecciones el proximas año
```

**Salida del Pipeline:**
- ✅ Texto limpiado y normalizado
- ✅ Categorías: "Política", "Nacional"
- ✅ Tags: "elecciones", "gobierno"
- ✅ H1 optimizado: "Gobierno convoca elecciones para el próximo año"
- ✅ Quality Score: 0.78

### Ejemplo 2: Artículo de Tecnología

**Entrada:**
```
Título: Nueva IA revoluciona el mercado
Contenido: Una empresa anunció hoy una tecnología 
revolucionaria basada en inteligencia artificial que 
promete cambiar la industria...
```

**Salida:**
- ✅ Categorías: "Tecnología", "Innovación"
- ✅ Tags: "IA", "startup", "tecnología"
- ✅ Quality Score: 0.92 ⭐⭐⭐⭐⭐

## Tips y Mejores Prácticas

### ✅ Haz ESTO

1. **Escribe en tu estilo natural**: El sistema mejorará la prosa

2. **Incluye hechos específicos**: Números, fechas, citas

3. **Estructura clara**: Párrafos cortos, separados

4. **Revisa el resultado**: Aunque SIA-R mejora mucho, siempre revisa

5. **Usa categorías consistentes**: El sistema aprende de tus patrones

### ❌ Evita ESTO

1. **Copiar y pegar desde otras fuentes**: Eso puede flagear plagio

2. **Afirmaciones sin fundamento**: "Todos saben que...", "obviamente..."

3. **Demasiado corto**: Mínimo 50 caracteres, ideal 300+

4. **Información contradictoria**: El sistema lo detectará

5. **Enlaces spam**: Se eliminarán automáticamente

## Entender los Avisos (Warnings)

Cuando ves avisos como estos, significa:

| Aviso | Qué significa | Acción |
|-------|---------------|--------|
| "High fact-check risk" | Posibles afirmaciones sin verificar | Agregar citas o verificar hechos |
| "Content failed verification" | Contradicciones detectadas | Revisar y corregir |
| "Increase keyword density" | SEO débil | Repetir la palabra clave principal |
| "Meta description too short" | SEO incompleto | El sistema lo extenderá automáticamente |
| "Multiple tense shifts" | Cambios de tiempo verbal | Mantener consistencia temporal |

## Preguntas Frecuentes

### P: ¿Cuánto tiempo toma procesar un artículo?
**R:** Típicamente 20-60 segundos, depende del largo y conexión con OpenAI.

### P: ¿Necesito credenciales de WordPress?
**R:** No en el frontend, ya están configuradas en el servidor.

### P: ¿Puedo deshacer una publicación?
**R:** Sí, desde el panel de WordPress como siempre. SIA-R solo publica en draft por defecto.

### P: ¿Qué pasa si el API de OpenAI falla?
**R:** El sistema reintenta automáticamente. Si falla, verás un error después de algunos segundos.

### P: ¿Puedo procesar múltiples artículos a la vez?
**R:** Sí, cada uno se procesa independientemente.

### P: ¿El sistema guarda mis artículos?
**R:** Sí, todos se registran en la base de datos para análisis y aprendizaje.

### P: ¿Cómo se protegen mis datos?
**R:** Todo está encriptado y autenticado con JWT. Solo tú ves tus artículos.

## Formatos de Respuesta

### Success Response (Éxito)

```json
{
  "status": "success",
  "execution_time_ms": 23450,
  "final_text": "Texto procesado...",
  "final_categories": ["Cat1", "Cat2"],
  "final_tags": ["tag1", "tag2"],
  "quality_score": 0.87,
  "ready_for_publication": true,
  "warnings": []
}
```

### Error Response (Error)

```json
{
  "status": "error",
  "error": "Error message here",
  "message": "Descripción del error"
}
```

## Códigos de Estado HTTP

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | OK - Solicitud exitosa | Pipeline completado |
| 201 | Created - Recurso creado | Post publicado en WP |
| 400 | Bad Request - Solicitud inválida | Falta título |
| 401 | Unauthorized - Sin autenticación | Token expirado |
| 500 | Server Error - Error interno | Fallo de OpenAI |

## Cheatsheet de Comandos

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -d '{"email":"user@test.com","password":"pass"}'

# Procesar
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"...","content":"..."}'

# Publicar
curl -X POST http://localhost:8000/api/wp/post \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"...","content":"...","status":"draft"}'

# Status
curl -X GET http://localhost:8000/api/status

# Estadísticas
curl -X GET http://localhost:8000/api/wp/stats
```

## Soporte y Ayuda

### Problemas Comunes

**"Error: Invalid credentials"**
- Verificar email y contraseña
- Solicitar reset de contraseña

**"Error: Connection timeout"**
- Verificar conexión a internet
- Esperar unos segundos y reintentar

**"Article not publishing"**
- Revisar que categorías/tags existan en WordPress
- Verificar permisos de usuario en WordPress

### Contactar Soporte

- Email: support@sia-r.com
- Teléfono: +34-XXX-XXX-XXX
- Chat: https://sia-r.com/chat

---

## Resumen

1. **Login** → Obtén token
2. **Prepara** → Tu artículo
3. **Procesa** → Envía al pipeline
4. **Revisa** → Comprueba calidad
5. **Publica** → A WordPress

¡Listo! Tu artículo está optimizado, verificado y publicado en segundos. 🚀

---

**Última actualización**: 4 de diciembre de 2025
**Versión**: 1.0.0
