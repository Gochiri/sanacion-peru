# SOP · Llamada de cierre y pago manual

Los dos procedimientos que van juntos: lo que hace el que cierra durante la llamada, y lo que
hace cuando la plata llega. Son las subtareas 1 y 2 de ENT-01.

**Dos dueños, no uno.** Por K11 **Joaquín cierra el mercado español y Luca el italiano**. La
documentación anterior dice «Luca» en todos lados porque es previa a esa decisión.

> **Por qué esto es un SOP y no un workflow.** El embudo automatizado termina en el recordatorio
> de la cita (WF4C). De ahí en adelante decide una persona, y el sistema solo reacciona a lo que
> esa persona marca. Por §12 los compradores por transferencia llevan *«tareas + plantilla de
> recordatorio de cobro, no automatización de mora»*: nadie persigue por WhatsApp a quien todavía
> está decidiendo.

---

## SOP 1 · La llamada de cierre

### Antes de entrar

Abrir el contacto en GHL y leer su postulación. Está todo ahí: qué le pasa, qué intentó, cuánto
puede invertir. Entrar sin leerla es empezar preguntando lo que ya contestó.

### Durante

Nada que tocar en el sistema. La llamada es la llamada.

Una sola cosa del guion es técnica y no se puede improvisar:

> **El plan en cuotas requiere tarjeta.**

Sin tarjeta guardada en el primer cobro, las cuotas 2 y 3 no se cobran solas: quedan en
recordatorios y alguien tiene que perseguirlas a mano. Si la persona no va a poner tarjeta, la
conversación es **contado**, no cuotas.

### Al colgar — tres cosas, en este orden

**1 · Mover la oportunidad a «Llamada realizada».**
Aunque no haya cerrado. La etapa registra que la llamada ocurrió; el resultado se ve después
por el estado de la oportunidad.

**2 · Fijar `Plan pago`** — `Contado`, `2 cuotas` o `3 cuotas`.
Este campo **no se deduce del cobro**: si no se pone a mano, queda vacío y nadie sabe después
qué se acordó. Es el campo `contact.plan_pago`.

**3 · Mandar la plantilla de cobro del mercado que corresponda.**

| Mercado | Plantilla | Cierra |
|---|---|---|
| Perú / LATAM | `datos_pago_es` | Joaquín |
| Italia | `datos_pago_it` | Luca |

Los datos van escritos dentro de la plantilla — no hay que copiarlos de ningún lado ni tipear
el CCI. Si por lo que sea hace falta el bloque suelto, está en los custom values
`datos_pago_pe` y `datos_pago_it`.

### Si dijo que sí y no transfiere

**Tarea asignada al que cerró, no secuencia automática.** Se le escribe o se le llama. Un
recordatorio automático pidiendo plata a alguien que todavía lo está pensando es cómo se pierde
una venta de $1.000.

---

## SOP 2 · Pago manual

Esta es la ruta principal de cobro, no un caso raro: por D10 el mercado peruano cae casi al
100 % por acá, y hoy los links de Stripe todavía no existen.

### El único paso

**Confirmar en el banco que la plata llegó. Después, y solo después, poner la etiqueta
`pago-manual` en el contacto.**

### Por qué el orden importa

La etiqueta **no se deshace**. Al ponerla arranca WF5 y en el mismo golpe:

- registra `Producto comprado = Escuela` y `Estado pago = Al día`
- marca `primer-pago-procesado`
- **cierra la oportunidad como Ganado**
- **avisa a Luca para dar de alta en System.io** — o sea, se le crea el acceso al alumno
- si fue contado, activa el bono y avisa a Christie por la sesión de 40 minutos
- **manda un evento Purchase a Meta**, que es con lo que el algoritmo aprende a quién buscar

Etiquetar antes de ver el dinero le da acceso a alguien que no pagó y le enseña a Meta a
buscar gente que no compra. Las dos cosas cuestan caro y ninguna se revierte con quitar la
etiqueta.

### Las cuotas siguientes

Se etiqueta igual. WF5 lo detecta —ya está `primer-pago-procesado`— y toma el camino corto:
marca `cuota-adicional` y avisa a Luca de que entró una cuota, **sin** reabrir la venta ni
mandar otro Purchase. No hay nada extra que hacer.

### Comprobante que no cuadra

Si el monto no coincide o el comprobante es dudoso: **no etiquetar**. Resolverlo primero. Es
más fácil cobrar una diferencia antes de dar el acceso que después.

---

## Lo que hace el sistema solo, para no repetirlo a mano

| Después de… | Se encarga | Nadie tiene que |
|---|---|---|
| Agendar la cita | WF4C | Confirmar ni recordar la llamada |
| Poner `pago-manual` | WF5 | Mover a Ganado, avisar a Luca o a Christie, mandar el Purchase |

Lo que sí queda en manos de una persona: la etapa *Llamada realizada*, el campo `Plan pago`,
mandar la plantilla de cobro, y confirmar que el dinero llegó.
