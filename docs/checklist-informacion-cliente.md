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
| **A2** | **Número para la API de WhatsApp — modo coexistencia (decisión Henry 15-ago).** Puede ser el número que ya usan (¿el `+51 986 199 020` del form u otro?): la conexión coexistente mantiene el WhatsApp Business del teléfono funcionando y las conversaciones se revisan tanto en el CRM como en la app. Solo falta que confirmen cuál número se conecta. *(Nota técnica interna: verificar en la subcuenta los límites de coexistencia — los grupos siguen sin ser administrables por API, y el historial/funciones varían. Lo del posible número italiano lo evaluamos nosotros primero — `P-02`; no prometerlo.)* | Bloquea todo el canal automatizado: plantillas, recordatorios, confirmaciones. |
| **A3** | **Dominio y DNS:** acceso al panel donde vive `lanuovacoscienza.com` (o el dominio que prefieran). Confirmar si quieren subdominio tipo `eventos.lanuovacoscienza.com`. | Bloquea publicación de páginas y verificación del dominio de envío de email. |
| **A4** | **Cobros:** (1) **¿Cómo paga hoy un alumno peruano en la práctica?** (¿Yape? ¿Plin? ¿transferencia BCP/Interbank? ¿tarjeta?) (2) **Datos exactos de pago manual** para las plantillas de cierre: IBAN para Italia, cuenta/CCI/QR Yape para Perú. *(Stripe se pospone — decisión Henry 15-ago: se conecta después directamente en GHL con el cliente; al hacerlo siguen vigentes las preguntas de país/titular de la cuenta y la restricción de moneda única (D10) — proponemos USD.)* | Sin (1) y (2), el primer cierre en Perú se improvisa por WhatsApp. La conexión de Stripe pasa a tarea de build, no de checklist. |
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

## D · Mensaje enviado al grupo (versión final acordada con Henry, 15-ago)

> Ajustes de Henry sobre el borrador: WhatsApp va en **modo coexistencia** (no hace falta número sin WhatsApp; se revisa en CRM y en la app) · Stripe se omite por ahora (se conecta directo en GHL después) · se quitaron del mensaje: videos (A7), validación IT de Luca (B4), legales (B7), Zoom (B9) y full day (C4) — **siguen vigentes en las secciones A/B/C de este checklist para pedirlos cuando toquen**.

