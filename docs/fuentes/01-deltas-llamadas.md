# Deltas de las tres llamadas vs. el handoff

> **Documento interno del equipo.** La sección 3 contiene acuerdos operativos con Jaime que no se comunican al cliente.
> Regla de lectura: donde un delta contradiga al handoff, **manda el delta**. El mapa v3 ya incorpora todo esto.

---

## 1 · Llamada de mapeo — 31-jul-2026, 108 min (Luca, Christie, Joaquín)

Lo que aporta por encima del handoff:

1. **Camino de pago por transferencia (no estaba mapeado).** Muchos compradores italianos no saben usar tarjeta: transfieren a Luca, y Luca compra el curso con su propia tarjeta poniendo el email del cliente. Es un alta manual real y recurrente → necesita ruta "pago manual" en el sistema (F1: tag + SOP; F2: rama formal de SP07/AP01).
2. **Webinar ≠ masterclass.** En el webinar (1,5 h) **no se vende**. Solo se vende en la masterclass (3 h: ~2 h formativas + ~40 min de pitch). Son dos tipos de evento con recordatorios y CTAs distintos.
3. **Cadencia sin cerrar entre Joaquín y Christie.** Joaquín: lanzamiento semanal (captación dom-mié → evento jueves → cierre vie-sáb). Christie: ciclo de 2 semanas con 4 webinars mar/jue + masterclass sábado, luego pausa. No se resolvió en la llamada. → `P-01` del mapa.
4. **Base histórica cuantificada:** ~1.000 contactos italianos en el correo de Luca (LS05).
5. **Horarios con datos:** Italia mar/jue 18:30 histórico; el mejor resultado fue **sábado 17:00 (70 conectados)**. Perú 11:00. Los falsos en vivo diarios se mencionaron a las 19:00/20:00 sin cerrar.
6. **Razón real del cambio a YouTube: fricción de Zoom** (la gente no sabe descargar/entrar). Refuerza la página propia con YouTube no listado.
7. **Bonos anidados:** el videocurso 5 leyes trae sus propios bonos (56 preguntas, test de herida emocional, meditación). Afecta el árbol de entrega de AP02.
8. **Las sesiones 1-a-1 de Christie siguen vivas** como producto; el 21 días es su puerta de entrada. No fueron sustituidas por la escuela.
9. **Joaquín es contraparte técnica capaz** (monta campañas, cambia destinos, instala píxel del lado de Meta, produce video). Receptor natural de la capacitación de tracking.
10. **Reflexología (low ticket más caro) está en Hotmart; 21 días en System.io.** El low ticket más rentable es el que hoy no deja base de datos.
11. **El dolor de los grupos ES en palabras de Christie:** los grupos en español "se han ido llenando y se han ido vaciando, porque todos quieren gratis, gratis, gratis, todo gratis" — llega puro curioso sin cualificación. Es la base del filtro de la encuesta (Q3/Q4, `P-03`).

---

## 2 · Llamada de cierre — 4-ago-2026, 49 min (Luca, Joaquín; Christie ausente)

### Compromisos adquiridos con el cliente (verbales, no todos en el estimado)

> Codificados `K1…K9` para no colisionar con los códigos `C1…C6` del checklist de información.

| # | Compromiso | Implicación |
|---|---|---|
| K1 | **Facturación por invoice** a Nueva Conciencia Formación SAC (RUC Perú). Los links de fastpaydirect quedaron descartados ("no le vayan a dar comprar"). | §4.2 del handoff obsoleta. Cobro del 2.º 50% también será por invoice. |
| K2 | **Páginas en español + italiano incluidas**; se habló de "un plugin/switch que cambie el idioma" y hasta de **inglés** ("mentalícense: español, italiano, inglés" — Luca). | El switch no existe nativo en GHL → se resuelve con réplicas + selector. Inglés NO está cotizado → F3. Gestionar expectativa. |
| K3 | **SOPs escritos + capacitación (~2 h)** por fase. | Los SOPs escritos no estaban contemplados en el handoff; las sesiones de capacitación sí (6.2: una en F1 · 6.3: dos en F2). Lo nuevo son los SOPs y la duración. |
| K4 | **Snapshot portable** si el cliente se va algún día. | Refuerza build replicable. |
| K5 | **Fase 1 sirve para lanzar este mismo mes** (agosto). Henry lo confirmó. | Fecha dura. El retraso de ~5 días come directamente esa promesa. |
| K6 | Plazo dicho: **4 semanas**, con intención de entregar en ~2. | |
| K7 | Asesoría de copy/VSL incluida (guía, no producción): el cliente crea videos y creativos, nosotros damos estructura y feedback. | |
| K8 | Se le dijo al cliente que la licencia GHL propia cuesta **$97/mes** + $10 WhatsApp + variables. | El cliente ya ancló $97. Relevante para el acuerdo con Jaime (ver §3). |
| K9 | Cambios futuros de embudo = re-mapeo + trabajo por horas o nueva implementación, no reconstrucción gratis. | Dicho explícitamente; nos protege. Debe quedar por escrito en los SOPs y el acta de entrega. |

