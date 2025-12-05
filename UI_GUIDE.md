# SIA-R Dashboard - Guía de Usuario de la Interfaz Web

## Descripción General

La interfaz web de SIA-R es una plataforma completa para gestionar, monitorear y controlar el pipeline de procesamiento de noticias. Proporciona un panel de control intuitivo, herramientas de revisión de contenido, y configuración avanzada de auto-publicación.

## Características Principales

- **Panel de Control (Dashboard)**: Vista general de estadísticas en tiempo real
- **Revisor de Artículos**: Sistema de aprobación/rechazo de contenido
- **Ejecutor de Pipeline**: Procesar artículos manualmente
- **Historial de Publicaciones**: Gestión de artículos publicados en WordPress
- **Logs de Ejecución**: Historial detallado de todas las ejecuciones
- **Métricas y Estadísticas**: Análisis de desempeño del sistema
- **Configuración**: Gestión de parámetros de auto-publicación y permisos

---

## Páginas de la Interfaz

### 1. Login (`/login`)

**Descripción**: Página de autenticación para acceder a la plataforma.

**Funcionalidades**:
- Ingreso con credenciales de usuario
- Generación de token JWT automático
- Almacenamiento seguro del token en localStorage
- Redirección automática al dashboard tras login exitoso
- Modo oscuro disponible

**Uso**:
```bash
# Acceder a la página
http://localhost:8000/login
```

---

### 2. Dashboard (`/dashboard`)

**Descripción**: Panel de control principal con estadísticas y acciones rápidas.

**Componentes**:
- **Tarjetas de Estadísticas**:
  - Total de artículos procesados (últimos 7 días)
  - Tasa de éxito del pipeline
  - Calidad promedio
  - Artículos pendientes de revisión

- **Tabla de Revisiones Pendientes**:
  - Listado de artículos en revisión
  - Acciones rápidas: Aprobar/Rechazar
  - Enlace a vista detallada de revisión

- **Artículos Recientes Publicados**:
  - Últimos artículos publicados en WordPress
  - Información de categoría y fecha

- **Gráficos**:
  - Distribución por categoría
  - Calidad promedio por categoría
  - Tendencias de procesamiento

**Uso**:
```bash
http://localhost:8000/dashboard
```

---

### 3. Revisor de Artículos (`/review/view/<id>`)

**Descripción**: Vista detallada para revisar y aprobar/rechazar artículos.

**Funcionalidades**:
- Visualización completa del contenido del artículo
- Métricas de calidad y riesgo
- Categorías y tags detectados
- Botones de acción: Aprobar o Rechazar
- Comparación con versión original (si aplica)

**Flujo de Revisión**:
1. Ver contenido procesado
2. Revisar métricas de calidad
3. Verificar categorías y tags
4. Tomar decisión: Aprobar o Rechazar
5. Si rechaza: ingresar motivo
6. Retornar al dashboard

**Parámetros URL**:
- `review_id`: ID único del artículo en revisión

---

### 4. Ejecutor de Pipeline (`/pipeline/run`)

**Descripción**: Herramienta para procesar nuevos artículos manualmente.

**Campos de Entrada**:
- **Título**: Título del artículo (mín. 5 caracteres)
- **Contenido**: Cuerpo del artículo (mín. 50 palabras)
- **Autor**: Nombre del autor (opcional)
- **URL Fuente**: Enlace al artículo original (opcional)
- **Categoría**: Selección de categoría o auto-detección

**Opciones Avanzadas**:
- ☐ Saltar limpieza de texto
- ☐ Saltar humanización

**Proceso**:
1. Completar formulario con datos del artículo
2. Hacer clic en "Ejecutar Pipeline"
3. Ver progreso de ejecución
4. Revisar resultados en modal emergente
5. Guardar para revisión o descartar

**Resultados Mostrados**:
- Puntuación de calidad (%)
- Riesgo de factualidad (%)
- Categorías detectadas
- Tags generados
- Vista previa del contenido procesado

---

### 5. Artículos Publicados (`/published`)

**Descripción**: Gestión de todos los artículos publicados en WordPress.

**Funcionalidades**:
- Listado paginado de artículos
- Búsqueda por título
- Filtro por categoría
- Ordenamiento por fecha/título
- Visualización de vistas (views)
- Botones de acción: Ver | Eliminar

**Información Mostrada**:
- Título del artículo
- Categoría
- Autor
- Fecha de publicación
- Número de vistas
- Enlace a WordPress

