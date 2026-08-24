# Tareas ClickUp — Fase 1 · Escuela de Sanación Biológica

Generado desde `mapa-implementacion-v3.md` (§3–§14, §16) con las convenciones de `ghl-clickup-task-builder`: **1 subtarea = 1 nodo del builder**. Pendiente de revisión de Henry antes de subir a ClickUp (falta List ID).

Orden de bloques = orden de construcción del §16. Dependencias del cliente citadas como A1–A7/B (checklist).

---

## BLOQUE SETUP — Día 1

### [SETUP-01] Cuenta base de la subcuenta
**Deps:** A3 (DNS) para dominio/email; el resto no espera.
| # | Subtarea | Config clave |
|---|---|---|
| 1 | Configurar zona horaria de la subcuenta | America/Lima |
| 2 | Cargar branding | `assets/brand/` (oro sobre negro; tema oscuro hasta tener transparente — B) |
| 3 | Conectar dominio de funnels | `lanuovacoscienza.com` o `eventos.` (A3) |
| 4 | Configurar dominio de envío de email + DNS | remitente `info@lanuovacoscienza.com` |
| 5 | Crear usuarios del cliente | Luca, Christie, Joaquín — sin permisos de configuración |
| 6 | Conectar LC WhatsApp en modo coexistencia | número confirmado por el cliente (A2) · iniciar verificación de negocio (A1) |

### [SETUP-02] Campos personalizados F1 (18)
**Deps:** ninguna. Nombres exactos del mapa §4 — los workflows los referencian literal.
| # | Subtarea | Campos |
|---|---|---|
| 1 | Grupo Atribución (7) | `idioma` (ES/IT) · `mercado` (Perú-LATAM/Italia) · `pais` (texto) · `fuente_contacto` (Meta Ads/TikTok/IG orgánico/Telegram/Referido/Base histórica) · `utm_campaign` · `utm_adset` · `utm_ad` (texto) |
| 2 | Grupo Calificación (5) | `cluster_sintoma` (4 clusters + Otro) · `sintoma_declarado` (texto largo) · `tiempo_con_sintoma` (4 rangos) · `nivel_calificacion` (Califica/A educar/No califica) · `motivo_descalificacion` (4 valores) |
| 3 | Grupo Evento (3) | `lanzamiento` (texto) · `fecha_evento` (fecha) · `asistio_evento` (casilla) |
| 4 | Grupo Venta (4) | `producto_comprado` (multi) · `plan_pago` (Contado/2/3) · `estado_pago` (4 valores) · `bono_llamada_christie` (casilla) |

### [SETUP-03] Custom values (23)
**Deps:** los valores reales llegan del cliente (A4, A5, B); crear todos con placeholder `PENDIENTE` para que nada quede hardcodeado (D5 — replicabilidad snapshot).
| # | Subtarea | Valores |
|---|---|---|
| 1 | Lanzamiento (5) | `nombre_lanzamiento_vigente` · `fecha_evento_vigente` · `hora_evento_pe` · `hora_evento_it` · `link_youtube_evento` |
| 2 | Links de flujo (10) | `link_grupo_whatsapp_es/it` · `link_registro_es/it` · `link_evento_es/it` · `link_calendario_cierre_pe/it` · `link_educativo_es/it` |
| 3 | Cobro (5) | `link_pago_contado` · `link_pago_2cuotas` · `link_pago_3cuotas` · `datos_pago_pe` · `datos_pago_it` |
| 4 | Otros (3) | `link_zoom_llamada` · `email_remitente` · `firma_luca` |

### [SETUP-04] Pipeline "Lanzamiento"
| # | Subtarea | Config clave |
|---|---|---|
| 1 | Crear pipeline con 10 etapas | Lead nuevo → Calificado → Registrado → Asistió → Postuló → Llamada agendada → Llamada realizada → Ganado / Perdido / No califica |
| 2 | Crear smart lists por mercado | filtro `mercado` = Perú-LATAM / Italia (sustituyen al 2.º pipeline) |

