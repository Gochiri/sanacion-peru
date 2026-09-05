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
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from esb_lib import cliente  # noqa: E402

# (workflow, texto viejo, texto nuevo, por qué)
RETOQUES: list[tuple[str, str, str, str]] = [
    ("WF3-ES - Recordatorios de evento",
     "{{custom_values.link_evento_es}}",
     "{{trigger_link.zsM5LP4jGLvvLbNG8hXy}}",
     "el enlace del evento va como trigger link, o WF4A no sabe quien entro"),

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


# (workflow, nombre del nodo, fields nuevos, por qué)
#
# El builder escribía `field` como fieldKey y `type` como el dataType del API en
# mayúsculas. La UI no resuelve eso: el desplegable sale vacío y el nodo da error.
# El formato bueno se sacó del nodo que Oliver recreó a mano en WF4A:
#     {"field": "<id>", "value": ["Si"], "title": "...", "type": "multiselect", "date": ""}
# o sea: **id** del campo, valor en array donde el campo admite varios, y el tipo
# de la UI en minúsculas.
RETOQUES_CAMPOS: list[tuple[str, str, list[dict], str]] = [
    ("WF5 - Cobro confirmado", "Activar bono si pago de contado",
     [{"field": "7YhSYFuz89u6Vf05Fk4u", "value": ["Si"],
       "title": "Bono llamada christie", "type": "multiselect", "date": ""}],
     "CHECKBOX -> multiselect (verificado contra WF4A)"),

    ("WF5 - Cobro confirmado", "Registrar datos de la venta",
     [{"field": "nHjHVOUlxUefgbhI9v5J", "value": ["Escuela"],
       "title": "Producto comprado", "type": "multiselect", "date": ""},
      {"field": "zSvMgseoMi5Zub9tQr3i", "value": "Al dia",
       "title": "Estado pago", "type": "singleselect", "date": ""}],
     "INFERIDO para MULTIPLE_OPTIONS y SINGLE_OPTIONS — verificar en la UI"),
]


LUCA     = "nEVI8WGKSdfvkR9FUyXM"
CHRISTIE = "BrFbQVQSRj6Q7UDUlNiK"
JOAQUIN  = "aKPs36EHpB9gaLMdNpHp"

# Formato REAL de internal_notification, leído del nodo que Oliver configuró a
# mano ("Avisar a Luca: cuota recibida"). Nada de esto era adivinable:
#   · todo cuelga de `email`, no de la raíz de attributes
#   · `from_name` / `from_email` en snake_case
#   · `selectedUser` (array de ids), no `users`
#   · `userType` vale "user", no "particularUser"
#   · el cuerpo es `html`, no `body`, y GHL lo guarda con estilos en línea
_P1 = ('margin:0px;font-family:verdana,geneva,sans-serif;font-size:16px; '
       'padding-left: 0px!important;margin: 0px;font-family: '
       'verdana,geneva,sans-serif;font-size: 16px;')
_PN = ('margin:0px;font-family:verdana,geneva,sans-serif;font-size:16px; '
       'padding-left: 0px!important;')


def cuerpo_html(parrafos: list[str]) -> str:
    """Mismo marcado que produce el editor de GHL, para que se vea igual."""
    return "".join(f'<p style="{_P1 if i == 0 else _PN}">{t}</p>'
                   for i, t in enumerate(parrafos))


def aviso(remitente_nombre, remitente_email, usuarios, asunto, parrafos) -> dict:
    return {"type": "email", "email": {
        "html": cuerpo_html(parrafos),
        "from_name": remitente_nombre,
        "from_email": remitente_email,
        "selectedUser": usuarios,
        "userType": "user",
        "subject": asunto,
        "attachments": [],
    }}


DE_NOMBRE = "La nueva conciencia"
DE_EMAIL  = "mail@lanuovacoscienza.com"

# «Avisar a Luca: cuota recibida» NO está aquí: lo configuró Oliver y es la
# fuente de la verdad. Solo se replican los otros dos.
RETOQUES_AVISOS: list[tuple[str, str, dict, str]] = [
    ("WF5 - Cobro confirmado", "Avisar a Luca: dar de alta en System.io",
     aviso(DE_NOMBRE, DE_EMAIL, [LUCA],
           "Alta pendiente · {{contact.name}} ya pagó la escuela",
           ["{{contact.name}} completó el pago de la escuela.",
            "Contacto: {{contact.email}} · {{contact.phone}}",
            "Producto: {{contact.producto_comprado}}",
            "Hay que crearle el acceso en System.io. Mientras no se haga, el "
            "alumno pagó y no puede entrar."]),
     "primer pago: pide alta manual"),

    ("WF5 - Cobro confirmado", "Avisar a Christie: sesion bono de 40 min",
     aviso(DE_NOMBRE, DE_EMAIL, [CHRISTIE],
           "Bono por entregar · sesión de 40 min con {{contact.name}}",
           ["{{contact.name}} pagó la escuela al contado, así que le corresponde "
            "la sesión de bienvenida de 40 minutos.",
            "Contacto: {{contact.email}} · {{contact.phone}}",
            "Conviene escribirle en los próximos días, mientras la decisión está "
            "fresca."]),
     "pago de contado: agendar el bono"),
]


# (workflow, nombre del nodo nuevo, después de qué nodo, attributes, por qué)
#
# Insertar es distinto de retocar: hay que coserlo a la cadena. Los nodos de
# WF4C se encadenan con `parentKey` / `next` / `order`, en línea recta, así que
# meter uno en medio es reapuntar el `next` del anterior y heredar el suyo.
#
# Solo vale para workflows en cadena simple. En uno con ramas (`if_else` en el
# formato rico del canvas) esto no sirve: ahí las transiciones viven dentro de
# las ramas y hay que hacerlo en la UI.
#
# ⚠ `{{appointment.start_time}}` va SIN verificar. `{{appointment.address}}` sí
# está probado (lo usa el recordatorio de 1 h). Si en el primer aviso real sale
# el texto literal en vez de la hora, es eso: se cambia y ya. Va igualmente
# porque un aviso de cita que no dice cuándo es no sirve de mucho.
INSERCIONES: list[tuple[str, str, str, dict, str]] = [
    ("WF4C - Cita agendada", "Avisar al equipo: cita agendada",
     "Mover a Llamada agendada",
     aviso(DE_NOMBRE, DE_EMAIL, [JOAQUIN, LUCA],
           "Cita agendada · {{contact.name}}",
           ["{{contact.name}} acaba de reservar una llamada de cierre.",
            "Cuándo: {{appointment.start_time}}",
            "Contacto: {{contact.email}} · {{contact.phone}}",
            "Su postulación está en la ficha del contacto. Conviene leerla antes "
            "de entrar: ahí cuenta qué le pasa y qué ha intentado."]),
     "Joaquin pidio enterarse al momento (llamada 4-sep); WF4C no avisaba a nadie"),

    ("WF4C - Cita agendada", "Avisar al equipo: la cita es en 1 hora",
     "Esperar hasta 1 h antes",
     aviso(DE_NOMBRE, DE_EMAIL, [JOAQUIN, LUCA],
           "En 1 hora · llamada con {{contact.name}}",
           ["En una hora es la llamada de cierre con {{contact.name}}.",
            "Contacto: {{contact.email}} · {{contact.phone}}",
            "Enlace: {{appointment.address}}"]),
     "Joaquin: «si me llega una hora antes yo lo agendo y lo tengo listo»"),
]


# (workflow, nombre del nodo, minutos antes de la cita, por qué)
#
# Formato leído del nodo que Oliver configuró a mano en «ZZ sonda - espera por
# fecha» (5-sep). No era adivinable y difiere del de una espera normal:
#   · `type` pasa de "time" a "appointment"
#   · `startAfter` **desaparece** y lo sustituye `appointmentStartAfter`
#   · `value` va en minutos totales y `distributed` es el desglose que muestra
#     la UI; los dos tienen que decir lo mismo
#   · `appointmentCondition: "skip"` — si no hay cita, se salta el nodo
#
# Esto arregla el mismo fallo que tiene WF3: las dos esperas de WF4C eran
# relativas a la entrada («1 día después», «23 horas después»), no a la cita.
# Quien reservara con una semana de antelación recibía «mañana es tu llamada» al
# día siguiente de reservar, el enlace de Zoom al otro, y el día de la llamada
# nada.
def _minutos(dias: int = 0, horas: int = 0) -> dict:
    return {"when": "before", "type": "minutes",
            "value": dias * 1440 + horas * 60,
            "distributed": {"months": 0, "days": dias, "hours": horas, "minutes": 0}}


RETOQUES_ESPERAS: list[tuple[str, str, dict, str]] = [
    ("WF4C - Cita agendada", "Esperar hasta 24 h antes de la cita",
     _minutos(dias=1), "era «1 dia despues de entrar», no 24 h antes de la cita"),

    ("WF4C - Cita agendada", "Esperar hasta 1 h antes",
     _minutos(horas=1), "era «23 horas despues», que solo cuadraba si la cita era manana"),
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
    # Cada fase reescribe nodos enteros. Si una ya se aplicó y alguien la afinó
    # después en la UI, volver a pasarla le encima lo escrito. Por eso se puede
    # correr una sola: `--solo inserciones`.
    ap.add_argument("--solo", choices=["retoques", "campos", "avisos", "inserciones", "esperas"],
                    help="ejecutar solo una fase (por defecto, todas)")
    args = ap.parse_args()
    fase = lambda n: args.solo in (None, n)  # noqa: E731

    c = cliente(); loc = c.location_id
    lst = c.request("GET", f"/workflow/{loc}") or []
    if isinstance(lst, dict):
        lst = lst.get("workflows") or lst.get("data") or []
    ids = {w.get("name"): (w.get("id") or w.get("_id")) for w in lst
           if isinstance(w, dict) and w.get("type") != "directory"}

    for nombre, viejo, nuevo, motivo in (RETOQUES if fase("retoques") else []):
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

        # `status` se reenvía a propósito: un PUT sin él lo deja en null y el
        # workflow queda DESPUBLICADO en silencio. Pasó con WF2, WF3-ES y WF4B.
        cuerpo = {
            "name": nombre,
            "version": actual.get("version", 1),
            "workflowData": {**wd, "templates": templates},
        }
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nombre:34} {n} sustitucion(es)  ({motivo})"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")

    if fase("campos"):
        aplicar_campos(c, loc, ids, args.dry_run)
    if fase("avisos"):
        aplicar_avisos(c, loc, ids, args.dry_run)
    if fase("inserciones"):
        aplicar_inserciones(c, loc, ids, args.dry_run)
    if fase("esperas"):
        aplicar_esperas(c, loc, ids, args.dry_run)


