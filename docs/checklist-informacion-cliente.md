# Checklist de información al cliente — v2 (post-form)

Qué falta pedirle a Luca, Christie y Joaquín después del form de onboarding (`fuentes/02-form-onboarding.md`).
**Regla:** cada ítem dice para qué sirve y qué bloquea si falta. Los códigos (A2, B5…) son los que referencia el mapa v3.

---

## ✅ Ya recibido por el form — NO volver a pedir

Logos (vertical + horizontal) · nombre de negocio (Salud Consciente) y de la escuela (NCA Academy) · dirección y localidad · redes (IG/FB/TikTok) · email del negocio (`info@lanuovacoscienza.com`) · horario general de atención · moneda de referencia (USD) · precios de: escuela contado ($1.000), 5 Leyes ($100), libro (S/80), sesiones 1-a-1 ($70/$180/$299) · método de pago preferido (transferencia IBAN) · que no piden seña.

---

## A · Llaves que bloquean el arranque — pedir HOY, con fecha límite 48 h

| # | Qué | Para qué / qué bloquea |
|---|---|---|
| **A1** | **Meta Business:** ¿Joaquín recuperó el admin del portafolio? Si en 48 h no hay acceso de administrador → autorización para **crear portafolio nuevo a nombre de Nueva Conciencia Formación SAC**. Incluye: quién es hoy admin del Business Manager, de la cuenta publicitaria y de la página de Facebook. | Bloquea **píxel + CAPI Y el alta de WhatsApp API** (los dos requieren Business Manager con admin). Es la dependencia nº 1 del proyecto. Sin histórico que perder: nunca hubo píxel en Perú y el de Italia no tiene CAPI. |
| **A2** | **Número para la API de WhatsApp.** El form dio `+51 986 199 020` como "WhatsApp del negocio": ¿ese es el número NUEVO destinado a la API, o es el que ya usan en el teléfono? El que se conecta a la API **no puede tener WhatsApp activo en la app** — si conectamos el actual, Luca pierde la app y los grupos. Si aún no hay número nuevo: conseguir un chip/número virtual hoy. Extra: ¿pueden conseguir un número italiano (+39)? (define `P-02`: un número por mercado da más confianza en Italia). | Bloquea todo el canal automatizado: plantillas, recordatorios, confirmaciones. |
| **A3** | **Dominio y DNS:** acceso al panel donde vive `lanuovacoscienza.com` (o el dominio que prefieran para funnels). Confirmar también si quieren subdominio tipo `eventos.lanuovacoscienza.com`. | Bloquea publicación de páginas y verificación del dominio de envío de email. |
| **A4** | **Stripe:** acceso de colaborador a la cuenta que hoy usa System.io. ¿Es una sola cuenta para los dos mercados? ¿En qué moneda cobra hoy Italia (EUR)? | Bloquea la conexión de cobro y los tres planes de la escuela (`P-09`). |
| **A5** | **El primer lanzamiento:** fecha exacta del primer evento del jueves · cadencia definitiva (semanal como dice Joaquín, o ciclo de 2 semanas como dice Christie — `P-01`) · horarios por mercado (dato propio a favor: su mejor asistencia fue un sábado 17:00 en Italia) · y **qué es el evento del jueves: ¿webinar sin venta o masterclass con venta?** (`P-10`). | Bloquea el copy de recordatorios, la programación de WF3 y el CTA de la página del evento. Cada día sin fecha corre el lanzamiento de agosto. |
| **A6** | **Precios que faltan:** 21 días, Dispersión del dolor, Reflexología (por mercado y moneda) · montos de la escuela en 2 y 3 cuotas · precio de la escuela para Italia (¿EUR 1.000?). | Los de la escuela bloquean los productos Stripe de F1. Los low ticket bloquean solo la escalera (F2), pero pedirlos ya. |

## B · Para construir bien — esta semana