### [SETUP-05] Pruebas de plataforma (fijan el diseño — ANTES de construir workflows)
**Deps:** ninguna. Sus resultados deciden la forma final de ACT-01, WF3, cobros y P-02.
| # | Subtarea | Qué se decide |
|---|---|---|
| 1 | Probar disqualify de survey: ¿registra el contacto y dispara `Survey Submitted`? | Si NO → fallback plan A en ACT-01 (encuesta sin disqualify, ruteo 100% en WF2) |
| 2 | Probar anclaje temporal de Wait: ¿acepta fecha/hora desde campo o solo Specific Date/Time? | Forma de WF3 (opción a: editar tiempos por lanzamiento / opción b: anclado) |
| 3 | Verificar si LC WhatsApp soporta 2.º número en la subcuenta | Cierra `P-02` (número italiano sí/no) |
| 4 | Probar corte a N ciclos en cobro recurrente / payment schedule de invoice | Mecánica definitiva de 2/3 cuotas (ACT-07) |
| 5 | Verificar límites del modo coexistencia del número conectado | Qué se ve/no se ve en app vs CRM — va al SOP |

---

## BLOQUE ACTIVOS — Días 2–3

### [ACT-01] Encuesta F01 — Registro al evento (ES)
**Deps:** SETUP-02, SETUP-05.1 · copy validado por Luca (B).
| # | Subtarea | Config clave |
|---|---|---|
| 1 | Paso datos: nombre, WhatsApp, email, país | mapear a campos estándar + `pais` |
| 2 | Casillas de consentimiento (2, obligatorias) | privacidad con datos de salud (RGPD Art. 9) + opt-in WhatsApp/email |
| 3 | Q1 cluster → `cluster_sintoma` | 4 clusters + Otro (no descalifica) |
| 4 | Q1b texto corto opcional → `sintoma_declarado` | pregunta aparte (el "Otro" inline no escribe 2.º campo) |
| 5 | Q2 tiempo → `tiempo_con_sintoma` | 4 rangos |
| 6 | Q3 expectativa (eliminatoria) | a=Califica / b=No califica (busca medicina) / c=A educar |
| 7 | Q4 inversión suave (P-03) | 3.ª opción → A educar |
| 8 | Campos ocultos | `utm_campaign/adset/ad`, `fuente_contacto`, `idioma`=ES, `lanzamiento` |
| 9 | Lógica de salto / disqualify | Califica → `/gracias-es` · resto → `/comienza-aqui-es` (o plan A según SETUP-05.1) |

### [ACT-02] Formulario F03 — Postulación (ES)
| # | Subtarea | Config clave |
|---|---|---|
| 1 | Campos: interés + mejor franja + reconfirmar WhatsApp | corto, 3 campos |
| 2 | Redirect post-envío | mensaje "te escribimos ya por WhatsApp" (el link de agenda llega 1:1 por WF4B) |

### [ACT-03] Funnel ES — 5 páginas
**Deps:** SETUP-01.3, brand · contenido del cliente (B: video educativo, links checkouts, testimonios).
| # | Subtarea | Config clave |
|---|---|---|
| 1 | `/registro-es` | promesa = anuncio (guion Joaquín, B3), VSL si existe, F01 embebida, banner cookies UE, noindex OFF |
| 2 | `/gracias-es` | botón `{{link_grupo_whatsapp_es}}` + qué viene + add-to-calendar |
| 3 | `/evento-es` | YouTube no listado embebido (`{{link_youtube_evento}}`), contador, botón postular → `/postulacion-es`, noindex ON |
| 4 | `/postulacion-es` | F03 embebida, noindex ON |
| 5 | `/comienza-aqui-es` | video educativo (`{{link_educativo_es}}`) + CTA checkout existente 21 Días (B) |
| 6 | Disclaimer médico en footer de las 5 | "no sustituye atención médica" (B7 pendiente del cliente) |

