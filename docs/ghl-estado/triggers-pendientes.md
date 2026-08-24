# Triggers — estado y esquema real

## ✅ Identificadores confirmados en la UI

Henry creó el trigger de WF2 a mano y al leerlo por API quedó la forma real. **Esto es lo que
antes había que adivinar**:

| Trigger (UI) | `type` | Condición | Verificado |
|---|---|---|---|
| Survey submitted | **`survey_submission`** | `{"field": "survey.id", "operator": "is-any-of", "value": ["<id>"]}` | ✅ UI |
| Contact created | **`contact_created`** | sin filtros | ✅ UI |
| Contact tag | **`contact_tag`** | `{"field": "tagsAdded", "operator": "index-of-true", "value": "<tag>"}` | ✅ UI |
| Pipeline stage changed | `pipeline_stage_changed` | `pipeline.id` + `pipeline_stage.id`, ambos `is-any-of` con array | ⚠️ sin verificar |
| Customer booked appointment | `customer_booked_appointment` | `{"field": "calendar.id", "operator": "is-any-of", "value": ["<id>"]}` | ⚠️ sin verificar |

**El patrón de nombres no es fiable:** "Contact created" → `contact_created` y "Contact tag" →
`contact_tag` siguen el snake_case, pero "Survey submitted" → **`survey_submission`**, no
`survey_submitted`. Por eso cada identificador nuevo hay que verlo en la UI antes de darlo por
bueno.

Dos detalles que no se adivinan:
- La condición usa **`survey.id`** con **`is-any-of`** y el valor en **array**, no `survey` con `eq`.
- Los campos personalizados se referencian **por id** (`contact.F4n43YBwtdya1dyJYdzO`), no por
  fieldKey.

⚠️ `contact_created` (WF1) **sigue sin verificar**: GHL acepta cualquier `type` sin validarlo, así
que hay que abrirlo en la UI y confirmar que aparece como "Contact Created".

## Estado

| Workflow | Trigger | Estado |
|---|---|---|
| WF1 | `contact_created` | ✅ verificado en UI |
| WF2 | `survey_submission` + F01 | ✅ verificado en UI |
| WF3 | `pipeline_stage_changed` → Registrado | creado — ⚠️ verificar |
| WF4A | Trigger Link Clicked | **espera la página del evento** (falta el dominio) |
| WF4B | Form Submitted (F03) | **espera F03** |
| WF4C | `customer_booked_appointment` | creado — ⚠️ verificar |
| WF5 | `contact_tag` → `pago-manual` | ✅ verificado en UI |

Los triggers se guardan con `active: false` mientras el workflow está en borrador.

## ⚠️ El filtro que rompía WF2

El trigger creado en la UI traía un segundo filtro:

```
Nivel calificacion == "Entender por que mi cuerpo enfermo y como sanarlo"
```

Con eso **WF2 solo se disparaba para quien califica**, así que los descalificados **nunca entraban
al workflow y nunca recibían la secuencia educativa** — se perdían en silencio, que es exactamente
el problema que el proyecto viene a resolver.

**Regla:** el trigger captura *todos* los envíos del survey; **la separación la hace la bifurcación
interna del workflow**, no el filtro del trigger. Filtro eliminado el 18-ago.

Vale para cualquier trigger: filtrar en la entrada descarta contactos sin dejar rastro; filtrar
dentro del workflow permite darle un camino a cada uno.