def aplicar_avisos(c, loc, ids, dry_run: bool) -> None:
    """Reescribe por completo los `attributes` de una notificación interna."""
    for nombre, nodo, attrs, motivo in RETOQUES_AVISOS:
        wid = ids.get(nombre)
        if not wid:
            print(f"  ✗ {nombre:34} no existe"); continue

        actual = c.request("GET", f"/workflow/{loc}/{wid}") or {}
        wd = actual.get("workflowData") or {}
        templates = [dict(t) for t in (wd.get("templates") or [])]

        tocados = 0
        for t in templates:
            if t.get("name") != nodo:
                continue
            t["attributes"] = attrs
            tocados += 1

        if not tocados:
            print(f"  = {nodo:38} no encontrado"); continue
        if dry_run:
            print(f"  · {nodo:38} ({motivo})  DRY-RUN"); continue

        cuerpo = {"name": nombre, "version": actual.get("version", 1),
                  "workflowData": {**wd, "templates": templates}}
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nodo:38} ({motivo})"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")


def aplicar_esperas(c, loc, ids, dry_run: bool) -> None:
    """Ancla una espera a la cita del contacto en vez de a su hora de entrada."""
    for nombre, nodo, cuando, motivo in RETOQUES_ESPERAS:
        wid = ids.get(nombre)
        if not wid:
            print(f"  ✗ {nombre:34} no existe"); continue

        actual = c.request("GET", f"/workflow/{loc}/{wid}") or {}
        wd = actual.get("workflowData") or {}
        templates = [dict(t) for t in (wd.get("templates") or [])]

        tocados = 0
        for t in templates:
            if t.get("name") != nodo:
                continue
            attrs = {**(t.get("attributes") or {})}
            attrs.pop("startAfter", None)      # o GHL se queda con la espera vieja
            attrs["type"] = "appointment"
            attrs["appointmentStartAfter"] = cuando
            attrs.setdefault("appointmentCondition", "skip")
            t["attributes"] = attrs
            tocados += 1

        if not tocados:
            print(f"  = {nodo:38} no encontrado"); continue
        h = cuando["value"] // 60
        if dry_run:
            print(f"  · {nodo:38} {h} h antes de la cita  ({motivo})  DRY-RUN"); continue

        cuerpo = {"name": nombre, "version": actual.get("version", 1),
                  "workflowData": {**wd, "templates": templates}}
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nodo:38} {h} h antes de la cita"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")


