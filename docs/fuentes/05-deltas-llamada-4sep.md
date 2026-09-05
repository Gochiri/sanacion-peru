# Deltas — llamada con Joaquín del 4-sep (38 min)

Grabación: https://fathom.video/share/a1WsZeyGhXKsoU3oVTcQ3_9s-Ch71Y9B
Asistentes: Oliver · Germán (Profit) · Joaquín (cliente).

Joaquín entró con dudas operativas y salió respondiendo las dos preguntas que teníamos
abiertas. Pero la llamada trajo bastante más: cambia la vía de cobro de la escuela, se
mueve la fecha de arranque y salen dos pedidos nuevos. Los compromisos siguen la
numeración de `03-deltas-llamada-28ago.md`, que terminó en `K14`.

---

## Lo que respondió

### K15 · Razón social sin «SAC», e intestatario italiano

La razón social es **«Nueva Consciencia Formación»**, sin SAC — *«sin saco»*, dijo. Y la
cuenta italiana es de **Luca Stefanizzi a título personal**: en Italia no hay empresa, la
SAC es solo la peruana.

Lo segundo ya lo teníamos escrito desde el onboarding —`02-form-onboarding.md:40` dice
*«TRANSFERENCIA BANCARIA (IBAN, titular Luca Stefanizzi)»*— y no lo habíamos conectado.

> ⚠️ **Lo que la llamada no resuelve es la S de «Con*s*ciencia».** El transcript de Fathom
> normaliza la ortografía y las dos grafías salen iguales. Va la del mensaje escrito del
> cliente. Importa porque ese nombre queda dentro de una plantilla de Meta que después no
> se edita.

## Lo que cambia

### K16 · La escuela no se cobra con links — solo transferencias

La escuela **nunca se vendió por Hotmart** porque nunca se vendió en Latinoamérica, y en
Italia nadie usa Hotmart. Hotmart queda **solo para low tickets**, y de esos el único link
que va a existir ahora es el del pase VIP.

Tumba una premisa que veníamos arrastrando: los tres `link_pago_*` no están «esperando a
Stripe», **no aplican al producto escuela**. La ruta manual no es el plan B, es el único.

### K17 · Fuera de Perú, LATAM paga por giro

Perú transfiere al BCP, Italia al IBAN de Luca, y **el resto de Latinoamérica manda giro
(Western Union)**. No existía nada de esto en el sistema, y los anuncios apuntan a LATAM.

Decisión de Oliver: **no se automatiza** — esos datos los da el que cierra, en la llamada.
La única precaución tomada es que la plantilla se llama **`datos_pago_pe`** y no
`datos_pago_es`, porque lleva una cuenta del BCP en soles escrita en el cuerpo: mandársela
a alguien de Colombia es darle una cuenta a la que no puede girar, y no salta ningún error.

### K18 · El curso del no-calificado se muda a Drive

Ya no va en System.io —*«nos ha dado bastantes problemas»*—. Joaquín lo descarga, lo sube a
un **Drive compartido partido por módulos** y nos pasa el enlace.

Consecuencia técnica: el guard de `comienza-aqui-es.html` solo aceptaba embeds de YouTube,
y Drive además no se deja embeber. Ya está resuelto: el recuadro tiene tres estados y con
un enlace normal saca una tarjeta con botón.

### K19 · Fechas — la entrega se mueve, el webinar no

| | Antes | Ahora |
|---|---|---|
| Entrega | — | **martes 8-sep** |
| Anuncios | lunes 7-sep | **miércoles 9-sep, 17:00-18:00** — Joaquín los programa el martes de noche |
| Webinars | 24-sep y 1-oct | **sin cambios** |

Los custom values de fecha no se tocan. Pero el hueco entre el 9 y el 24 es justo lo que
hace crítico el anclaje temporal de WF3 (ver abajo).

## Lo que pidió

### K20 · Avisos internos al agendar

Joaquín quiere enterarse cuando alguien reserva, y también una hora antes: *«si me llega
una hora antes yo lo agendo y lo tengo listo»*. **WF4C no avisaba a nadie** — tenía cero
nodos de notificación interna, frente a 1 de WF1 y 3 de WF5. Ya están puestos los dos.

### K21 · Nutrición por correo entre el registro y el evento

Su argumento: unos se inscriben el 3 de septiembre y otros el 19, y los primeros pasan
semanas sin recibir nada. Es correcto, y **nunca se planteó**: los 7 emails de F1 son
confirmación y recordatorios. Lo que se descartó en su día (`SP09`) era nurturing
*post-venta perdida*, otra cosa distinta.

**Alcance nuevo, y bloqueado por el mismo problema que P0.**

### K22 · La llamada de cierre dura 30-40 min, pero una por hora

*«Una hora por cliente»*, porque a veces la persona dice que va a transferir y hay que
esperarla en la llamada. Germán lo encuadró bien: la reunión puede figurar como de 30 o 40
minutos, pero solo entra una por hora. Los dos calendarios están a 60/60.

### Sin decidir

**PIX (Brasil).** Se mencionó de pasada y quedó en el aire.

---

## 🚨 Lo que apareció al rastrear la llamada, y no salió en ella

**Los recordatorios de WF3 se disparan al registrarse, no antes del evento.** Las cinco
esperas son deltas relativos (`{"type":"days","value":1,"when":"after"}`) y el trigger es
el instante del registro. La cadena entera —24 h, 3 h, en vivo, no-show— corre en las 48
horas siguientes a que alguien se inscribe.

Con anuncios el 9 y webinar el 24, quien se registre el primer día recibe *«mañana es la
clase»* el 10, *«estamos en vivo»* el 11 con el trigger link a una sala vacía, y el mensaje
de no-show dos horas después. Y como ese trigger link dispara **WF4A**, además queda marcado
como asistente: la etapa del pipeline se corrompe.

Estaba anotado sin resolver en `mapa-implementacion-v3.md:169`. **Es la prioridad número
uno** y necesita que alguien configure un nodo de espera por fecha en la UI para poder leer
el esquema real, igual que se hizo con `internal_notification`.
