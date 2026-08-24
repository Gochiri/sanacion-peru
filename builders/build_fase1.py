#!/usr/bin/env python3
"""Construye WF1–WF5 de la Fase 1 en la subcuenta de la Escuela de Sanación Biológica.

    source tools/ghl-cli/.venv/bin/activate
    set -a && source tools/ghl-cli/.env && set +a
    python builders/build_fase1.py --dry-run     # ver los pasos sin tocar GHL
    python builders/build_fase1.py               # crear los workflows (draft)

Los workflows se crean SIEMPRE en borrador. Los triggers se configuran en la UI
(ver docs/tareas-fase1-clickup.md); este builder crea la cadena de acciones.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from esb_lib import (  # noqa: E402
    CARPETA, bifurcar, campo, capi, carpeta, cargar_estado, cliente, cond,
    desplegar, email, esperar, etiqueta, mover_a_etapa, notificar, resumen, whatsapp,
)

E = cargar_estado()
PIPE, ET = E["pipelineId"], E["etapas"]
CV = lambda k: "{{custom_values." + k + "}}"          # noqa: E731
mover = lambda n, etapa, status="open": mover_a_etapa(n, PIPE, ET[etapa], status)  # noqa: E731


# ── WF1 · Captación y atribución (LS01+LS02+LS04) ────────────────────────
def wf1():
    return [
        campo("Estampar lanzamiento vigente",
              [("contact.lanzamiento", CV("nombre_lanzamiento_vigente"))]),
        campo("Volcar UTMs a campos",
              [("contact.utm_campaign", "{{contact.utm_campaign}}"),
               ("contact.utm_adset", "{{contact.utm_adset}}"),
               ("contact.utm_ad", "{{contact.utm_ad}}")]),
        *bifurcar("Es contacto italiano?",
            [cond("contact.phone", "contains", "+39")],
            rama_si=[
                campo("Idioma IT / mercado Italia",
                      [("contact.idioma", "IT"), ("contact.mercado", "Italia")]),
                mover("Crear oportunidad IT en Lead nuevo", "Lead nuevo"),
                etiqueta("Marcar oportunidad creada (IT)", ["oportunidad-creada"]),
                whatsapp("Link de registro IT", "respuesta-entrada-desconocido",
                         f"Ciao {{{{contact.first_name}}}}, iscriviti qui: {CV('link_registro_it')}"),
            ],
            rama_no=[
                campo("Idioma ES / mercado Peru-LATAM",
                      [("contact.idioma", "ES"), ("contact.mercado", "Peru-LATAM")]),
                mover("Crear oportunidad ES en Lead nuevo", "Lead nuevo"),
                etiqueta("Marcar oportunidad creada (ES)", ["oportunidad-creada"]),
                whatsapp("Link de registro ES", "respuesta-entrada-desconocido",
                         f"Hola {{{{contact.first_name}}}}, registrate aqui: {CV('link_registro_es')}"),
                esperar("Esperar 30 min por registro", 30, "minutes"),
                notificar("Avisar a Luca: escribio y no se registro",
                          "Lead sin registrar",
                          "{{contact.name}} ({{contact.phone}}) escribio y no completo el registro."),
            ]),
    ]


# ── WF2 · Registro y calificación (LS03+SP01+eliminatoria D6) ────────────
def wf2():
    return [
        etiqueta("Marcar registrado", ["registrado"]),
        *bifurcar("Califica para la escuela?",
            [cond("contact.nivel_calificacion", "eq", "Califica")],
            rama_si=[
                mover("Mover a Registrado", "Registrado"),
                whatsapp("Bienvenida con link del grupo", "bienvenida-registro",
                         f"Hola {{{{contact.first_name}}}}! Ya estas registrado. Unete al grupo "
                         f"para recibir el acceso: {CV('link_grupo_whatsapp_es')}"),
                email("Confirmacion de registro", "Tu lugar esta confirmado",
                      f"<p>Te esperamos el {CV('fecha_evento_vigente')} a las "
                      f"{CV('hora_evento_pe')}.</p>"),
                capi("CAPI: Registro", "CompleteRegistration"),
            ],
            rama_no=[
                mover("Mover a No califica", "No califica"),
                etiqueta("Etiquetar para remarketing", ["a-educar"]),
                whatsapp("Contenido educativo (sin link de grupo)", "educativo-no-califica",
                         f"Gracias por escribirnos. Te dejamos este contenido para "
                         f"entender la causa emocional del sintoma: {CV('link_educativo_es')}"),
                email("Email educativo no califica",
                      "Un primer paso para entender tu sintoma",
                      f"<p>Te compartimos este material: {CV('link_educativo_es')}</p>"),
            ]),
    ]


# ── WF3 · Recordatorios de evento + no-show (SP02) ───────────────────────
def wf3():
    return [
        esperar("Esperar hasta T-24h del evento", 1, "days"),
        whatsapp("Recordatorio 24 h", "recordatorio-24h",
                 f"Manana es la clase: {CV('fecha_evento_vigente')} a las {CV('hora_evento_pe')}."),
        email("Email recordatorio 24 h", "Manana nos vemos",
              f"<p>Manana a las {CV('hora_evento_pe')}.</p>"),
        esperar("Esperar hasta T-3h", 21, "hours"),
        whatsapp("Recordatorio 3 h", "recordatorio-3h",
                 "Hoy es el dia. En 3 horas comenzamos."),
        esperar("Esperar hasta T-15min", 3, "hours"),
        whatsapp("Estamos en vivo (trigger link 1:1)", "en-vivo",
                 f"Estamos comenzando. Entra aqui: {CV('link_evento_es')}"),
        email("Email en vivo", "Estamos en vivo",
              f"<p>Entra ahora: {CV('link_evento_es')}</p>"),
        esperar("Esperar 2 h tras el evento", 2, "hours"),
        # `asistio_evento` es CHECKBOX: GHL espera boolean, no array/cadena.
        *bifurcar("No asistio al evento?",
            [cond("contact.asistio_evento", "eq", False)],
            rama_si=[
                whatsapp("Recuperacion de no-show (copy suave)", "no-show",
                         "Te perdiste la clase de hoy, pero te dejamos lo esencial."),
            ]),
    ]


# ── WF4 · Asistencia / postulación / agenda (SP03+SP04+SP05) ─────────────
def wf4a():
    return [
        campo("Marcar asistencia", [("contact.asistio_evento", "Si")]),
        mover("Mover a Asistio", "Asistio"),
        capi("CAPI: Asistencia", "ViewContent"),
    ]


def wf4b():
    return [
        mover("Mover a Postulo", "Postulo"),
        capi("CAPI: Postulacion", "Schedule"),
        *bifurcar("Es del mercado Italia?",
            [cond("contact.mercado", "eq", "Italia")],
            rama_si=[whatsapp("Enviar calendario Italia", "postulacion-agenda",
                              f"Prenota la tua chiamata: {CV('link_calendario_cierre_it')}")],
            rama_no=[whatsapp("Enviar calendario Peru", "postulacion-agenda",
                              f"Agenda tu llamada con Luca: {CV('link_calendario_cierre_pe')}")]),
    ]


def wf4c():
    return [
        mover("Mover a Llamada agendada", "Llamada agendada"),
        whatsapp("Confirmacion de cita", "confirmacion-cita",
                 "Tu llamada quedo agendada. Te esperamos."),
        esperar("Esperar hasta 24 h antes de la cita", 1, "days"),
        whatsapp("Recordatorio cita 24 h", "recordatorio-cita-24h",
                 "Manana es tu llamada con Luca."),
        esperar("Esperar hasta 1 h antes", 23, "hours"),
        whatsapp("Recordatorio cita 1 h + Zoom", "recordatorio-cita-1h",
                 f"En 1 hora es tu llamada. Enlace: {CV('link_zoom_llamada')} "
                 f"(instala Zoom antes para no perder tiempo)."),
    ]


# ── WF5 · Cobro confirmado (SP07-lite) ───────────────────────────────────
def wf5():
    return [
        campo("Registrar datos de la venta",
              [("contact.producto_comprado", "Escuela"),
               ("contact.estado_pago", "Al dia")]),
        etiqueta("Marcar primer pago procesado", ["primer-pago-procesado"]),
        # Ganado NO es una etapa: es el status de la oportunidad.
        mover("Cerrar oportunidad como Ganado", "Llamada realizada", status="won"),
        notificar("Avisar a Luca: dar de alta en System.io",
                  "Alta manual de alumno",
                  "{{contact.name}} ({{contact.email}}) pago. Crear acceso en System.io."),
        capi("CAPI: Compra", "Purchase"),
        *bifurcar("Pago de contado?",
            [cond("contact.plan_pago", "eq", "Contado")],
            rama_si=[
                campo("Activar bono de llamada con Christie",
                      [("contact.bono_llamada_christie", "Si")]),
                notificar("Avisar a Christie: sesion bono de 40 min",
                          "Nuevo alumno con bono de sesion",
                          "{{contact.name}} pago de contado y tiene derecho a la sesion de 40 min."),
            ]),
    ]


WORKFLOWS = [
    ("WF1 - Captacion y atribucion", wf1),
    ("WF2 - Registro y calificacion", wf2),
    ("WF3 - Recordatorios de evento", wf3),
    ("WF4A - Asistencia", wf4a),
    ("WF4B - Postulacion", wf4b),
    ("WF4C - Cita agendada", wf4c),
    ("WF5 - Cobro confirmado", wf5),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="mostrar los pasos sin tocar GHL")
    ap.add_argument("--solo", help="construir un solo workflow (ej: WF2)")
    args = ap.parse_args()

    seleccion = [(n, f) for n, f in WORKFLOWS
                 if not args.solo or n.upper().startswith(args.solo.upper())]
    if not seleccion:
        sys.exit(f"Sin coincidencias para --solo {args.solo}")

    c = None if args.dry_run else cliente()
    fid = None
    if not args.dry_run:
        fid = carpeta(c, CARPETA)
        if not fid:
            sys.exit("No se pudo crear/encontrar la carpeta")
        print(f"Carpeta: {CARPETA} ({fid})")

    import time
    resultados = []
    for i, (nombre, fn) in enumerate(seleccion):
        if not args.dry_run and i:
            time.sleep(2)      # el backend falla si se guardan muchos seguidos
        r = desplegar(c, nombre, fn(), fid, dry_run=args.dry_run)
        resultados.append(r)
        if args.dry_run:
            print(f"\n── {nombre} ──")
            for linea in r["detalle"]:
                print(f"   {linea}")

    resumen(resultados)


if __name__ == "__main__":
    main()
