# Mapa de Implementación v3 — Escuela de Sanación Biológica

**Marca:** Salud Consciente (ES) / dominio `lanuovacoscienza.com` · **Escuela:** NCA Academy · **Empresa fiscal:** Nueva Conciencia Formación SAC
**Subcuenta:** creada, en la agencia GHL de Jaime · **Estado:** Fase 1 en ejecución con ~5 días de retraso · **Compromiso:** el sistema debe soportar un lanzamiento en agosto (K5)
**Fuentes:** handoff (`fuentes/00-handoff.md`) + deltas de las tres llamadas (`fuentes/01-deltas-llamadas.md`) + form de onboarding (`fuentes/02-form-onboarding.md`).
**Regla:** donde este mapa contradiga al handoff, manda este mapa. Los puntos abiertos están numerados `P-01…P-14` (§18) para iterar. Los compromisos con el cliente se citan como `K1…K9` (deltas §2).

---

## 0 · Actores y responsabilidades

| Quién | Rol |
|---|---|
| Henry | Responsable del proyecto, relación con el cliente |
| Oliver | Implementación en GHL |
| Germán | Estrategia y configuración |
| **Jaime** | Dueño de la cuenta madre GHL. **Toda conversación de costos de plataforma/consumos con el cliente pasa por él, no por nosotros.** Pasarle el ancla que ya escuchó el cliente: $97 licencia + $10 WhatsApp (K8) |
| Luca | Closer, contenido, validación del italiano (encuesta, plantillas, emails y páginas — con horas reservadas, ver B4). Su WhatsApp Business actual y sus grupos quedan intactos |
| Christie | Masterclass, entrega, sesión bono 40 min |
| Joaquín | Contraparte técnica del cliente: ads, creativos, VSLs, píxel del lado Meta. Receptor principal de la capacitación de tracking |

---

## 1 · Decisiones de arquitectura v3

| # | Decisión | Estado |
|---|---|---|
| D1 | **Híbrido System.io**: los cursos se quedan; GHL es la fuente única de datos/marketing/cobro. Sync bidireccional por API en F2, con **PoC temprana de la API** antes de comprometer AP01. | Cerrada (handoff 3.1) |
| D2 | **WhatsApp en modo coexistencia** (actualizada 15-ago, decisión Henry): el número puede ser el que ya usan — la conexión coexistente mantiene el WhatsApp Business del teléfono funcionando y las conversaciones se ven en CRM y en la app. Los grupos siguen siendo manuales (la API no los administra, con o sin coexistencia); el dato se captura por formulario, no en conversación. ⚠️ Verificar en la subcuenta los límites reales de coexistencia, y LC WhatsApp históricamente soporta **un solo número por subcuenta** — no prometer un segundo número sin verificar (`P-02`). | Actualizada 15-ago · pendiente `P-02` |
| D3 | **Una subcuenta, dos mercados**: campos `idioma`/`mercado`; réplica por idioma. En F1, **un solo pipeline** con campo `mercado` (mínimo viable 6.2), no dos. Consecuencia dura: **una subcuenta = una moneda de cobro** (ver D10). | Cerrada · revisar en F2 (`P-04`) |
| D4 | **Idiomas por réplica, no por "switch"**: páginas separadas `-es` / `-it` enlazadas con selector visible. El "plugin que cambia el idioma" prometido en el cierre no existe nativo en GHL — la réplica cumple la promesa funcional. **Inglés = Fase 3**: prometido de palabra, sin cotizar, no se construye ahora; nomenclatura preparada (`-en`). **El copy en italiano lo produce Luca (traduce con IA, como su contenido — T7); nosotros maquetamos y él valida** (`P-13`). | Cerrada (interna) · `P-07` `P-13` |
| D5 | **Infraestructura y facturación**: subcuenta en la agencia de Jaime; sin rebilling automático (Jaime sin Stripe) → consumos refacturados manualmente por Jaime. **Build 100% replicable por snapshot: todo link/número/precio/dato del cliente en custom values, cero hardcode.** | Cerrada (llamada interna) |
| D6 | **Primer lanzamiento sin IA**: encuesta de registro con preguntas eliminatorias sustituye a IA01. Quien no califica no entra al grupo; se le educa con contenido/low ticket. IA bilingüe en F2. | Cerrada (llamada cierre, T1) |
| D7 | **Cobro del proyecto por invoice** (links fastpaydirect descartados). Cliente fiscal: Nueva Conciencia Formación SAC. **Estado real: cobrado el 50% de Fase 1 ($1.050). El 2.º 50% de F1 va contra la entrega** (tarea en ClickUp atada al hito) **y no se factura con el bloqueo Meta sin resolver** (handoff 7.1; resuelto = admin recuperado o portafolio nuevo operativo). **F2 está en el horizonte pero NO facturada** — se cobra su 50% al confirmarla (ver §15). | Cerrada (K1) · P-08 resuelto |
| D8 | **Ruta de pago manual (transferencia)**: en Italia hay compradores que transfieren a Luca y él matricula a mano. F1: tag `pago-manual` + SOP que dispara las mismas acciones post-venta; F2: rama formal en SP07/AP01. **El form lo confirma: el cliente declara "transferencia bancaria (IBAN)" como SU método principal.** Y en Perú es probable que casi todo pago real entre por Yape/Plin/transferencia local (ver D10) — esta ruta es de primera clase, no un caso borde. | Nueva (llamada mapeo, delta 1 + form) |
| D9 | **Stripe SÍ entra en F1** con los tres planes del high ticket. Resuelve la contradicción de la llamada de cierre (T3): sin cobro conectado, el lanzamiento de agosto no sirve. Coincide con handoff 6.2. | Resuelta v3 |
| D10 | **Realidad de cobro (restricciones de plataforma, no preferencias):** (a) GHL maneja **una moneda por subcuenta** — hay que elegir UNA para todo lo que cobre GHL (recomendado: **USD**, coincide con el form). Si Italia exige EUR: payment links creados directo en Stripe + captura vía Inbound Webhook (el trigger nativo de pago no los ve), o segunda vía en F2. (b) **Stripe no da cuentas a comercios domiciliados en Perú** — la cuenta será la italiana/personal de Luca (coherente con el IBAN del form): confirmar país y titular en A4. (c) Alumnos peruanos pagan típicamente Yape/Plin/transferencia → **el mercado Perú puede caer casi al 100% por la ruta `pago-manual`**; los datos de cobro reales van en custom values (`datos_pago_pe` / `datos_pago_it`). | Nueva v3 (verificación técnica) |

