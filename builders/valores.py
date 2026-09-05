"""Carga en los custom values lo que el cliente confirmó el 4-sep.

Hay dos clases de valor y por eso hay dos comandos:

  · **ciclo**  — lo que cambia en cada webinar (fecha, hora, nombre del
                 lanzamiento). Son dos ciclos y hay que rotarlos: el ciclo 2 se
                 carga el 25-sep, en cuanto termina el primer webinar.
  · **fijos**  — lo que no cambia entre ciclos (datos de cobro manual).
  · **personas** — fotos y biografías de la página de registro.

    python3 builders/valores.py ciclo 1
    python3 builders/valores.py ciclo 2 --aplicar
    python3 builders/valores.py fijos --aplicar
    python3 builders/valores.py personas --aplicar

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

# Estos valores son para **copiar y pegar**, no para meterlos en un mensaje
# automático: WhatsApp rechaza los parámetros de plantilla que traen saltos de
# línea, y estos son bloques de varias líneas. Las plantillas `datos_pago_es` y
# `datos_pago_it` llevan los datos escritos en el cuerpo por esa razón.
#
# En la llamada del 4-sep Joaquín confirmó la razón social: «Nueva Consciencia
# Formación», **sin «SAC»** («sin saco», dijo). El SAC ya está quitado.
#
# Lo que la llamada NO resuelve es la S de «Con*s*ciencia»: el transcript
# normaliza la ortografía, así que las dos grafías salen iguales en el texto.
# Va la del mensaje escrito del cliente, que es la única evidencia que se puede
# leer. **No bloquea el cobro** —una transferencia por CCI encamina por el
# número de cuenta— pero ese nombre queda escrito dentro de una plantilla de
# Meta que después no se edita, así que hay que mirar el mensaje original.
FIJOS = {
    "datos_pago_pe": (
        "Transferencia bancaria (Perú)\n"
        "Titular: Nueva Consciencia Formación\n"
        "Banco: BCP · cuenta en soles\n"
        "Cuenta: 1937405302029\n"
        "CCI: 00219300740530202918"
    ),
    # El intestatario lo confirmó Joaquín el 4-sep: la cuenta italiana es de
    # Luca a título personal, porque en Italia no hay empresa. Y ya estaba
    # escrito desde el onboarding — 02-form-onboarding.md:40 dice «titular Luca
    # Stefanizzi». Importa que esté: desde octubre de 2025 los bancos de la UE
    # verifican que el nombre del beneficiario coincida con el IBAN.
    "datos_pago_it": (
        "Bonifico bancario (Italia)\n"
        "Intestatario: Luca Stefanizzi\n"
        "Banca: Intesa Sanpaolo\n"
        "IBAN: IT98L0306979654100000006623"
    ),
}


# Fotos y biografías de la sección «quiénes la dan» de registro-es. Eran
# literales pegados en el HTML hasta el 5-sep; ahora son custom values para que
# cambiar una foto no obligue a volver a pegar la página entera en GHL.
#
# ⚠ Las dos fotos llegaron a Media Storage como «3.png» y «4.png», sin nada que
# diga cuál es cuál, y el CDN de GHL no se puede abrir desde aquí para mirarlas.
# El reparto va por el orden en que el cliente mandó las biografías: Christie
# primero, Luca después. **Hay que abrir la página y comprobarlo** — si están
# cruzadas se arregla intercambiando estos dos valores, sin tocar el HTML.
_MEDIA = "https://assets.cdn.filesafe.space/oszNQJYK0E15KB4S06nM/media/"

PERSONAS = {
    "foto_christie_url": _MEDIA + "6a9b51cf3dd2068ce69941a0.png",   # 3.png
    "foto_luca_url":     _MEDIA + "6a9b51cfe29b3baf97c14427.png",   # 4.png
    # Recortadas de las que mandó el cliente. En la tarjeta caben dos o tres
    # líneas al lado del retrato; más largo desequilibra la sección y nadie lo
    # lee. Se queda qué hacen y con qué trabajan, y se va la cola de promesa
    # («bienestar, abundancia y plenitud», «la vida que realmente desean»), que
    # en nicho salud además conviene no repetir.
    "bio_christie": (
        "Creadora de la Escuela Nueva Consciencia Academy y experta en "
        "transformación personal y sanación cuántica. Acompaña a liberar "
        "bloqueos emocionales y a reconectar con el propio potencial."
    ),
    "bio_luca": (
        "Autor y mental coach, creador de la Academia Nueva Consciencia. "
        "Trabaja con la mente y las emociones para ayudar a superar bloqueos, "
        "miedos y limitaciones."
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
            # Crear en vez de rendirse: los valores de la landing nacieron aquí,
            # no existían en la subcuenta.
            print("  %s %-28s (nuevo) → %s"
                  % ("+" if escribir else "·", clave,
                     nuevo.replace("\n", " / ")[:46]))
            if escribir:
                cod, r = publico.pedir(
                    "POST", "/locations/%s/customValues" % os.environ["GHL_LOCATION_ID"],
                    {"name": clave.replace("_", " ").capitalize(), "value": nuevo})
                if cod not in (200, 201):
                    print("      ✗ %s %s" % (cod, r))
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
    elif args[:1] == ["personas"]:
        print("Fotos y biografías de la landing")
        cargar(PERSONAS, escribir)
    else:
        raise SystemExit(__doc__)

    if not escribir:
        print("\n— simulación. Añade --aplicar para escribirlo.")
