"""Carga en los custom values lo que el cliente confirmó el 4-sep.

Hay dos clases de valor y por eso hay dos comandos:

  · **ciclo**  — lo que cambia en cada webinar (fecha, hora, nombre del
                 lanzamiento). Son dos ciclos y hay que rotarlos: el ciclo 2 se
                 carga el 25-sep, en cuanto termina el primer webinar.
  · **fijos**  — lo que no cambia entre ciclos (datos de cobro manual).

    python3 builders/valores.py ciclo 1
    python3 builders/valores.py ciclo 2 --aplicar
    python3 builders/valores.py fijos --aplicar

El formato de cada valor está fijado por dónde se consume, no por gusto:
`fecha_evento_es` se lee en las fichas de registro-es y gracias-es, y la
variante `_iso` alimenta la cuenta atrás de evento-es y el botón «añadir al
calendario» de gracias-es. Si se rompe el ISO, la cuenta atrás no arranca.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import publico  # noqa: E402

CICLOS = {
    # Webinar 1 · LATAM jueves 24-sep 20:00 Perú · Italia sábado 26-sep 18:00
    "1": {
        "nombre_lanzamiento_vigente": "LNZ-2026-W39",
        "fecha_evento_es": "jueves 24 de septiembre",
        "fecha_evento_es_iso": "2026-09-24T20:00:00-05:00",
        "hora_evento_pe": "8:00 p. m. (hora de Perú)",
        "fecha_evento_it": "sabato 26 settembre",
        "fecha_evento_it_iso": "2026-09-26T18:00:00+02:00",
        "hora_evento_it": "18:00 (ora italiana)",
    },
    # Webinar 2 · LATAM jueves 1-oct 20:00 Perú · Italia sábado 3-oct 18:00
    "2": {
        "nombre_lanzamiento_vigente": "LNZ-2026-W40",
        "fecha_evento_es": "jueves 1 de octubre",
        "fecha_evento_es_iso": "2026-10-01T20:00:00-05:00",
        "hora_evento_pe": "8:00 p. m. (hora de Perú)",
        "fecha_evento_it": "sabato 3 ottobre",
        "fecha_evento_it_iso": "2026-10-03T18:00:00+02:00",
        "hora_evento_it": "18:00 (ora italiana)",
    },
}

# El cliente escribió «Nueva Consciencia» (con S) en los datos bancarios, y en
# el resto del proyecto la razón social figura como «Nueva Conciencia». Aquí va
# tal cual lo mandó: el titular tiene que coincidir con el del banco o la
# transferencia rebota. Confirmarlo antes de que salga a un cliente.
FIJOS = {
    "datos_pago_pe": (
        "Transferencia bancaria (Perú)\n"
        "Titular: Nueva Consciencia Formación SAC\n"
        "Banco: BCP · cuenta en soles\n"
        "Cuenta: 1937405302029\n"
        "CCI: 00219300740530202918"
    ),
    # ⚠ Falta el titular de la cuenta italiana. Un bonifico sin intestatario se
    # devuelve. Completar antes de darlo a nadie.
    "datos_pago_it": (
        "Bonifico bancario (Italia)\n"
        "Banca: Intesa Sanpaolo\n"
        "IBAN: IT98L0306979654100000006623"
    ),
}


def _indice() -> dict[str, dict]:
    cod, r = publico.pedir("GET", "/locations/%s/customValues" % os.environ["GHL_LOCATION_ID"])
    if cod != 200:
        raise SystemExit("No se pudieron leer los custom values: %s" % r)
    salida = {}
    for c in r.get("customValues", []):
        clave = c.get("fieldKey", "").replace("{{ custom_values.", "").replace(" }}", "").strip()
        salida[clave] = c
    return salida


def cargar(valores: dict[str, str], escribir: bool) -> None:
    indice = _indice()
    for clave, nuevo in valores.items():
        cv = indice.get(clave)
        if cv is None:
            print("  ✗ %-28s no existe en la subcuenta" % clave)
            continue
        actual = cv.get("value") or ""
        if actual == nuevo:
            print("  = %-28s ya estaba" % clave)
            continue
        print("  %s %-28s %s → %s"
              % ("→" if escribir else "·", clave,
                 (actual[:22] or "(vacío)"), nuevo.replace("\n", " / ")[:46]))
        if not escribir:
            continue
        cod, r = publico.pedir(
            "PUT", "/locations/%s/customValues/%s" % (os.environ["GHL_LOCATION_ID"], cv["id"]),
            {"name": cv["name"], "value": nuevo})
        if cod != 200:
            print("      ✗ %s %s" % (cod, r))


if __name__ == "__main__":
    args = sys.argv[1:]
    escribir = "--aplicar" in args
    args = [a for a in args if a != "--aplicar"]

    if args[:1] == ["ciclo"]:
        n = args[1] if len(args) > 1 else "1"
        if n not in CICLOS:
            raise SystemExit("Ciclos disponibles: %s" % ", ".join(CICLOS))
        print("Ciclo %s" % n)
        cargar(CICLOS[n], escribir)
    elif args[:1] == ["fijos"]:
        print("Datos de cobro manual")
        cargar(FIJOS, escribir)
    else:
        raise SystemExit(__doc__)

    if not escribir:
        print("\n— simulación. Añade --aplicar para escribirlo.")