### [ACT-04] Calendarios de cierre
**Deps:** disponibilidad real de Luca (B).
| # | Subtarea | Config clave |
|---|---|---|
| 1 | Calendario "Cierre — Perú" | America/Lima · 30 min · buffer · máx/día · solo por link |
| 2 | Calendario "Cierre — Italia" | franjas de Luca **convertidas a hora Lima** · widget con selector de TZ activado |
| 3 | Nota SOP: auditoría DST | recalibrar el calendario IT en cada cambio de hora europeo (mar/oct) |

### [ACT-05] Plantillas WhatsApp ES (11) → aprobación Meta
**Deps:** A1/A2 (WABA activa). **Enviar a aprobación el mismo día 1 si es posible — camino crítico.** Formato utility puro, cero lenguaje de "curación".
| # | Plantilla | Contenido clave |
|---|---|---|
| 1 | `bienvenida-registro` | link grupo `{{link_grupo_whatsapp_es}}` |
| 2 | `recordatorio-24h` | fecha/hora del evento |
| 3 | `recordatorio-3h` | hoy es el día |
| 4 | `en-vivo` | **trigger link** a `/evento-es` (la URL 1:1 que mide asistencia) |
| 5 | `no-show` | recuperación suave (el clic es proxy — copy sin reproche) |
| 6 | `postulacion-agenda` | `{{link_calendario_cierre_pe}}` |
| 7 | `confirmacion-cita` | fecha/hora en TZ del contacto |
| 8 | `recordatorio-cita-24h` | |
| 9 | `recordatorio-cita-1h` | `{{link_zoom_llamada}}` + cómo instalar Zoom |
| 10 | `respuesta-entrada-desconocido` | `{{link_registro_es}}` |
| 11 | `educativo-no-califica` | contenido educativo + `{{link_educativo_es}}` |

### [ACT-06] Emails ES (7)
Espejo de canal (respaldo del límite de tier de WhatsApp): confirmación-registro · recordatorio-24h · en-vivo · no-show · confirmación-cita · recordatorio-cita-24h · educativo-no-califica. Remitente `{{email_remitente}}`.

### [ACT-07] Cobros — producto Escuela
**Deps:** A4 (datos de pago) + A6 (montos cuotas) + decisión moneda única USD (D10). Stripe se conecta con el cliente (decisión Henry).
| # | Subtarea | Config clave |
|---|---|---|
| 1 | Producto Escuela NCA Academy — contado | $1.000 USD (invoice o payment link GHL — NUNCA link del dashboard de Stripe, WF5 no lo vería) |
| 2 | Plan 2 cuotas | invoice con payment schedule + **tarjeta guardada obligatoria** (monto A6) |
| 3 | Plan 3 cuotas | ídem (mecánica final según SETUP-05.4) |
| 4 | Volcar links a custom values | `link_pago_contado/2cuotas/3cuotas` |
| 5 | Guion de cierre (SOP Luca) | "el plan en cuotas requiere tarjeta" · transferencia/Yape → tag `pago-manual` + `datos_pago_{mercado}` |

### [ACT-08] Píxel + CAPI
**Deps:** A1 resuelto (admin o portafolio nuevo). Reparto exclusivo de canales — el píxel de navegador NO dispara eventos de conversión.
| # | Subtarea | Config clave |
|---|---|---|
| 1 | Instalar píxel a nivel funnel | solo PageView/ViewContent |
| 2 | Condicionar píxel al banner de cookies (tráfico UE) | |
| 3 | Verificar acción "Facebook Conversion API" en workflows | ¿acepta evento custom "Asistencia"? Si no → mapear a Schedule/ViewContent |
| 4 | Documento de mapeo de eventos para Joaquín | Registro/Asistencia/Postulación/Purchase — server-side only, antes de que monte campañas |

---

## BLOQUE WORKFLOWS — Días 3–4

