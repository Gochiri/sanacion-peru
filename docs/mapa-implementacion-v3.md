# Mapa de Implementación v3 — Escuela de Sanación Biológica

**Marca:** Salud Consciente (ES) / dominio `lanuovacoscienza.com` · **Escuela:** NCA Academy · **Empresa fiscal:** Nueva Conciencia Formación SAC
**Subcuenta:** creada, en la agencia GHL de Jaime · **Estado:** Fase 1 en ejecución con ~5 días de retraso · **Compromiso:** el sistema debe soportar un lanzamiento en agosto (C5)
**Fuentes:** handoff (`fuentes/00-handoff.md`) + deltas de las tres llamadas (`fuentes/01-deltas-llamadas.md`) + form de onboarding (`fuentes/02-form-onboarding.md`).
**Regla:** donde este mapa contradiga al handoff, manda este mapa. Los puntos abiertos están numerados `P-01…P-12` (§18) para iterar.

---

## 0 · Actores y responsabilidades

| Quién | Rol |
|---|---|
| Henry | Responsable del proyecto, relación con el cliente |
| Oliver | Implementación en GHL |
| Germán | Estrategia y configuración |
| **Jaime** | Dueño de la cuenta madre GHL. **Toda conversación de costos de plataforma/consumos con el cliente pasa por él, no por nosotros.** |
| Luca | Closer, contenido, validación del italiano. Su WhatsApp Business actual y sus grupos quedan intactos |
| Christie | Masterclass, entrega, sesión bono 40 min |
| Joaquín | Contraparte técnica del cliente: ads, creativos, VSLs, píxel del lado Meta. Receptor principal de la capacitación de tracking |

---

## 1 · Decisiones de arquitectura v3

| # | Decisión | Estado |
|---|---|---|
| D1 | **Híbrido System.io**: los cursos se quedan; GHL es la fuente única de datos/marketing/cobro. Sync bidireccional por API en F2, con **PoC temprana de la API** antes de comprometer AP01. | Cerrada (handoff 3.1) |
| D2 | **WhatsApp**: número nuevo con API oficial para el flujo automatizado; el número de Luca y los grupos siguen manuales; el dato se captura por formulario, no en conversación. | Cerrada (handoff 3.2) · pendiente `P-02` (1 vs 2 números) |
| D3 | **Una subcuenta, dos mercados**: campos `idioma`/`mercado`; réplica por idioma. En F1, **un solo pipeline** con campo `mercado` (mínimo viable 6.2), no dos. | Cerrada · revisar en F2 (`P-04`) |
| D4 | **Idiomas por réplica, no por "switch"**: páginas separadas `-es` / `-it` enlazadas con selector visible. El "plugin que cambia el idioma" prometido en el cierre no existe nativo en GHL — la réplica cumple la promesa funcional (el visitante elige idioma con un clic). **Inglés = Fase 3**: prometido de palabra, sin cotizar, no se construye ahora; la nomenclatura queda preparada (`-en`). | Cerrada (interna) · `P-07` |
| D5 | **Infraestructura y facturación**: subcuenta en la agencia de Jaime; sin rebilling automático (Jaime sin Stripe) → consumos refacturados manualmente por Jaime. **Build 100% replicable por snapshot: todo link/número/precio/dato del cliente en custom values, cero hardcode.** | Cerrada (llamada interna) |
| D6 | **Primer lanzamiento sin IA**: encuesta de registro con preguntas eliminatorias sustituye a IA01. Quien no califica no entra al grupo; se le educa con contenido/low ticket. IA bilingüe en F2. | Cerrada (llamada cierre, T1) |
| D7 | **Cobro del proyecto por invoice** (links fastpaydirect descartados). Cliente fiscal: Nueva Conciencia Formación SAC. El 2.º 50% se agenda como tarea contra el hito de entrega — no está automatizado. | Cerrada (C1) |
| D8 | **Ruta de pago manual (transferencia)**: en Italia hay compradores que transfieren a Luca y él matricula a mano. F1: tag `pago-manual` + SOP que dispara las mismas acciones post-venta; F2: rama formal en SP07/AP01. **El form de onboarding lo confirma con fuerza: el cliente declara "transferencia bancaria (IBAN)" como SU método de pago principal** — esta ruta es de primera clase, no un caso borde. | Nueva (llamada mapeo, delta 1 + form) |
| D9 | **Stripe SÍ entra en F1** con los tres planes del high ticket. Resuelve la contradicción de la llamada de cierre (T3): sin cobro conectado, el lanzamiento de agosto no sirve. Coincide con handoff 6.2. | Resuelta v3 |