---

## 2 · Objetivo de la Fase 1

> **"Desde el primer jueves, ninguna persona se pierde."**
> Todo lead queda capturado, atribuido y calificado; los calificados llegan al grupo y al evento con recordatorios; los interesados postulan y agendan solos; el pago queda registrado y medido. Luca solo aparece en la llamada de cierre.

Lo que **no** hace la F1 (y se dice así al cliente para no generar expectativa): responder conversaciones con IA, dar de alta en System.io automáticamente, cobrar/perseguir cuotas, ventana de cierre vie-sáb automatizada, nurturing largo, escalera de low tickets, dashboards. **Tampoco incluye:** gestión de ads (posible F3 — T6), producción de videos/creativos (los produce el cliente; nosotros damos estructura y feedback acotado — K7, ver §14), ni redacción de textos legales (los provee el cliente — B7).

---

## 3 · Cuenta base (F1)

- Dominio para funnels: candidato `lanuovacoscienza.com` (o subdominio `eventos.`) → **falta acceso DNS (checklist A3)**. ⚠️ El dominio es la marca italiana; qué marca va por mercado es `P-11`
- Dominio de envío de email dedicado + verificación DNS · remitente candidato: `info@lanuovacoscienza.com`
- Branding de subcuenta: **logos recibidos** (`assets/brand/`, oro sobre negro, vertical + horizontal). Vienen con fondo negro incrustado → páginas en tema oscuro, o pedir transparente/vector (checklist B8)
- Zona horaria base **America/Lima** (los calendarios manejan Roma con conversión — ver §9)
- Usuarios: Luca, Christie, Joaquín (+ equipo Profit). Roles: cliente sin permisos de configuración
- Integración nativa **Stripe** (cuenta del cliente — país/titular por confirmar, A4; moneda única D10)
- **LC WhatsApp** en la subcuenta, **en modo coexistencia (D2)**: puede ser el número actual — la app del teléfono sigue funcionando y las conversaciones se ven en CRM y en la app. Falta que el cliente confirme cuál número se conecta (¿el `+51 986 199 020` del form u otro?) — checklist A2. Costos y mensualidad se hablan con Jaime, no con nosotros
- Píxel de Meta a nivel funnel (solo PageView/ViewContent) + eventos de conversión por CAPI desde workflows (§13) · **banner de consentimiento de cookies para tráfico UE** (§13)

### 3b · Precios conocidos (form de onboarding)

| Producto | Precio | Falta |
|---|---|---|
| Escuela **NCA Academy** | $1.000 contado (coincide con "oferta de cierre") | montos 2 y 3 cuotas · qué se le cobra a Italia bajo moneda única (D10) |
| Videocurso 5 Leyes | $100 | precio IT |
| Libro "La Nueva Consciencia" | S/ 80 (**soles** — no cobrable por la subcuenta en USD; se queda en su canal actual) | |
| Sesiones 1-a-1 | $70 · pack 3 $180 · pack 6 $299 | fuera del alcance del estimado → `P-12` |
| 21 días · Dispersión del dolor · Reflexología | **sin precio** | checklist A6 (bloquea escalera F2, no F1) |

## 4 · Campos personalizados (subset F1)

Se crean en F1 los que los flujos F1 escriben o leen; el resto se crea en F2 para no ensuciar.