> Convención física: `WF1 — Captación y atribución`, etc. WF4 se publica como 3 workflows (A/B/C) porque GHL une todos los triggers a un mismo flujo lineal.

### [WF1] Captación y atribución *(LS01+LS02+LS04)*
**Trigger(s):** Contact Created (re-enrollment OFF) + Customer Replied (Reply Channel = WhatsApp).
**Deps:** SETUP-02/03/04 · plantilla 10 aprobada.
| # | Nodo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Contact Created (sin filtros, re-enrollment OFF) |
| 2 | Trigger | Trigger: Customer Replied (Reply Channel = WhatsApp) |
| 3 | Update Fields | Update Fields: utm_campaign + utm_adset + utm_ad (🏷️ variables de sesión; ⚠️ los ocultos del form los escribe la encuesta) |
| 4 | IF | IF: Phone contiene "+39" → Update idioma=IT + mercado=Italia |
| 5 | IF | IF: Phone contiene "+51" → Update idioma=ES + mercado=Perú-LATAM |
| 6 | Send WhatsApp | Send WhatsApp (libre, ventana abierta): "¿Prefieres español o italiano?" — solo rama idioma vacío + entró por WhatsApp |
| 7 | Update Field | Update Field: lanzamiento = {{custom_values.nombre_lanzamiento_vigente}} |
| 8 | IF | IF: canal de entrada = WhatsApp → Update fuente_contacto = WhatsApp |
| 9 | Guard IF | Guard IF: tag `oportunidad-creada` existe → saltar creación |
| 10 | Create Opportunity | Crear oportunidad → Lanzamiento / Lead nuevo (⚠️ usar "Crear oportunidad", NO la deprecada) |
| 11 | Add Tag | Add Tag: `oportunidad-creada` |
| 12 | IF | IF: entró por WhatsApp Y sin tag `registrado` → Send WhatsApp (libre): link de registro según idioma ({{link_registro_es/it}}) |
| 13 | Goal Event | Goal: Survey Submitted (F01/F02) → End Workflow |
| 14 | Wait + Notify | Wait 30 min → Send Internal Notification a Luca: "lead escribió y no se registró" |

### [WF2] Registro y calificación *(LS03+SP01+eliminatoria D6)*
**Trigger:** Survey Submitted (F01 y F02).
**Deps:** ACT-01 · plantillas 1 y 11 aprobadas · ACT-08.3 para CAPI.
| # | Nodo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Survey Submitted (F01 — registro ES) |
| 2 | Trigger | Trigger: Survey Submitted (F02 — registro IT) |
| 3 | Update Fields | Update Fields: idioma + mercado según encuesta de origen (F01→ES/Perú · F02→IT/Italia) |
| 4 | Add Tag | Add Tag: `registrado` (apaga la rama 12-14 de WF1) |
| 5 | IF | IF: Q3 = "medicamento o tratamiento médico" → rama NO CALIFICA |
| 6 | Update Fields | Update Fields (rama no-califica): nivel_calificacion=No califica + motivo=Busca pastillas o medicina |
| 7 | IF | IF: Q3 = "curiosidad" O Q4 = "solo contenido gratuito" → rama A EDUCAR (nivel=A educar + motivo=Curiosidad) |
| 8 | Update Stage | Update Opportunity Stage → No califica (solo rama no-califica; a-educar conserva oportunidad + tag `a-educar`) |
| 9 | Send WhatsApp | Send WhatsApp Template: `educativo-no-califica` (ambas ramas descalificadas — SIN link de grupo) |
| 10 | Send Email | Send Email: educativo-no-califica → End Workflow (ramas descalificadas) |
| 11 | Update Field | Update Field (rama califica): nivel_calificacion = Califica |
| 12 | Update Stage | Update Opportunity Stage → Registrado |
| 13 | Send WhatsApp | Send WhatsApp Template: `bienvenida-registro` (link grupo según idioma — IF idioma → ES/IT) |
| 14 | Send Email | Send Email: confirmación-registro (fecha/hora del evento por custom values) |
| 15 | CAPI | Facebook Conversion API: evento **Registro** |

