"""Reenvía el enlace del grupo italiano a quien recibió uno que ya no abre.

**Por qué existe.** El enlace del grupo de WhatsApp italiano cambió tres veces
en tres semanas (ver `GRUPOS` en `valores.py`). Cada cambio deja fuera a todo el
que ya recibió el anterior: el enlace viaja en un mensaje que está en su móvil, y
ahí no llega ningún cambio nuestro. El 24-sep el cliente avisó de que llevaba dos
días sin que entrara nadie, con 21 italianos registrados en ese tramo.

**Cómo se usa.** No lleva trigger a propósito, por dos razones: crear triggers
por API no funciona —el POST devuelve 200 y nunca se engancha, ver
`docs/ghl-estado/triggers-pendientes.md`— y aquí no hace falta, porque los
destinatarios ya existen. Se inscriben a mano:

    Contactos → filtrar por Mercado = Italia → seleccionar todos
             → Acciones → Añadir a workflow → este

Nace en **borrador**. Quien lo publica decide cuándo sale.

    python3 builders/reenvio_grupo_it.py --dry-run
    python3 builders/reenvio_grupo_it.py
"""
from __future__ import annotations

import argparse
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from esb_lib import (  # noqa: E402
    CARPETA, carpeta, cliente, desplegar, ensamblar, guardar, resumen, whatsapp_v2,
)

NOMBRE = "WF-IT - Reenvio del enlace del grupo (una vez)"

# El texto de la plantilla ya aprobada por Meta. Lo que de verdad se manda son
# los parámetros —el nombre y el enlace—; el texto va aquí para que el nodo no
# mienta a quien lo abra en el builder.
CUERPO = ("Ciao {{contact.first_name}}, la tua iscrizione è confermata. "
          "Entra nel gruppo per ricevere l'accesso: "
          "{{custom_values.link_grupo_whatsapp_it}}\n\n"
          "Ci vediamo nel gruppo!")


def pasos() -> list[dict]:
    """Un solo nodo, sin guarda de mercado.

    La llevaba —un `if_else` que comprobara `Mercado = Italia`, para que un
    español inscrito por error no recibiera un mensaje en italiano— pero GHL
    rechaza por API el formato de `if_else` que sabemos construir: «Condition:
    Expected boolean, received array». Los que hay en la cuenta se hicieron en
    la UI y usan otro formato, con `version: 2`.

    No merece la pena pelearse con eso para un envío de una vez: la guarda de
    verdad es la lista desde la que se inscribe, filtrada por Mercado = Italia.
    Quien lo dispare que mire esa lista antes.
    """
    return [whatsapp_v2("Reenvio del enlace del grupo",
                        "bienvenida_registro_it", CUERPO)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        resumen([desplegar(None, NOMBRE, pasos(), None, dry_run=True)])
        return

    c = cliente()

    # Si ya existe se reescribe, en vez de dejar un duplicado en la cuenta del
    # cliente cada vez que se corrige algo.
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
    print("\nQueda en BORRADOR. Para usarlo: Contactos → Mercado = Italia →"
          " seleccionar → Anadir a workflow, y publicarlo.")


if __name__ == "__main__":
    main()
