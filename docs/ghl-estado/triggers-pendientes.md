# Triggers — ninguno configurado, y por qué

Estado: **los 7 workflows están sin trigger.** No es un olvido: es que casi todos cuelgan de
recursos que todavía no existen en la subcuenta.

## Se pueden crear por API, pero con una trampa

`POST /workflow/{loc}/trigger` funciona y el trigger persiste. **Pero GHL no valida el `type`:**
acepta `contact_created` y `contact_create` por igual, y guarda lo que reciba. Si el identificador
es incorrecto, queda un trigger que **nunca dispara** — peor que no tenerlo, porque en la UI
parece configurado.

No hay endpoint de catálogo (`/trigger/types`, `/trigger-config`… todos 404), así que los
identificadores solo se confirman viéndolos en un trigger hecho desde la UI.

El único verificado en código real es **`contact_tag`** (lo usa el CampaignBuilder del CLI):

```json
{"type": "contact_tag", "masterType": "highlevel", "status": "draft",
 "workflowId": "<id>", "location_id": "<loc>", "name": "<nombre>",
 "conditions": [{"operator": "index-of-true", "field": "tagsAdded",
                 "value": "<tag>", "title": "Tag Added", "type": "select",
                 "id": "tag-added"}],
 "actions": [{"workflow_id": "<id>", "type": "add_to_workflow"}],
 "active": true, "triggersChanged": true, "schedule_config": {}}
```

Leerlos: `GET /workflow/{loc}/trigger?workflowId=<id>`.
Nota: aunque se mande `active: true`, GHL lo guarda como `false` mientras el workflow esté en borrador.

## Qué necesita cada workflow

| Workflow | Trigger | Depende de | Estado |
|---|---|---|---|
| WF1 | Contact Created + Customer Replied (WhatsApp) | — / canal WhatsApp | Contact Created se puede ya (falta confirmar identificador). El de WhatsApp espera el número (llave A2) |
| WF2 | Survey Submitted (F01/F02) | **encuesta de registro** | Bloqueado: ACT-01, se hace en UI |
| WF3 | Opportunity Stage Changed → Registrado | pipeline ✅ | Se puede ya (falta confirmar identificador) |
| WF4A | Trigger Link Clicked (link del evento) | **trigger link + página del evento** | Bloqueado: ACT-03, se hace en UI |
| WF4B | Form Submitted (F03) | **formulario de postulación** | Bloqueado: ACT-02, se hace en UI |
| WF4C | Customer Booked Appointment | **calendarios de cierre** | Bloqueado: ACT-04, se hace en UI |
| WF5 | Payment Received + Contact Tag Added `pago-manual` | productos de cobro / tag ✅ | La rama de tag se puede ya; Payment Received espera ACT-07 |

## Conclusión

Los triggers **no son el cuello de botella**: lo son los recursos de los que cuelgan.
5 de 7 esperan formularios, calendarios o páginas — todo trabajo de UI que el API no cubre
(ver `ghl-cli-uso.md`). Configurar los triggers es el último paso, no el siguiente.

Cuando se creen esos recursos en la UI, conviene configurar **un trigger a mano** y leerlo con el
GET de arriba: eso confirma los identificadores reales y permite automatizar el resto.

## Tags de trigger

`pago-manual` no lo añade ningún workflow — lo recibe el contacto cuando paga por transferencia o
Yape (D8/D10), y es lo que dispara la rama manual de WF5. Por eso no salía en `tags_usados()` y se
creó aparte. Ya existe en la subcuenta.
