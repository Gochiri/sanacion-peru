# Datos que mandó el cliente — 4-sep

Lo que faltaba desde julio: fechas, horas, datos de cobro y disponibilidad de cierre.
Con esto los 7 custom values de fecha y los 2 de cobro dejan de estar en `PENDIENTE`,
y los dos calendarios pasan de un horario inventado a la agenda real.

## Calendario del lanzamiento

| Fecha | Qué pasa |
|---|---|
| **lun 7-sep** | Arrancan los anuncios |
| **dom 20-sep** | Empieza la semana de operación del webinar |
| **jue 24-sep · 20:00 Perú** | Webinar de venta — LATAM, ciclo 1 |
| **sáb 26-sep · 18:00 Italia** | Webinar de venta — Italia, ciclo 1 |
| **jue 1-oct · 20:00 Perú** | Webinar de venta — LATAM, ciclo 2 |
| **sáb 3-oct · 18:00 Italia** | Webinar de venta — Italia, ciclo 2 |

Son **dos ciclos**, y los custom values de fecha solo aguantan uno a la vez. El ciclo 2
se carga el **25-sep**, en cuanto termina el primer webinar:
`python3 builders/valores.py ciclo 2 --aplicar`.

> **Ojo con el día de Italia.** En la llamada del 28-ago (K12) se anotó que el webinar
> italiano iba en sábado, y las dos fechas que mandó el cliente son sábado — coinciden.
> Lo que **no** coincide es el día respecto de LATAM: jueves allá, sábado aquí. Los dos
> mercados van desfasados dos días, y por eso WF3-ES y WF3-IT tienen que seguir separados.

## Cobro manual

**Perú** — solo transferencia interbancaria:

```
Titular: Nueva Consciencia Formación SAC
Banco:   BCP · cuenta en soles
Cuenta:  1937405302029
CCI:     00219300740530202918
```

⚠ El cliente escribe **«Nueva Consciencia»** (con S). En el resto del proyecto la razón
social figura como **«Nueva Conciencia»** (handoff, invoice, K1). **No bloquea el cobro**: una
transferencia por CCI encamina por el número de cuenta, y el titular es solo lo que ve el que
paga al confirmar. Pero ese nombre queda escrito dentro de la plantilla `datos_pago_es`, que
una vez aprobada por Meta **no se edita** — así que hay que resolverlo antes de mandarla.

**Italia**:

```
Banca: Intesa Sanpaolo
IBAN:  IT98L0306979654100000006623
```

⚠ **Falta el intestatario, y este sí bloquea.** Desde octubre de 2025 los bancos de la UE
tienen que verificar que el nombre del beneficiario coincida con el IBAN antes de ejecutar un
bonifico: sin él, al comprador le salta un aviso de discrepancia justo cuando está pagando
$1.000. Hace falta **antes del 26-sep**, que es cuando vende Italia. Por D10 lo más probable
es que la cuenta sea de Luca a título personal, pero un dato bancario no se supone.

## Disponibilidad de cierre — **una hora por cliente**

Los dos calendarios estaban a 30 minutos. Ahora van a 60, sin colchón entre turnos.

**Joaquín** (mercado español, hora de Perú):

| Fechas | Horario |
|---|---|
| vie 25-sep | 9:00–17:00 |
| sáb 26-sep | 9:00–12:00 |
| lun 28 a mié 30-sep | 9:00–17:00 |
| vie 2-oct | 9:00–17:00 |
| sáb 3-oct | 9:00–12:00 |
| lun 5 a vie 9-oct | 9:00–17:00 |
| sáb 10-oct | 9:00–12:00 |

Los jueves 24-sep y 1-oct **no** están: son los días de webinar. El jueves 8-oct sí.

**Luca** (mercado italiano): **15:00–19:00 hora italiana**, del 28-sep al 2-oct y del
5 al 10-oct.

## Para los que no califican

Curso gratuito **«La Verdad que Sana»**, alojado en **System.io**. Falta la URL —
es lo que llena `embed_video_educativo_es`.
