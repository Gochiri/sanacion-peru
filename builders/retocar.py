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

        r = c.request("PUT", f"/workflow/{loc}/{wid}", {
            "name": nombre,
            "version": actual.get("version", 1),
            "workflowData": {**wd, "templates": templates},
        })
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nombre:34} {n} sustitucion(es)  ({motivo})"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")


if __name__ == "__main__":
    main()