### [WF3] Recordatorios de evento *(SP02)* + no-show mínimo
**Trigger:** Opportunity Stage Changed → Registrado (pipeline Lanzamiento) · re-enrollment ON (cada lanzamiento).
**Deps:** SETUP-05.2 (define anclaje) · plantillas 2/3/4/5 · A5 (fecha/hora del evento).
| # | Nodo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Opportunity Stage Changed → Registrado |
| 2 | Wait | Wait: Specific Date/Time = T-24h del evento (⚠️ REVISAR anclaje: editar por lanzamiento — SOP — salvo que SETUP-05.2 habilite campo fecha/hora) |
| 3 | Guard IF | Guard IF: Opportunity Stage sigue en Registrado (si ya es Ganado/Perdido → End) |
| 4 | Send WhatsApp + Email | Send WhatsApp Template `recordatorio-24h` + Send Email recordatorio-24h |
| 5 | Wait | Wait: Specific Date/Time = T-3h |
| 6 | Send WhatsApp | Send WhatsApp Template: `recordatorio-3h` |
| 7 | Wait | Wait: Specific Date/Time = T-15min |
| 8 | Send WhatsApp + Email | Send WhatsApp Template `en-vivo` (trigger link 1:1 a /evento) + Send Email en-vivo |
| 9 | Wait | Wait: 2 horas |
| 10 | IF | IF: asistio_evento está vacío → Send WhatsApp Template `no-show` (copy suave: clic = proxy) |
| 11 | End | End Workflow |

### [WF4-A] Asistencia
**Trigger:** Trigger Link Clicked (link del evento).
| # | Nodo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Trigger Link Clicked → link `/evento` |
| 2 | Update Field | Update Field: asistio_evento = ✓ |
| 3 | Update Stage | Update Opportunity Stage → Asistió |
| 4 | CAPI | Facebook Conversion API: evento **Asistencia** (o estándar mapeado — ACT-08.3) |

### [WF4-B] Postulación
**Trigger:** Form/Survey Submitted (F03). **Deps:** plantilla 6 aprobada.
| # | Nodo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Form Submitted (F03 — postulación) |
| 2 | Update Stage | Update Opportunity Stage → Postuló |
| 3 | CAPI | Facebook Conversion API: evento **Postulación** |
| 4 | IF + Send | IF idioma → Send WhatsApp Template `postulacion-agenda` con {{link_calendario_cierre_pe}} o {{link_calendario_cierre_it}} |

### [WF4-C] Cita agendada + recordatorios
**Trigger:** Customer Booked Appointment (calendarios de cierre). **Deps:** ACT-04 · plantillas 7/8/9.
| # | Nodo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Customer Booked Appointment (In Calendar Group: cierre PE + IT) |
| 2 | Update Stage | Update Opportunity Stage → Llamada agendada |
| 3 | Send WhatsApp | Send WhatsApp Template: `confirmacion-cita` (hora en TZ del contacto — merge field de cita) |
| 4 | Wait | Wait: Event/Appointment Time − 24 h |
| 5 | Send WhatsApp | Send WhatsApp Template: `recordatorio-cita-24h` |
| 6 | Wait | Wait: Event/Appointment Time − 1 h |
| 7 | Send WhatsApp | Send WhatsApp Template: `recordatorio-cita-1h` ({{link_zoom_llamada}} + cómo instalar Zoom) |

