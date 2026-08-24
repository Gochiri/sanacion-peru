#!/usr/bin/env python3
"""Completa el despliegue: crea solo los workflows que falten o quedaron vacíos.

El PUT del API interno rechaza de forma intermitente cuando se guardan varios
workflows seguidos (rate limit no documentado: el mismo payload pasa al
reintentar más tarde). Este script va de uno en uno, con pausas largas, y es
idempotente: se puede relanzar hasta que todo quede completo.
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from esb_lib import CARPETA, carpeta, cliente, es_marcador, guardar
from build_fase1 import WORKFLOWS

PAUSA = 8          # segundos entre workflows
INTENTOS = 6

def main():
    c = cliente(); loc = c.location_id
    fid = carpeta(c, CARPETA)

    lst = c.request("GET", f"/workflow/{loc}") or []
    if isinstance(lst, dict):
        lst = lst.get("workflows") or lst.get("data") or []
    existentes = {}
    for w in lst:
        if isinstance(w, dict) and w.get("type") != "directory":
            wid = w.get("id") or w.get("_id")
            got = c.request("GET", f"/workflow/{loc}/{wid}") or {}
            pasos = len((got.get("workflowData") or {}).get("templates") or [])
            existentes[w.get("name")] = (wid, pasos)

    for nombre, fn in WORKFLOWS:
        steps = [s for s in fn() if not es_marcador(s)]
        wid, pasos = existentes.get(nombre, (None, 0))

        if wid and pasos == len(steps):
            print(f"  = {nombre:34} ya completo ({pasos} pasos)")
            continue

        if not wid:
            r = c.request("POST", f"/workflow/{loc}", {"name": nombre, "parentId": fid})
            wid = r.get("id") if r else None
            if not wid:
                print(f"  ✗ {nombre:34} no se pudo crear")
                continue

        ok = False
        for i in range(INTENTOS):
            ok, r = guardar(c, wid, nombre, steps)
            if ok:
                break
            time.sleep(PAUSA)
        print(f"  {'✓' if ok else '✗'} {nombre:34} {len(steps)} pasos"
              f"{'' if ok else '  ' + str(r.get('message', r))[:80]}")
        time.sleep(PAUSA)

if __name__ == "__main__":
    main()
