# Triggers — qué falta y cómo se pone (paso a paso)

## Por qué van en la UI y no por API

Se intentó por API y **salió mal**: GHL **no valida el `type` del trigger**. Acepta cualquier
cadena y deja un trigger que en la interfaz parece bien configurado pero **nunca dispara**. De los
que se adivinaron entonces, la mitad estaban mal (`pipeline_stage_changed` en vez de
`pipeline_stage_updated`, `customer_booked_appointment` en vez de `customer_appointment`…).

Por eso la regla es: **los triggers se crean a mano y el API solo se usa para leerlos** y
comprobar que quedaron bien.

## Los IDs que vas a necesitar

| Qué | ID |
|---|---|
| Pipeline | `NCuspbUzn0AhWXAPn3g7` |
| Etapa · Registrado | `f8453476-5203-4acf-81b8-9e72311290ab` |
| Calendario Español (Joaquín) | `befuzgaXYSmsD2qUZdkl` |
| Calendario Italiano (Luca) | `MNg4SJeHdqjOfoGjJpKQ` |
| Encuesta F01 | `iheVfI7xkesInu8jKLKB` |
| Formulario F03 | `DTwkB4aTiEIqUGNI9Qjo` |

---

## 1 · WF4C — ROTO, arreglar primero

**Qué pasó:** su trigger apuntaba al calendario `yCYC1PwGWrYRxifCIvBX`, que **se borró** al
rehacer los calendarios con el tipo correcto. Ahora mismo **WF4C no dispara con ninguna cita**:
nadie recibe confirmación ni recordatorios de su llamada.

**Arreglo:** abrir WF4C → el trigger *Customer Booked Appointment* → en el filtro del calendario,
**quitar la condición de calendario**.

Se quita en vez de apuntarla al nuevo porque ahora hay **dos** calendarios y WF4C sirve a los dos.
Dejando solo `contactMode = contact`, cualquier cita de cualquiera de los dos lo dispara.

> ⚠️ Gap conocido: el copy de WF4C está solo en español, así que quien reserve en italiano
> recibirá mensajes en español. Es el mismo hueco que WF2 y se resuelve al partirlo por idioma.

---

## 2 · WF3-ES — le falta el filtro de mercado

Hoy dispara con **cualquiera** que entre a la etapa *Registrado*, incluidos los italianos. Como
ahora existe WF3-IT, los dos se pisarían y un italiano recibiría los dos juegos de recordatorios.

**Arreglo:** abrir WF3-ES → su trigger *Pipeline Stage Changed* → añadir un filtro más:

- Campo: **Mercado** (el campo personalizado del contacto)
- Operador: **es igual a**
- Valor: **Peru-LATAM**

---

## 3 · WF3-IT — no tiene trigger

Crear uno igual al de WF3-ES pero para el otro mercado:

- Tipo: **Pipeline Stage Changed**
- Pipeline: el de la tabla de arriba
- Etapa: **Registrado**
- Filtro extra: **Mercado** · es igual a · **Italia**

> Este es el único caso donde un filtro de más en el trigger es correcto. No confundirlo con
> el filtro que rompió WF2 en su día (ver `triggers-pendientes.md`): aquel dejaba fuera a los
> descalificados, que sí tenían que entrar.

---

## 4 · WF4A — no tiene trigger, y ahora ya se puede

Es el que marca **quién asistió al evento**. Va en dos partes.

**a) Crear el trigger link.** Marketing → Trigger Links → nuevo:

- Nombre: `evento-es-en-vivo`
- URL de destino: la de la página del evento publicada

**b) Usarlo en los dos sitios:**

1. En **WF3-ES**, el mensaje *«Estamos en vivo»* debe llevar **ese trigger link**, no la URL
   directa. Es lo único que permite saber quién entró.
2. En **WF4A**, crear el trigger **Trigger Link Clicked** apuntando a ese link.

> **Por qué importa:** el link del grupo de WhatsApp es el mismo para todos y **no marca a nadie**.
> Solo el trigger link enviado 1:1 identifica a la persona. Por eso el mensaje del grupo debe decir
> «entra por el link que te llegó a tu WhatsApp», y el % de asistencia se lee como métrica del
> canal individual, no del total.

Cuando exista la página italiana, repetir con `evento-it-en-vivo` y un WF4A-IT.

---

## Comprobar que quedaron bien

```bash
set -a && . tools/ghl-cli/.env && set +a
PYTHONPATH=builders python3 - <<'PY'
from esb_lib import cliente
c = cliente(); loc = c.location_id
lst = c.request("GET", f"/workflow/{loc}") or []
if isinstance(lst, dict): lst = lst.get("workflows") or lst.get("data") or []
for w in lst:
    if w.get("type") == "directory": continue
    wid = w.get("id") or w.get("_id")
    r = c.request("GET", f"/workflow/{loc}/trigger?workflowId={wid}")
    trs = r if isinstance(r, list) else ((r or {}).get("triggers") or [])
    print(w.get("name"), "->", [t.get("type") for t in trs] or "SIN TRIGGER")
PY
```

Si un `type` no está entre los cinco del catálogo (`contact_created`, `contact_tag`,
`survey_submission`, `pipeline_stage_updated`, `customer_appointment`), el trigger está muerto
aunque la interfaz lo muestre bien.
