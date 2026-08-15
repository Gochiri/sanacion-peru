# Checklist de información al cliente — v2 (post-form)

Qué falta pedirle a Luca, Christie y Joaquín después del form de onboarding (`fuentes/02-form-onboarding.md`).
**Regla:** cada ítem dice para qué sirve y qué bloquea si falta. Los códigos A/B/C son los que referencia el mapa v3 (los compromisos de las llamadas se citan aparte como `K1…K9`).

---

## ✅ Ya recibido por el form — NO volver a pedir

Logos (vertical + horizontal) · nombre de negocio (Salud Consciente) y de la escuela (NCA Academy) · dirección y localidad · redes (IG/FB/TikTok) · email del negocio (`info@lanuovacoscienza.com`) · horario general de atención · moneda de referencia (USD) · precios de: escuela contado ($1.000), 5 Leyes ($100), libro (S/80), sesiones 1-a-1 ($70/$180/$299) · método de pago preferido (transferencia IBAN) · que no piden seña.

---

## A · Llaves que bloquean el arranque — pedir HOY, con fecha límite 48 h

| # | Qué | Para qué / qué bloquea |
|---|---|---|
| **A1** | **Meta Business:** ¿Joaquín recuperó el admin del portafolio? Si en 48 h no hay acceso → autorización para **crear portafolio nuevo a nombre de Nueva Conciencia Formación SAC**. Incluye: quién es hoy admin del Business Manager, de la cuenta publicitaria y de la página de Facebook. **Si vamos por portafolio nuevo, reunir EN PARALELO los documentos de verificación de negocio: ficha RUC / constitución de la SAC, email @lanuovacoscienza.com activo y teléfono verificable** — la verificación tarda días y es requisito del WhatsApp API. | Bloquea **píxel + CAPI Y el alta de WhatsApp API**. Dependencia nº 1. Sin histórico que perder: nunca hubo píxel en Perú y el de Italia no tiene CAPI. |
| **A2** | **Número para la API de WhatsApp.** El form dio `+51 986 199 020`: ¿ese es el número NUEVO destinado a la API, o el que ya usan? El que se conecta **no puede tener WhatsApp activo en la app** — si conectamos el actual, Luca pierde la app y los grupos. Si no hay número nuevo: conseguir chip/número virtual hoy. *(Lo del posible número italiano lo evaluamos nosotros primero — depende de si la plataforma soporta un segundo número, `P-02`; no prometerlo.)* | Bloquea todo el canal automatizado: plantillas, recordatorios, confirmaciones. |
| **A3** | **Dominio y DNS:** acceso al panel donde vive `lanuovacoscienza.com` (o el dominio que prefieran). Confirmar si quieren subdominio tipo `eventos.lanuovacoscienza.com`. | Bloquea publicación de páginas y verificación del dominio de envío de email. |
| **A4** | **Cobros, la foto completa:** (1) acceso de colaborador a la cuenta Stripe que usa System.io — **¿de qué país es la cuenta y quién es el titular?** (Stripe no opera para comercios domiciliados en Perú; asumimos que es la cuenta italiana/personal de Luca). (2) **¿Cómo paga hoy un alumno peruano en la práctica?** (¿Yape? ¿Plin? ¿transferencia BCP/Interbank? ¿tarjeta?) (3) **Datos exactos de pago manual** para las plantillas de cierre: IBAN para Italia, cuenta/CCI/QR Yape para Perú. (4) Aviso nuestro, no pregunta: la plataforma cobra en **una sola moneda** — proponemos USD (como su form); el precio a Italia bajo USD se confirma en A6. | Bloquea la conexión de cobro, los tres planes de la escuela y los custom values `datos_pago_pe`/`datos_pago_it`. Sin (2) y (3), el primer cierre en Perú se improvisa por WhatsApp. |
| **A5** | **El primer lanzamiento:** fecha exacta del primer evento del jueves · **¿arranca solo Perú, solo Italia o ambos?** (`P-14` — reordena todo el plan de construcción) · cadencia definitiva (semanal como dice Joaquín, o ciclo de 2 semanas como dice Christie — `P-01`) · horarios por mercado (dato propio: su mejor asistencia fue un sábado 17:00 en Italia) · **¿el evento del jueves vende (masterclass) o solo educa (webinar)?** (`P-10`) · y mientras no haya full day en Lima: **¿Perú cierra por llamada de 30 min con Luca?** (así lo asume el mapa). | Bloquea copy de recordatorios, programación de WF3, CTA de la página del evento y el orden de los 5 días de build. |
| **A6** | **Precios que faltan:** 21 días, Dispersión del dolor, Reflexología (por mercado) · montos de la escuela en 2 y 3 cuotas · precio de la escuela para Italia bajo moneda única USD (¿$1.000 también?). | Los de la escuela bloquean los productos de cobro de F1. Los low ticket bloquean solo la escalera (F2), pero pedirlos ya. |
| **A7** | **Estado de producción del contenido del lanzamiento:** ¿cuántas clases diarias de falso-en-vivo están ya grabadas? ¿Quién graba las que faltan y el video del evento del jueves, y para qué fecha? ¿Hay VSL o se graba? | **El sistema puede estar listo el día 5 y no haber nada que emitir el jueves.** Es la dependencia gemela de las llaves técnicas: sin videos confirmados a fecha, el lanzamiento se corre una semana — se dice hoy (riesgo 15 del mapa). |