---

## 2 · Objetivo de la Fase 1

> **"Desde el primer jueves, ninguna persona se pierde."**
> Todo lead queda capturado, atribuido y calificado; los calificados llegan al grupo y al evento con recordatorios; los interesados postulan y agendan solos; el pago queda registrado y medido. Luca solo aparece en la llamada de cierre.

Lo que **no** hace la F1 (y se dice así al cliente para no generar expectativa): responder conversaciones con IA, dar de alta en System.io automáticamente, cobrar/perseguir cuotas, ventana de cierre vie-sáb automatizada, nurturing largo, escalera de low tickets, dashboards.

---

## 3 · Cuenta base (F1)

- Dominio para funnels: candidato `lanuovacoscienza.com` (o subdominio `eventos.`) → **falta acceso DNS (checklist A3)**. ⚠️ El dominio es la marca italiana; qué marca va por mercado es `P-11`
- Dominio de envío de email dedicado + verificación DNS · remitente candidato: `info@lanuovacoscienza.com`
- Branding de subcuenta: **logos recibidos** (`assets/brand/`, oro sobre negro, vertical + horizontal). Vienen con fondo negro incrustado → páginas en tema oscuro, o pedir transparente/vector (checklist B8)
- Zona horaria base **America/Lima** (los calendarios manejan Roma aparte)
- Usuarios: Luca, Christie, Joaquín (+ equipo Profit). Roles: cliente sin permisos de configuración
- Integración nativa **Stripe** (cuenta del cliente — la misma que usa System.io, ver `P-09` monedas)
- **LC WhatsApp** en la subcuenta — número nuevo. ⚠️ El form da `+51 986 199 020` como "WhatsApp del negocio": **confirmar si es el número destinado a la API o el actual** — el actual NO se conecta (perdería la app y los grupos de Luca, contra D2). Checklist A2. Costos y mensualidad se hablan con Jaime, no con nosotros
- Píxel de Meta instalado a nivel funnel + acción CAPI en workflows (§13)

### 3b · Precios conocidos (form de onboarding)

| Producto | Precio | Falta |
|---|---|---|
| Escuela **NCA Academy** | $1.000 contado (coincide con "oferta de cierre") | montos 2 y 3 cuotas · precio Italia (¿EUR?) |
| Videocurso 5 Leyes | $100 | precio IT |
| Libro "La Nueva Consciencia" | S/ 80 (**soles**) | |
| Sesiones 1-a-1 | $70 · pack 3 $180 · pack 6 $299 | fuera del alcance del estimado → `P-12` |
| 21 días · Dispersión del dolor · Reflexología | **sin precio** | checklist A6 (bloquea escalera F2, no F1) |

## 4 · Campos personalizados (subset F1)

Se crean en F1 los que los flujos F1 escriben o leen; el resto (cuotas, cohorte, System.io, replay) se crea en F2 para no ensuciar.

| Grupo | Campos F1 |
|---|---|
| Atribución | `idioma` · `mercado` · `pais` · `fuente_contacto` · `utm_campaign` · `utm_adset` · `utm_ad` |
| Calificación | `cluster_sintoma` · `sintoma_declarado` · `tiempo_con_sintoma` · `nivel_calificacion` · `motivo_descalificacion` |
| Evento | `lanzamiento` · `fecha_evento` (por custom value del lanzamiento vigente) · `asistio_evento` · `modalidad_evento` |
| Venta | `producto_comprado` · `plan_pago` · `estado_pago` · `bono_llamada_christie` |

