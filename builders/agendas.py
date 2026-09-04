"""Carga la disponibilidad real de cierre en los dos calendarios.

Cómo funciona un calendario de GHL, comprobado contra `/free-slots` el 4-sep:

  · `openHours`      → patrón **semanal** recurrente. Es lo que abre los días.
  · `availabilities` → excepciones **por fecha**. Con `hours: []` esa fecha
                       queda cerrada aunque el patrón semanal la abra.
  · `deleted: true`  → NO borra la entrada: le vacía las horas, o sea la cierra.
  · Callejón sin salida probado: con `openHours: []` y solo `availabilities`,
    los **sábados no aparecen** por más que estén en las fechas. El patrón
    semanal no es opcional.
  · El calendario **no tiene timezone propio**: mandar `timezone` da 422. Usa el
    de la subcuenta (America/Bogota, UTC-5). Por eso el horario de Luca va
    convertido a hora de Perú y no en hora italiana.

La venta ocurre en una ventana cerrada (25-sep a 10-oct). El patrón semanal por
sí solo dejaría reservable cualquier lunes de noviembre, cuando ya no hay nadie
vendiendo. Por eso, además del patrón, se cierran una por una **todas las fechas
del horizonte reservable que no estén en la ventana**.

    python3 builders/agendas.py            # muestra lo que haría
    python3 builders/agendas.py --aplicar
"""
from __future__ import annotations

import datetime
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import publico  # noqa: E402

# ── Lo que dio el cliente ────────────────────────────────────────────────────
# Joaquín cierra el mercado español. Horas de Perú, que es la hora de la
# subcuenta. Los jueves 24-sep y 1-oct no están: son los días de webinar.
JOAQUIN = {
    "2026-09-25": (9, 17), "2026-09-26": (9, 12),
    "2026-09-28": (9, 17), "2026-09-29": (9, 17), "2026-09-30": (9, 17),
    "2026-10-02": (9, 17), "2026-10-03": (9, 12),
    "2026-10-05": (9, 17), "2026-10-06": (9, 17), "2026-10-07": (9, 17),
    "2026-10-08": (9, 17), "2026-10-09": (9, 17), "2026-10-10": (9, 12),
}

# Luca cierra Italia de 15:00 a 19:00 hora italiana. En septiembre y octubre
# Italia está en CEST (UTC+2) y Perú en UTC-5: siete horas menos. Las 15-19
# italianas son las 08-12 peruanas, y así hay que cargarlas. (Italia sale de
# CEST el 25-oct, después de la ventana, así que el desfase no cambia.)
DESFASE_IT = -7
LUCA = {f: (15 + DESFASE_IT, 19 + DESFASE_IT) for f in [
    "2026-09-28", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02",
    "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09",
    "2026-10-10",
]}

# Hasta dónde se cierran fechas sobrantes. Con `allowBookingFor` en 45 días, el
# día más tardío alcanzable desde el final de la ventana (10-oct) es el 24-nov.
HORIZONTE = "2026-11-30"
DIAS_RESERVA = 45

VENTANAS = [
    {"id": "befuzgaXYSmsD2qUZdkl", "quien": "Joaquin (ES)", "dias": JOAQUIN,
     "descripcion": "Llamada de una hora con Joaquin para cerrar la inscripcion a la escuela."},
    {"id": "MNg4SJeHdqjOfoGjJpKQ", "quien": "Luca (IT)", "dias": LUCA,
     "descripcion": "Chiamata di un'ora con Luca per chiudere l'iscrizione alla scuola."},
]

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def _patron(dias: dict[str, tuple[int, int]]) -> list:
    """Patrón semanal deducido de las fechas: por cada día de la semana, la
    franja más amplia que aparezca. Las fechas concretas lo recortan después."""
    porsemana: dict[int, tuple[int, int]] = {}
    for f, (a, c) in dias.items():
        d = datetime.date.fromisoformat(f).weekday()  # 0=lunes
        ya = porsemana.get(d)
        porsemana[d] = (min(a, ya[0]), max(c, ya[1])) if ya else (a, c)
    # GHL numera 0=domingo ... 6=sábado; datetime numera 0=lunes ... 6=domingo.
    return [{"daysOfTheWeek": [(d + 1) % 7],
             "hours": [{"openHour": a, "openMinute": 0,
                        "closeHour": c, "closeMinute": 0}]}
            for d, (a, c) in sorted(porsemana.items())]