**Filtros**:
- Búsqueda por título
- Por categoría
- Ordenamiento personalizado

---

### 6. Logs de Ejecución (`/logs`)

**Descripción**: Historial detallado de todas las ejecuciones del pipeline.

**Información Registrada**:
- Fecha y hora de ejecución
- Artículo procesado
- Estado: Exitoso | Fallido | Pendiente
- Tiempo de ejecución (ms)
- Puntuación de calidad
- Mensaje de error (si aplica)

**Funcionalidades**:
- Búsqueda por nombre de artículo
- Filtro por estado
- Filtro por fecha
- Vista detallada por log
- Eliminar logs individuales
- Limpiar todos los logs

**Detalles del Log**:
- Información completa de ejecución
- Etapas completadas
- Métricas de calidad
- Mensaje de error completo
- Botón para reintentar ejecución

---

### 7. Métricas y Estadísticas (`/metrics`)

**Descripción**: Análisis detallado del rendimiento del pipeline.

**Períodos Disponibles**:
- Últimos 7 días
- Últimos 30 días
- Últimos 90 días
- Todo el tiempo

**Métricas Principales**:
- **Artículos Procesados**: Total en el período
- **Tasa de Éxito**: Porcentaje de ejecuciones exitosas
- **Calidad Promedio**: Puntuación media
- **Tiempo Promedio**: Tiempo de ejecución

**Gráficos**:
1. **Distribución por Categoría** (Gráfico de rosca)
   - Muestra cantidad de artículos por categoría
   - Porcentaje del total

2. **Calidad por Categoría** (Gráfico de barras)
   - Puntuación promedio de calidad
   - Escalas de 0 a 100%

3. **Tendencia de Procesamiento** (Gráfico de línea)
   - Evolución del número de artículos por día
   - Identifica picos de actividad

**Tablas Adicionales**:
- **Top Categorías**: Las 5 categorías con más artículos
- **Problemas Comunes**: Errores frecuentes y su frecuencia

---

### 8. Configuración (`/settings`)

**Descripción**: Panel de administración para configurar comportamientos del sistema.

#### 8.1 Auto-publicación

**Parámetros**:
- **Activar Auto-publicación**: Toggle para activar/desactivar
- **Puntuación Mínima de Calidad**: Slider 0-100% (default: 75%)
- **Puntuación Máxima de Riesgo**: Slider 0-100% (default: 30%)
- **Puntuación Mínima SEO**: Slider 0-100% (default: 60%)

**Categorías Permitidas**:
- ☐ Tecnología
- ☐ Política
- ☐ Economía
- ☐ Deportes
- ☐ Salud

**Lógica**:
Un artículo será auto-publicado si:
1. Auto-publicación está activada
2. Calidad >= Umbral configurado
3. Riesgo <= Umbral configurado
4. SEO >= Umbral configurado
5. Categoría está en lista permitida

#### 8.2 Permisos y Roles

**Roles Disponibles**:

| Rol | Ver Panel | Revisar | Publicar | Configurar |
|-----|-----------|---------|----------|------------|
| **Editor** | ✓ | ✓ | ✗ | ✗ |
| **Publicador** | ✓ | ✓ | ✓ | ✗ |
| **Administrador** | ✓ | ✓ | ✓ | ✓ |

**Asignación**:
- Los roles se asignan automáticamente desde WordPress
- Los permisos se verifican en cada acción

#### 8.3 Notificaciones

**Opciones**:
- ☑ Notificar cuando termina el procesamiento
- ☑ Notificar en caso de error
- ☑ Notificar cuando se publica automáticamente
- Email para notificaciones

#### 8.4 Integraciones

**WordPress**:
- URL de WordPress
- Token de autenticación
- Botón para probar conexión

**OpenAI API**:
- Clave de API
- Botón para probar conexión
- Nota: La clave no se almacena en BD

---

## API REST - Endpoints de UI

### Estructura de Autenticación

Todos los endpoints requieren token JWT:

```http
Authorization: Bearer <token>
```

### Endpoints Disponibles

#### Status y Dashboard
```
GET /api/ui/status
```
Obtiene estado general del dashboard.

```json
{
  "status": "operational",
  "stats": { /* estadísticas */ },
  "pending_reviews": 5
}
```

#### Revisiones
```
GET /api/ui/reviews?status=pending&limit=20
```
Obtiene artículos en revisión.