Quedan para F2: `estado_ia`, `intentos_previos` (si no entra en la encuesta final), `vio_replay`, `cuota_actual`, `cohorte`, `alta_systemio`.

## 5 · Custom values (replicabilidad — D5)

Todo lo que cambia entre lanzamientos o entre clientes va aquí, nunca escrito a mano en workflows/plantillas/páginas:

`nombre_lanzamiento_vigente` · `fecha_evento_vigente` · `hora_evento_pe` · `hora_evento_it` · `link_grupo_whatsapp_es` · `link_grupo_whatsapp_it` · `link_registro_es` · `link_registro_it` · `link_evento_es` · `link_evento_it` · `link_youtube_evento` (se actualiza por lanzamiento) · `link_calendario_cierre_pe` · `link_calendario_cierre_it` · `link_pago_contado` · `link_pago_2cuotas` · `link_pago_3cuotas` (por mercado si aplica `P-09`) · `link_zoom_llamada` · `link_educativo_es` · `link_educativo_it` · `email_remitente` · `firma_luca`

**SOP "cambiar de lanzamiento"** = actualizar 4 custom values (nombre, fecha, horas, link YouTube). Nada más se toca.

## 6 · Pipeline (F1 — único)

**Lanzamiento** — etapas:
`Lead nuevo → Calificado → Registrado → Asistió → Postuló → Llamada agendada → Llamada realizada → Ganado / Perdido / No califica`

- El campo `mercado` separa las vistas (smart lists / filtros por mercado en lugar de dos pipelines).
- Nota: el cierre difiere entre mercados (IT: masterclass + llamada · PE: full day presencial con venta en sala). Mientras el full day de Lima no tenga fecha/formato (bloqueante 7.5), las etapas genéricas sirven para ambos. Revisar división en F2 (`P-04`).

## 7 · Formularios y encuestas (F1)

### F01 / F02 — Registro al evento (ES / IT) — *el punto de captura del negocio*
Implementar como **encuesta GHL (survey)** con lógica de salto y descalificación — no como form simple — para poder rutear por respuesta. Fallback si la lógica se queda corta: form + ruteo en WF2 con envío del link de grupo solo a calificados.

- **Datos:** nombre · WhatsApp · email · país
- **Campos ocultos:** `utm_campaign` / `utm_adset` / `utm_ad` (de la URL) · `fuente_contacto` · `idioma` · `lanzamiento`
- **Q1 — síntoma** *(segmenta, no descalifica)*: "¿Cuál de estos describe mejor lo que vives hoy?" → Dolores articulares o musculares / Digestivo (gastritis, reflujo, colon irritable) / Ansiedad, pánico o depresión / Piel (dermatitis, psoriasis) / Otro: \_\_\_ → `cluster_sintoma` (+ texto a `sintoma_declarado`)
- **Q2 — tiempo** *(segmenta)*: "¿Hace cuánto buscas solución?" → Menos de 6 meses / 6 meses a 2 años / Más de 2 años / Más de 5 años → `tiempo_con_sintoma`
- **Q3 — expectativa** *(la eliminatoria)*: "¿Qué esperas encontrar en esta clase?" →
  a) Entender la causa emocional de mi síntoma y cómo abordarla → **Califica**
  b) Un medicamento o tratamiento médico para mi enfermedad → **No califica** (`motivo_descalificacion` = Busca pastillas o medicina)
  c) Solo curiosidad, quiero mirar → **A educar** (`motivo_descalificacion` = Curiosidad)
- **Q4 (opcional, `P-03`)** — versión suave del filtro de inversión: "Si esta clase te muestra un camino claro, ¿estarías dispuesto/a a invertir en tu proceso?" → Sí / Necesitaría saber más / No, busco solo contenido gratuito (última → A educar)

**Salidas:** Califica → `/gracias` (grupo + instrucciones) · No califica / A educar → `/comienza-aqui` (educativa, sin link de grupo).
La redacción exacta la valida Luca (es su tono y su lenguaje de "conflicto emocional") — checklist B4.

