# Estado real de la subcuenta GHL

Volcados desde el API con `tools/ghl-cli`. **Fuente de verdad de IDs y fieldKeys** para construir workflows.
Regenerar con los comandos de `docs/ghl-cli-uso.md` tras cualquier cambio en la UI.

| Archivo | Contenido |
|---|---|
| `custom-fields.json` | 19 campos con `fieldKey`, tipo y opciones |
| `custom-values.json` | 23 custom values con su `fieldKey` de merge |
| `pipeline.json` | Pipeline Lanzamiento: id + los 8 `stageId` |

## Subcuenta

| Dato | Valor |
|---|---|
| Nombre | Salud Consciente |
| Location ID | `oszNQJYK0E15KB4S06nM` |
| Company ID | `o5gKaDPEDSvPWqDucCZB` |
| País / ciudad | PE · Lima |
| Zona horaria | **America/Bogota** ⚠️ (el mapa asume America/Lima — mismo offset UTC-5 sin DST, funcionalmente equivalente; cambiar por claridad) |
| Contacto | Luca Stefanizzi · stefanizziluca274@gmail.com · **+51 980 861 915** ⚠️ |
| Logo | vacío |

⚠️ **El teléfono de la subcuenta (+51 980 861 915) no coincide con el del form (+51 986 199 020).** Sumar a A2:
cuál de los dos se conecta a la API de WhatsApp.

## Construido el 16-ago (por API, no UI)

- ✅ **SETUP-02** — 19 campos personalizados. `fieldKey` limpios y exactos (`contact.idioma`, `contact.cluster_sintoma`…).
- ✅ **SETUP-03** — 23 custom values. Los que dependen del cliente quedaron en `PENDIENTE` (cero hardcode, D5).
- ✅ **SETUP-04** — Pipeline `Lanzamiento` con 8 etapas.

### Decisión tomada al construir el pipeline

El mapa §6 lista 10 etapas terminando en `Ganado / Perdido / No califica`. En GHL, **Ganado y Perdido no son
etapas: son el _status_ de la oportunidad** (`won` / `lost`). Se construyó así:

- **8 etapas:** Lead nuevo → Calificado → Registrado → Asistio → Postulo → Llamada agendada → Llamada realizada → No califica
- **Ganado / Perdido:** status de la oportunidad. WF5 debe marcar `status = won`, no mover a una etapa "Ganado".
- `No califica` sí es etapa: es un destino real del flujo que no es victoria ni derrota.

→ Actualizar WF2 (nodo 8) y WF5 (nodo 5) del plan de tareas con esta forma.

### Nota sobre acentos en nombres

GHL **elimina** los acentos al generar el `fieldKey` en vez de transliterarlos: `"País"` → `contact.pas`.
Por eso los campos se nombraron sin acentos ("Cluster sintoma", "Nivel calificacion"). **Regla para todo lo que
se cree por API o UI:** nombres sin acentos, o el fieldKey queda roto.

## Lo que el API público SÍ permite crear (descubierto probando)

La CLI solo *lista* campos, valores y pipelines, pero el API público **sí acepta POST** en los tres:

| Recurso | Endpoint | Estado |
|---|---|---|
| Custom fields | `POST /locations/{loc}/customFields` | ✅ verificado |
| Custom values | `POST /locations/{loc}/customValues` | ✅ verificado |
| Pipelines | `POST /opportunities/pipelines` · `PUT /opportunities/pipelines/{id}` | ✅ verificado (⚠️ el PUT rechaza `locationId` en el body; preservar los `id` de etapas existentes o se recrean) |

→ **SETUP-02/03/04 salen del trabajo de UI.** Quedan en UI: formularios/encuestas, calendarios, funnels y páginas.
