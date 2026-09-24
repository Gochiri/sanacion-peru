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

## El modo --ghl

    python3 builders/previsualizar.py --ghl paginas/*.html

Lo mismo, pero escribiendo en `paginas/generado/` y **eso es lo que se pega en
GHL**, no el archivo de `paginas/`.

Existe porque el 5-sep se comprobó que **GHL no sustituye los merge fields** en
las páginas publicadas: al `src` del logo le llegaba `{{custom_values.logo_url}}`
como texto. Se verificó que el archivo existe en Media Storage y que su URL abre
sola, así que el problema no era la imagen. Con seis páginas dependiendo de esto
—el calendario de `agenda-es` incluido, que es la única función de esa página—
resultaba más barato quitar la dependencia que averiguar por qué GHL decide
sustituir o no, a cuatro días de encender los anuncios.

Los archivos de `paginas/` siguen llevando los merge fields: son la versión
legible y la fuente única. **Lo generado no se edita nunca.**

⚠️ Tres páginas llevan la fecha del evento dentro —`registro-es`, `gracias-es` y
`evento-es`—, así que **al cambiar de ciclo hay que regenerarlas y volver a
pegarlas**. Va en la misma sentada que `valores.py ciclo 2 --aplicar`.
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


def sin_comentarios(html: str) -> str:
    """Quita los comentarios y las líneas en blanco, sin tocar nada más.

    Existe porque el 24-sep una página dejó de renderizarse al pegarla en GHL:
    salía en blanco, sin ni siquiera el fondo negro que pone nuestro CSS, o sea
    que el bloque entero no llegaba. Lo único que había cambiado era el tamaño
    —de 15.794 a 17.293 caracteres— y buena parte de eso son comentarios, que
    son para quien lea el repo y al navegador no le dicen nada.

    No es minificado: no toca nombres, ni espacios dentro de una línea, ni junta
    reglas. Solo borra lo que no se ejecuta, para que lo pegado sea lo más
    parecido posible a lo que hay en `paginas/` cuando haya que depurarlo.
    """
    m = re.search(r"(<script[^>]*>)(.*?)(</script>)", html, re.S)
    if m is None:
        cab, js, cola, ini, fin = "", "", "", html, ""
    else:
        cab, js, cola = m.group(1), m.group(2), m.group(3)
        ini, fin = html[:m.start()], html[m.end():]

    def podar(s: str) -> str:
        s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)     # comentarios CSS
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)      # comentarios HTML
        return "\n".join(l for l in s.split("\n") if l.strip())

    # Dentro del script solo se quitan las líneas que son enteras un comentario:
    # un `//` a media línea puede ser el de `https://`.
    js = "\n".join(l for l in js.split("\n")
                   if l.strip() and l.strip()[:2] != "//")
    return podar(ini) + cab + js + cola + podar(fin)


def previsualizar(ruta: str, cv: dict[str, str], para_ghl: bool = False,
                  compacto: bool = False) -> None:
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
    if compacto:
        html = sin_comentarios(html)

    if para_ghl:
        carpeta = "paginas/generado"
        nombre = ruta.rsplit("/", 1)[-1]
    else:
        carpeta = SALIDA
        nombre = ruta.rsplit("/", 1)[-1].replace(".html", "-preview.html")
    destino = "%s/%s" % (carpeta, nombre)
    os.makedirs(carpeta, exist_ok=True)
    open(destino, "w").write(html)

    print("\n%s → %s" % (ruta, destino))
    print("   %d valores sustituidos · %d caracteres" % (len(usados), len(html)))
    if vacios:
        print("   ⚠ vacíos o en PENDIENTE: %s" % ", ".join(sorted(vacios)))
    if faltan:
        print("   ✗ no existen en la subcuenta: %s" % ", ".join(sorted(faltan)))

    if para_ghl:
        # La comprobación que define el arreglo: si queda un merge field vivo en
        # lo generado, esa página se sigue rompiendo al publicarla.
        quedan = set(PATRON.findall(html))
        if quedan:
            print("   ✗ SIGUEN SIN SUSTITUIR: %s" % ", ".join(sorted(quedan)))
        else:
            print("   ✓ sin merge fields, listo para pegar")


if __name__ == "__main__":
    args = sys.argv[1:]
    para_ghl = "--ghl" in args
    compacto = "--compacto" in args
    rutas = [a for a in args if a not in ("--ghl", "--compacto")]
    if not rutas:
        raise SystemExit(__doc__)
    cv = valores()
    for r in rutas:
        previsualizar(r, cv, para_ghl, compacto)
    if para_ghl:
        print("\nEsto es lo que se pega en GHL. Los de paginas/ no.")