def _fechas(dias: dict[str, tuple[int, int]]) -> list:
    """Las fechas de la ventana con sus horas, y cerradas todas las demás."""
    salida = [{"date": f + "T00:00:00.000Z",
               "hours": [{"openHour": a, "openMinute": 0,
                          "closeHour": c, "closeMinute": 0}]}
              for f, (a, c) in sorted(dias.items())]

    abiertos = {(datetime.date.fromisoformat(f).weekday() + 1) % 7 for f in dias}
    d = datetime.date.today()
    fin = datetime.date.fromisoformat(HORIZONTE)
    while d <= fin:
        f = d.isoformat()
        # Solo hace falta cerrar los días que el patrón semanal abriría.
        if f not in dias and (d.weekday() + 1) % 7 in abiertos:
            salida.append({"date": f + "T00:00:00.000Z", "hours": []})
        d += datetime.timedelta(days=1)
    return salida


def aplicar(cal: dict, escribir: bool) -> None:
    fechas = _fechas(cal["dias"])
    cuerpo = {
        "description": cal["descripcion"],
        # Una hora por cliente, como pidió el cliente. Estaban los dos a 30 min.
        "slotDuration": 60, "slotDurationUnit": "mins",
        "slotInterval": 60, "slotIntervalUnit": "mins",
        # Sin colchón: con 15 min de buffer los turnos salen a las 9:00, 10:15,
        # 11:30... y la rejilla deja de ser horaria.
        "slotBuffer": 0,
        "appoinmentPerSlot": 1,
        "appoinmentPerDay": max((c - a) for a, c in cal["dias"].values()),
        "allowBookingFor": DIAS_RESERVA, "allowBookingForUnit": "days",
        "openHours": _patron(cal["dias"]),
        "availabilities": fechas,
    }

    print("\n%s · %s" % (cal["quien"], cal["id"]))
    for f, (a, c) in sorted(cal["dias"].items()):
        d = DIAS[datetime.date.fromisoformat(f).weekday()]
        print("   %s %-9s %02d:00-%02d:00  → %d turnos" % (f, d, a, c, c - a))
    print("   patrón semanal: %s" % ", ".join(
        "%s %02d-%02d" % (["dom", "lun", "mar", "mié", "jue", "vie", "sáb"][h["daysOfTheWeek"][0]],
                          h["hours"][0]["openHour"], h["hours"][0]["closeHour"])
        for h in cuerpo["openHours"]))
    print("   fechas cerradas fuera de ventana: %d (hasta %s)"
          % (sum(1 for f in fechas if not f["hours"]), HORIZONTE))
    if not escribir:
        print("   — simulación, no se escribió nada")
        return

    cod, r = publico.pedir("PUT", "/calendars/" + cal["id"], cuerpo)
    print("   PUT %s" % cod, "" if cod == 200 else r)


def comprobar() -> None:
    """Contrasta contra /free-slots, que es la única fuente de verdad.

    El endpoint rechaza rangos de más de 31 días, así que se pregunta por tramos.
    """
    def ms(f):
        return int(datetime.datetime.fromisoformat(f + "T00:00:00+00:00").timestamp() * 1000)

    print("\n── Turnos reales que ve una persona ──")
    for cal in VENTANAS:
        hay = {}
        d, fin = datetime.date.today(), datetime.date.fromisoformat(HORIZONTE)
        while d < fin:
            hasta = min(d + datetime.timedelta(days=30), fin)
            cod, r = publico.pedir(
                "GET", "/calendars/%s/free-slots?startDate=%d&endDate=%d&timezone=America/Lima"
                % (cal["id"], ms(d.isoformat()), ms(hasta.isoformat())))
            if cod != 200:
                print("   ✗ %s: %s" % (d, r))
            hay.update({k: v["slots"] for k, v in r.items()
                        if k[:2] == "20" and v.get("slots")})
            d = hasta

        print("\n%s — %d fechas reservables" % (cal["quien"], len(hay)))
        for k in sorted(hay):
            marca = "" if k in cal["dias"] else "  ⚠ FUERA DE VENTANA"
            print("   %s  %2d turnos  %s→%s%s"
                  % (k, len(hay[k]), hay[k][0][11:16], hay[k][-1][11:16], marca))
        faltan = [f for f in cal["dias"] if f not in hay]
        if faltan:
            print("   ⚠ sin turnos: %s" % ", ".join(sorted(faltan)))


if __name__ == "__main__":
    escribir = "--aplicar" in sys.argv
    for cal in VENTANAS:
        aplicar(cal, escribir)
    if escribir:
        comprobar()
    else:
        print("\nPara escribirlo: python3 builders/agendas.py --aplicar")
