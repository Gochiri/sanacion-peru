# API interno de workflows — hallazgos verificados

Probado el 16-ago contra la subcuenta real con un workflow sandbox (creado, probado y **borrado**;
la subcuenta quedó en 0 workflows). Resuelve los dos huecos abiertos en `ghl-cli-uso.md`.

## 1. El versionado optimista rompe el builder de la CLI ⚠️

`CampaignBuilder.build()` manda `"version": 1` **fijo** en el PUT. Cada guardado exitoso **incrementa la
versión** del workflow, así que el segundo PUT sobre el mismo workflow falla con:

> `{"msg":"Your version is outdated, Please refresh your page and try again."}`

Consecuencia: el builder solo funciona en workflows recién creados. **`--update` está roto** — cualquier
re-deploy falla. Y el error se confunde fácil con un problema de datos.

**Solución obligatoria en nuestros builders:** leer la versión antes de cada PUT.

```python
def guardar(c, loc, wid, nombre, steps):
    got = c.request("GET", f"/workflow/{loc}/{wid}") or {}
    return c.request("PUT", f"/workflow/{loc}/{wid}", {
        "name": nombre, "version": got.get("version", 1),
        "workflowData": {"templates": link_steps(steps)},
    })
```

## 2. Forma obligatoria de un step

Un step sin `order` / `parentKey` / `next` es rechazado. Usar siempre `link_steps()`:

```python
{"id": <uuid>, "type": <action_type>, "name": <display>, "attributes": {...},
 "order": <int>, "parentKey": <id anterior o None>, "next": <id siguiente>}
```

## 3. GHL valida el `type`, NO los `attributes`

Un `type` fuera de la lista blanca da `"<nombre>" action has a corrupted type`. Pero los `attributes`
se guardan **crudos, sin validación semántica** — se puede guardar un nodo que la UI luego no sepa
renderizar. → El esquema de attributes de cada tipo hay que copiarlo de un nodo hecho en la UI.

## 4. Lista blanca real: 53 tipos válidos

Volcada en `action-types.json`. **Tres tipos que la CLI declara como verificados ya NO son válidos:**
`find_opportunity`, `goto`, `workflow_goal`.

Confirmados funcionando con nuestros attributes (PUT OK + persisten tras GET):
`add_contact_tag` · `update_contact_field` · `create_opportunity` · `facebook_conversion_api` ·
`internal_notification` · `if_else` · `wait` · `sms` · `email`

## 5. Los dos huecos, resueltos

### WhatsApp: NO existe un tipo dedicado ❌

Rechazados: `whatsapp`, `wa`, `whatsapp_message`, `send_whatsapp`.
Los tipos de mensajería son: `sms`, `email`, `call`, `voicemail`, `messenger`, `gmb`, `instagram-dm`,
`fb_interactive_messenger`, `ig_interactive_messenger`.

→ **El envío de WhatsApp se construye con el tipo `sms`**, y GHL enruta por canal. Nuestras 11 plantillas
van como pasos `sms`.
→ **PENDIENTE de verificar en UI:** cómo se especifica canal=WhatsApp y cómo se referencia una plantilla
aprobada de Meta dentro de los attributes. Hacer un nodo "Send WhatsApp" en la UI y leerlo con GET.

### Cambio de etapa: se hace con `create_opportunity` ❌→✅

Rechazados: `update_opportunity`, `update_opportunity_stage`, `move_opportunity`, `edit_opportunity`,
`opportunity_stage`. Solo existen `create_opportunity` y `remove_opportunity`.

→ **`create_opportunity` con el `stageId` destino es la forma de mover de etapa** (se comporta como upsert
sobre la oportunidad existente del contacto en ese pipeline). Attributes verificados:

```json
{"pipelineId": "<id>", "stageId": "<id>", "status": "open", "name": "{{contact.name}}"}
```

→ **PENDIENTE de verificar:** que sobre una oportunidad ya existente actualice en vez de duplicar.
Prueba: contacto con oportunidad en `Registrado` → correr un `create_opportunity` a `Asistio` → contar
oportunidades del contacto.

## 6. Impacto en el plan de tareas

| Antes | Ahora |
|---|---|
| "Update Opportunity Stage → X" en WF2/WF3/WF4/WF5 | `create_opportunity` con el `stageId` destino |
| "Send WhatsApp Template" en WF1–WF5 | paso tipo `sms` (canal por verificar en UI) |
| Etapas Ganado/Perdido | `status` de la oportunidad (`won`/`lost`), no etapas |