| Grupo | Campos F1 |
|---|---|
| Atribución | `idioma` · `mercado` · `pais` · `fuente_contacto` · `utm_campaign` · `utm_adset` · `utm_ad` |
| Calificación | `cluster_sintoma` · `sintoma_declarado` · `tiempo_con_sintoma` · `nivel_calificacion` · `motivo_descalificacion` |
| Evento | `lanzamiento` · `fecha_evento` · `asistio_evento` |
| Venta | `producto_comprado` · `plan_pago` · `estado_pago` · `bono_llamada_christie` |

Quedan para F2: `estado_ia`, `intentos_previos`, `modalidad_evento` (depende de `P-10` y ningún flujo F1 lo usa aún), `vio_replay`, `cuota_actual`, `cohorte`, `alta_systemio`.

## 5 · Custom values (replicabilidad — D5)

Todo lo que cambia entre lanzamientos o entre clientes va aquí, nunca escrito a mano en workflows/plantillas/páginas:

`nombre_lanzamiento_vigente` · `fecha_evento_vigente` · `hora_evento_pe` · `hora_evento_it` · `link_grupo_whatsapp_es` · `link_grupo_whatsapp_it` · `link_registro_es` · `link_registro_it` · `link_evento_es` · `link_evento_it` · `link_youtube_evento` (se actualiza por lanzamiento) · `link_calendario_cierre_pe` · `link_calendario_cierre_it` · `link_pago_contado` · `link_pago_2cuotas` · `link_pago_3cuotas` · `datos_pago_pe` (Yape/Plin/CCI — D10) · `datos_pago_it` (IBAN) · `link_zoom_llamada` · `link_educativo_es` · `link_educativo_it` · `email_remitente` · `firma_luca`

**SOP "cambiar de lanzamiento"** = actualizar **5 custom values** (nombre, fecha, hora PE, hora IT, link YouTube) **+ lo que exija el anclaje de recordatorios de WF3** (ver §10 — según lo que soporte la subcuenta, puede sumar editar 3 tiempos de espera).

## 6 · Pipeline (F1 — único)

**Lanzamiento** — etapas:
`Lead nuevo → Calificado → Registrado → Asistió → Postuló → Llamada agendada → Llamada realizada → Ganado / Perdido / No califica`

- El campo `mercado` separa las vistas (smart lists / filtros por mercado en lugar de dos pipelines).
- Nota: el cierre difiere entre mercados (IT: masterclass + llamada · PE: full day presencial con venta en sala). Mientras el full day de Lima no tenga fecha (bloqueante 7.5), **el cierre de Perú en F1 es por llamada de 30 min con Luca** — confirmarlo con el cliente (checklist A5, `P-14`). Revisar división de pipelines en F2 (`P-04`).

## 7 · Formularios y encuestas (F1)

### F01 / F02 — Registro al evento (ES / IT) — *el punto de captura del negocio*
Implementar como **encuesta GHL (survey)** con lógica de salto — con dos salvaguardas obligatorias:

> ⚠️ **Prueba del día 1 (bloqueante):** descalificarse en Q3 con un contacto real y verificar (i) que el contacto queda creado con las respuestas guardadas y (ii) que el trigger de encuesta enviada dispara. Si cualquiera falla, **el fallback pasa a ser el plan A**: encuesta sin disqualify (todos llegan al final, redirect único a página neutra) y WF2 rutea — el link del grupo solo les llega 1:1 a los calificados.

- **Datos:** nombre · WhatsApp · email · país
- **Consentimientos (obligatorios — RGPD Art. 9, la encuesta captura datos de salud de consumidores UE):** ☑ acepto la política de privacidad (redacción que cubra datos de salud) · ☑ acepto recibir comunicaciones por WhatsApp y email (opt-in que Meta exige documentar)
- **Campos ocultos:** `utm_campaign` / `utm_adset` / `utm_ad` (de la URL) · `fuente_contacto` · `idioma` · `lanzamiento`
- **Q1 — síntoma** *(segmenta, no descalifica)*: "¿Cuál de estos describe mejor lo que vives hoy?" → Dolores articulares o musculares / Digestivo (gastritis, reflujo, colon irritable) / Ansiedad, pánico o depresión / Piel (dermatitis, psoriasis) / Otro → `cluster_sintoma`
- **Q1b — texto corto opcional**: "Cuéntanos en una frase qué vives" → `sintoma_declarado` (pregunta aparte: el "Otro" inline de Q1 no escribe en un segundo campo)
- **Q2 — tiempo** *(segmenta)*: "¿Hace cuánto buscas solución?" → Menos de 6 meses / 6 meses a 2 años / Más de 2 años / Más de 5 años → `tiempo_con_sintoma`
- **Q3 — expectativa** *(la eliminatoria)*: "¿Qué esperas encontrar en esta clase?" →
  a) Entender la causa emocional de mi síntoma y cómo abordarla → **Califica**
  b) Un medicamento o tratamiento médico para mi enfermedad → **No califica** (`motivo_descalificacion` = Busca pastillas o medicina)
  c) Solo curiosidad, quiero mirar → **A educar** (`motivo_descalificacion` = Curiosidad)
