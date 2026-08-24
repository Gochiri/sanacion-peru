# Builders — Fase 1

Construyen los workflows de la Fase 1 en la subcuenta vía API interna de GHL.

```bash
source tools/ghl-cli/.venv/bin/activate
set -a && source tools/ghl-cli/.env && set +a

python builders/build_fase1.py --dry-run     # ver los pasos sin tocar GHL
python builders/build_fase1.py               # desplegar (siempre en borrador)
python builders/build_fase1.py --solo WF3    # un solo workflow
```

- `esb_lib.py` — constructores de nodos + despliegue. Encapsula todo lo verificado contra la cuenta real.
- `build_fase1.py` — definición de WF1–WF5.

## Estado: 7 workflows · 37 pasos desplegados (draft)

| Workflow | Pasos | Pendientes |
|---|---|---|
| WF1 Captación y atribución | 8 | 1 WA · 4 IF |
| WF2 Registro y calificación | 6 | 2 WA · 4 IF |
| WF3 Recordatorios de evento | 10 | 4 WA · 2 IF |
| WF4A Asistencia | 1 | 2 IF |
| WF4B Postulación | 2 | 2 WA · 3 IF |
| WF4C Cita agendada | 5 | 3 WA · 1 IF |
| WF5 Cobro confirmado | 5 | 4 IF |

**Todos en borrador.** Los triggers se configuran en la UI — el builder crea la cadena de acciones.

## Lo que falta y por qué

### 1. WhatsApp — 12 nodos · falta esquema de UI
No existe un tipo `whatsapp` en GHL (rechaza `whatsapp`/`wa`/`whatsapp_message`/`send_whatsapp`).
Se crearon como `sms` marcados `[PENDIENTE-WA]`, con la plantilla anotada en los attributes.
Falta confirmar cómo se marca canal=WhatsApp y cómo se referencia la plantilla aprobada de Meta.

### 2. Bifurcaciones `if_else` — 20 · falta esquema de UI
El `if_else` **no es un paso lineal**: es un nodo de canvas con `nodeType`
(`condition-node` / `branch-yes` / `branch-no`) cuyas salidas son las ramas, no un `next`.
Aislado pasa el PUT; encadenado con `link_steps` lo rechaza. **No se despliegan** — se reportan
como `[PENDIENTE-IF]` con su condición para insertarlas a mano.

### 3. Movimientos de etapa — falta esquema de UI
No existe acción de "cambiar etapa": se usa `create_opportunity` (hace upsert). El tipo es válido,
pero con `{pipelineId, stageId, status, name}` GHL responde *"Pipeline is required., Opportunity
Name is required."* — los nombres reales de los campos son otros.

### 4. Eventos CAPI — 4 · bloqueado por el cliente (llave A1)
No es problema de esquema: el nodo exige **Event Type, Access Token y Pixel**, y los tres salen del
Business Manager de Meta, que sigue sin administrador. Se despliegan en cuanto A1 se resuelva.

## Cómo cerrar los pendientes 1–3

Una sola pasada por la UI los resuelve. Crear en cualquier workflow de prueba:

1. un nodo **Send WhatsApp** con una plantilla,
2. un nodo **If/Else** con una condición y sus dos ramas,
3. un nodo **Crear oportunidad** con pipeline y etapa elegidos,

guardar, y leerlos con:

```bash
python - <<'PY'
import sys; sys.path.insert(0, "builders")
from esb_lib import cliente
import json
c = cliente()
wid = "<ID del workflow de prueba>"
got = c.request("GET", f"/workflow/{c.location_id}/{wid}")
print(json.dumps((got.get("workflowData") or {}).get("templates"), indent=2, ensure_ascii=False))
PY
```

Con esos tres esquemas se actualizan `whatsapp()`, `bifurcar()` y `mover_a_etapa()` en `esb_lib.py`
y el despliegue queda completo.

## Detalles del API que costó descubrir

| Hallazgo | Consecuencia |
|---|---|
| **Versionado optimista.** Cada PUT incrementa la versión; el builder de la CLI manda `version:1` fijo → su `--update` está roto. | `guardar()` lee la versión antes de cada PUT. |
| **Firebase aplica rate limit** al refresh y cada proceso pedía token nuevo → la sesión se caía tras unas ejecuciones. | `TokenCacheado` guarda el id_token en disco (~1 h). |
| `update_contact_field` exige **`title` y `type`** por campo, no solo `field`/`value`. | `campo()` los resuelve desde `docs/ghl-estado/custom-fields.json`. |
| GHL valida el `type` contra lista blanca de 53, pero **guarda los attributes sin validar**. | El esquema de cada tipo se copia de la UI, no se inventa. |
| Los steps necesitan `order`/`parentKey`/`next`. | Siempre `link_steps()`. |
| El backend **falla de forma intermitente** al guardar varios workflows seguidos. | Hasta 3 reintentos con pausa. |
