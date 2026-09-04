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


---

## 28-ago · Dos hallazgos que cambian cómo se despliega

### 1 · `next: null` ya no se acepta — hay que omitir la clave

Al reguardar workflows que llevaban semanas sin tocarse, GHL respondió:

> `Action validation failed for sms (…): Next is invalid. Please provide a valid value.`

El nodo terminal llevaba `"next": null`, que es lo que siempre se había mandado.
Probadas tres variantes sobre un workflow real: **omitir la clave funciona**; cadena vacía y
lista vacía no hicieron falta. Corregido con un barrido al final de `ensamblar()`, que cubre
también los nodos que llegan ya enlazados desde `bifurcar()` (sus ramas y su relleno también
ponían `next=None`).

### 2 · Un workflow tocado en la UI ya no se puede reescribir desde el builder

Es el hallazgo importante. Cuando alguien edita un workflow en la UI, GHL lo reescribe al
**formato rico del canvas** y deja de aceptar el nuestro.

| | Formato del builder | Formato tras pasar por la UI |
|---|---|---|
| Condición | `attributes.if = [{field, operator, value}]` | `attributes.branches[].segments[].conditions[]` |
| Campo | `"contact.nivel_calificacion"` | `conditionSubType: "F4n43YBwtdya1dyJYdzO"` (**id** del campo) |
| Operador | `"eq"` | `conditionOperator: "=="` |
| Extra | — | `currentRecipeType`, `sibling`, `cat`, `advanceCanvasMeta` con posiciones |

A partir de ahí, un PUT con el formato antiguo se rechaza con *"Action validation failed for
if_else"* o *"Add at least one branch"*.

**Y aunque se aceptara, no habría que hacerlo**: reescribir borra las correcciones hechas a mano
en la UI, que son las buenas — los triggers de esta cuenta se arreglaron ahí.

Se comprobó en vivo: `WF3-IT`, creado por API y nunca tocado en la UI, **sí** acepta el formato
del builder. `WF1`, `WF2`, `WF3-ES`, `WF4B` y `WF5`, todos tocados en la UI, lo rechazan.

**Regla de trabajo que queda:**

- Workflow **nuevo** o que nadie tocó → `completar.py` (reescritura completa).
- Workflow **ya tocado en la UI** → `retocar.py`: lee sus templates, sustituye solo la cadena
  que cambia y los devuelve. No toca la estructura ni las condiciones.

Aplicado así el 28-ago, con verificación posterior: los 8 workflows conservan sus pasos y sus
condiciones, `fecha_evento_vigente` ya no aparece en ninguno, WF3-ES usa `fecha_evento_es` y
WF3-IT `fecha_evento_it`.


---

## 4-sep · Un PUT sin `status` despublica el workflow

Al revisar antes de lanzar aparecieron cuatro workflows que **no corren**. Tres de ellos —WF2,
WF3-ES y WF4B— son **exactamente los tres que se retocaron con `retocar.py`**.

La causa: el PUT enviaba `{name, version, workflowData}` **sin `status`**, y GHL lo deja en `null`.
No da error, no avisa: el workflow simplemente deja de estar publicado. Es el mismo patrón que el
de `workflowData` (un PUT sin él borra todos los pasos), aplicado a otro campo.

`retocar.py` ya reenvía el `status` que tenía el workflow. **Regla general para esta API: en un
PUT hay que reenviar todo lo que no se quiera perder, porque lo que no se manda se borra.**

### Cómo comprobarlo

```python
got = c.request("GET", f"/workflow/{loc}/{wid}")
print(got.get("status"))   # published / draft / None
```

`None` y `draft` significan lo mismo de cara al lanzamiento: **no corre**.
