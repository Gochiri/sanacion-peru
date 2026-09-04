#!/usr/bin/env python3
"""Retoques quirúrgicos sobre workflows que ya se editaron en la UI.

**Por qué existe.** Los workflows que alguien tocó en la UI de GHL quedan
guardados en el formato *rico* del canvas: las condiciones dejan de ser
`attributes.if = [{field, operator, value}]` y pasan a
`attributes.branches[].segments[].conditions[]`, con `conditionType`,
`conditionSubType` (el id del campo), `conditionOperator`, más `sibling`,
`cat` y las posiciones del canvas.

A partir de ese momento el builder ya no puede reescribirlos:

1. GHL **rechaza** el formato antiguo con "Action validation failed for
   if_else" / "Add at least one branch".
2. Y aunque lo aceptara, reescribirlos **borraría las correcciones hechas a
   mano** en la UI, que son las buenas.

Así que para cambiar un texto o una referencia a un custom value en esos
workflows se leen sus templates, se sustituye la cadena donde aparezca y se
devuelven tal cual. Nada más se toca.

    python builders/retocar.py --dry-run
    python builders/retocar.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from esb_lib import cliente  # noqa: E402

# (workflow, texto viejo, texto nuevo, por qué)
RETOQUES: list[tuple[str, str, str, str]] = [
    ("WF3-ES - Recordatorios de evento",
     "{{custom_values.link_evento_es}}",
     "{{trigger_link.zsM5LP4jGLvvLbNG8hXy}}",
     "el enlace del evento va como trigger link, o WF4A no sabe quien entro"),

    ("WF3-ES - Recordatorios de evento",
     "{{custom_values.fecha_evento_vigente}}",
     "{{custom_values.fecha_evento_es}}",
     "K12: cada mercado tiene su dia (jueves ES / sabado IT)"),

    ("WF4B - Postulacion",
     "Agenda tu llamada con Luca",
     "Agenda tu llamada de cierre",
     "K11: en espanol cierra Joaquin, no Luca"),

    ("WF2 - Registro y calificacion",
     "Te esperamos el {{custom_values.fecha_evento_vigente}} a las "
     "{{custom_values.hora_evento_pe}}.",
     "Tu lugar quedo confirmado. Te enviamos el recordatorio con el dia y la "
     "hora, y el acceso por el grupo: {{custom_values.link_grupo_whatsapp_es}}",
     "WF2 no bifurca por mercado: no puede saber que fecha toca"),
]


# (workflow, nombre del nodo, fields nuevos, por qué)
#
# El builder escribía `field` como fieldKey y `type` como el dataType del API en
# mayúsculas. La UI no resuelve eso: el desplegable sale vacío y el nodo da error.
# El formato bueno se sacó del nodo que Oliver recreó a mano en WF4A:
#     {"field": "<id>", "value": ["Si"], "title": "...", "type": "multiselect", "date": ""}
# o sea: **id** del campo, valor en array donde el campo admite varios, y el tipo
# de la UI en minúsculas.
RETOQUES_CAMPOS: list[tuple[str, str, list[dict], str]] = [
    ("WF5 - Cobro confirmado", "Activar bono si pago de contado",
     [{"field": "7YhSYFuz89u6Vf05Fk4u", "value": ["Si"],
       "title": "Bono llamada christie", "type": "multiselect", "date": ""}],
     "CHECKBOX -> multiselect (verificado contra WF4A)"),

    ("WF5 - Cobro confirmado", "Registrar datos de la venta",
     [{"field": "nHjHVOUlxUefgbhI9v5J", "value": ["Escuela"],
       "title": "Producto comprado", "type": "multiselect", "date": ""},
      {"field": "zSvMgseoMi5Zub9tQr3i", "value": "Al dia",
       "title": "Estado pago", "type": "singleselect", "date": ""}],
     "INFERIDO para MULTIPLE_OPTIONS y SINGLE_OPTIONS — verificar en la UI"),
]


LUCA     = "nEVI8WGKSdfvkR9FUyXM"
CHRISTIE = "BrFbQVQSRj6Q7UDUlNiK"
REMITENTE = {"fromEmail": "mail@lanuovacoscienza.com", "fromName": "La nueva conciencia"}

# (workflow, nombre del nodo, attributes nuevos, por qué)
#
# ⚠️ El formato de `internal_notification` NO está verificado: los nombres de los
# atributos de remitente y destinatario van inferidos. Si en la UI sigue saliendo
# el aviso naranja, configurar UNO a mano, leerlo por API y replicar el formato
# bueno aquí. No adivinar dos veces (ver triggers-pendientes.md).
RETOQUES_AVISOS: list[tuple[str, str, dict, str]] = [
    ("WF5 - Cobro confirmado", "Avisar a Luca: dar de alta en System.io",
     {**REMITENTE, "type": "email", "userType": "particularUser", "users": [LUCA],
      "subject": "Alta pendiente · {{contact.name}} ya pagó la escuela",
      "body": ("{{contact.name}} completó el pago de la escuela.\n\n"
               "Contacto:  {{contact.email}} · {{contact.phone}}\n"
               "Producto:  {{contact.producto_comprado}}\n\n"
               "Hay que crearle el acceso en System.io. Mientras no se haga, "
               "el alumno pagó y no puede entrar.")},
     "primer pago: pide alta manual"),

    ("WF5 - Cobro confirmado", "Avisar a Christie: sesion bono de 40 min",
     {**REMITENTE, "type": "email", "userType": "particularUser", "users": [CHRISTIE],
      "subject": "Bono por entregar · sesión de 40 min con {{contact.name}}",
      "body": ("{{contact.name}} pagó la escuela al contado, así que le corresponde "
               "la sesión de bienvenida de 40 minutos.\n\n"
               "Contacto:  {{contact.email}} · {{contact.phone}}\n\n"
               "Conviene escribirle en los próximos días, mientras la decisión "
               "está fresca.")},
     "pago de contado: agendar el bono"),

    ("WF5 - Cobro confirmado", "Avisar a Luca: cuota recibida",
     {**REMITENTE, "type": "email", "userType": "particularUser", "users": [LUCA],
      "subject": "Cuota recibida · {{contact.name}}",
      "body": ("Entró una cuota más de {{contact.name}}.\n\n"
               "No hay que hacer nada: la venta ya está registrada y el alumno ya "
               "tiene su acceso. Es solo para que quede constancia del cobro.")},
     "cuota posterior: NO pide accion"),
]


def sustituir(valor, viejo: str, nuevo: str) -> tuple[object, int]:
    """Recorre listas y diccionarios sustituyendo en cualquier cadena."""
    if isinstance(valor, str):
        return (valor.replace(viejo, nuevo), valor.count(viejo))
    if isinstance(valor, list):
        cambiados = 0
        salida = []
        for v in valor:
            v2, n = sustituir(v, viejo, nuevo)
            salida.append(v2); cambiados += n
        return salida, cambiados
    if isinstance(valor, dict):
        cambiados = 0
        salida = {}
        for k, v in valor.items():
            v2, n = sustituir(v, viejo, nuevo)
            salida[k] = v2; cambiados += n
        return salida, cambiados
    return valor, 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    c = cliente(); loc = c.location_id
    lst = c.request("GET", f"/workflow/{loc}") or []
    if isinstance(lst, dict):
        lst = lst.get("workflows") or lst.get("data") or []
    ids = {w.get("name"): (w.get("id") or w.get("_id")) for w in lst
           if isinstance(w, dict) and w.get("type") != "directory"}

    for nombre, viejo, nuevo, motivo in RETOQUES:
        wid = ids.get(nombre)
        if not wid:
            print(f"  ✗ {nombre:34} no existe")
            continue

        actual = c.request("GET", f"/workflow/{loc}/{wid}") or {}
        wd = actual.get("workflowData") or {}
        templates, n = sustituir(wd.get("templates") or [], viejo, nuevo)

        if not n:
            print(f"  = {nombre:34} nada que cambiar  ({motivo})")
            continue
        if args.dry_run:
            print(f"  · {nombre:34} {n} sustitucion(es)  ({motivo})  DRY-RUN")
            continue

        # `status` se reenvía a propósito: un PUT sin él lo deja en null y el
        # workflow queda DESPUBLICADO en silencio. Pasó con WF2, WF3-ES y WF4B.
        cuerpo = {
            "name": nombre,
            "version": actual.get("version", 1),
            "workflowData": {**wd, "templates": templates},
        }
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nombre:34} {n} sustitucion(es)  ({motivo})"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")

    aplicar_campos(c, loc, ids, args.dry_run)
    aplicar_avisos(c, loc, ids, args.dry_run)


def aplicar_avisos(c, loc, ids, dry_run: bool) -> None:
    """Reescribe por completo los `attributes` de una notificación interna."""
    for nombre, nodo, attrs, motivo in RETOQUES_AVISOS:
        wid = ids.get(nombre)
        if not wid:
            print(f"  ✗ {nombre:34} no existe"); continue

        actual = c.request("GET", f"/workflow/{loc}/{wid}") or {}
        wd = actual.get("workflowData") or {}
        templates = [dict(t) for t in (wd.get("templates") or [])]

        tocados = 0
        for t in templates:
            if t.get("name") != nodo:
                continue
            t["attributes"] = attrs
            tocados += 1

        if not tocados:
            print(f"  = {nodo:38} no encontrado"); continue
        if dry_run:
            print(f"  · {nodo:38} ({motivo})  DRY-RUN"); continue

        cuerpo = {"name": nombre, "version": actual.get("version", 1),
                  "workflowData": {**wd, "templates": templates}}
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nodo:38} ({motivo})"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")


def aplicar_campos(c, loc, ids, dry_run: bool) -> None:
    """Reescribe por completo los `fields` de un nodo, localizado por su nombre."""
    for nombre, nodo, campos, motivo in RETOQUES_CAMPOS:
        wid = ids.get(nombre)
        if not wid:
            print(f"  ✗ {nombre:34} no existe"); continue

        actual = c.request("GET", f"/workflow/{loc}/{wid}") or {}
        wd = actual.get("workflowData") or {}
        templates = [dict(t) for t in (wd.get("templates") or [])]

        tocados = 0
        for t in templates:
            if t.get("name") != nodo:
                continue
            t["attributes"] = {**(t.get("attributes") or {}), "fields": campos}
            tocados += 1

        if not tocados:
            print(f"  = {nodo:34} no encontrado en {nombre}"); continue
        if dry_run:
            print(f"  · {nodo:34} {len(campos)} campo(s)  ({motivo})  DRY-RUN"); continue

        cuerpo = {"name": nombre, "version": actual.get("version", 1),
                  "workflowData": {**wd, "templates": templates}}
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nodo:34} {len(campos)} campo(s)  ({motivo})"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")


if __name__ == "__main__":
    main()
