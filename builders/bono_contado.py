"""Separa el bono de contado de WF5, que hoy se lo lleva todo el mundo.

**El problema.** En WF5 el nodo se llama «Activar bono si pago de contado», pero
ese «si» no existe: no hay ninguna condición delante. Se vio el 29-sep
recorriendo el grafo real del workflow, no el orden de la lista. Tal como está,
la primera persona que pague en tres cuotas activa el bono igual y a Christie le
llega el aviso de entregarle una sesión de 40 minutos que no le corresponde.

**Por qué un workflow aparte y no una rama dentro de WF5.** GHL rechaza por API
el formato de `if_else` que sabemos construir —«Condition: Expected boolean,
received array»—, así que meter una condición nueva dentro de WF5 no se puede
desde aquí. Y no hace falta: el closer ya marca el cobro con una etiqueta, así
que basta con que haya dos y que cada una entre donde toca.

    pago-manual-cuotas   →  WF5                (lo común: venta, alta, Meta)
    pago-manual-contado  →  WF5  +  este       (y además el bono)

**Lo que queda por hacer a mano**, porque crear triggers por API no engancha —el
POST devuelve 200 y el trigger no aparece (`docs/ghl-estado/triggers-pendientes.md`):

  1. En WF5, añadir las dos etiquetas como disparador, junto a `pago-manual`.
  2. En este, la etiqueta `pago-manual-contado` como disparador.
  3. Cuando este se publique, quitar de WF5 los dos nodos del bono —«Activar
     bono si pago de contado» y «Avisar a Christie»—, que pasan a vivir aquí.
     Eso lo hago yo por API cuando se dé la orden; hasta entonces WF5 no se toca
     y su comportamiento no cambia.

Nace en **borrador**.

    python3 builders/bono_contado.py --dry-run
    python3 builders/bono_contado.py
"""
from __future__ import annotations

import argparse
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from esb_lib import (  # noqa: E402
    CARPETA, campo, carpeta, cliente, desplegar, guardar, resumen, uid,
)

# El cliente lo renombró al publicarlo, el 29-sep: el bono es solo de LATAM,
# porque Christie da la sesión en español. Si esto no coincide con el nombre
# real, volver a correr el script crearía un workflow duplicado.
NOMBRE = "WF5b - Bono de contado LATAM"

# El id de Christie en la subcuenta, copiado del nodo que hoy vive en WF5.
CHRISTIE = "BrFbQVQSRj6Q7UDUlNiK"

CUERPO = (
    '<p style="margin:0px;font-family:verdana,geneva,sans-serif;font-size:16px;'
    ' padding-left: 0px!important;margin: 0px;font-family: verdana,geneva,sans-serif;'
    'font-size: 16px;">{{contact.name}} pagó la escuela al contado, así que le '
    'corresponde la sesión de bienvenida de 40 minutos.</p>'
    '<p style="margin:0px;font-family:verdana,geneva,sans-serif;font-size:16px;'
    ' padding-left: 0px!important;">Contacto: {{contact.email}} · {{contact.phone}}</p>'
    '<p style="margin:0px;font-family:verdana,geneva,sans-serif;font-size:16px;'
    ' padding-left: 0px!important;">Conviene escribirle en los próximos días, '
    'mientras la decisión está fresca.</p>'
)


def aviso_christie() -> dict:
    return {
        "id": uid(), "type": "internal_notification",
        "name": "Avisar a Christie: sesion bono de 40 min",
        "cat": "", "workflowsActionType": "INTERNAL",
        "attributes": {
            "type": "email",
            "email": {
                "html": CUERPO,
                "from_name": "La nueva conciencia",
                "from_email": "mail@lanuovacoscienza.com",
                "selectedUser": [CHRISTIE],
                "userType": "user",
                "subject": "Bono por entregar · sesión de 40 min con {{contact.name}}",
                "attachments": [],
            },
            "__name__": "Avisar a Christie: sesion bono de 40 min",
        },
    }


def pasos() -> list[dict]:
    return [
        # El plan de pago no lo escribía nadie, aunque el campo existe con sus
        # tres opciones. Si la etiqueta dice contado, que quede registrado.
        campo("Registrar el plan: contado", [("contact.plan_pago", "Contado")]),
        campo("Activar el bono", [("contact.bono_llamada_christie", "Si")]),
        aviso_christie(),
    ]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        resumen([desplegar(None, NOMBRE, pasos(), None, dry_run=True)])
        return

    c = cliente()
    lst = c.request("GET", f"/workflow/{c.location_id}") or []
    if isinstance(lst, dict):
        lst = lst.get("workflows") or lst.get("data") or []
    ya = [w for w in lst if isinstance(w, dict) and w.get("name") == NOMBRE]
    if ya:
        wid = ya[0].get("id") or ya[0].get("_id")
        ok, r = guardar(c, wid, NOMBRE, pasos())
        print("%s %s  (ya existía: %s)" % ("✓" if ok else "✗", NOMBRE, wid))
        if not ok:
            print("   %s" % str(r)[:300])
    else:
        fid = carpeta(c, CARPETA)
        if not fid:
            sys.exit("No se pudo crear/encontrar la carpeta")
        resumen([desplegar(c, NOMBRE, pasos(), fid)])
    print("\nQueda en BORRADOR y sin disparador. Los tres pasos que faltan están"
          " en la cabecera de este archivo.")


if __name__ == "__main__":
    main()
