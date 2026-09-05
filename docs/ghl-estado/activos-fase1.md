# Activos de Fase 1 — estado tras la respuesta del cliente (18-ago)

## Qué SÍ se puede crear por API (descubierto probando)

| Recurso | Endpoint | Estado |
|---|---|---|
| Calendarios | `POST /calendars/` | ✅ funciona — ⚠️ `openHours` necesita **una entrada por día**: `[{"daysOfTheWeek":[1],...}, {"daysOfTheWeek":[2],...}]`. Un array con varios días da *"must be a valid day of week"* |
| Productos | `POST /products/` | ✅ funciona |
| Precios | `POST /products/{id}/price` | ✅ `one_time` y `recurring` con `totalCycles` |

## Qué NO se puede — va a UI

| Recurso | Por qué |
|---|---|
| **Formularios y encuestas** | `POST /forms/` responde *"This route is not yet supported by the IAM Service"*. En el API interno todas las rutas probadas dan 404/403. **F01 (registro) y F03 (postulación) se hacen en la UI.** |
| **teamMembers del calendario** | **Limitación confirmada del API**: no se aceptan ni en POST ni en PUT, con 6 formas distintas probadas (userId simple, con priority/isPrimary, con meetingLocation, array de strings, con y sin eventType). Siempre queda `[]`. **Se asigna en la UI.** |

---

## Calendario de cierre — Perú ⚠️ provisional

- **id:** `yCYC1PwGWrYRxifCIvBX`
- **link:** https://api.leadconnectorhq.com/widget/booking/yCYC1PwGWrYRxifCIvBX
- 30 min · buffer 15 min · máx 6/día · lun-vie 9:00-18:00 · reserva con 2 h de antelación

**Dos cosas lo dejan incompleto:**

1. ~~Luca no existe como usuario~~ → ✅ **resuelto el 18-ago**: Luca Stefanizzi ya es usuario
   (`nEVI8WGKSdfvkR9FUyXM`, rol `user`) con permisos de operación pero sin configuración,
   workflows, funnels ni campañas. **GHL le envió invitación por email** a
   `stefanizziluca274@gmail.com` — avisar al cliente de que la va a recibir.
2. **`teamMembers` sigue vacío**: es limitación del API, no del usuario. Crear a Luca no lo
   resolvió — hay que **asignarlo en la UI** (Calendarios → Llamada de cierre - Perú → Team members).
3. El horario 9-18 lun-vie es **provisional**: falta la disponibilidad real de Luca (checklist B5).

Usuarios de la subcuenta en `usuarios.json`. Los tres del cliente ya están creados.

⚠️ **Christie quedó con rol `admin`**, a diferencia de Luca y Joaquín (`user`). Un admin puede
modificar workflows, funnels y configuración — y ya vimos lo fácil que es romper algo sin querer
(el filtro de más en el trigger de WF2 dejaba fuera a todos los descalificados). Decidir si se deja
así por ser co-dueña del negocio, o se baja a `user`.

## Producto de cobro — Escuela NCA Academy

- **id:** `6a8cbb4032d4e69ff955515f` · moneda **USD**

| Plan | Importe | Ciclos | Total |
|---|---|---|---|
| Contado | $1000 | 1 | $1000 |
| 2 cuotas de 500 | $500 | 2 | $1000 |
| 3 cuotas de 335 | $335 | 3 | $1005 |

Precios confirmados por el cliente el 18-ago. Italia usa EUR (1000/500/335) pero **GHL maneja
una sola moneda por subcuenta** (D10): como arranca Perú, se difiere a Fase 2.

⚠️ Los **links de pago** (`link_pago_*`) siguen en `PENDIENTE`: se generan al conectar Stripe,
que necesita las credenciales del cliente.

## Custom values: 7/23 con valor real

Llenados ahora: `link_calendario_cierre_pe` · `link_educativo_es` (5 Leyes ES en Hotmart) ·
`link_educativo_it` (21 Días IT) · `link_youtube_evento` (canal ES, provisional: es el canal,
no el video del evento).

Los 16 restantes esperan: dominio (para las páginas), fecha del evento, links de los grupos,
Stripe, y los datos de cobro manual.


---

## Destrabe del 28-ago — las tres llaves técnicas

Reportado por Oliver tras la llamada con el cliente. **Aún no verificado contra la subcuenta**:
el contenedor arranca limpio y no hay credenciales cargadas en esta sesión.

| Llave | Estado | Qué abre |
|---|---|---|
| **Meta** | Acceso al portafolio concedido | Los 4 eventos CAPI dejan de estar bloqueados por permisos |
| **Dominio** | Configurado al 100 % | Publicar las páginas; con la del evento y su trigger link, **WF4A deja de estar sin disparador** |
| **WhatsApp** | Número **conectado** | Los **13 nodos `[PENDIENTE-WA]`** pueden pasar a canal real |