### F03 — Postulación a la escuela (post-evento)
Corta: confirma interés real + mejor franja horaria + reconfirma WhatsApp. Dispara la agenda (WF4). Réplica IT.

### E01 — Resultado de llamada
**Pasa a F2** (SP06). En F1, Luca mueve la etapa a mano tras cada llamada — SOP de 30 segundos.

## 8 · Funnels y páginas (F1 · cada una en ES + réplica IT)

| Página | Contenido / función |
|---|---|
| `/registro-{es,it}` | Promesa coherente con el anuncio (guion de Joaquín — checklist B3), VSL corto si existe, encuesta embebida. UTMs pasan a campos ocultos. |
| `/gracias-{es,it}` | Confirmación + botón al grupo de WhatsApp + qué va a pasar (clases diarias, evento del jueves) + add-to-calendar. |
| `/evento-{es,it}` | **Página propia del evento**: YouTube **no listado** embebido, contador, botón "Quiero postular a la escuela" (→ F03), aviso de caducidad. Noindex, acceso solo por link. Razón de ser: si transmiten en YouTube abierto se pierde asistencia, CTA y urgencia (riesgo 2 del handoff) — y la razón real del cambio desde Zoom era fricción, que esta página también elimina. |
| `/comienza-aqui-{es,it}` | Destino del no-califica/a-educar: video educativo gratuito + CTA al low ticket **existente** (checkout actual de System.io/Hotmart — en F1 NO se construyen funnels de low ticket). `P-05` |

**Medición de asistencia (honesta):** el link a `/evento` enviado por WhatsApp/email es un **trigger link** → el clic marca `asistio_evento` y mueve a *Asistió*. Es un proxy por clic, no visionado real (eso requeriría JS custom — no entra en F1). El botón de postulación da la señal fuerte.

Fuera de F1: página de replay con caducidad (F2), 5 páginas de venta low ticket (F2, ver §15), página `/estimado` (ya cumplió su función).

## 9 · Calendarios (F1)

| Calendario | Config |
|---|---|
| Llamada de cierre — Italia | Europe/Rome · 30 min · disponibilidad real de Luca (checklist B5) · solo accesible por link post-postulación |
| Llamada de cierre — Perú | America/Lima · 30 min · ídem |

Confirmación + recordatorios de cita los maneja WF4. La sesión bono de Christie se agenda manual en F1 (volumen bajo: solo pagos de contado); calendario propio en F2.

## 10 · Workflows (F1 — 5 consolidados)

> Nomenclatura física en GHL: `WF1 — Captación y atribución`, etc. El mapeo a los códigos del roadmap se mantiene para trazabilidad con el handoff.

### WF1 · Captación y atribución *(LS01 + LS02 + LS04)*
- **Triggers:** contacto creado · mensaje WhatsApp entrante de número sin contacto · clic en trigger links de orgánico (bio IG/TikTok, Telegram).
- **Acciones:** volcar UTMs → campos; fijar `fuente_contacto`; fijar `idioma`/`mercado` (por formulario de origen, por página, o por prefijo telefónico +39→IT / +51→PE; ambiguo → rama que pregunta con mensaje simple); estampar `lanzamiento` vigente; crear oportunidad en *Lead nuevo*.
- Entrada por WhatsApp sin registro (sin IA en F1): **respuesta automática única** con el link de registro del idioma detectado + notificación a Luca solo si el contacto responde algo que no es registro.

### WF2 · Registro y calificación *(LS03 + SP01 + eliminatoria D6)*
- **Trigger:** envío de F01/F02.
- **Acciones:** escribir calificación (`cluster_sintoma`, `tiempo_con_sintoma`, `nivel_calificacion`, `motivo_descalificacion`);
  - **Califica** → etapa *Registrado* · WhatsApp de bienvenida con link del grupo (plantilla) · email de confirmación con fecha/hora del evento · evento CAPI **Registro**.
  - **No califica / A educar** → etapa *No califica* (o tag `a-educar` sin cerrar oportunidad) · secuencia ligera: 1 WhatsApp + 1 email con el contenido educativo · tag para remarketing futuro. Sin link de grupo.

