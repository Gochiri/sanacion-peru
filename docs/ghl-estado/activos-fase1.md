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