### Los 13 nodos de WhatsApp

Se crearon como `sms` con el nombre marcado `[PENDIENTE-WA]` y la plantilla anotada en
`attributes._plantilla_meta` (ver `whatsapp()` en `builders/esb_lib.py`), justo para poder
localizarlos y corregirlos en bloque cuando hubiera canal. Ese momento llegó.

Reparto: WF1 lleva 2 · WF2 lleva 2 · WF3 lleva 4 · WF4B lleva 2 · WF4C lleva 3.

**Primer paso al retomar**: leer por API cómo quedó el canal de WhatsApp en la subcuenta —
qué `type` acepta el nodo y cómo se referencia la plantilla aprobada. Eso es lo que nunca se
pudo confirmar (GHL rechaza `whatsapp`, `wa`, `whatsapp_message` y `send_whatsapp` con
*corrupted type*).

### Sigue pendiente

- **Fecha del primer jueves** — destraba los 13 custom values vacíos.
- **WF4B sin disparador** — se crea en la UI: *Form submitted* → F03 `DTwkB4aTiEIqUGNI9Qjo`.
- **Asignar a Luca al calendario** en la UI (`teamMembers` es limitación del API).
- **La etapa «Calificado» está huérfana** — eliminarla o darle uso.


---

## Reconstrucción del 28-ago tras la llamada

### Calendarios — ahora son dos (K11)

| Calendario | id | Cierra | Link cargado en |
|---|---|---|---|
| Llamada de cierre - Espanol | `yCYC1PwGWrYRxifCIvBX` | **Joaquín** | `link_calendario_cierre_pe` |
| Llamada de cierre - Italiano | `rQxxtyI3yf2BxWUiF07s` | **Luca** | `link_calendario_cierre_it` |

Se **reutilizó** el que ya existía como el de español en vez de crear uno nuevo, porque su link
ya estaba cargado en el custom value y en los pasos de WF4B.

> **Hallazgo:** el calendario existente tenía `openHours: {}` — es decir, **no era reservable**.
> El 9-18 L-V que figuraba como provisional en la documentación nunca llegó a aplicarse. Ahora
> los dos llevan 5 entradas (una por día, como exige el API).

⚠️ Siguen pendientes dos cosas en la UI: **asignar a Joaquín y a Luca** a su calendario
(`teamMembers` es limitación del API) y **poner las franjas reales** cuando el cliente las dé.
Ojo con las 7 h de diferencia entre mercados.

### WF3 se partió en dos (K12)

`WF3 - Recordatorios de evento` pasó a ser **`WF3-ES - Recordatorios de evento`** (renombrado
sobre el mismo id `45167ab6-…`, **para no perder su disparador**) y se creó
**`WF3-IT - Promemoria evento`**.

**Por qué dos workflows y no uno con bifurcación:** GHL **rechaza las bifurcaciones anidadas**
(`encadenar()` en `esb_lib.py` lo documenta: *"Add at least one branch"*), y el chequeo de
no-show ya es una. Al necesitar además bifurcar por mercado, la única forma válida era separar.
Y encaja con el negocio: distinto día, distinto idioma, distinto closer.

⚠️ **`WF3-IT` nace sin disparador.** Hay que crearlo en la UI igual que el de WF3-ES
(`pipeline_stage_updated` → etapa Registrado) **más un filtro de mercado = Italia**, y añadir el
filtro simétrico al de WF3-ES. Es el único caso donde un filtro en el trigger es correcto —
no confundirlo con el filtro de más que rompió WF2.

### Custom values

- `Fecha evento es` y `Fecha evento it` **creados** (K12: jueves ES / sábado IT).
  `Fecha evento vigente` queda **en desuso**.
- Los dos links de calendario, cargados.

### El link de Zoom ya no es un custom value

Confirmado por Christie: **cambia en cada llamada**. WF4C pasó a usar `{{appointment.address}}`,
que es donde GHL deja la ubicación/enlace de la reunión.
⚠️ **Verificar con una reserva real** antes del lanzamiento — no está confirmado por API.

### Nota sobre WF2 — hueco conocido

WF2 bifurca por **calificación**, no por mercado, así que un registrado italiano recibe hoy el
grupo y el contenido educativo **en español**. Mientras el arranque era solo Perú daba igual;
con lanzamiento simultáneo (K10) ya no.

Se quitó de su email la referencia a `fecha_evento_vigente` (que ya no existe como dato único):
la fecha y la hora las lleva ahora el recordatorio de WF3-ES / WF3-IT, que sí son por mercado.