### WF3 · Recordatorios de evento *(SP02)*
- **Programado sobre `fecha_evento_vigente`** para oportunidades en *Registrado*: T-24 h (WhatsApp + email) · T-3 h (WhatsApp) · T-15 min "estamos en vivo" (WhatsApp con trigger link a `/evento`).
- Las clases diarias de falso-en-vivo se anuncian **en el grupo, manualmente** (Joaquín/Luca) en F1 — los grupos no son administrables por API. Automatizar avisos individuales diarios = F2 si el costo de plantillas lo justifica.

### WF4 · Asistencia, postulación y agenda *(SP03 + SP04 + SP05)*
- Clic en trigger link del evento → `asistio_evento` ✓ · etapa *Asistió* · CAPI **Asistencia**.
- Clic en botón postular / F03 enviado → etapa *Postuló* · CAPI **Postulación** · WhatsApp con `link_calendario_cierre_{mercado}`.
- Cita creada → etapa *Llamada agendada* · confirmación · recordatorios T-24 h y T-1 h (con `link_zoom_llamada` + instrucciones de instalar Zoom — dolor conocido del cliente).
- **No-show mínimo:** registrado que no clicó el link del evento → T+2 h mensaje "te lo perdiste, aquí lo importante + próximo paso". La ventana de cierre completa vie-sáb (SP08) es F2.

### WF5 · Cobro confirmado *(SP07-lite)*
- **Trigger:** pago Stripe recibido (contado o 1.ª cuota).
- **Acciones:** etapa *Ganado* · `producto_comprado`/`plan_pago`/`estado_pago` · notificación interna a Luca con SOP de **alta manual en System.io** (AP01 lo automatiza en F2) · si contado → `bono_llamada_christie` ✓ + notificación a Christie · CAPI **Compra**.
- **Rama pago manual (D8):** Luca aplica tag `pago-manual` → mismas acciones sin evento Stripe.

## 11 · Plantillas de WhatsApp (F1)

Cada una en **ES + IT** (~10 × 2 = **20 aprobaciones de Meta** → camino crítico, enviar a aprobación el día 1):

1. `bienvenida-registro` (link grupo) · 2. `recordatorio-24h` · 3. `recordatorio-3h` · 4. `en-vivo` (trigger link evento) · 5. `no-show` · 6. `postulacion-agenda` (link calendario) · 7. `confirmacion-cita` · 8. `recordatorio-cita-24h` · 9. `recordatorio-cita-1h` (Zoom + cómo entrar) · 10. `respuesta-entrada-desconocido` (link registro)

El italiano lo valida Luca antes de enviarse a Meta (checklist B4).

## 12 · Stripe (F1)

- Producto **Escuela** con tres modalidades: contado · 2 cuotas · 3 cuotas — vía invoice con calendario de pagos o plantilla recurrente con número de ciclos. Moneda por mercado: `P-09`.
- Flujo: Luca cierra en la llamada → envía `link_pago_X` (custom value) → WF5 hace el resto.
- Reintentos de cobro, mora y retiro de acceso = F2 (AP04). En F1, pago fallido notifica a Luca (manual, como hoy — sin pérdida de función).

## 13 · Píxel + CAPI (F1)

| Evento | Se dispara en |
|---|---|
| Registro (CompleteRegistration/Lead) | WF2, al calificar |
| Asistencia (evento custom) | WF4, clic trigger link |
| Postulación (Schedule/custom) | WF4 |
| Compra (Purchase) | WF5 |

**Bloqueado por el admin del portafolio de Meta — y el bloqueo es doble:** también el alta de WhatsApp API requiere un Business Manager con administrador. **Recomendación v3:** si en 48 h Joaquín no recupera el admin, crear **portafolio nuevo a nombre de Nueva Conciencia Formación SAC** con estructura de permisos sana. Costo real de histórico: casi nulo (nunca instalaron píxel en Perú; el de Italia en System.io no tiene CAPI ni campañas activas). Beneficio: desbloquea píxel + WhatsApp API de una vez y elimina el riesgo de un admin fantasma para siempre.