- **Q4 (opcional, `P-03`)** — filtro de inversión suave: "Si esta clase te muestra un camino claro, ¿estarías dispuesto/a a invertir en tu proceso?" → Sí / Necesitaría saber más / No, busco solo contenido gratuito (última → A educar)

**Salidas:** Califica → `/gracias` (grupo + instrucciones) · No califica / A educar → `/comienza-aqui` (educativa, sin link de grupo).
La redacción exacta la valida Luca (tono y lenguaje de "conflicto emocional") — checklist B4.

### F03 — Postulación a la escuela (post-evento)
Corta: confirma interés real + mejor franja horaria + reconfirma WhatsApp. **Vive en la página `/postulacion` (§8)**; su envío es el disparador real de la agenda en WF4. Réplica IT.

### E01 — Resultado de llamada
**Pasa a F2** (SP06). En F1, Luca mueve la etapa a mano tras cada llamada — SOP de 30 segundos.

## 8 · Funnels y páginas (F1 · cada una en ES + réplica IT — 5 páginas por idioma)

| Página | Contenido / función |
|---|---|
| `/registro-{es,it}` | Promesa coherente con el anuncio (guion de Joaquín — checklist B3), VSL corto si existe, encuesta embebida. UTMs pasan a campos ocultos. Banner de consentimiento (UE). |
| `/gracias-{es,it}` | Confirmación + botón al grupo de WhatsApp + qué va a pasar (clases diarias, evento del jueves) + add-to-calendar. |
| `/evento-{es,it}` | **Página propia del evento**: YouTube **no listado** embebido, contador, botón "Quiero postular a la escuela" → lleva a `/postulacion`, aviso de caducidad. Noindex, acceso solo por link. Razón de ser: transmitir en YouTube abierto mata asistencia, CTA y urgencia (riesgo 2). |
| `/postulacion-{es,it}` | Aloja F03. El envío dispara WF4 (etapa *Postuló* + agenda). Sin esta página el paso central de F1 no tiene dónde ocurrir. |
| `/comienza-aqui-{es,it}` | Destino del no-califica/a-educar: video educativo gratuito + CTA al low ticket **existente** (checkout actual de System.io/Hotmart — en F1 NO se construyen funnels de low ticket). `P-05` · contenido y links: checklist B10 |

**Medición de asistencia (honesta y con letra chica):** los trigger links solo atribuyen el clic cuando GHL los envía **1:1** (URL única por contacto en la plantilla `en-vivo` y el email espejo). El link pegado **en el grupo es la misma URL para todos y no marca a nadie** → el mensaje del grupo debe decir "entra por el link que te llegó a tu WhatsApp", y el % de asistencia se lee como métrica de canal individual, no total. No existe trigger de "clic en botón de página": la señal fuerte de interés es el envío de F03.

## 9 · Calendarios (F1)

| Calendario | Config |
|---|---|
| Llamada de cierre — Italia | franjas de Luca **convertidas a hora Lima** (la disponibilidad se define contra la TZ de la subcuenta) · 30 min · solo por link post-postulación |
| Llamada de cierre — Perú | America/Lima · 30 min · ídem |

- Widget de booking con **selector de zona horaria activado** (el lead italiano ve su hora local).
- Plantillas de confirmación/recordatorio de cita: usar merge fields que rendericen **en la zona del contacto** — si no, al italiano le llega "11:30" cuando su cita es 18:30.
- ⚠️ **Cambio de hora europeo** (Italia tiene DST, Perú no): el offset cambia en marzo y octubre — auditoría del calendario IT en cada cambio (entra al SOP; el próximo cae en octubre 2026, en plena operación).
- Disponibilidad real de Luca pendiente (checklist B5). Sesión bono de Christie: manual en F1; calendario propio en F2.

## 10 · Workflows (F1 — 5 consolidados)

> Nomenclatura física: `WF1 — Captación y atribución`, etc. WF1–WF4 = los 4 del mínimo viable del handoff 6.2; **WF5 se añade en virtud de D8/D9** (cobro en F1).

### WF1 · Captación y atribución *(LS01 + LS02 + LS04)*
- **Triggers:** contacto creado · mensaje WhatsApp entrante de número sin contacto · clic en trigger links de orgánico (bio IG/TikTok, Telegram).
- **Acciones:** volcar UTMs → campos; fijar `fuente_contacto`; fijar `idioma`/`mercado` (por formulario de origen, por página, o por prefijo +39→IT / +51→PE; ambiguo → preguntar); estampar `lanzamiento`; oportunidad en *Lead nuevo*.
- Entrada por WhatsApp sin registro: **respuesta automática única** con el link de registro + notificación a Luca solo si el contacto responde algo que no es registro. *(El mensaje entrante abre la ventana de 24 h → estas respuestas NO necesitan plantilla aprobada.)*

### WF2 · Registro y calificación *(LS03 + SP01 + eliminatoria D6)*
- **Trigger:** envío de F01/F02 (o final de encuesta en modo fallback — §7).
- **Acciones:** escribir calificación;
  - **Califica** → etapa *Registrado* · WhatsApp de bienvenida con link del grupo (plantilla 1) · email de confirmación · CAPI **Registro**.
  - **No califica / A educar** → etapa *No califica* (o tag `a-educar`) · **plantilla `educativo-no-califica`** (el trigger es un formulario: no hay ventana de 24 h abierta — sin plantilla aprobada esta rama muere en silencio) + email educativo · tag para remarketing. Sin link de grupo.