def aplicar_inserciones(c, loc, ids, dry_run: bool) -> None:
    """Cose un nodo nuevo justo detrás de otro, en un workflow de cadena simple.

    Es idempotente por el nombre del nodo: si ya está, no lo duplica. Importa,
    porque este script se corre varias veces mientras se afina un texto.
    """
    for nombre, nodo, detras_de, attrs, motivo in INSERCIONES:
        wid = ids.get(nombre)
        if not wid:
            print(f"  ✗ {nombre:34} no existe"); continue

        actual = c.request("GET", f"/workflow/{loc}/{wid}") or {}
        wd = actual.get("workflowData") or {}
        templates = [dict(t) for t in (wd.get("templates") or [])]

        if any(t.get("name") == nodo for t in templates):
            print(f"  = {nodo:38} ya estaba"); continue

        pos = next((i for i, t in enumerate(templates)
                    if t.get("name") == detras_de), None)
        if pos is None:
            print(f"  ✗ {nodo:38} no encuentro «{detras_de}»"); continue

        anterior = templates[pos]
        nuevo = {
            "id": str(uuid.uuid4()),
            "type": "internal_notification",
            "name": nodo,
            "parentKey": anterior["id"],
            "order": 0,          # se renumera abajo
            "attributes": attrs,
        }
        # Hereda el `next` del anterior; si era el último, el nuevo lo es.
        if anterior.get("next"):
            nuevo["next"] = anterior["next"]
            siguiente = next((t for t in templates
                              if t.get("id") == anterior["next"]), None)
            if siguiente is not None:
                siguiente["parentKey"] = nuevo["id"]
        anterior["next"] = nuevo["id"]

        templates.insert(pos + 1, nuevo)
        for i, t in enumerate(templates):
            t["order"] = i

        if dry_run:
            print(f"  · {nodo:38} tras «{detras_de}»  ({motivo})  DRY-RUN"); continue

        cuerpo = {"name": nombre, "version": actual.get("version", 1),
                  "workflowData": {**wd, "templates": templates}}
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nodo:38} tras «{detras_de}»"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")