## 14 · Capacitación y SOPs (F1 — C3)

1 sesión (~2 h, grabada) + SOPs escritos:
leer el pipeline y las vistas por mercado · qué hace cada WF · SOP llamada de cierre (mover etapa + enviar link de pago) · SOP pago manual (tag `pago-manual`) · SOP alta en System.io · SOP cambiar de lanzamiento (4 custom values) · SOP responder dentro de la ventana de 24 h vs plantillas · qué NO tocar.

## 15 · Fase 2 — alcance comprometido + re-escopeo

**Comprometido en el estimado (6.3):** IA bilingüe con escalada · System.io API (AP01 alta automática + sync inverso) · entrega de bonos (árbol anidado — delta 7) · recordatorios de encuentros · cuotas con reintentos, mora y retiro de acceso (AP04) · ventana de cierre vie-sáb (SP08) · escalera 5 low tickets con páginas · upsell/carrito abandonado · base histórica (~1.000 contactos IT — LS05) · campañas a base propia · testimonios automáticos (solo escritos — T4; pedir video como objetivo) · 2 capacitaciones.
**Nuevo en F2 por deltas:** rama formal de pago por transferencia en SP07/AP01 (D8) · página de replay con caducidad · calendario propio de Christie · E01/SP06 · webhook Hotmart · PoC System.io API **adelantada** (se hace durante F1, es 1-2 h y desriesga F2).

**Re-escopeo (handoff 6.1) — decisión interna pendiente (`P-08` define el margen):**
- Si se facturó **solo F1**: cabe renegociar F2 → opción 1 (escalera a F3, F2 ≈ 40 h).
- Si se facturó **el paquete completo**: única salida sin renegociar = **opción 2** — 1 plantilla de página de venta + 4 réplicas de copy, y automatización completa (upsell/carrito) solo para 2 productos: **21 días** (el que más rota) y **reflexología** (el más caro, hoy sin base de datos). Los otros 3 con página + order form simple.
- Recomendación: **opción 2** en ambos casos; la 1 solo si la conversación comercial ya está abierta.

## 16 · Orden de construcción (recuperar los 5 días)

**Hoy (día 0):** enviar checklist al cliente (`checklist-informacion-cliente.md`) — las 6 llaves de la sección A condicionan todo lo demás. Avisar a Jaime por el grupo.

| Día | Track |
|---|---|
| 1 | Cuenta base · campos · custom values · pipeline · redactar 20 plantillas y **enviarlas a aprobación** · iniciar alta WhatsApp API (si hay número + Meta) · PoC System.io API (si llega la key) |
| 2–3 | Funnels ES completos (4 páginas + encuesta con lógica) · productos Stripe |
| 3–4 | WF1–WF5 · pruebas E2E con contacto de prueba (registro→grupo→evento→postulación→cita→pago test) |
| 4–5 | Réplica IT (páginas + plantillas, validación de Luca) · píxel + CAPI (si hay acceso Meta) · QA · agendar capacitación |

**Dependencias externas duras (fuera de nuestro control):** número WhatsApp · acceso/decisión Meta · dominio/DNS · acceso Stripe · precios y fecha del lanzamiento · aprobación de plantillas por Meta (horas–días; verificación de negocio puede tomar más si el portafolio es nuevo).

**Regla del retraso:** todo lo que no depende del cliente se construye ya; ningún track espera a otro.

## 17 · Riesgos (actualizado)

Vigentes del handoff §8: grupos manuales (1) · YouTube abierto (2) · cuenta publicitaria frágil en nicho salud (3) · validación de italiano (4) · System.io API sin probar (5 — mitigado con PoC en F1) · segundo 50% manual (6).