**Decisión pendiente:** partir WF2 en ES/IT como se hizo con WF3. Implica además crear la
encuesta **F02 en italiano** (los formularios no se pueden crear por API, van a UI).


### Limpieza de custom values (28-ago)

Borrados los dos que quedaron muertos, tras comprobar que **ningún** workflow los referenciaba:

- `fecha_evento_vigente` → lo sustituyen `fecha_evento_es` y `fecha_evento_it` (K12).
- `link_zoom_llamada` → el enlace cambia en cada llamada, WF4C lo toma de `{{appointment.address}}`.

Quedan **11 de 23** con valor real. Los 12 que faltan, por quién los desbloquea:

| Depende de | Valores |
|---|---|
| **Cliente** | `fecha_evento_es`, `fecha_evento_it`, `hora_evento_pe`, `hora_evento_it`, `datos_pago_pe`, `datos_pago_it` |
| **Nosotros** (páginas, ya hay dominio) | `link_evento_es`, `link_evento_it`, `link_registro_it` |
| **Jaime** (conectar Stripe) | `link_pago_contado`, `link_pago_2cuotas`, `link_pago_3cuotas` |


---

## 4-sep · Corrección: `teamMembers` NO era limitación del API

Este documento decía que `teamMembers` era una limitación del API tras probar seis formas. **Era
un diagnóstico equivocado.** Lo señaló Oliver al buscar dónde asignar el usuario en la UI y no
encontrarlo.

**La causa real es el TIPO de calendario.** Los dos se habían creado como `calendarType: "event"`,
que no admite miembros de equipo — ni por API ni por UI. Y el tipo **no se puede cambiar después**:
un PUT con `calendarType: "round_robin"` responde **200 pero lo ignora en silencio**, dejando el
tipo y el equipo como estaban. Es el peor tipo de fallo: parece que funcionó.

Verificado creando uno nuevo: `calendarType: "round_robin"` **sí acepta `teamMembers` en el POST**.

### Cómo quedaron

| Calendario | id | tipo | dueño |
|---|---|---|---|
| Llamada de cierre - Español | `befuzgaXYSmsD2qUZdkl` | `round_robin` | Joaquín |
| Chiamata di chiusura - Italiano | `MNg4SJeHdqjOfoGjJpKQ` | `round_robin` | Luca |

Los dos antiguos (`yCYC1PwG…`, `rQxxtyI3…`) se borraron, y `link_calendario_cierre_pe` / `_it`
apuntan a los nuevos. WF4B lee esos custom values, así que sigue el cambio sin tocarlo.

### De paso

- El italiano pasó a llamarse **en italiano**: el nombre lo lee el visitante en el widget.
- **`calendarTimezone` no existe** como propiedad (422 *property should not exist*). En un
  round robin la zona sale del **perfil del usuario asignado** — que es lo correcto, y resuelve
  que el calendario de Luca estuviera heredando GMT-5. **Verificar que el perfil de Luca esté en
  horario de Italia.**

### Regla que queda

**El tipo de calendario se elige al crear y no se corrige después.** Para llamadas 1-a-1 con
dueño, `round_robin` (aunque sea una sola persona). `event` sirve solo para calendarios sin
responsable asignado.


---

## Carga de los datos del cliente — 4-sep

Fuente: `docs/fuentes/04-datos-cliente-4sep.md`. Todo lo de abajo ya está escrito en la
subcuenta y verificado leyéndolo de vuelta.

### Custom values — 9 salieron de `PENDIENTE`

`builders/valores.py`. Dos comandos, porque hay dos clases de valor:

- **`ciclo 1|2`** — fecha y hora del webinar por mercado, más `nombre_lanzamiento_vigente`.
  Cambian entre los dos webinars. **El ciclo 2 se carga el 25-sep.**
- **`fijos`** — `datos_pago_pe` y `datos_pago_it`. No cambian.

Siguen en `PENDIENTE` y no dependen de nosotros: los 3 `link_pago_*` (esperan Stripe),
`embed_video_educativo_es` (falta la URL de System.io) y todo el bloque `_it` de páginas
(esperan que Luca valide los textos).

### Calendarios — cómo funciona de verdad la disponibilidad

`builders/agendas.py`. Comprobado contra `/calendars/{id}/free-slots`, que es la única
fuente de verdad: leer el objeto del calendario no basta, porque guarda cosas que después
no se reservan.

| Mecánica | Qué pasa |
|---|---|
| `openHours` | Patrón **semanal**. Es lo que abre los días. No es opcional. |
| `availabilities` | Excepciones **por fecha**. Con `hours: []` esa fecha queda cerrada aunque el patrón la abra. |
| `deleted: true` | **No borra** la entrada: le vacía las horas. O sea, cierra ese día. |
| `timezone` en el calendario | **422 «property timezone should not exist»**. Hereda el de la subcuenta (`America/Bogota`, UTC-5). Por eso el horario italiano de Luca va cargado en hora de Perú: 15-19 Italia = **08-12 Perú**. |
| `/free-slots` | Rechaza rangos de **más de 31 días**. Hay que preguntar por tramos o parece que el calendario está vacío. |