### Decisiones técnicas nuevas
| # | Decisión | Detalle |
|---|---|---|
| T1 | **Primer lanzamiento sin IA**: formulario con **preguntas eliminatorias** ("tres preguntas que si no las responden de determinada manera, no entran al grupo" — Germán, aceptado por Luca). Quien no califica → gracias + video/low ticket para educarlo. | Adelanta una versión ligera de EV05 a la Fase 1. La IA llega en F2. |
| T2 | El **grupo de WhatsApp sigue siendo el hub** en F1: anuncio → landing → formulario → grupo → link del evento por el grupo. | Los grupos siguen siendo manuales (API no los administra). |
| T3 | **Contradicción sobre Stripe en F1**: Henry primero dijo que F1 no incluye "asistente y conexión de pasarela", 30 segundos después se corrigió: "lo único que no incluye es la IA". El handoff §6.2 SÍ incluye Stripe en F1. | Resolución en mapa v3: **Stripe entra en F1** (sin cobro no hay lanzamiento útil). |
| T4 | **Sin testimonios en video** (tema sensible: cáncer, tumores — la gente no se muestra). Solo escritos, abundantes. | Afecta páginas de venta y PS01/PS02. Objetivo F2: pedir videos igualmente (Henry insistió en su valor). |
| T5 | Píxel + CAPI confirmados dentro de F1 ("sale lo del píxel" — sí). | Sigue bloqueado por el admin del portafolio (nadie lo tocó en la llamada). |
| T6 | Ads los corre Joaquín; gestión de ads por nosotros = posible **Fase 3** ("plan de ads" no incluido). | |
| T7 | Traducción de contenido la hace Luca con IA (Heygen/etc.). El copy del embudo en italiano sigue sin dueño formal. | |

### Lo que quedó abierto al cierre de la llamada
- Fase 1 sola vs. paquete completo: Luca coqueteó con el completo ("comprar el completo, que tiene el descuento") pero cerró con "estamos en comunicación para lo que es la primera fase". → confirmar qué se facturó (`P-08`).
- Datos fiscales: los envió después (el pago ya se hizo).
- Admin del portafolio Meta: sin tocar. Sigue crítico.

---

## 3 · Llamada interna con Jaime — 6-ago-2026, 30 min (Henry, Germán, Oliver, Jaime) — **NO de cara al cliente**

1. **Jaime es el dueño de la relación**: Luca es SU cliente; Profit ejecuta la implementación. Hubo vacío de comunicación (Jaime no estuvo en mapeo ni cierre; no se definió antes dónde viviría la cuenta).
2. **Resolución (post-llamada, confirmada por Henry): la subcuenta del cliente vive en la agencia GHL de Jaime.** El Location ID de las notas viejas de la CLI no aplica; ya existe subcuenta real.
3. **La mensualidad y los consumos** (licencia, WhatsApp, IA, email) **los negocia y cobra Jaime directamente con el cliente**. Nosotros no hablamos de costos de plataforma con Luca/Christie/Joaquín: cualquier pregunta se remite a Jaime. (El cliente ya ancló $97 como referencia — K8.)
4. **La agencia de Jaime no tiene Stripe habilitado** → no hay rebilling SaaS automático: los consumos se refacturan **manualmente** (reportes/capturas mensuales) hasta que Jaime active Stripe (dijo ~1 mes). Riesgo operativo recurrente; el que factura es Jaime.
5. **El build debe ser replicable por snapshot.** Plan explícito de revender la implementación a otros mentores (empezando por la esposa de Jaime, mapeo pendiente de agendar). Consecuencia técnica: **todo link, número, precio y dato del cliente va en custom values; cero hardcode** en workflows, plantillas y páginas.
6. **Comunicación:** grupo compartido con Jaime; avisarle avances. Retraso reconocido (~5 días): "que no piensen que cobramos y no respondimos".
7. La IA (Conversation AI $97-127/mes) **no se activa aún**: primero medir volumen real de leads/mensajes del primer lanzamiento (además la IA es F2). Coherente con T1.
8. El Stripe que se conecta a la subcuenta para **cobros del cliente a sus alumnos** es el Stripe del cliente — independiente del tema rebilling de Jaime. No se mezclan.

---

## 4 · Estado consolidado a 15-ago

- Trato **cerrado y pagado** (invoice, Nueva Conciencia Formación SAC). Alcance facturado por confirmar internamente (`P-08`).
- Subcuenta **creada** en la agencia de Jaime; tenemos acceso.
- Retraso: **~5 días** sobre el arranque de F1.
- Bloqueante Meta (7.1) **sigue sin resolver** y ahora afecta doble: píxel/CAPI **y** el alta de WhatsApp API (ambos requieren Business Manager con admin).
- Cadencia de lanzamiento (`P-01`), número(s) WhatsApp (`P-02`) y fecha del primer lanzamiento siguen abiertos → checklist al cliente.
