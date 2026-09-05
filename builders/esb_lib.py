"""Librería compartida para construir los workflows de la Escuela de Sanación Biológica.

Encapsula todo lo verificado contra la subcuenta real el 16-ago
(ver docs/ghl-estado/api-interno-hallazgos.md):

  - PUT con versionado optimista: SIEMPRE leer la versión antes de guardar.
  - Los steps necesitan order/parentKey/next (link_steps).
  - GHL valida el `type` contra una lista blanca de 53, pero NO valida attributes.
  - No existe tipo `whatsapp`  -> los envíos van como `sms` (esquema por confirmar en UI).
  - No existe cambio de etapa  -> se usa `create_opportunity` con el stageId destino.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "ghl-cli"))

from cli_anything.gohighlevel.utils.ghl_internal_client import (  # noqa: E402
    InternalGHLClient, TokenManager,
)
from cli_anything.gohighlevel.utils.workflow_builder import link_steps  # noqa: E402

ESTADO = Path(__file__).resolve().parents[1] / "docs" / "ghl-estado"
CARPETA = "Escuela Sanacion - Fase 1"

# Marca los nodos que quedan a la espera del esquema real de WhatsApp.
WHATSAPP_PENDIENTE = "[PENDIENTE-WA]"


def uid() -> str:
    return str(uuid.uuid4())


# ── Estado de la subcuenta ───────────────────────────────────────────────

def cargar_estado() -> dict:
    """IDs y fieldKeys reales de la subcuenta (volcados por el CLI)."""
    pipe = json.loads((ESTADO / "pipeline.json").read_text())
    campos = json.loads((ESTADO / "custom-fields.json").read_text())
    valores = json.loads((ESTADO / "custom-values.json").read_text())
    return {
        "pipelineId": pipe["pipelineId"],
        "etapas": {e["nombre"]: e["stageId"] for e in pipe["etapas"]},
        "campos": {c["fieldKey"]: c for c in campos},
        "valores": {v["fieldKey"] for v in valores},
    }


CACHE_TOKEN = Path(__file__).resolve().parent / ".token-cache.json"


class TokenCacheado(TokenManager):
    """TokenManager con caché en disco.

    Firebase aplica rate limit al endpoint de refresh y cada proceso nuevo pedía
    un token nuevo, lo que tumbaba la sesión tras unas pocas ejecuciones. El
    id_token dura ~1 h: se guarda en disco y se reutiliza mientras siga fresco.
    """

    def get_token(self) -> str:
        import time
        if not self._token and CACHE_TOKEN.exists():
            try:
                d = json.loads(CACHE_TOKEN.read_text())
                if time.time() - d.get("t", 0) < 3000:
                    self._token, self._token_time = d["token"], d["t"]
            except Exception:
                pass
        token = super().get_token()
        try:
            CACHE_TOKEN.write_text(json.dumps({"token": token, "t": self._token_time}))
        except Exception:
            pass
        return token


def cliente() -> InternalGHLClient:
    loc = os.environ.get("GHL_LOCATION_ID", "").strip()
    if not loc:
        sys.exit("Falta GHL_LOCATION_ID (source tools/ghl-cli/.env)")
    return InternalGHLClient(TokenCacheado(), loc)


# ── Constructores de nodos (solo tipos verificados) ──────────────────────

_META_CAMPOS: dict[str, dict] = {}


def campo(nombre: str, asignaciones: list[tuple[str, str]]) -> dict:
    """update_contact_field — escribe uno o más campos del contacto.

    Cada entrada necesita `title` y `type` además de `field`/`value`: sin ellos
    GHL responde "Title is required., Type is required.". Se resuelven desde el
    volcado real de la subcuenta (docs/ghl-estado/custom-fields.json).
    """
    global _META_CAMPOS
    if not _META_CAMPOS:
        _META_CAMPOS = cargar_estado()["campos"]

    # El nodo tiene que hablar el idioma de la UI, no el del API:
    #   · `field` va con el **id** del campo, no con el fieldKey. Con el fieldKey
    #     el desplegable sale vacío y el nodo queda con error (pasó en WF5).
    #   · `value` va en **array** en los campos que admiten varios valores.
    #   · `type` va en **minúsculas** con el nombre de la UI, no el dataType.
    # Verificado contra el nodo que se recreó a mano en WF4A.
    TIPOS_UI = {
        "CHECKBOX": ("multiselect", True),
        "MULTIPLE_OPTIONS": ("multiselect", True),
        "SINGLE_OPTIONS": ("singleselect", False),
    }

    fields = []
    for f, v in asignaciones:
        meta = _META_CAMPOS.get(f, {})
        if not meta:
            raise ValueError(f"Campo desconocido: {f} (¿está en custom-fields.json?)")
        tipo_ui, es_lista = TIPOS_UI.get(meta["dataType"],
                                         (meta["dataType"].lower(), False))
        fields.append({
            "field": meta["id"],
            "value": ([v] if not isinstance(v, list) else v) if es_lista else v,
            "title": meta["nombre"],
            "type": tipo_ui,
            "date": "",
        })
    return {
        "id": uid(), "type": "update_contact_field", "name": nombre,
        # `actionType` lo llevan todos los nodos de campo de la cuenta,
        # incluidos los que se configuraron a mano en la UI. Sin él el nodo se
        # guarda igual, pero queda distinto a los demás.
        "attributes": {"fields": fields, "actionType": "update_field_data"},
    }


def etiqueta(nombre: str, tags: list[str], quitar: bool = False) -> dict:
    """add_contact_tag / remove_contact_tag."""
    return {
        "id": uid(), "type": "remove_contact_tag" if quitar else "add_contact_tag",
        "name": nombre, "attributes": {"tags": tags},
    }


def mover_a_etapa(nombre: str, pipeline_id: str, stage_id: str,
                  status: str = "open") -> dict:
    """create_opportunity — en GHL no existe "cambiar etapa": esta acción hace
    upsert sobre la oportunidad del contacto, así que sirve para mover de etapa.
    Para cerrar la venta se pasa status="won" (Ganado no es una etapa).

    Esquema descubierto contra la cuenta real: los campos van en snake_case y
    `opportunity_source`, `monetary_value` y `fields` son obligatorios aunque
    la documentación no los mencione.
    """
    return {
        "id": uid(), "type": "create_opportunity", "name": nombre,
        "attributes": {
            "pipeline_id": pipeline_id,
            "stage_id": stage_id,
            "opportunity_name": "{{contact.name}}",
            "opportunity_source": "Workflow",
            "monetary_value": 0,
            "status": status,
            "fields": [],
        },
    }


CAPI_PENDIENTE = "[PENDIENTE-CAPI]"


def capi(nombre: str, evento: str) -> dict:
    """MARCADOR de evento CAPI — no se despliega todavía.

    ⚠️ Bloqueado por dependencia del cliente, no por esquema: el nodo exige
    "Event Type, Access Token y Pixel" y los tres salen del Business Manager de
    Meta, que sigue sin administrador resuelto (llave A1 del checklist).

    En cuanto A1 se resuelva, estos nodos se despliegan con el píxel y el token.
    Recordar el reparto exclusivo: el píxel del navegador solo PageView/ViewContent;
    estos 4 eventos van SOLO server-side o Meta los cuenta doble.
    """
    return {
        "_marcador": CAPI_PENDIENTE, "name": nombre,
        "ramas": [{"nombre": f"evento {evento} (requiere pixel + token de Meta)",
                   "condiciones": []}],
    }


def notificar(nombre: str, asunto: str, cuerpo: str) -> dict:
    """internal_notification — aviso al equipo, no al contacto."""
    return {
        "id": uid(), "type": "internal_notification", "name": nombre,
        "attributes": {"type": "email", "subject": asunto, "body": cuerpo},
    }


def esperar(nombre: str, valor: int, unidad: str = "days") -> dict:
    """wait — ojo: GHL usa 'hour' en singular y 'days'/'minutes' en plural."""
    api_unidad = {"minutes": "minutes", "hours": "hour", "hour": "hour",
                  "days": "days"}.get(unidad, unidad)
    return {
        "id": uid(), "type": "wait", "name": nombre,
        "attributes": {
            "type": "time",
            "startAfter": {"type": api_unidad, "value": valor, "when": "after"},
            "name": nombre, "cat": "", "isHybridAction": True,
            "hybridActionType": "wait", "convertToMultipath": False,
            "transitions": [],
        }, "cat": "",
    }


def bifurcar(nombre: str, condiciones: list[dict], rama_si: list[dict],
             rama_no: list[dict] | None = None, operador: str = "and") -> list[dict]:
    """if_else — devuelve la LISTA de nodos de la bifurcación, ya enlazados.

    El if_else no es un paso lineal: es un nodo de canvas cuyo `next` es un
    ARRAY con los ids de sus ramas ("If/else condition node must have next as
    array"). Cada rama es un nodo aparte con nodeType branch-yes / branch-no,
    y su `next` apunta al primer paso de esa rama.

    Los pasos de cada rama se encadenan entre sí y NO deben pasar por
    link_steps() después, o se les pisa el parentKey.
    """
    cid, yid, nid = uid(), uid(), uid()

    def encadenar(pasos: list[dict], padre: str) -> list[dict]:
        """Encadena los pasos de una rama. NO admite bifurcaciones anidadas:
        el canvas de GHL las rechaza con "Add at least one branch" (probado)."""
        salida = []
        for i, paso in enumerate(pasos):
            paso = {**paso}
            paso["parentKey"] = padre if i == 0 else pasos[i - 1]["id"]
            paso["next"] = pasos[i + 1]["id"] if i < len(pasos) - 1 else None
            salida.append(paso)
        return salida

    # Los marcadores (CAPI pendiente) no son nodos reales: se apartan del
    # encadenado y se devuelven al final para que el despliegue los reporte.
    marcadores = [s for s in rama_si + (rama_no or []) if es_marcador(s)]
    si = encadenar([s for s in rama_si if not es_marcador(s)], yid)
    no = encadenar([s for s in (rama_no or []) if not es_marcador(s)], nid)
    for n in si + no:
        n["_en_rama"] = True     # ensamblar() no debe re-encadenarlos

    # GHL exige SIEMPRE dos ramas y que ninguna esté vacía. Si la definición no
    # da rama "no", se rellena con un paso inocuo (tag) para satisfacer al canvas.
    if not no:
        # GHL exige que la rama exista y no esté vacía. Se usa una espera mínima
        # como no-op: a diferencia de un tag, no ensucia los datos del contacto.
        relleno = esperar(f"{nombre} - sin accion", 1, "minutes")
        relleno.update(parentKey=nid, next=None, _en_rama=True)
        no = [relleno]
    ramas_ids = [yid, nid]
    nodos = [
        {"id": cid, "type": "if_else", "name": nombre, "nodeType": "condition-node",
         "attributes": {"name": nombre, "operator": operador, "if": condiciones},
         "next": ramas_ids, "parentKey": None},
        {"id": yid, "type": "if_else", "name": f"{nombre} - Si", "nodeType": "branch-yes",
         "attributes": {"name": f"{nombre} - Si"},
         "next": si[0]["id"] if si else None, "parentKey": cid},
    ]
    nodos.append(
        {"id": nid, "type": "if_else", "name": f"{nombre} - No", "nodeType": "branch-no",
         "attributes": {"name": f"{nombre} - No"},
         "next": no[0]["id"], "parentKey": cid})
    nodos += si + no

    for i, n in enumerate(nodos):
        n["order"] = i
    return nodos + marcadores


def es_marcador(step: dict) -> bool:
    return "_marcador" in step


def cond(field: str, operator: str, value: Any) -> dict:
    return {"field": field, "operator": operator, "value": value}


def email(nombre: str, asunto: str, cuerpo_html: str) -> dict:
    return {
        "id": uid(), "type": "email", "name": nombre,
        "attributes": {
            "subject": asunto, "body": cuerpo_html, "html": cuerpo_html,
            "fromName": "{{custom_values.firma_luca}}", "attachments": [],
            "conditions": [],
            "trackingOptions": {"hasTrackingLinks": False,
                                "hasUtmTracking": False, "hasTags": False},
        },
    }


def whatsapp(nombre: str, plantilla: str, cuerpo: str) -> dict:
    """Envío de WhatsApp.

    ⚠️ PENDIENTE: no existe un tipo `whatsapp` en GHL (verificado: rechaza
    whatsapp/wa/whatsapp_message/send_whatsapp con "corrupted type"). Se
    construye como `sms` y GHL enruta por canal, pero falta confirmar en la UI
    cómo se marca canal=WhatsApp y cómo se referencia la plantilla aprobada.

    Hasta confirmarlo, el nodo se crea como `sms` con el nombre marcado
    [PENDIENTE-WA] y la plantilla anotada en los attributes, para localizarlos
    y corregirlos en bloque después.
    """
    return {
        "id": uid(), "type": "sms", "name": f"{WHATSAPP_PENDIENTE} {nombre}",
        "attributes": {
            "body": cuerpo, "attachments": [],
            "_plantilla_meta": plantilla,   # anotación nuestra, GHL la ignora
            "_canal_pendiente": "whatsapp",
        },
    }


# ── Despliegue ───────────────────────────────────────────────────────────

def tags_usados(workflows: list) -> set[str]:
    """Todos los tags que referencian los workflows: los que añaden/quitan y los
    que aparecen en condiciones de bifurcación."""
    usados: set[str] = set()
    for _, fn in workflows:
        for s in fn():
            if es_marcador(s):
                continue
            a = s.get("attributes", {})
            usados.update(a.get("tags", []) or [])
            for cnd in a.get("if", []) or []:
                if isinstance(cnd, dict) and cnd.get("field") == "contact.tags":
                    if cnd.get("value"):
                        usados.add(cnd["value"])
    return usados


def crear_tags(c: InternalGHLClient, tags: set[str]) -> list[str]:
    """Crea los tags a nivel de subcuenta y devuelve los que existen al terminar.

    Los tags deben existir en la subcuenta para poder seleccionarlos en triggers
    y condiciones desde la UI. `add_contact_tag` los crearía en tiempo de
    ejecución, pero entonces no aparecen en los selectores al configurar.

    Ojo: el endpoint responde con cuerpo VACÍO, así que `create_location_tag()`
    del cliente devuelve False aunque haya funcionado. Por eso aquí se verifica
    contra el listado real en lugar de confiar en el valor de retorno.
    """
    from cli_anything.gohighlevel.utils import ghl_client as g
    for tag in sorted(tags):
        c.request("POST", f"/workflow/{c.location_id}/tags/create", {"tag": tag})
    existentes = {t if isinstance(t, str) else t.get("name")
                  for t in g.get(f"/locations/{c.location_id}/tags").get("tags", [])}
    return sorted(tags - existentes)      # los que faltaron


def listar_todo(c: InternalGHLClient) -> list[dict]:
    """Workflows Y carpetas de la subcuenta.

    Ojo: `GET /workflow/{loc}` devuelve SOLO workflows — las carpetas no
    aparecen. Para verlas hay que usar `/workflow/{loc}/directory`, que
    responde {count, rows}.
    """
    r = c.request("GET", f"/workflow/{c.location_id}/directory") or {}
    return r.get("rows", []) if isinstance(r, dict) else []


def carpeta(c: InternalGHLClient, nombre: str) -> str | None:
    """Devuelve el id de la carpeta, reutilizándola si ya existe.

    Antes se buscaba en `GET /workflow/{loc}`, que no lista carpetas: nunca la
    encontraba y creaba una nueva en cada corrida, dejando duplicados en la
    cuenta del cliente.
    """
    for f in listar_todo(c):
        if f.get("type") == "directory" and f.get("name") == nombre:
            return f.get("id") or f.get("_id")
    r = c.request("POST", f"/workflow/{c.location_id}",
                  {"name": nombre, "type": "directory"})
    return r.get("id") if r else None


def ensamblar(steps: list[dict]) -> list[dict]:
    """Enlaza una mezcla de pasos planos y bifurcaciones.

    Los pasos planos se encadenan en secuencia; los nodos de una bifurcación ya
    vienen enlazados entre sí (`bifurcar()`), así que solo hay que engancharlos
    al último paso plano anterior. Al final se renumera `order` de forma global:
    si dos bloques repiten el índice GHL responde "corrupted order".
    """
    salida: list[dict] = []
    anterior: dict | None = None      # último nodo de la cadena plana

    for paso in steps:
        paso = {**paso}
        if "nodeType" in paso:
            # nodo de bifurcación: solo se ajusta el enganche del condition-node
            if paso["nodeType"] == "condition-node":
                if anterior is not None:
                    anterior["next"] = paso["id"]
                    paso["parentKey"] = anterior["id"]
                anterior = None       # tras ramificar ya no hay cadena plana
            salida.append(paso)
            continue

        if paso.pop("_en_rama", False):
            salida.append(paso)      # ya enlazado por bifurcar()
            continue

        # paso plano
        if anterior is not None:
            anterior["next"] = paso["id"]
            paso["parentKey"] = anterior["id"]
        else:
            paso.setdefault("parentKey", None)
        paso["next"] = None
        salida.append(paso)
        anterior = paso

    # GHL dejó de aceptar `next: null` — responde "Next is invalid. Please
    # provide a valid value." La clave hay que **omitirla** en los nodos
    # terminales. Se barre aquí al final para cubrir también los nodos que
    # vienen ya enlazados desde bifurcar().
    for s in salida:
        if s.get("next", "sin-clave") is None:
            s.pop("next", None)

    for i, s in enumerate(salida):
        s["order"] = i
    return salida


def guardar(c: InternalGHLClient, wid: str, nombre: str, steps: list[dict]) -> tuple[bool, Any]:
    """PUT leyendo la versión actual primero.

    Imprescindible: GHL usa versionado optimista y el builder de la CLI manda
    version:1 fijo, por eso su --update está roto.
    """
    templates = ensamblar(steps)

    actual = c.request("GET", f"/workflow/{c.location_id}/{wid}") or {}
    r = c.request("PUT", f"/workflow/{c.location_id}/{wid}", {
        "name": nombre, "version": actual.get("version", 1),
        "workflowData": {"templates": templates},
    })
    return bool(r and not r.get("_error")), r


def desplegar(c: InternalGHLClient, nombre_wf: str, steps: list[dict],
              folder_id: str, dry_run: bool = False) -> dict:
    """Crea el workflow (draft) y guarda sus pasos."""
    reales = [s for s in steps if not es_marcador(s)]
    bifurcaciones = [s for s in steps if es_marcador(s)]  # solo quedan los CAPI
    pendientes = [s["name"] for s in reales if WHATSAPP_PENDIENTE in s.get("name", "")]

    detalle = []
    for s in steps:
        if es_marcador(s):
            ramas = " | ".join(r["nombre"] for r in s["ramas"])
            detalle.append(f'   {s["_marcador"]} {s["name"]}  ->  {ramas}')
        else:
            detalle.append(f'   [{s["type"]}] {s["name"]}')

    if dry_run:
        return {"workflow": nombre_wf, "pasos": len(reales),
                "pendientes_wa": len(pendientes), "bifurcaciones": len(bifurcaciones),
                "dry_run": True, "detalle": detalle}

    r = c.request("POST", f"/workflow/{c.location_id}",
                  {"name": nombre_wf, "parentId": folder_id})
    wid = r.get("id") if r else None
    if not wid:
        return {"workflow": nombre_wf, "error": f"no se pudo crear: {r}"}

    # El backend de GHL falla de forma intermitente al guardar varios workflows
    # seguidos (mismo payload pasa al reintentar). Hasta 3 intentos con pausa.
    import time
    ok, resp = False, None
    for intento in range(5):
        ok, resp = guardar(c, wid, nombre_wf, reales)
        if ok:
            break
        time.sleep(2.0 * (intento + 1))

    return {"workflow": nombre_wf, "id": wid, "pasos": len(reales),
            "pendientes_wa": len(pendientes), "bifurcaciones": len(bifurcaciones),
            "guardado": ok, "error": (None if ok else str(resp)[:200])}


def resumen(resultados: list[dict]) -> None:
    print("\n" + "=" * 66)
    total = sum(r.get("pasos", 0) for r in resultados)
    wa = sum(r.get("pendientes_wa", 0) for r in resultados)
    bif = sum(r.get("bifurcaciones", 0) for r in resultados)
    for r in resultados:
        if r.get("error"):
            print(f"  ✗ {r['workflow']:44} {r['error'][:60]}")
        else:
            estado = "DRY-RUN" if r.get("dry_run") else ("OK" if r.get("guardado") else "FALLÓ")
            print(f"  {'✓' if estado != 'FALLÓ' else '✗'} {r['workflow']:44} "
                  f"{r['pasos']:2} pasos  ({r['pendientes_wa']} WA, "
                  f"{r.get('bifurcaciones',0)} IF)  {estado}")
    print("=" * 66)
    print(f"  {len(resultados)} workflows · {total} pasos desplegados")
    print(f"  PENDIENTES: {wa} nodos WhatsApp · {bif} eventos CAPI")
    if wa:
        print(f'\n  WhatsApp: creados como `sms` marcados "{WHATSAPP_PENDIENTE}" —')
        print("            falta confirmar canal y plantilla aprobada de Meta.")
    if bif:
        print(f'  CAPI: no desplegados ("{CAPI_PENDIENTE}") — requieren pixel y')
        print("        access token de Meta (llave A1 del checklist).")