## B · Para construir bien — esta semana

| # | Qué | Para qué |
|---|---|---|
| **B1** | Links de invitación de los grupos de WhatsApp del lanzamiento (ES y IT). | Página de gracias y plantilla de bienvenida (custom values). |
| **B2** | Canal de YouTube: quién sube el video del falso-en-vivo y acceso o coordinación para que sea **no listado**. Confirmación explícita de que el evento NO se transmite en abierto. | Si va en abierto se cae la medición de asistencia, el CTA y la urgencia — y WF4 se queda sin disparador. |
| **B3** | Guion/promesa de los anuncios (Joaquín) + el funnel anterior que no convirtió + VSL si existe. | Coherencia anuncio → landing, y es el insumo de la asesoría de estructura/feedback comprometida (K7). |
| **B4** | **Bloque de validación en italiano de Luca, con horas reservadas y fecha límite (día 3):** encuesta de registro + 11 plantillas de WhatsApp + 7 emails + las 5 páginas replicadas. Propuesta operativa (`P-13`): **Luca produce/traduce el copy IT con IA (como hace con su contenido), nosotros maquetamos y él valida** — la traducción está fuera del alcance del estimado. | Las plantillas IT no pueden ir a aprobación de Meta sin esto. Si el primer ciclo es solo Perú (A5), pierde urgencia — pero se agenda igual. |
| **B5** | Disponibilidad real de Luca para llamadas de cierre: franjas concretas por mercado (no el horario general del negocio), buffer entre llamadas, máximo por día. | Sin esto los calendarios agendan cuando Luca duerme (7 h de diferencia entre mercados). |
| **B6** | Testimonios escritos: los 10–20 mejores, con permiso de uso (y si alguno se anima a video, oro puro — ya se les dijo). | Landing y página del evento. |
| **B7** | **Textos legales — requisito ANTES de publicar páginas, no "en el camino":** política de privacidad (que cubra **datos de salud** — la encuesta los captura y hay consumidores UE: RGPD Art. 9), términos, y descargo médico ("esto no sustituye atención médica"). **Los textos los provee el cliente** (su abogado o los que ya usen); nosotros colocamos el descargo estándar y el banner de cookies. *(Si no tienen nada, ofrecer un borrador genérico es decisión de Henry — es trabajo no cotizado con responsabilidad en nicho salud.)* | Sin esto no se publican los funnels: exposición legal real + Meta rechaza anuncios y plantillas en nicho salud. |
| **B8** | Logos en fondo transparente o el archivo vectorial (AI/SVG). Los PNG recibidos traen el fondo negro incrustado. | Sin transparente, todas las páginas quedan obligadas a tema oscuro. |
| **B9** | Link/cuenta de Zoom que usa Luca para las llamadas de cierre. | Recordatorios de cita (con instrucciones de instalación — dolor conocido de su público). |
| **B10** | **Contenido de la página del no-calificado:** video o pieza educativa gratuita (¿existe en ES? ¿en IT?) + **URLs de los checkouts actuales de los low tickets** (21 días en System.io, Reflexología en Hotmart). | Sin esto, `/comienza-aqui` y la secuencia de descalificados se construyen con placeholders y se entregan vacías. Son links que tienen a mano. |

## C · Para Fase 2 — pedir ya, no bloquea F1

| # | Qué | Para qué |
|---|---|---|
| **C1** | API key de System.io + export de contactos y compradores (CSV). | PoC temprana de la API durante F1 (desriesga AP01) + rescate de base histórica (~1.000 contactos IT — LS05). |
| **C2** | Export de compradores de Hotmart + acceso para configurar el webhook de compra. | Capturar al comprador de Reflexología (el low ticket más caro, hoy sin base). |
| **C3** | Contenido de la aplicación de síntomas (Luca ya ofreció pasarlo). | KB del bot IA de F2. Es grande: recibirlo ya para evaluar Conversation AI nativo vs n8n. |
| **C4** | Guion del pitch de la masterclass + full day de Lima: fecha, aforo, precio de entrada, y si el cierre es en sala o con llamada posterior. | Define la rama Perú del pipeline y si hace falta venta de entradas. |
| **C5** | ¿Quién valida las respuestas del bot en italiano y cuántas horas semanales puede dedicarle? (¿Luca?) | Riesgo 4 del handoff: cuello de botella del cronograma de F2. |
| **C6** | Lista exacta de entregables por producto del high ticket, incluidos los bonos anidados del videocurso 5 Leyes (56 preguntas, test de herida emocional, meditación). | Árbol de entrega de AP02 (onboarding del alumno). |