### WF3 · Recordatorios de evento *(SP02)*
- Para oportunidades en *Registrado*: **T-24 h** (WhatsApp + email) · **T-3 h** (WhatsApp) · **T-15 min** "estamos en vivo" (WhatsApp con trigger link 1:1 a `/evento` + email espejo).
- ⚠️ **Anclaje temporal — decidir el día 1 probando en la subcuenta:** los campos de fecha no guardan hora, así que "programado sobre `fecha_evento_vigente`" no se sostiene solo. Opciones: **(a)** tiempos de espera fijados dentro de WF3 y editados en cada lanzamiento (+1 paso al SOP — plan por defecto, cero riesgo) · **(b)** si la versión de Wait de la subcuenta soporta fecha/hora desde campo o cita, anclar ahí y el SOP se queda en 5 custom values · **(c)** n8n con cron leyendo custom values (último recurso).
- Las clases diarias de falso-en-vivo se anuncian **en el grupo, manualmente** (Joaquín/Luca) — los grupos no son administrables por API.

### WF4 · Asistencia, postulación y agenda *(SP03 + SP04 + SP05)*
- Clic en el trigger link 1:1 del evento → `asistio_evento` ✓ · etapa *Asistió* · CAPI **Asistencia**.
- **Envío de F03** (desde `/postulacion`) → etapa *Postuló* · CAPI **Postulación** · WhatsApp con `link_calendario_cierre_{mercado}` (plantilla 6).
- Cita creada → etapa *Llamada agendada* · confirmación · recordatorios T-24 h y T-1 h (con `link_zoom_llamada` + instrucciones de instalar Zoom — dolor conocido).
- **No-show mínimo:** registrado que **ni clicó el link ni respondió nada** → T+2 h mensaje de recuperación (copy suave: el clic es proxy — puede haber asistido por el link del grupo). Ventana de cierre completa vie-sáb (SP08) es F2.

### WF5 · Cobro confirmado *(SP07-lite)*
- **Trigger:** pago recibido **procesado por GHL** (links/invoices creados en GHL — los checkouts de System.io con el mismo Stripe NO disparan nada hasta el webhook de F2).
- **Filtro de entrada:** solo el **primer** pago (condición `estado_pago` vacío / sin tag `primer-pago-procesado`) — sin esto, cada cuota re-dispara etapa *Ganado* y duplica el CAPI **Purchase** hacia Meta.
- **Acciones:** etapa *Ganado* · `producto_comprado`/`plan_pago`/`estado_pago` · tag `primer-pago-procesado` · notificación a Luca con SOP de **alta manual en System.io** (AP01 en F2) · si contado → `bono_llamada_christie` ✓ + notificación a Christie · CAPI **Compra**.
- **Rama pago manual (D8/D10):** Luca aplica tag `pago-manual` → mismas acciones sin evento Stripe. **En Perú esta rama puede ser la principal** (Yape/Plin — confirmar en A4).

## 11 · Plantillas de WhatsApp (F1)

Cada una en **ES + IT** — **11 plantillas × 2 idiomas = 22 aprobaciones de Meta** (camino crítico):

1. `bienvenida-registro` (link grupo) · 2. `recordatorio-24h` · 3. `recordatorio-3h` · 4. `en-vivo` (trigger link evento) · 5. `no-show` · 6. `postulacion-agenda` (link calendario) · 7. `confirmacion-cita` · 8. `recordatorio-cita-24h` · 9. `recordatorio-cita-1h` (Zoom + cómo entrar) · 10. `respuesta-entrada-desconocido` (link registro) · 11. `educativo-no-califica`

- **Día 1 se envían a aprobación las 11 en ES.** Las 11 en IT salen en cuanto Luca valide el texto (checklist B4, fecha límite día 3) — no bloquean el arranque si el primer ciclo es solo Perú (`P-14`).
- Redactar en formato **utility puro** (referencia a la inscripción existente, sin lenguaje promocional): Meta recategoriza a marketing los recordatorios con tono promo → más costo y riesgo de pausa por quality rating. En nicho salud, ni una promesa de "curación" en plantillas.
- ⚠️ **Límite de mensajería del número nuevo:** sin verificación de negocio ~250 conversaciones iniciadas/24 h; verificado arranca en ~1.000/día. Un jueves con cientos de registrados puede topar el techo → lanzar la verificación del Business Manager el día 1 (junto con A1), revisar el tier antes del primer envío masivo, escalonar envíos si hace falta, y **el email de WF2/WF3 es el canal espejo declarado**.

### 11b · Emails (F1)

Mismo régimen que las plantillas (ES + IT, valida Luca — B4): 1. confirmación-registro · 2. recordatorio-24h · 3. en-vivo (espejo del T-15) · 4. no-show · 5. confirmación-cita · 6. recordatorio-cita-24h · 7. educativo-no-califica. **7 × 2 idiomas = 14 emails.**

