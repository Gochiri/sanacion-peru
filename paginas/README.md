# Páginas del funnel — HTML para pegar en GHL

Cada archivo es un bloque completo (estilos + marcado) para pegar en un elemento
**Custom Code / HTML** de una página de funnel de GHL.

## Estado

| Página | Archivo | Estado |
|---|---|---|
| Registro ES | `registro-es.html` | ✅ lista para revisar |
| Evento ES | `evento-es.html` | ✅ lista para revisar |
| Gracias ES | — | pendiente |
| Postulación ES | — | pendiente |
| Comienza aquí ES | — | pendiente |
| Réplicas IT (5) | — | pendientes · copy lo produce y valida Luca (P-13/B4) |

## Hallazgo al empezar

**No existía ningún funnel en la subcuenta** (`/funnels/funnel/list` → `count: 0`), y
`link_registro_es` apuntaba al **widget pelado de la encuesta**
(`api.leadconnectorhq.com/widget/survey/…`). Es decir: el tráfico de anuncios caía en un
formulario sin promesa, sin contexto y sin nada que generara confianza — en nicho salud, donde
la desconfianza es la objeción principal. Esa sola diferencia justifica la página.

Al publicar, **actualizar `link_registro_es`** con la URL de la nueva página.

## Reglas que sigue el HTML

- **Reset del builder de GHL**: neutraliza `.c-section`, `.c-row`, `.c-column` y demás
  contenedores, que si no encajonan el diseño. Adaptado a fondo oscuro.
- **Full-bleed** con `margin-left:calc(50% - 50vw)`, secciones a todo el ancho y wrap interno.
- **Clases con prefijo `sc-`**: nunca `.container`, `.content`, `.section`, `.row`, `.column`,
  que chocan con las del builder.
- Tipografía y paddings fluidos con `clamp()`; `overflow-x:clip` (no `hidden`, que rompe sticky).

## Diseño

Editorial sobre fondo oscuro. Negro cálido `#0E0C0A` + el oro del logo `#D4A24C` + hueso
`#F2EDE4`. **Fraunces** display + **Manrope** cuerpo + **JetBrains Mono** etiquetas.
Reglas finas doradas entre secciones, números grandes como anclas, capitular en la sección
de prosa.

**El fondo oscuro no es preferencia:** los logos entregados traen el negro incrustado
(checklist B8). Sobre fondo claro el logo aparecería dentro de un recuadro negro. Cuando manden
el vectorial o el PNG transparente se puede replantear.

## Lo que falta reemplazar antes de publicar

| Placeholder | Qué poner |
|---|---|
| `URL_FOTO_CHRISTIE`, `URL_FOTO_LUCA` | **Fotos reales.** Sin foto del creador la conversión cae en LATAM, y poner stock es peor que no poner nada |
| `PENDIENTE_BIO_CHRISTIE`, `PENDIENTE_BIO_LUCA` | Dos o tres líneas que escriban ellos, con datos reales |

**El logo ya no es un placeholder.** Sale de `{{custom_values.logo_url}}`, así que se cambia en
un solo sitio y se actualiza en todas las páginas a la vez. Los dos que subió el cliente están
cargados: `logo_url` (el que se usa) y `logo_url_alt` (el otro). Si el que se ve no es el
horizontal, se intercambian los dos valores y listo — sin tocar ningún HTML.

⚠️ Los dos llegaron en **JPEG**, que no admite transparencia: el fondo negro sigue incrustado.
El tema oscuro se mantiene por eso.

**Fechas y horas se rellenan solas** desde `{{custom_values.fecha_evento_es}}` y
`{{custom_values.hora_evento_pe}}`: al cargar esos valores, la página queda completa.

## Decisiones que conviene conocer

- **La encuesta va embebida como iframe de GHL, a propósito.** Lo normal sería un formulario
  propio con POST, pero el envío de esta encuesta es el **disparador de WF2**. Cambiarla por un
  formulario propio dejaría el flujo entero sin trigger.
- **Sin cuenta atrás.** Sin fecha real sería urgencia inventada, y la fecha aún no está.
  Cuando llegue, el contador va en la página del evento, que es donde tiene sentido.
- **Sin testimonios.** No hay ninguno con nombre y foto (checklist B6). Un testimonio anónimo
  o inventado hace más daño que su ausencia.
- **Sin CTA de WhatsApp.** En LATAM suele ser el canal principal, pero aquí competiría con el
  único objetivo de la página, que es el registro. El grupo de WhatsApp llega después, al
  registrarse.
- **Píxel y Open Graph no van en el HTML**: se configuran en los ajustes del funnel de GHL.


---

## Evento ES — notas propias

Es una **sala**, no una página de venta: el video manda y todo lo demás se aparta. Barra fina
arriba, reproductor a lo ancho, y bajo él una sola acción.

### Se configura sola entre lanzamientos

Nada de lo variable está escrito en el HTML. Cada ciclo solo se actualizan custom values:

| Valor | Qué poner |
|---|---|
| `embed_youtube_es` | `https://www.youtube.com/embed/XXXXXXXXXXX` del video **no listado** |
| `fecha_evento_es_iso` | `2026-09-12T20:00:00-05:00` — mueve la cuenta atrás |
| `link_postulacion_es` | URL de la página de postulación (destino del CTA) |

### La cuenta atrás no se inventa

Lee `fecha_evento_es_iso`. Si el valor no está cargado —o dice `PENDIENTE`, o GHL no lo
sustituye— la fecha no parsea y la página **se queda en «Preparando la transmisión»** en vez de
mostrar un contador falso. Al llegar la hora cambia sola a «En vivo ahora» y para el reloj.

### En los ajustes del funnel

- **NOINDEX.** La página se reparte solo por el link 1:1 que manda WF3, y eso es lo que permite
  medir quién asistió. Si se indexa, el link deja de significar nada.
- Píxel y Open Graph van ahí también, no en el HTML.

### Urgencia real, no inventada

El aviso dice lo que de verdad pasa —la clase no queda grabada y la página se cierra al terminar
el ciclo— sin poner una fecha límite que nadie ha confirmado.