**Callejón sin salida que costó dos intentos:** con `openHours: []` y solo `availabilities`,
las fechas entre semana sí aparecen pero **los sábados no**, por más que estén cargados.
El patrón semanal hace falta.

Estado actual de los dos: **60 min por turno**, sin colchón, patrón semanal + las 13 (ES)
y 11 (IT) fechas de la ventana, y **cerradas una por una las 62/64 fechas del horizonte
reservable que caen fuera**. Con eso no se puede reservar ni antes del 25-sep ni después
del 10-oct. `allowBookingFor` subió de 30 a 45 días para que el 24-sep se vea la ventana
entera.

> ⚠ **Los sábados no dan turno y no se arregla por API.** Con el patrón semanal abriendo
> el sábado y la fecha cargada, `/free-slots` sigue sin devolver nada — y una sonda con
> `openHours` de lunes a domingo confirma que **GHL solo entrega lunes a viernes**. Es
> configuración de disponibilidad **del usuario**, que el API público no expone. Se pierden
> **26-sep, 3-oct y 10-oct de Joaquín** (9 turnos) y **10-oct de Luca** (4 turnos).
> Se arregla en la UI, en la disponibilidad de cada usuario.

⚠ **Joaquín también quedó con rol `admin`**, igual que Christie. De los tres del cliente,
solo Luca es `user`.


---

## Estado tras la llamada del 4-sep

Fuente: `docs/fuentes/05-deltas-llamada-4sep.md`.

### 🚨 Lo que bloquea el lanzamiento

**Las esperas de WF3 son relativas al registro, no a la fecha del evento.** Verificado
leyendo los nodos: `{"type":"days","value":1,"when":"after"}`. Con los anuncios el 9-sep y
el webinar el 24, todo el que se registre temprano recibe la secuencia completa de
recordatorios en sus primeras 48 horas — y el trigger link de «estamos en vivo» dispara
WF4A, así que además queda marcado como asistente.

Para arreglarlo hace falta **el esquema real de una espera anclada a fecha**, que no
conocemos. Se resuelve como se resolvió `internal_notification`: alguien configura **un**
nodo en la UI y se lee por API.

### Hecho

| | |
|---|---|
| `datos_pago_pe` | Sin «SAC». Sigue pendiente confirmar la S de «Con*s*ciencia» |
| `datos_pago_it` | Intestatario **Luca Stefanizzi** |
| Plantillas de cobro | 19 en total. `datos_pago_pe` se llama así, y no `_es`, porque lleva la cuenta del BCP en soles en el cuerpo |
| **WF4C** | Dos `internal_notification` nuevos — al agendar y una hora antes. Antes tenía cero |
| Fotos y bios | Cuatro custom values nuevos: `foto_christie_url`, `foto_luca_url`, `bio_christie`, `bio_luca`. Ya no hay literales en `registro-es.html` |
| `comienza-aqui-es` | El recuadro del curso acepta embed de YouTube, enlace normal (tarjeta con botón) o nada |

`retocar.py` aprendió dos cosas: a **insertar** nodos —cosiéndolos con `parentKey`/`next`/
`order`, solo en cadenas simples— y `--solo <fase>`, porque cada fase reescribe nodos
enteros y volver a pasar una que ya se afinó a mano en la UI le escribe encima.

`valores.py` aprendió a **crear** los custom values que no existen, no solo a actualizarlos.

### Pendiente, por orden

1. **El anclaje de WF3** — necesita el nodo de ejemplo en la UI
2. **Nutrición entre registro y evento** (K21) — depende de lo anterior
3. **Pase VIP** (K13/K14) — espera el link de Hotmart y el contenido de Joaquín
4. Enlace del Drive del curso → `embed_video_educativo_es`
5. Confirmar la S de «Consciencia» antes de mandar `datos_pago_pe` a Meta
6. Verificar a dónde lleva `go.hotmart.com/C104290931W` — **tres documentos dicen tres
   productos distintos** (21 Días, 5 Leyes, Reflexología) y es el único CTA de la página del
   no-calificado. Desde el entorno de trabajo el CDN y Hotmart están bloqueados por política
   de red, así que hay que abrirlo a mano
7. Réplicas italianas de las 5 páginas — esperan la validación de Luca (B4)
8. WF2 no bifurca por mercado: un registrado italiano recibe el grupo y el contenido en español
9. La etapa «Calificado» sigue huérfana