### [WF5] Cobro confirmado *(SP07-lite)*
**Triggers:** Payment Received (pagos procesados por GHL) + Contact Tag Added `pago-manual`. **Deps:** ACT-07.
| # | Nodo | Subtarea |
|---|---|---|
| 1 | Trigger | Trigger: Payment Received (⚠️ solo dispara con links/invoices creados en GHL — ventas por System.io NO llegan hasta el webhook de F2) |
| 2 | Trigger | Trigger: Contact Tag Added → `pago-manual` (rama transferencia/Yape — D8/D10) |
| 3 | Guard IF | Guard IF: tag `primer-pago-procesado` existe → End (una cuota 2/3 NO re-dispara Ganado ni duplica Purchase) |
| 4 | Update Fields | Update Fields: producto_comprado=Escuela + estado_pago=Al día (⚠️ plan_pago lo fija Luca en el SOP de cierre — el workflow no lo infiere del pago) |
| 5 | Update Stage | Update Opportunity Stage → Ganado |
| 6 | Add Tag | Add Tag: `primer-pago-procesado` |
| 7 | IF | IF: plan_pago = Contado → Update bono_llamada_christie ✓ + Send Internal Notification a Christie |
| 8 | Notify | Send Internal Notification a Luca: "alta manual en System.io" (SOP — AP01 lo automatiza en F2) |
| 9 | CAPI | Facebook Conversion API: evento **Purchase** |

---

## BLOQUE RÉPLICA IT — Días 4–5 *(solo si el primer ciclo incluye Italia — P-14/A5)*

### [REP-01] Réplica IT de encuesta y páginas
F02 (clon de F01 en IT) + 5 páginas `-it`. **Deps:** copy IT de Luca (B4/P-13) · P-11 (¿marca La Nuova Coscienza en IT?).

### [REP-02] Plantillas y emails IT
11 plantillas + 7 emails en IT → aprobación Meta. **Deps:** validación de Luca (fecha límite día 3).

---

## BLOQUE QA + ENTREGA — Día 5

### [QA-01] Pruebas E2E
| # | Subtarea |
|---|---|
| 1 | E2E califica: registro → gracias → grupo → trigger link evento → postulación → cita → pago test → Ganado + notificaciones |
| 2 | E2E no-califica: Q3=medicina → /comienza-aqui + plantilla educativa + etapa No califica |
| 3 | E2E pago-manual: tag → Ganado + notificaciones sin Stripe |
| 4 | Verificar CAPI en Events Manager (4 eventos, sin duplicados con píxel) |
| 5 | Verificar recordatorios de cita en TZ del contacto (caso IT) |

### [ENT-01] SOPs + capacitación
| # | Subtarea |
|---|---|
| 1 | SOP llamada de cierre (mover etapa + enviar cobro + cuotas con tarjeta + plan_pago) |
| 2 | SOP pago manual (tag `pago-manual` + datos_pago) |
| 3 | SOP alta System.io |
| 4 | SOP cambiar de lanzamiento (5 custom values + tiempos WF3 si aplica) |
| 5 | SOP día de evento (T-24h plantillas OK + E2E link · T-2h video no listado + custom value · T-30min prueba real · guardia Profit 1.º y 2.º jueves) |
| 6 | SOP ventana 24h vs plantillas + límites coexistencia + auditoría DST calendario IT |
| 7 | Acta de entrega con cláusula K9 (cambios de embudo se cotizan aparte) |
| 8 | Sesión de capacitación ~2h (grabada) |

---

## BLOQUE ADMIN (sin fecha de build)

### [ADM-01] Cobro del 2.º 50% de F1 ($1.050)
Contra el hito de entrega. **Condición D7: no se factura con el bloqueo Meta sin resolver.**

### [ADM-02] Propuesta de Fase 2 estructurada
Opción 2 de fábrica (§15 del mapa): plantilla + 4 réplicas, automatización completa solo 21 Días + Reflexología. Presentar tras el primer lanzamiento exitoso.

---

**Totales:** 24 tareas padre · ~110 subtareas. Al subir a ClickUp, cada subtarea de workflow se expande al formato completo `## Acción en GHL` (tabla de campos) + `## Contexto` según la skill. Falta: **List ID de ClickUp** y el OK de Henry sobre este desglose.