> Hola Luca, Christie, Joaquín 👋 ¡Buenas!
>
> Antes que nada, gracias por llenar el formulario 🙏 — con los logos, precios y datos del negocio ya arrancamos la construcción del sistema. Para avanzar sin frenos y llegar al lanzamiento de agosto, les dejamos la lista de lo que necesitamos de su lado, en orden de urgencia 👇
>
> *🔴 URGENTE — lo ideal es tenerlo en 48 h:*
>
> *1️⃣ Meta (Facebook):* Joaquín, ¿pudiste recuperar el administrador del portafolio? Si no se puede, les proponemos crear uno nuevo a nombre de Nueva Conciencia Formación SAC — no pierden nada y desbloquea el píxel Y el WhatsApp automatizado de una vez. Si vamos por el nuevo, vayan juntando en paralelo: ficha RUC de la SAC, el correo del dominio activo y un teléfono verificable (Meta los pide para verificar el negocio).
> *2️⃣ Número de WhatsApp para el sistema:* ¿conectamos el +51 986 199 020 que pusieron en el form, u otro? La conexión es en modo *coexistencia*: el WhatsApp Business del teléfono sigue funcionando normal, y las conversaciones las van a poder revisar tanto en el CRM como en la app de WhatsApp Business. Solo confírmennos cuál número usamos 📲
> *3️⃣ Dominio:* acceso al panel donde compraron `lanuovacoscienza.com` para conectar las páginas y el correo.
> *4️⃣ Cobros:* ¿cómo les paga hoy en la práctica un alumno peruano (Yape, Plin, transferencia, tarjeta)? Pásennos los datos exactos de cobro de cada mercado (IBAN de Italia, cuenta/QR de Perú) para dejarlos cargados en el sistema 💳
> *5️⃣ El primer lanzamiento:* ¿arrancamos con Perú, con Italia o con ambos? Fecha del primer jueves, si va semanal o cada 2 semanas, horarios por mercado, y si ese jueves ya se vende (masterclass) o solo se educa (webinar). Y mientras no haya full day en Lima: ¿el cierre en Perú es por llamada de 30 min con Luca?
> *6️⃣ Precios que faltan:* la escuela en 2 y 3 cuotas (¿y a Italia también $1.000?), 21 Días, Dispersión del Dolor y Reflexología.
>
> *🟡 ESTA SEMANA:*
>
> *7️⃣* Links de invitación de los grupos de WhatsApp del lanzamiento (español e italiano).
> *8️⃣* Canal de YouTube: quién sube el video y coordinar que sea *no listado* (si se transmite en abierto perdemos la medición de asistencia y la urgencia).
> *9️⃣* Joaquín: el guion/promesa de los anuncios + el funnel anterior que no convirtió + VSL si existe (para que la página diga lo mismo que el anuncio).
> *🔟* Disponibilidad real de Luca para las llamadas de cierre: franjas concretas por mercado, descanso entre llamadas y máximo por día.
> *1️⃣1️⃣* Sus 10-20 mejores testimonios escritos con permiso de uso (y si alguno se anima a video, oro puro ✨).
> *1️⃣2️⃣* Logos en fondo transparente o el archivo original (AI/SVG) — los que llegaron traen el fondo negro pegado.
> *1️⃣3️⃣* El video o contenido educativo gratuito para quien aún no califica + los links de compra actuales del 21 Días y Reflexología.
>
> *🟢 SIN APURO (pero mejor ya):*
>
> *1️⃣4️⃣* API key de System.io + export de contactos y compradores (nos sirve para rescatar su base histórica 💰).
> *1️⃣5️⃣* Export de compradores de Hotmart.
> *1️⃣6️⃣* El contenido de la aplicación de síntomas que ofreció Luca (será el cerebro del asistente en la Fase 2).
>
> Cualquier punto que no sepan cómo resolver, nos dicen y lo vemos juntos en una llamada corta 📞 Lo urgente es del 1 al 6 — con eso nada nos detiene. ¡Vamos con todo! 💪🚀

---

## Interno (no va al cliente)

- `P-08` ✅ resuelto (15-ago): cobrado el **50% de F1**; F2 en horizonte, sin facturar. Plan de F2 en §15 del mapa: se estructura con la opción 2 de fábrica ANTES de cobrarla y se cierra contra el éxito del primer lanzamiento. Tareas ClickUp: 2.º 50% de F1 contra entrega (condición Meta) + propuesta F2 estructurada.
- La sección C sigue siendo "pedir ya": con F2 en horizonte, la PoC de System.io y el contenido de la app de síntomas son los que desriesgan (y ayudan a vender) esa fase.
- Costos de plataforma/consumos: si el cliente pregunta, **remitir a Jaime** (acuerdo interno 6-ago). **Pasarle a Jaime el ancla que el cliente ya escuchó: $97 licencia + $10 WhatsApp (K8)** — si cotiza por encima, la promesa la hicimos nosotros.
- Avisar a Jaime por el grupo compartido: form recibido, mapa v3 listo, checklist enviado.
- **Pruebas de plataforma del día 1 (antes de prometer nada más):** disqualify de survey dispara trigger (§7) · anclaje temporal de WF3 (§10) · ¿LC WhatsApp soporta 2º número? (`P-02`) · corte a N ciclos en suscripciones (§12).
- El 2.º 50% **no se factura** con el bloqueo Meta sin resolver (condición D7, heredada del handoff 7.1).
