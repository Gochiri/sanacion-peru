# Triggers — catálogo real y lecciones

## Los 5 identificadores verificados en la UI

| Trigger (nombre en la UI) | `type` real | Condiciones |
|---|---|---|
| Contact created | `contact_created` | sin filtros |
| Contact tag | `contact_tag` | `tagsAdded` · `index-of-true` · `"<tag>"` |
| Survey submitted | `survey_submission` | `survey.id` · `is-any-of` · `["<id>"]` |
| Pipeline stage changed | **`pipeline_stage_updated`** | `opportunity.pipelineId` · `==` · `"<id>"`<br>`opportunity.pipelineStageId` · `==` · `"<id>"` |
| Customer booked appointment | **`customer_appointment`** | `contactMode` · `is-any-of` · `["contact"]`<br>`calendar.id` · `==` · `"<id>"` |

## ⚠️ Adivinar identificadores no funciona — crearlos en la UI

De los que se intentaron por API sin haberlos visto antes, **la mitad salieron mal**, y GHL los
acepta igual porque **no valida el `type`**: quedan como triggers que nunca disparan pero que en la
UI parecen configurados.

Lo que se falló al adivinar, con el patrón detrás:

| Lo que parecía | Lo que es | Lección |
|---|---|---|
| `pipeline_stage_changed` | `pipeline_stage_updated` | el nombre visible **no** se convierte a snake_case: "changed" → `updated` |
| `customer_booked_appointment` | `customer_appointment` | el nombre visible se **acorta** |
| `pipeline.id` / `pipeline_stage.id` | `opportunity.pipelineId` / `opportunity.pipelineStageId` | los campos van en **notación de objeto sobre la entidad**, no como recurso suelto |
| `is-any-of` con array | `==` con valor simple | el operador por defecto es `==`; `is-any-of` solo en `survey.id` y `contactMode` |
| *(no lo puse)* | `contactMode` · `is-any-of` · `["contact"]` | los triggers de cita **exigen** decidir a quién se inscribe (contacto / invitados / ambos) |

**Regla operativa: los triggers se crean en la UI.** Es más rápido que adivinar, verificar y
corregir — y evita dejar triggers muertos. El API sirve para **leerlos** (`GET
/workflow/{loc}/trigger?workflowId=<id>`), que es como se construyó este catálogo.

## Estado

| Workflow | Trigger | Estado |
|---|---|---|
| WF1 | `contact_created` | ✅ |
| WF2 | `survey_submission` + F01 | ✅ (se le quitó un filtro que rompía el flujo, ver abajo) |
| WF3 | `pipeline_stage_updated` → Lanzamiento/Registrado | ✅ corregido en UI |
| WF4A | Trigger Link Clicked | **espera la página del evento** (falta el dominio) |
| WF4B | Form Submitted (F03 `DTwkB4aTiEIqUGNI9Qjo`) | F03 ✅ creado — **falta el trigger, se hace en UI** |
| WF4C | `customer_appointment` → calendario de cierre | ✅ corregido en UI |
| WF5 | `contact_tag` → `pago-manual` | ✅ |
| **WF6-ES** | `pipeline_stage_updated` → Lanzamiento / **Registrado** + **Mercado = Peru-LATAM** | ✅ 6-sep |
| **WF2-IT** | `survey_submission` → **F02** `UTqIwgAEt0xjmcBeA75j` | ✅ 6-sep |
| **WF6-IT** | `pipeline_stage_updated` → Lanzamiento / **Registrado** + **Mercado = Italia** | ⬜ **falta — el workflow ya está en italiano, en borrador** |
| **WF4B** | dos triggers `form_submission`: F03 y **F03-IT** `bGZjMxYQ78jACMs2keUO` | ✅ 6-sep |

**WF2-IT** es el gemelo de WF2 con un solo cambio en el trigger: la encuesta es **F02**, no F01.
Sin filtro de mercado: la encuesta ya decide el mercado por sí sola, y filtrar la entrada por
un campo es lo que rompió WF2 en su día.

**WF4B** hoy dispara solo con F03. La postulación italiana llega por **F03-IT**, así que hay que
añadirla al trigger — WF4B ya bifurca por `mercado` por dentro y manda a cada uno a su calendario.

⚠️ **El filtro de mercado de WF6-IT no es opcional.** Sin él recogería también a los españoles,
que es exactamente el fallo de abajo pero al revés.

⚠️ **WF6 nació sin filtro de mercado y por eso mandaba los tres correos en español también a los
italianos** — su trigger es la misma etapa *Registrado* que alcanzan los dos mercados. Corregido
el 6-sep copiando la condición literal de WF3-ES. **Cuando se haga WF6-IT, su filtro es `Italia`.**

**WF6-ES** lleva el mismo trigger que WF3-ES, a propósito: la etapa *Registrado* solo la alcanza
quien califica, así que la nutrición no le llega al descalificado. Al crearlo, **no** añadir
ningún filtro extra — es exactamente el error que dejaba a los descalificados fuera de WF2 (ver
abajo). Y hay que **publicarlo**: nace como borrador.

## ⚠️ No filtrar la calificación en el trigger

El trigger de WF2 traía un segundo filtro `Nivel calificacion == "<frase de califica>"`. Con eso
**WF2 solo se disparaba para quien califica**: los descalificados nunca entraban al workflow y
nunca recibían la secuencia educativa — se perdían en silencio, que es el problema que el proyecto
viene a resolver.

**Regla:** el trigger captura *todos* los envíos; **la separación la hace la bifurcación interna**.
Filtrar en la entrada descarta contactos sin dejar rastro; filtrar dentro le da un camino a cada uno.