---

## D · Mensaje listo para enviar (WhatsApp, sección A)

> Luca, Christie, Joaquín — ¡gracias por el formulario! 🙏 Con eso ya arrancamos la construcción. Para no frenar el lanzamiento de agosto necesitamos **7 cosas esta semana** (idealmente en 48 h):
>
> 1️⃣ **Meta:** Joaquín, ¿pudiste recuperar el administrador del portafolio? Si no se puede, les proponemos crear uno nuevo a nombre de Nueva Conciencia Formación SAC — no pierden nada y desbloquea el píxel Y el WhatsApp automatizado de una vez. Si vamos por el nuevo, vayan juntando en paralelo: ficha RUC de la SAC, que el correo del dominio esté activo y un teléfono verificable (Meta los pide para verificar el negocio).
> 2️⃣ **Número de WhatsApp para el sistema:** ¿el +51 986 199 020 que pusieron en el form es el número nuevo, o el que ya usan? El del sistema tiene que ser un número SIN WhatsApp activo en el teléfono (el de Luca y sus grupos no se tocan). Si no hay número nuevo aún, con un chip nuevo nos basta.
> 3️⃣ **Dominio:** acceso al panel de `lanuovacoscienza.com` (donde compraron el dominio) para conectar las páginas y el correo.
> 4️⃣ **Cobros:** invitación de colaborador a la cuenta Stripe que usan en System.io — ¿de qué país es esa cuenta y a nombre de quién está? Y muy importante: ¿cómo les paga hoy en la práctica un alumno peruano (Yape, Plin, transferencia, tarjeta)? Pásennos los datos exactos de cobro de cada mercado (IBAN de Italia, cuenta/QR de Perú) para dejarlos cargados en el sistema. Ojo: la plataforma cobra en una sola moneda — proponemos dólares, como pusieron en el form.
> 5️⃣ **El primer lanzamiento:** ¿arrancamos con Perú, con Italia o con ambos? Fecha del primer jueves, si va semanal o cada 2 semanas, horarios por mercado, y si ese jueves ya se vende (masterclass) o solo se educa (webinar). Y mientras no haya full day en Lima, ¿el cierre en Perú es por llamada de 30 min con Luca?
> 6️⃣ **Precios que faltan:** escuela en 2 y 3 cuotas (¿y a Italia le cobramos también $1.000?), 21 días, Dispersión y Reflexología.
> 7️⃣ **Los videos:** ¿cuántas clases diarias ya están grabadas? ¿Quién graba las que faltan y el video del jueves, y para cuándo? El sistema va a estar listo — necesitamos que haya qué emitir. 🎥
>
> Con eso nada nos detiene. Lo de la lista B (grupos, YouTube, testimonios, textos legales, validación del italiano) se los vamos pidiendo en el camino — solo adelanto uno: **antes de publicar páginas necesitamos su política de privacidad y el descargo médico** (les decimos exactamente qué debe cubrir). 💪

---

## Interno (no va al cliente)

- `P-08` ✅ resuelto (15-ago): cobrado el **50% de F1**; F2 en horizonte, sin facturar. Plan de F2 en §15 del mapa: se estructura con la opción 2 de fábrica ANTES de cobrarla y se cierra contra el éxito del primer lanzamiento. Tareas ClickUp: 2.º 50% de F1 contra entrega (condición Meta) + propuesta F2 estructurada.
- La sección C sigue siendo "pedir ya": con F2 en horizonte, la PoC de System.io y el contenido de la app de síntomas son los que desriesgan (y ayudan a vender) esa fase.
- Costos de plataforma/consumos: si el cliente pregunta, **remitir a Jaime** (acuerdo interno 6-ago). **Pasarle a Jaime el ancla que el cliente ya escuchó: $97 licencia + $10 WhatsApp (K8)** — si cotiza por encima, la promesa la hicimos nosotros.
- Avisar a Jaime por el grupo compartido: form recibido, mapa v3 listo, checklist enviado.
- **Pruebas de plataforma del día 1 (antes de prometer nada más):** disqualify de survey dispara trigger (§7) · anclaje temporal de WF3 (§10) · ¿LC WhatsApp soporta 2º número? (`P-02`) · corte a N ciclos en suscripciones (§12).
- El 2.º 50% **no se factura** con el bloqueo Meta sin resolver (condición D7, heredada del handoff 7.1).
