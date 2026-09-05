"""Sustituye los custom values en una página y deja un HTML que se puede abrir.

**Por qué hace falta.** Las páginas se pegan en GHL con los merge fields dentro
(`{{custom_values.logo_url}}`), y quien los sustituye es GHL al servir la página.
Abrir el archivo del repo en un navegador no muestra la página: muestra el
esqueleto, con el logo roto y los textos vacíos — que es exactamente lo que
parece un fallo y no lo es.

Esto baja los valores reales de la subcuenta y los mete en una copia, para poder
mirar la página antes de pegarla. Sirve sobre todo para lo que no se puede
comprobar de otro modo: si las fotos están cruzadas, si un texto largo desborda,
si un valor quedó en PENDIENTE.

El archivo que genera es **solo para mirar**. En GHL se pega el del repo, con los
merge fields intactos.

    python3 builders/previsualizar.py paginas/registro-es.html
    python3 builders/previsualizar.py paginas/*.html
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import publico  # noqa: E402

SALIDA = os.environ.get(
    "CLAUDE_SCRATCHPAD",
    "/tmp/claude-0/-home-user-sanacion-peru/8b93f7c4-8cd1-51a3-b897-da67d66c1b82/scratchpad",
)

# GHL escribe la clave con espacios («{{ custom_values.x }}») pero en las páginas
# van sin ellos. Se aceptan las dos formas.
PATRON = re.compile(r"\{\{\s*custom_values\.([a-zA-Z0-9_]+)\s*\}\}")


def valores() -> dict[str, str]:
    cod, r = publico.pedir("GET", "/locations/%s/customValues" % os.environ["GHL_LOCATION_ID"])
    if cod != 200:
        raise SystemExit("No se pudieron leer los custom values: %s" % r)
    salida = {}
    for c in r.get("customValues", []):
        clave = c.get("fieldKey", "").replace("{{ custom_values.", "").replace(" }}", "").strip()
        salida[clave] = c.get("value") or ""
    return salida


def previsualizar(ruta: str, cv: dict[str, str]) -> None:
    html = open(ruta).read()
    usados, faltan, vacios = set(), set(), set()

    def cambiar(m):
        clave = m.group(1)
        if clave not in cv:
            faltan.add(clave)
            return m.group(0)
        usados.add(clave)
        if not cv[clave] or cv[clave] == "PENDIENTE":
            vacios.add(clave)
        return cv[clave]

    html = PATRON.sub(cambiar, html)

    nombre = ruta.rsplit("/", 1)[-1].replace(".html", "-preview.html")
    destino = "%s/%s" % (SALIDA, nombre)
    os.makedirs(SALIDA, exist_ok=True)
    open(destino, "w").write(html)

    print("\n%s → %s" % (ruta, destino))
    print("   %d valores sustituidos" % len(usados))
    if vacios:
        print("   ⚠ vacíos o en PENDIENTE: %s" % ", ".join(sorted(vacios)))
    if faltan:
        print("   ✗ no existen en la subcuenta: %s" % ", ".join(sorted(faltan)))


if __name__ == "__main__":
    rutas = sys.argv[1:]
    if not rutas:
        raise SystemExit(__doc__)
    cv = valores()
    for r in rutas:
        previsualizar(r, cv)