## 12 · Cobros (F1)

- **Moneda única de la subcuenta: decidir antes de crear productos (D10)** — recomendado USD. El precio a Italia bajo esa moneda se confirma en A6.
- Producto **Escuela**: contado · 2 cuotas · 3 cuotas — vía **invoice con calendario de pagos y tarjeta guardada obligatoria en el primer cobro** (sin tarjeta guardada, las cuotas 2-3 son solo recordatorios y se vuelve a la persecución manual). Esto entra al guion de cierre de Luca: *"el plan en cuotas requiere tarjeta"*. No usar payment link de suscripción para cuotas salvo verificar en la subcuenta que el corte a N ciclos funciona.
- Flujo: Luca cierra en la llamada → envía `link_pago_X` o `datos_pago_{mercado}` (custom values) → WF5 (o tag `pago-manual`) hace el resto.
- **Compradores por transferencia/Yape/Plin:** sus cuotas son **tareas + plantilla de recordatorio de cobro**, no automatización de mora — no prometer AP04 sobre pagos sin tarjeta.
- Reintentos y mora automatizados = F2 (AP04), y solo aplican a la minoría con tarjeta guardada.

## 13 · Píxel + CAPI (F1)

| Evento | Canal | Se dispara en |
|---|---|---|
| PageView / ViewContent | Píxel (navegador) | páginas del funnel |
| Registro | **CAPI server-side (solo workflows)** | WF2, al calificar |
| Asistencia | CAPI server-side | WF4 (verificar si la acción acepta nombre custom; si no, mapear a evento estándar tipo Schedule/ViewContent) |
| Postulación | CAPI server-side | WF4 |
| Compra (Purchase) | CAPI server-side | WF5 (solo primer pago — filtro §10) |

- **Reparto exclusivo de canales** (píxel = solo vistas; conversiones = solo server-side): la acción CAPI de workflows no coordina `event_id` con el píxel del navegador — si ambos disparan el mismo evento, Meta lo cuenta doble y Joaquín optimiza sobre datos inflados. Dejar el mapeo por escrito para Joaquín antes de que monte campañas.
- **Banner de consentimiento de cookies** en los funnels con disparo condicionado del píxel para tráfico UE (el Garante italiano sanciona esto).
- **Bloqueado por el admin del portafolio Meta — bloqueo doble** (píxel/CAPI y alta de WhatsApp API). **Recomendación:** si en 48 h no se recupera el admin, crear **portafolio nuevo a nombre de Nueva Conciencia Formación SAC**. Costo de histórico: casi nulo (nunca hubo píxel en PE; el de IT no tiene CAPI). La **verificación de negocio** del portafolio nuevo necesita documentos (ficha RUC/constitución, email del dominio, teléfono verificable — checklist A1) y tiene tiempo propio: días, no horas.

## 14 · Capacitación, SOPs y asesoría (F1)

**1 sesión (~2 h, grabada) + SOPs escritos (K3):**
leer el pipeline y las vistas por mercado · qué hace cada WF · SOP llamada de cierre (mover etapa + enviar cobro; cuotas = con tarjeta) · SOP pago manual (tag `pago-manual`) · SOP alta en System.io · SOP cambiar de lanzamiento (§5) · SOP ventana de 24 h vs plantillas · auditoría del calendario IT en cambios de hora europeos (§9) · qué NO tocar · **cláusula K9 por escrito: cambios futuros de embudo = re-mapeo y cotización aparte, no reconstrucción gratis** (va también en el acta de entrega).

**SOP "día de evento" + guardia (nuevo):** el primer jueves es el momento de mayor exposición del proyecto y necesita run-of-show: T-24 h verificar plantillas aprobadas + prueba E2E del trigger link · T-2 h video subido como **no listado** y `link_youtube_evento` actualizado · T-30 min prueba real del link (un custom value viejo manda a toda la audiencia a un link muerto a T-15) · durante el evento, un responsable de Profit **de guardia** (primer y segundo lanzamiento) vigilando conversaciones y errores.

**Asesoría de copy/VSL (K7 — acotada):** estructura + hasta 2 rondas de feedback por pieza sobre los videos/creativos que produce el cliente. No es producción; el material de B3 alimenta esta asesoría.

## 15 · Fase 2 — alcance comprometido + re-escopeo

**Comprometido en el estimado (handoff 6.3):** IA bilingüe con escalada · System.io API (AP01 alta automática + sync inverso) · entrega de bonos (árbol anidado — delta 7) · recordatorios de encuentros · cuotas con reintentos, mora y retiro de acceso (AP04 — solo pagos con tarjeta, ver §12) · ventana de cierre vie-sáb (SP08) · escalera 5 low tickets con páginas · upsell/carrito abandonado · base histórica (~1.000 contactos IT — LS05) · campañas a base propia · testimonios automáticos (solo escritos — T4; pedir video como objetivo) · 2 capacitaciones **+ SOPs escritos de F2 (K3: son "por fase" — contabilizarlos en las horas del re-escopeo)**.