```
GET /api/ui/review/<id>
```
Obtiene detalles de un artículo específico.

```
POST /api/ui/review/<id>/approve
```
Aprueba un artículo para publicación.

```
POST /api/ui/review/<id>/reject
```
Rechaza un artículo.

```json
{
  "reason": "Contenido duplicado"
}
```

#### Artículos Publicados
```
GET /api/ui/published?limit=50
```
Obtiene artículos publicados en WordPress.

#### Configuración
```
GET /api/ui/settings
```
Obtiene configuración actual (solo administrador).

```
POST /api/ui/settings
```
Actualiza configuración.

#### Métricas
```
GET /api/ui/metrics?period=7d
```
Obtiene métricas y estadísticas.

Períodos: `7d`, `30d`, `90d`, `all`

#### Logs
```
GET /api/ui/logs?limit=50&offset=0
```
Obtiene historial de ejecuciones.

```
DELETE /api/ui/logs/<id>
```
Elimina un log específico.

```
POST /api/ui/logs/clear
```
Elimina todos los logs.

#### Ejecutar Pipeline
```
POST /api/ui/run
```
Ejecuta el pipeline manualmente.

```json
{
  "title": "Nuevo Artículo",
  "content": "Contenido del artículo...",
  "author": "Nombre del Autor",
  "url": "https://fuente.com/articulo",
  "category": "Tecnología"
}
```

---

## Características Especiales

### Modo Oscuro

**Activación**:
1. Hacer clic en el botón de tema en la navbar
2. La preferencia se guarda en localStorage
3. Se sincroniza automáticamente en todas las páginas

**Estilos**:
- Fondo oscuro (#1a1a1a)
- Texto claro para mejor legibilidad
- Contraste mejorado en elementos interactivos

### Notificaciones Toast

Mensajes de confirmación y error aparecen como notificaciones:
- **Verde**: Éxito
- **Rojo**: Error
- **Amarillo**: Advertencia
- **Azul**: Información

Se cierran automáticamente después de 5 segundos.

### Responsive Design

- **Desktop**: Diseño completo de columnas múltiples
- **Tablet**: Adaptación para pantallas medianas
- **Mobile**: Navegación vertical, tablas simplificadas

---

## Atajos de Teclado

*(Pueden agregarse en futuras versiones)*

- `Ctrl + K`: Búsqueda rápida
- `?`: Mostrar ayuda

---

## Troubleshooting

### "No estoy autenticado"

**Solución**: 
- Ir a `/login`
- Ingresar credenciales
- Asegurar que el token se guarda en localStorage

### "Error 403 - Insufficient permissions"

**Causa**: Tu rol no tiene permisos para esta acción.

**Solución**:
- Contacta al administrador
- Verifica tu rol en WordPress

### "Artículo no cargando en dashboard"

**Solución**:
- Recargar página (F5)
- Limpiar caché del navegador
- Verificar conexión a internet

### "Logs desaparecieron"

**Causas posibles**:
- Alguien ejecutó "Limpiar todos los logs"
- Base de datos se reinició
- Error de base de datos

**Prevención**: Regular auditoría de permisos

---

## Mejores Prácticas

1. **Revisión de Artículos**:
   - Revisar calidad del contenido procesado
   - Verificar que las categorías son correctas
   - Rechazar si el contenido no es de calidad

2. **Configuración de Auto-publicación**:
   - Empezar conservador (umbrales altos)
   - Reducir gradualmente según resultados
   - Monitorear regularmente las métricas

3. **Gestión de Logs**:
   - Guardar logs importantes antes de limpiar
   - Limpiar regularmente para mejor rendimiento
   - Revisar errores frecuentes

4. **Seguridad**:
   - No compartir tokens JWT
   - Cerrar sesión al terminar
   - Cambiar contraseña regularmente

---

## Próximas Características

- [ ] Exportar reportes a PDF/Excel
- [ ] Programador de ejecuciones automáticas
- [ ] Webhooks personalizados
- [ ] Estadísticas avanzadas
- [ ] Integración con Google Analytics
- [ ] API pública para desarrolladores
- [ ] Soporte multi-idioma

---

## Soporte

Para reportar problemas o sugerencias:
1. Verificar documentación técnica en `manual_tecnico.md`
2. Revisar logs de error en `/logs`
3. Contactar al equipo de desarrollo
