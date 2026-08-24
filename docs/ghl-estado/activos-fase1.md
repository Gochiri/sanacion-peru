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
| **teamMembers del calendario** | Ni el POST ni el PUT los aceptan (queda `[]` en las 3 formas probadas). Se asigna en la UI. |

---

## Calendario de cierre — Perú ⚠️ provisional

- **id:** `yCYC1PwGWrYRxifCIvBX`
- **link:** https://api.leadconnectorhq.com/widget/booking/yCYC1PwGWrYRxifCIvBX
- 30 min · buffer 15 min · máx 6/día · lun-vie 9:00-18:00 · reserva con 2 h de antelación

**Dos cosas lo dejan incompleto:**

1. **`teamMembers` está vacío** — el API no los acepta.
2. **Luca no existe como usuario en la subcuenta.** Los únicos usuarios son Germán, Henry y
   Oliver (equipo Profit). El calendario es de Luca: hasta que sea usuario, las citas no
   pueden asignársele.
3. El horario 9-18 lun-vie es **inventado**: falta la disponibilidad real de Luca (checklist B5).

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