def aplicar_campos(c, loc, ids, dry_run: bool) -> None:
    """Reescribe por completo los `fields` de un nodo, localizado por su nombre."""
    for nombre, nodo, campos, motivo in RETOQUES_CAMPOS:
        wid = ids.get(nombre)
        if not wid:
            print(f"  ✗ {nombre:34} no existe"); continue

        actual = c.request("GET", f"/workflow/{loc}/{wid}") or {}
        wd = actual.get("workflowData") or {}
        templates = [dict(t) for t in (wd.get("templates") or [])]

        tocados = 0
        for t in templates:
            if t.get("name") != nodo:
                continue
            t["attributes"] = {**(t.get("attributes") or {}), "fields": campos}
            tocados += 1

        if not tocados:
            print(f"  = {nodo:34} no encontrado en {nombre}"); continue
        if dry_run:
            print(f"  · {nodo:34} {len(campos)} campo(s)  ({motivo})  DRY-RUN"); continue

        cuerpo = {"name": nombre, "version": actual.get("version", 1),
                  "workflowData": {**wd, "templates": templates}}
        if actual.get("status"):
            cuerpo["status"] = actual["status"]
        r = c.request("PUT", f"/workflow/{loc}/{wid}", cuerpo)
        ok = bool(r and not r.get("_error"))
        print(f"  {'✓' if ok else '✗'} {nodo:34} {len(campos)} campo(s)  ({motivo})"
              f"{'' if ok else '  ' + str(r.get('message'))[:110]}")


if __name__ == "__main__":
    main()