Nuevos:
7. **Bloqueo Meta ahora es doble** (píxel/CAPI **y** WhatsApp API). Mitigación §13.
8. **Aprobación de plantillas Meta en el camino crítico** (20 plantillas, 2 idiomas). Mitigación: redactar y enviar el día 1.
9. **Refacturación manual de consumos** (Jaime sin Stripe): fricción mensual, factura Jaime. Fuera de nuestro alcance técnico; documentado para que no nos salpique.
10. **Expectativa "switch de idioma"** (C2): se prometió un plugin; se entrega réplica + selector. Comunicarlo como equivalente funcional antes de la entrega, no en la entrega.
11. **Inglés prometido sin cotizar** (C2): contener como F3 desde la primera conversación de avances.
12. **Fecha dura de agosto + 5 días de retraso**: si las llaves de la sección A del checklist no llegan en 48 h, el primer lanzamiento del ciclo se corre una semana — decirlo ahora, no después.
13. **Compliance del nicho:** promesas de sanación → disclaimer médico en páginas y cuidado en el copy de plantillas (Meta rechaza plantillas de "curación"). Redactar en tono educativo.

## 18 · Puntos de iteración

| # | Punto | Recomendación | Decide |
|---|---|---|---|
| P-01 | Cadencia: semanal (Joaquín) vs quincenal (Christie) | Técnicamente indiferente (custom values absorben ambas). Empujar a que el cliente cierre **antes del primer copy de recordatorios**. Dato a favor de flexibilidad: su mejor asistencia fue un sábado 17:00 | Cliente |
| P-02 | 1 vs 2 números WhatsApp API | **2 números si Luca puede conseguir un número italiano** (+39 genera confianza en IT; +51 escribiéndole a italianos parece spam). Si no, 1 número con enrutamiento por `idioma`. En F1 el costo delta es bajo; el "2 bots" del handoff solo aplica en F2 | Equipo + cliente |
| P-03 | Q4 de inversión en la encuesta | Incluir la **versión suave** (filtra "todo gratis" —dolor declarado por Christie— sin matar conversión de una clase gratuita) | Equipo, valida Luca |
| P-04 | Pipeline único F1 | Mantener. Dividir por mercado solo si el full day de Lima (7.5) lo exige en F2 | Equipo |
| P-05 | Destino del no-califica | `/comienza-aqui` con video gratuito + link al checkout **existente** del 21 días. No construir funnel nuevo en F1 | Equipo |
| P-06 | Replay en F1 | No — F2. El grupo comparte el link como hoy; la página con caducidad llega con SP08 | Equipo |
| P-07 | Inglés | F3. No construir; solo convención de nombres preparada | Henry (comercial) |
| P-08 | ¿Qué se facturó: F1 sola o paquete completo? | **Confirmar internamente** — define el margen de re-escopeo de F2 (§15) y la urgencia de materiales F2 | Henry |
| P-09 | Moneda por mercado. El form declara "$ Dólar" en genérico, pero el libro está en soles y falta confirmar EUR para Italia. ¿Stripe del cliente es una cuenta o dos? | Preguntar en checklist A4/A6. Afecta productos Stripe y links de pago | Cliente |
| P-10 | Evento del jueves: ¿webinar (sin venta) o masterclass (con venta)? El delta 2 dice que son cosas distintas y la "estrategia nueva" no lo aclara | Preguntar en checklist A5 — cambia el CTA de la página del evento y el copy de recordatorios | Cliente |
| P-11 | Marca por mercado: el form dice **Salud Consciente**, pero el dominio/email es **lanuovacoscienza.com** ("La Nuova Coscienza") | Preguntar qué marca y qué logo van en las páginas italianas antes de la réplica IT | Cliente |
| P-12 | Sesiones 1-a-1 con precios de pack ($70/$180/$299) están vivas y no estaban en el alcance del estimado | **No entran en F1.** Registrarlas como escalón de la escalera en F2 (calendario + cobro propios) solo si el cliente lo pide — y entonces es conversación comercial, no cortesía | Henry (comercial) |

---

## 19 · Siguiente paso del pipeline interno

Con los `P-xx` resueltos: `ghl-clickup-task-builder` sobre los §3–14 de este mapa (1 subtarea = 1 nodo del builder) → `ghl-playwright-builder` contra la subcuenta real. Generar tareas **solo de F1** hasta resolver `P-08`.