**Nuevo en F2 por deltas:** rama formal de pago por transferencia en SP07/AP01 (D8) · calendario propio de Christie · PoC System.io API **adelantada a F1** (1-2 h, desriesga AP01).
**Ya previsto en el handoff, consolidado aquí:** E01/SP06 · webhook Hotmart · página de replay con caducidad.

**Re-escopeo (handoff 6.1) — `P-08` RESUELTO: se cobró solo el 50% de F1; F2 en horizonte, sin facturar.**
Consecuencia: la ventana para estructurar F2 **antes de cobrarla** está abierta — no hay nada que renegociar porque nada de F2 se ha cobrado. Plan:
- **La propuesta/confirmación de F2 se presenta con la opción 2 integrada de fábrica como EL plan de trabajo** (no como recorte): 1 plantilla de página de venta + 4 réplicas de copy, y automatización completa (upsell/carrito abandonado) solo para 2 productos — **21 días** (el que más rota) y **reflexología** (el más caro, hoy sin base). Los otros 3, página + order form simple. Así F2 cabe en $1.950 (~40-45 h) sin tocar lo prometido en el estimado.
- Si el cliente pide la escalera completa página-por-página con automatización total de los 5, esa diferencia se cotiza como **F3/adicional** (junto con inglés y gestión de ads, que ya viven ahí).
- **Momento de cierre de F2:** contra el éxito del primer lanzamiento — es el mejor argumento comercial y evita vender F2 con F1 aún sin entregar.
- La opción 1 del handoff (sacar la escalera entera a F3) queda como plan B solo si Henry decide abrir esa conversación.

## 16 · Orden de construcción (recuperar los 5 días)

**Hoy (día 0):** enviar checklist al cliente (secciones A completas, con fecha límite 48 h) · avisar a Jaime por el grupo (avances + ancla $97/K8).

| Día | Track |
|---|---|
| 1 | Cuenta base · campos · custom values · pipeline · **pruebas de plataforma en la subcuenta real: disqualify de survey (§7), anclaje temporal de WF3 (§10), multi-número LC WhatsApp (P-02), corte a N ciclos (§12)** · redactar 11 plantillas ES + 7 emails ES y **enviar plantillas ES a aprobación** · iniciar alta WhatsApp API + verificación de negocio (si hay número + Meta) · PoC System.io API (si llega la key) |
| 2–3 | Funnels ES completos (**5 páginas** + encuesta con lógica + banner de consentimiento) · productos de cobro (moneda única decidida) |
| 3–4 | WF1–WF5 · pruebas E2E (registro→grupo→evento→postulación→cita→pago test, y la rama no-califica) · **fecha límite validación IT de Luca (B4)** |
| 4–5 | Réplica IT (5 páginas + 11 plantillas + 7 emails — si el primer ciclo incluye Italia, `P-14`) · píxel + CAPI (si hay acceso Meta) · QA · agendar capacitación · SOP día de evento listo |

**Dependencias externas duras:** número WhatsApp · acceso/decisión Meta **+ documentos de verificación de negocio (tiempo propio: días)** · dominio/DNS · acceso Stripe (país/titular) · precios y fecha del lanzamiento · **producción de contenido del cliente (clases diarias, video del jueves, VSL — A7)** · aprobación de plantillas Meta · validación IT de Luca (si aplica).

**Reglas del retraso:** todo lo que no depende del cliente se construye ya; ningún track espera a otro. **Si las llaves A no llegan en 48 h o los videos no están confirmados a fecha, el primer lanzamiento se corre una semana — se dice hoy, no después.** Si el primer ciclo es solo Perú (`P-14`), toda la réplica IT sale del camino crítico.

## 17 · Riesgos (actualizado)

Vigentes del handoff §8: grupos manuales (1) · YouTube abierto (2) · cuenta publicitaria frágil en nicho salud (3) · validación de italiano (4) · System.io API sin probar (5 — mitigado con PoC en F1) · segundo 50% manual (6 — **con condición D7: no facturarlo con Meta sin resolver**).

Nuevos:
7. **Bloqueo Meta doble** (píxel/CAPI y WhatsApp API). Mitigación §13.
8. **Aprobación de plantillas + verificación de negocio + límite de tier** del número nuevo en el camino crítico (22 plantillas, 2 idiomas; ~250 convs/día sin verificar). Mitigación §11.
9. **Refacturación manual de consumos** (Jaime sin Stripe): fricción mensual, factura Jaime.
10. **Expectativa "switch de idioma"** (K2): se entrega réplica + selector. Comunicarlo como equivalente funcional antes de la entrega.
11. **Inglés prometido sin cotizar** (K2) y **gestión de ads no incluida** (T6): contener ambos como F3 en la primera conversación de avances.
12. **Fecha dura de agosto + 5 días de retraso**: regla explícita en §16.
13. **Compliance del nicho:** promesas de sanación → disclaimer médico en páginas, plantillas en tono educativo (Meta rechaza plantillas de "curación").
14. **RGPD/datos de salud (UE):** la encuesta captura categoría especial Art. 9 de consumidores italianos → consentimientos de §7 + banner de cookies de §13 **antes de publicar páginas**, no después.
15. **Contenido del cliente sin confirmar** (clases diarias, video del jueves, VSL): el sistema puede estar listo el día 5 y no haber nada que emitir el jueves. Mitigación: A7 hoy + regla de §16.
16. **Ancla de precios $97+$10 (K8):** la mensualidad la fija Jaime — alinearlo antes de que hable de precios con el cliente.
17. **Primer jueves sin protocolo**: mitigado con SOP día de evento + guardia (§14).