| # | Qué | Para qué |
|---|---|---|
| **B1** | Links de invitación de los grupos de WhatsApp del lanzamiento (ES y IT). | Van en la página de gracias y en la plantilla de bienvenida (custom values). |
| **B2** | Canal de YouTube: quién sube el video del falso-en-vivo y acceso o coordinación para que sea **no listado**. Confirmación explícita de que el evento NO se transmite en abierto. | Si va en abierto se cae la medición de asistencia, el CTA y la urgencia — y WF4 se queda sin disparador. |
| **B3** | Guion/promesa de los anuncios (Joaquín) + el funnel anterior que no convirtió (ya lo pidió Henry en la llamada) + VSL si existe. | Coherencia anuncio → landing (la landing repite la promesa del anuncio o el lead rebota). |
| **B4** | Validación de las preguntas del formulario de registro (les mandamos el borrador de §7 del mapa): Luca ajusta el tono en ES y produce la versión IT. Igual con las ~10 plantillas de WhatsApp en italiano. | Las plantillas van a aprobación de Meta el día 1 — el italiano tiene que estar validado antes. |
| **B5** | Disponibilidad real de Luca para llamadas de cierre: franjas concretas por mercado (no el horario general del negocio), buffer entre llamadas, máximo por día. | Sin esto los calendarios agendan cuando Luca duerme (los mercados están a 7 h de distancia). |
| **B6** | Testimonios escritos: los 10–20 mejores, con permiso de uso (y si alguno se anima a video, oro puro — se les dijo en la llamada). | Landing y página del evento. |
| **B7** | Textos legales: política de privacidad, términos, y **descargo médico** ("esto no sustituye atención médica"). Si no tienen, proponemos borrador y lo revisa su gente. | Nicho salud: sin disclaimer, Meta puede rechazar anuncios y plantillas, y hay exposición legal real. |
| **B8** | Logos en fondo transparente o el archivo vectorial (AI/SVG). Los PNG recibidos traen el fondo negro incrustado. | Sin transparente, todas las páginas quedan obligadas a tema oscuro. |
| **B9** | Link/cuenta de Zoom que usa Luca para las llamadas de cierre. | Va en los recordatorios de cita (con instrucciones de instalación — dolor conocido de su público). |

## C · Para Fase 2 — pedir ya, no bloquea F1

| # | Qué | Para qué |
|---|---|---|
| **C1** | API key de System.io + export de contactos y compradores (CSV). | PoC temprana de la API durante F1 (desriesga AP01) + rescate de la base histórica (~1.000 contactos IT — LS05). |
| **C2** | Export de compradores de Hotmart + acceso para configurar el webhook de compra. | Capturar al comprador de Reflexología (el low ticket más caro, hoy sin base). |
| **C3** | Contenido de la aplicación de síntomas (Luca ya ofreció pasarlo). | Base de conocimiento del bot IA de F2. Es grande: conviene recibirlo ya para evaluarlo (Conversation AI nativo vs n8n). |
| **C4** | Guion del pitch de la masterclass + full day de Lima: fecha, aforo, precio de entrada, y si el cierre es en sala o con llamada posterior. | Define la rama Perú del pipeline y si hace falta venta de entradas (pregunta 7 del handoff). |
| **C5** | ¿Quién valida las respuestas del bot en italiano y cuántas horas semanales puede dedicarle? (¿Luca?) | Riesgo 4 del handoff: es el cuello de botella del cronograma de F2. |
| **C6** | Lista exacta de entregables por producto del high ticket, incluidos los bonos anidados del videocurso 5 Leyes (56 preguntas, test de herida emocional, meditación). | Árbol de entrega de AP02 (onboarding del alumno). |

---

## D · Mensaje listo para enviar (WhatsApp, sección A)

> Luca, Christie, Joaquín — ¡gracias por el formulario! 🙏 Con eso ya arrancamos la construcción. Para no frenar el lanzamiento de agosto necesitamos **6 cosas esta semana** (idealmente en 48 h):
>
> 1️⃣ **Meta:** Joaquín, ¿pudiste recuperar el administrador del portafolio? Si no se puede, les proponemos crear uno nuevo a nombre de Nueva Conciencia Formación SAC — no pierden nada y desbloquea el píxel Y el WhatsApp automatizado de una vez. Dinos cuál camino.
> 2️⃣ **Número de WhatsApp para el sistema:** ¿el +51 986 199 020 que pusieron en el form es el número nuevo, o el que ya usan? El del sistema tiene que ser un número SIN WhatsApp activo en el teléfono (el de Luca y sus grupos no se tocan). Si no hay número nuevo aún, con un chip nuevo nos basta. ¿Y habría chance de un número italiano también?
> 3️⃣ **Dominio:** acceso al panel de `lanuovacoscienza.com` (donde compraron el dominio) para conectar las páginas y el correo.
> 4️⃣ **Stripe:** invitación de colaborador a la cuenta que usan en System.io. ¿Italia cobra en euros o dólares?
> 5️⃣ **El primer lanzamiento:** fecha del primer jueves, si va semanal o cada 2 semanas, horarios por mercado, y si ese jueves ya se vende (masterclass) o solo se educa (webinar).
> 6️⃣ **Precios que faltan:** escuela en 2 y 3 cuotas (¿y en euros para Italia?), 21 días, Dispersión y Reflexología.
>
> Con eso nada nos detiene. Lo de la lista B (grupos, YouTube, testimonios, textos legales) se los vamos pidiendo en el camino. 💪

---

## Interno (no va al cliente)

- `P-08`: confirmar con Henry qué se facturó (¿F1 sola o paquete completo?) — define el margen de re-escopeo de F2 (§15 del mapa).
- Costos de plataforma/consumos: si el cliente pregunta, **remitir a Jaime** (acuerdo interno 6-ago).
- Avisar a Jaime por el grupo compartido: form recibido, mapa v3 listo, checklist enviado — para que no se repita el vacío de comunicación.
