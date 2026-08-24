# Esquemas reales de nodos de workflow

Descubiertos contra la subcuenta real leyendo los mensajes de validación de GHL.
**No se pudo usar el navegador:** la política de red de este entorno permite los dominios de API
(`services.` / `backend.leadconnectorhq.com`) pero **bloquea `app.gohighlevel.com`**, así que la UI
es inalcanzable desde aquí. El método fue provocar errores de validación e iterar sobre lo que pedían.

## Regla general

GHL valida el `type` contra una lista blanca de 53 (`action-types.json`) y **valida los attributes por
tipo**, pero los mensajes de error no dicen el nombre del campo que falta — dicen la etiqueta de la UI
("Pipeline is required"). Los nombres reales van en **snake_case**.

## `update_contact_field`

```json
{"fields": [{"field": "contact.idioma", "value": "ES",
             "title": "Idioma", "type": "SINGLE_OPTIONS"}]}
```
`title` y `type` son obligatorios (*"Title is required., Type is required."*). Se resuelven desde
`custom-fields.json`.

## `create_opportunity` — también sirve para mover de etapa

```json
{"pipeline_id": "<id>", "stage_id": "<id>",
 "opportunity_name": "{{contact.name}}", "opportunity_source": "Workflow",
 "monetary_value": 0, "status": "open", "fields": []}
```

- Todo en **snake_case**: `pipelineId`/`stageId`/`name` son rechazados.
- `opportunity_source`, `monetary_value` y `fields` son **obligatorios** aunque no sean evidentes.
- `status`: `open` para mover de etapa · `won` para cerrar la venta (Ganado no es una etapa).
- No existe acción de "cambiar etapa": esta hace upsert sobre la oportunidad del contacto.

## `if_else` — no es un paso lineal

Es un nodo de canvas: **su `next` es un ARRAY** con los ids de sus ramas
(*"If/else condition node must have next as array"*). Son tres nodos:

```json
{"type": "if_else", "nodeType": "condition-node",
 "attributes": {"name": "Es italiano?", "operator": "and",
                "if": [{"field": "contact.phone", "operator": "contains", "value": "+39"}]},
 "next": ["<id rama si>", "<id rama no>"]}

{"type": "if_else", "nodeType": "branch-yes",
 "attributes": {"name": "..."}, "next": "<primer paso de la rama>"}

{"type": "if_else", "nodeType": "branch-no",
 "attributes": {"name": "..."}, "next": "<primer paso de la rama>"}
```

- Las ramas necesitan `name` en attributes.
- Los pasos de cada rama se encadenan con `parentKey` al nodo de rama.
- **Campos CHECKBOX**: la condición espera **boolean**, no cadena
  (*"Condition: Expected boolean, received array"*) → `{"operator": "eq", "value": false}`.

## `facebook_conversion_api` — bloqueado por el cliente

Exige **Event Type, Access Token y Pixel**. Los tres salen del Business Manager de Meta, que sigue sin
administrador (llave A1). No es un problema de esquema: **la llave A1 impide incluso crear el nodo**.

## WhatsApp — sigue pendiente

No existe tipo `whatsapp` (rechaza `whatsapp`/`wa`/`whatsapp_message`/`send_whatsapp`). Los nodos se
crean como `sms` marcados `[PENDIENTE-WA]`. Falta confirmar cómo se marca canal=WhatsApp y cómo se
referencia la plantilla aprobada de Meta — y eso **sí requiere ver un nodo hecho en la UI**, que desde
este entorno no es alcanzable.

## `order` y enlazado

- Todo nodo necesita `order`, `parentKey` y `next`.
- El `order` es **global y secuencial** en el workflow: si un bloque repite índices, GHL responde
  *"action has a corrupted order"*. Lo resuelve `ensamblar()` en `esb_lib.py`.

## Rate limit del PUT interno

Guardar varios workflows seguidos falla de forma intermitente con errores genéricos; **el mismo payload
pasa al reintentar más tarde**. `completar.py` despliega de uno en uno con pausas de 8 s y es
idempotente (relanzable hasta que todo quede completo).
