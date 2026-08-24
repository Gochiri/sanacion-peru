# GHL CLI — instalado en `tools/ghl-cli`

CLI de GoHighLevel (Lead Gen Jay) vendorizado en el repo para iterar sobre la subcuenta desde terminal.
Instalado y verificado el 16-ago. `.env` y `.venv/` están gitignorados — **nunca commitear credenciales**.

## Arranque en una sesión nueva

El contenedor es efímero: el código está en el repo pero el venv no. En cada sesión nueva:

```bash
cd tools/ghl-cli && ./install.sh     # recrea .venv (~20 s)
# editar .env con GHL_API_KEY y GHL_LOCATION_ID
./ghl contacts list --limit 5        # smoke test
```

## Credenciales

| Variable | De dónde sale | Para qué |
|---|---|---|
| `GHL_API_KEY` | GHL → Ajustes → Integraciones privadas → Crear (dar todos los scopes) | Todo el API público |
| `GHL_LOCATION_ID` | El ID largo en la URL de la subcuenta | Identifica la subcuenta del cliente |
| `GHL_FIREBASE_REFRESH_TOKEN` | Extensión de Chrome incluida (`chrome-extension/`), desde el navegador de quien esté logueado en GHL | **Solo** para crear workflows (API interna) |

⚠️ El refresh token de Firebase equivale a la sesión completa de GHL. Tratarlo como contraseña; caduca y hay que regrabarlo.

## Qué SÍ resuelve de la Fase 1

| Tarea del plan | Comando |
|---|---|
| Leer campos/valores/pipelines existentes | `./ghl locations custom-fields` · `custom-values` · `./ghl opportunities pipelines` |
| Auditar workflows ya creados | `./ghl --json workflows list` |
| **Crear workflows** (WF1–WF5) | `./ghl --experimental workflows create --from-json <campaign.json>` |
| Cargar contactos de prueba para QA E2E | `./ghl contacts create ...` + `./ghl opportunities create/update --stage-id` |
| Verificar submissions de la encuesta | `./ghl forms submissions` |
| Revisar conversaciones y mensajes | `./ghl conversations list/messages/send` |
| Facturas del cobro | `./ghl payments create-invoice` · `invoices` |

## Qué NO resuelve — sigue siendo trabajo de UI (Playwright o manual)

La CLI **solo lista** (no crea): **campos personalizados** (SETUP-02), **custom values** (SETUP-03),
**pipelines y etapas** (SETUP-04), **formularios/encuestas** (ACT-01/02), **calendarios** (ACT-04).
Y **no toca funnels ni páginas** (ACT-03) — no existe ese grupo de comandos.

→ El plan de construcción no cambia: SETUP-02/03/04 y ACT-01/02/03/04 se hacen en la UI.
La CLI aporta en **verificación** (leer estado real) y en **WF1–WF5**.

## Detalle importante del builder de workflows

`workflow_builder.py` declara **56 action types verificados** contra el API interno — entre ellos todo lo que
necesitan nuestros workflows: `update_contact_field`, `if_else`, `create_opportunity`, `add_contact_tag`,
`internal_notification`, `wait`, `facebook_conversion_api`, `update_custom_value`, `webhook`, `conversation_ai` (F2).

Pero los *helpers* de la CLI (`workflows create-step`) solo construyen **6**: email, sms, wait, tag, webhook, ai.
Para los otros 50 hay que escribir el dict del paso a mano, en un builder propio al estilo de `builders/*.py`.

**Dos huecos a verificar antes de comprometer la CLI para WF1–WF5:**
1. **WhatsApp como acción de workflow** no aparece en los 56 tipos (sí hay `sms`, `email`, `messenger`, `instagram-dm`).
   Nuestros WF son WhatsApp-intensivos (11 plantillas) → confirmar en la subcuenta cómo se serializa un envío de
   WhatsApp con plantilla antes de decidir si los WF se construyen por CLI o en UI.
2. **Cambio de etapa de oportunidad** no está entre los 56 (hay `create_opportunity`, `find_opportunity`,
   `remove_opportunity`). WF2/WF3/WF4 mueven etapas constantemente → verificar si `create_opportunity` sobre una
   oportunidad existente actualiza la etapa, o si hace falta otro tipo.

Método para resolver ambos: crear un workflow de prueba en la UI con esos dos nodos, leerlo con
`./ghl --json workflows list` y copiar la forma real del payload.
