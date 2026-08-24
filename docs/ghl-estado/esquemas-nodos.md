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

## Reglas de las ramas (descubiertas a golpes)

- El condition-node **necesita exactamente 2 ramas**: con una sola,
  *"If/else condition node needs at least 2 branches, found 1"*.
- **Ninguna rama puede estar vacía**: *"Add at least one branch."* Si la definición
  no da rama "no", `bifurcar()` la rellena con un tag inocuo.
- Los pasos **dentro** de una rama ya vienen enlazados: si el ensamblador los vuelve a
  encadenar, GHL responde *"Node has 2 incoming edges"*. Van marcados `_en_rama`.

## Las bifurcaciones NO se pueden anidar

Meter un `if_else` dentro de la rama de otro hace que GHL rechace el workflow con
*"Add at least one branch"* repetido por cada rama. Probado con el enlazado corregido para
respetar los nodos internos: falla igual. **Toda bifurcación va en el primer nivel.**

Consecuencia práctica: si una rama necesita decidir entre más de dos caminos, hay que
resolverlo con campos que ya vengan decididos desde el formulario, no ramificando dentro.

## Listar carpetas

`GET /workflow/{loc}` devuelve **solo workflows**. Las carpetas aparecen únicamente en
`GET /workflow/{loc}/directory` → `{count, rows}`. Buscar la carpeta en el endpoint
equivocado hacía que nunca se encontrara y se creara una nueva en cada corrida
(se limpiaron 2 carpetas huérfanas que quedaron en la cuenta del cliente).

## `order` y enlazado

- Todo nodo necesita `order`, `parentKey` y `next`.
- El `order` es **global y secuencial** en el workflow: si un bloque repite índices, GHL responde
  *"action has a corrupted order"*. Lo resuelve `ensamblar()` en `esb_lib.py`.

## ⚠️ Un PUT sin `workflowData` BORRA todos los pasos

El PUT de `/workflow/{loc}/{id}` **reemplaza** el documento: si el body no incluye
`workflowData`, el workflow queda con **0 pasos**. Pasó al intentar publicar un workflow
de prueba mandando solo `{name, status, version}` — se vació entero.

**Regla:** cualquier PUT sobre un workflow existente debe llevar `workflowData` completo,
aunque solo se quiera cambiar el nombre o el estado. Leer primero con GET y reenviar todo.

```python
got = c.request("GET", f"/workflow/{loc}/{wid}")
c.request("PUT", f"/workflow/{loc}/{wid}", {
    "name": got["name"], "version": got["version"],
    "workflowData": got["workflowData"],   # <- imprescindible
    "status": "published",
})
```

## Condiciones de las bifurcaciones — sin verificar en UI

La forma que usamos se guarda sin error:

```json
{"name": "Es contacto italiano?", "operator": "and",
 "if": [{"field": "contact.phone", "operator": "contains", "value": "+39"}]}
```

Pero **GHL no valida los attributes**, así que guardarse no prueba que la UI la renderice
ni que el motor la evalúe. Un intento de verificarlo ejecutando un workflow de prueba no
fue concluyente (el workflow se vació por el bug del PUT de arriba antes de correr).

→ **Pendiente de confirmar en la UI:** abrir un nodo If/Else y ver si el campo aparece
relleno. Si aparece vacío, hay que copiar el esquema real de una condición hecha a mano.

## Tags: hay que crearlos a nivel de subcuenta

`add_contact_tag` crea el tag en tiempo de ejecución, pero entonces **no aparece en los
selectores de la UI** al configurar triggers y condiciones. Hay que crearlos antes con
`POST /workflow/{loc}/tags/create`.

⚠️ Ese endpoint responde con **cuerpo vacío**, así que `create_location_tag()` del cliente
devuelve `False` aunque haya funcionado (falla al parsear "" como JSON). Nunca confiar en
su valor de retorno: verificar contra `GET /locations/{loc}/tags`. Es lo que hace
`crear_tags()` en `esb_lib.py`, que ya corre dentro del despliegue.

Los 5 tags de la Fase 1 están en `tags.json`.

## Rate limit del PUT interno

Guardar varios workflows seguidos falla de forma intermitente con errores genéricos; **el mismo payload
pasa al reintentar más tarde**. `completar.py` despliega de uno en uno con pausas de 8 s y es
idempotente (relanzable hasta que todo quede completo).
