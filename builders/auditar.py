"""Recorre el embudo español de punta a punta y dice qué está conectado.

**Contra la subcuenta, no contra la documentación.** Es la lección del 5-sep:
`forms-a-crear.md` llevaba una semana afirmando que los formularios italianos no
hacían falta, cosa que había dejado de ser cierta el 28-ago. Un documento no se
entera de que alguien tocó algo en la UI; el API sí.

    python3 builders/auditar.py
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import esb_lib  # noqa: E402
import publico  # noqa: E402

OK, MAL, OJO = "✓", "✗", "⚠"


def _cv() -> dict[str, str]:
    cod, r = publico.pedir("GET", "/locations/%s/customValues" % os.environ["GHL_LOCATION_ID"])
    return {c.get("fieldKey", "").replace("{{ custom_values.", "").replace(" }}", "").strip():
            (c.get("value") or "") for c in (r.get("customValues", []) if cod == 200 else [])}


def _workflows(c) -> dict:
    salida = {}
    for w in esb_lib.listar_todo(c):
        n = w.get("name", "")
        if not n.startswith("WF"):
            continue
        full = c.request("GET", "/workflow/%s/%s" % (c.location_id, w["id"])) or {}
        tr = c.request("GET", "/workflow/%s/trigger?workflowId=%s" % (c.location_id, w["id"])) or []
        salida[n] = {
            "status": full.get("status"),
            "pasos": (full.get("workflowData") or {}).get("templates", []),
            "triggers": tr if isinstance(tr, list) else [],
        }
    return salida


# Cada parada del recorrido: (título, qué workflow lo mueve, qué custom values
# tienen que tener valor real para que funcione)
RECORRIDO = [
    ("1 · El anuncio lleva a la página de registro", None, ["link_registro_es", "logo_url"]),
    ("2 · Se registra y queda calificado",  "WF2 - Registro y calificacion",
     ["link_grupo_whatsapp_es"]),
    ("3 · Recibe la nutrición mientras espera", "WF6-ES - Nutricion pre-evento", []),
    ("4 · Le llegan los recordatorios",     "WF3-ES - Recordatorios de evento",
     ["fecha_evento_es", "fecha_evento_es_ghl", "hora_evento_pe", "link_evento_es"]),
    ("5 · Entra al evento y queda marcado", "WF4A - Asistencia",
     ["embed_youtube_es", "fecha_evento_es_iso"]),
    ("6 · Postula",                          "WF4B - Postulacion",
     ["link_postulacion_es", "link_agenda_es"]),
    ("7 · Agenda la llamada",                "WF4C - Cita agendada",
     ["link_calendario_cierre_pe"]),
    ("8 · Paga y se le da de alta",          "WF5 - Cobro confirmado", ["datos_pago_pe"]),
    ("· Si no califica",                     None,
     ["link_comienza_aqui_es", "link_educativo_es", "embed_video_educativo_es"]),
]


def main() -> None:
    c = esb_lib.cliente()
    cv, wfs = _cv(), _workflows(c)
    problemas = []

    print("\n" + "=" * 72)
    print("  CAMINO ESPAÑOL, DE PUNTA A PUNTA")
    print("=" * 72)

    for titulo, wf, valores in RECORRIDO:
        print("\n%s" % titulo)
        if wf:
            d = wfs.get(wf)
            if not d:
                print("   %s %s no existe" % (MAL, wf)); problemas.append(wf + " no existe")
            else:
                pub = d["status"] == "published"
                tiene_tr = bool(d["triggers"])
                print("   %s %-34s %s · %d pasos · %s"
                      % (OK if pub and tiene_tr else MAL, wf, d["status"], len(d["pasos"]),
                         "con trigger" if tiene_tr else "SIN TRIGGER"))
                if not pub:
                    problemas.append("%s sin publicar" % wf)
                if not tiene_tr:
                    problemas.append("%s sin trigger" % wf)
                # Un nodo ya convertido pierde la marca del nombre —GHL los llama
                # a todos «WhatsApp»—, así que lo que cuenta es el tipo: los que
                # siguen esperando plantilla son los que aún son `sms`.
                wa = [t for t in d["pasos"] if t.get("type") == "sms"]
                if wa:
                    print("     %s %d nodo(s) todavía como SMS, esperando plantilla" % (OJO, len(wa)))
        for k in valores:
            v = cv.get(k)
            if v is None:
                print("   %s %-34s no existe en la subcuenta" % (MAL, k))
                problemas.append("%s no existe" % k)
            elif not v or v == "PENDIENTE":
                print("   %s %-34s PENDIENTE" % (MAL, k))
                problemas.append("%s sin valor" % k)
            else:
                print("   %s %-34s %s" % (OK, k, v.replace("\n", " / ")[:44]))

    # Lo que no está en el recorrido pero rompe igual
    print("\n" + "-" * 72)
    print("  OTRAS COMPROBACIONES")
    print("-" * 72)

    sin_pub = [n for n, d in wfs.items() if d["status"] != "published"]
    print("   %s workflows sin publicar: %s"
          % (OK if not sin_pub else MAL, ", ".join(sin_pub) or "ninguno"))

    wa_total = sum(len([t for t in d["pasos"] if t.get("type") == "sms"])
                   for d in wfs.values())
    hechos = sum(len([t for t in d["pasos"] if t.get("type") == "whatsapp_v2"])
                 for d in wfs.values())
    print("   %s nodos esperando plantilla de WhatsApp: %d  (ya convertidos: %d)"
          % (OJO if wa_total else OK, wa_total, hechos))

    # Cada variable del cuerpo tiene que tener su clave de mapeo en attributes,
    # o GHL manda el parámetro vacío y Meta rechaza el envío entero.
    sueltas = []
    for n, d in wfs.items():
        for t in d["pasos"]:
            if t.get("type") != "whatsapp_v2":
                continue
            at = t.get("attributes", {})
            faltan = set(re.findall(r"\{\{[^}]+\}\}", at.get("message") or ""))
            faltan -= {k for k in at if k.startswith("{{")}
            if faltan or not at.get("template_id"):
                sueltas.append("%s / %s" % (n, at.get("__name__") or t.get("name")))
    print("   %s nodos de WhatsApp mal mapeados: %s"
          % (MAL if sueltas else OK, ", ".join(sueltas) or "ninguno"))
    problemas += ["%s mal mapeado" % x for x in sueltas]

    # Una rama de if_else sin pasos no da error en GHL —la deja pasar y el
    # contacto sale por ahí sin que ocurra nada—, así que no se ve mirando el
    # workflow: se ve leyendo los `next`. Fue el fallo de WF4C el 7-sep, con la
    # rama italiana a medias: quien no fuera Peru-LATAM se quedaba sin la etapa
    # y sin los tres mensajes.
    vacias = []
    for n, d in wfs.items():
        for t in d["pasos"]:
            if t.get("type") != "if_else" or t.get("nodeType") not in ("branch-yes", "branch-no"):
                continue
            if not t.get("next"):
                cond = next((x for x in d["pasos"] if x.get("id") == t.get("parentKey")), {})
                vacias.append("%s / %s → %s"
                              % (n, (cond.get("attributes") or {}).get("name") or "bifurcacion",
                                 "rama si" if t.get("nodeType") == "branch-yes" else "rama no"))
    print("   %s ramas de bifurcacion vacias: %s"
          % (MAL if vacias else OK, "; ".join(vacias) or "ninguna"))
    problemas += ["rama vacia en %s" % x.split(" /")[0] for x in vacias]

    cod, r = publico.pedir("GET", "/surveys/?locationId=%s&limit=50" % os.environ["GHL_LOCATION_ID"])
    encuestas = [s.get("name") for s in (r.get("surveys", []) if cod == 200 else [])]
    print("   %s encuestas: %s" % (OJO if len(encuestas) < 2 else OK, ", ".join(encuestas)))
    if len(encuestas) < 2:
        print("     (sin la italiana no puede existir WF2-IT: su trigger filtra por encuesta)")

    it = sorted(k for k, v in cv.items() if k.endswith("_it") and (not v or v == "PENDIENTE"))
    print("   %s valores italianos sin valor: %d" % (OJO, len(it)))
    for k in it:
        print("       %s" % k)

    print("\n" + "=" * 72)
    if problemas:
        print("  %d cosa(s) que romperían el camino español:" % len(problemas))
        for p in problemas:
            print("    · %s" % p)
    else:
        print("  El camino español está entero.")
    print("=" * 72 + "\n")


if __name__ == "__main__":
    main()