## 18 · Puntos de iteración

| # | Punto | Recomendación | Decide |
|---|---|---|---|
| P-01 | Cadencia: semanal (Joaquín) vs quincenal (Christie) | Técnicamente indiferente (custom values absorben ambas). Cerrar **antes del primer copy de recordatorios**. Dato: su mejor asistencia fue un sábado 17:00 | Cliente |
| P-02 | 1 vs 2 números WhatsApp API | **Verificar primero en la subcuenta si LC WhatsApp soporta más de un número** (históricamente NO: un número por subcuenta). Caso probable: **1 número con enrutamiento por `idioma`**. El +39 solo se promete si la plataforma lo soporta — no antes | Equipo (verificación técnica) |
| P-03 | Q4 de inversión en la encuesta | Incluir la **versión suave** — filtra el "todos quieren gratis, gratis, gratis" que Christie describió en la llamada de mapeo (delta 11) sin matar la conversión de una clase gratuita. Valida Luca (B4) | Equipo, valida Luca |
| P-04 | Pipeline único F1 | Mantener. Dividir por mercado solo si el full day de Lima (7.5) lo exige en F2 | Equipo |
| P-05 | Destino del no-califica | `/comienza-aqui` con video gratuito + link al checkout **existente** del 21 días. No construir funnel nuevo en F1 | Equipo |
| P-06 | Replay en F1 | No — F2. El grupo comparte el link como hoy; la página con caducidad llega con SP08 | Equipo |
| P-07 | Inglés | F3. No construir; solo convención de nombres preparada | Henry (comercial) |
| P-08 | ¿Qué se facturó: F1 sola o paquete completo? | ✅ **RESUELTO (15-ago): cobrado el 50% de F1; F2 en horizonte sin facturar.** Ver plan en §15: F2 se estructura (opción 2 de fábrica) antes de cobrarla, y se cierra contra el éxito del primer lanzamiento | Henry ✅ |
| P-09 | Moneda de cobro | **Restricción de plataforma, no preferencia: una moneda por subcuenta (D10).** Recomendado USD (coincide con el form). EUR-Italia solo vía links directos de Stripe + inbound webhook, o F2 | Equipo comunica, cliente acepta |
| P-10 | Evento del jueves: ¿webinar (sin venta) o masterclass (con venta)? | Preguntar en checklist A5 — cambia el CTA de la página del evento y el copy de recordatorios | Cliente |
| P-11 | Marca por mercado: el form dice **Salud Consciente**, pero el dominio/email es **lanuovacoscienza.com** | Preguntar qué marca y logo van en las páginas italianas antes de la réplica IT | Cliente |
| P-12 | Sesiones 1-a-1 con precios de pack ($70/$180/$299) vivas y fuera del estimado | **No entran en F1.** Escalón de la escalera en F2 solo si el cliente lo pide — y es conversación comercial, no cortesía | Henry (comercial) |
| P-13 | Quién escribe el copy IT de páginas y emails (T7: "sin dueño formal"; la traducción está fuera de alcance del estimado) | **Luca lo produce/traduce con IA (como hace con su contenido); nosotros maquetamos y él valida.** Pedirle horas reservadas en semana de lanzamiento (B4) | Cliente acepta la propuesta |
| P-14 | ¿El primer lanzamiento es PE, IT o ambos? ¿Y Perú cierra por llamada mientras no haya full day? | Preguntar en A5. Si solo PE: la réplica IT sale del camino crítico y B4 pierde urgencia. El mapa asume cierre PE por llamada de 30 min — confirmarlo | Cliente |

---

## 19 · Siguiente paso del pipeline interno

Con los `P-xx` resueltos: `ghl-clickup-task-builder` sobre los §3–14 de este mapa (1 subtarea = 1 nodo del builder) → `ghl-playwright-builder` contra la subcuenta real. **Se generan tareas solo de F1** (P-08 resuelto: F2 no está facturada — sus tareas se generan cuando se confirme, con la estructura de §15). Las 4 pruebas de plataforma del día 1 (§16) van primero: sus resultados fijan la forma final de WF3, la encuesta, P-02 y las cuotas. Añadir además dos tareas de ClickUp desde ya: **cobro del 2.º 50% de F1 contra el hito de entrega** (con la condición Meta de D7) y **preparar la propuesta de F2 estructurada** para presentarla tras el primer lanzamiento exitoso.
