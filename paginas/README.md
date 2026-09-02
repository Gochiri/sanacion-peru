# Páginas del funnel — HTML para pegar en GHL

Cada archivo es un bloque completo (estilos + marcado) para pegar en un elemento
**Custom Code / HTML** de una página de funnel de GHL.

## Estado

| Página | Archivo | Estado |
|---|---|---|
| Registro ES | `registro-es.html` | ✅ lista para revisar |
| Evento ES | — | pendiente |
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
| `URL_LOGO` | Subir el logo a Media de GHL y pegar su URL |
| `URL_FOTO_CHRISTIE`, `URL_FOTO_LUCA` | **Fotos reales.** Sin foto del creador la conversión cae en LATAM, y poner stock es peor que no poner nada |
| `PENDIENTE_BIO_CHRISTIE`, `PENDIENTE_BIO_LUCA` | Dos o tres líneas que escriban ellos, con datos reales |

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
