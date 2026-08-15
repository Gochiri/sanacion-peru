# HANDOFF — Implementación GHL · Escuela de Sanación Biológica
### Documento de traspaso para retomar el proyecto en Claude Code
**Cliente:** Luca Stefanizzi & Christie Salvatierra (+ Joaquín Vargas, marketing)
**Mercados:** Italia (italiano) y Perú (español)
**Origen:** consultoría de mapeo del 31 de julio de 2026, 108 minutos
**Estado:** mapeo cerrado y aprobado internamente · estimado emitido · pendiente de firma del cliente
**Responsable:** Henry Buenaño · ejecutan Oliver Guerrero y Germán Borrello

> ⚠️ **Nota de vigencia (15-ago):** este documento quedó desactualizado en varios puntos por la llamada de cierre (4-ago) y la llamada interna con Jaime (6-ago). Ver `01-deltas-llamadas.md` y el `mapa-implementacion-v3.md`, que manda sobre este archivo.

---
## 0 · Cómo usar este documento
Este archivo contiene todo lo necesario para planificar y ejecutar la implementación sin volver a leer la transcripción de la llamada. Está ordenado de contexto a ejecución.
Lo que **no** contiene: el detalle conversacional de la sesión con el cliente y las iteraciones de diseño del board. Si hace falta ese nivel, la transcripción original y el board v2 están en los activos del punto 11.
Prioridad de lectura para arrancar rápido: **sección 3** (decisiones cerradas), **sección 6** (corte de fases y horas) y **sección 7** (bloqueantes).
---
## 1 · El cliente en diez líneas
Negocio de infoproductos sobre un método propio de sanación basado en las cinco leyes biológicas: la enfermedad entendida como consecuencia de un conflicto emocional. Ocho años de trayectoria, posicionamiento sólido en Italia, apenas arrancando en Perú.
- **Producto principal (high ticket):** "la escuela", 24 encuentros por cohorte, acceso de por vida. Valor anclado en 10.000 USD, precio regular 1.500–2.000, oferta de cierre 1.000. Pago de contado, 2 o 3 cuotas.
- **Bonos del high ticket:** videocurso 5 leyes biológicas, camino de 21 días, aplicación de síntomas, sesión de 40 min con Christie (solo pago de contado).
- **Cinco productos low ticket:** libro (el más barato), 21 días, dispersión del dolor, 5 leyes biológicas, reflexología emocional (el más caro). Repartidos entre System.io y Hotmart. Se venden solo de forma orgánica en grupos.
- **Stack actual:** System.io (cursos, base, cobros con Stripe), Hotmart (sin base de datos), WhatsApp Business en teléfono sin API, grupos de WhatsApp, Zoom. Sin CRM, sin píxel, sin captura de datos.
- **Números reales:** 17 ventas de high ticket en ~2 meses (8 en junio, 9 la semana previa a la llamada). Cierre cercano al 100% de quien llega a la llamada de venta. Funnel web anterior: 3.000 clics → 5 registros. Grupos italianos de 400+ personas → 20-25 asistentes al webinar.
- **Facturación estimada:** ~8.500 EUR/mes. Este dato define el techo de lo que pueden pagar.
- **Avatar declarado:** persona que ya agotó la medicina tradicional y lleva años sin encontrar solución.
- **Segmentación por síntoma, 4 clusters:** dolores articulares · digestivo (gastritis, reflujo, colon irritable) · ansiedad, pánico, depresión · piel (dermatitis, psoriasis). Un webinar por cluster.
- **Cuello de botella:** Luca hace todo a mano — educa, filtra, agenda, cobra, matricula, persigue cuotas y expulsa morosos, en dos idiomas.
### Estrategia nueva (desde agosto 2026)
Esta es la estrategia sobre la que está construido todo el mapa. La anterior quedó obsoleta y **no debe usarse como referencia**.
Lanzamiento semanal: captación domingo a miércoles → evento el jueves → cierre viernes y sábado → domingo reinicia. Clases "falso en vivo" diarias emitidas por YouTube en lugar de Zoom. WhatsApp como canal central con plantillas.
**Diferencia crítica entre mercados:** en Italia el cierre es masterclass online + llamada de 30 min con Luca. En Perú el cierre es un evento presencial tipo full day en Lima, y la venta ocurre en la sala. Los webinars sí son online en ambos mercados.
---
## 2 · Estado del proyecto
| Fecha | Hito |
|---|---|
| 31-jul-2026 | Consultoría de mapeo, 108 min. Cliente pagó 150 USD por ella. |
| 31-jul-2026 | Mapeo interno completo (roadmap de 29 workflows). |
| 1-ago-2026 | Board de cara al cliente en Claude Design, v1 → v2 con 9 correcciones. |
| 1-ago-2026 | PDF explicativo del mapeo, 11 páginas. |
| 1-ago-2026 | Estimado HTML wide, links de pago creados en modo Live. |
| **Ahora** | Publicando el estimado como paso `/estimado` de un funnel GHL. Falta enviarlo. |
---
## 3 · Decisiones de arquitectura cerradas
Las tomó Henry el 1-ago. **No se reabren sin motivo nuevo.**
### 3.1 Híbrido con System.io — los cursos se quedan
GHL es la fuente única de datos, marketing, ventas y cobro. System.io sigue siendo el aula: **no se migra contenido de cursos**.
Sincronización bidireccional vía API/webhook:
- Pago confirmado en GHL → alta del alumno en System.io por API
- Compra entrante en System.io → webhook → crea o actualiza contacto en GHL
System.io tiene API pública y webhooks — verificado en pantalla durante la llamada. Hotmart queda fuera del alcance de migración; solo se captura al comprador vía webhook para no perderlo.
### 3.2 WhatsApp API coexistente + captura por formulario
- **Número nuevo con API oficial** para el flujo automatizado, plantillas y notificaciones.
- **Número actual de WhatsApp Business de Luca queda intacto**, con sus grupos y su trato personal. La API oficial no administra grupos, así que los grupos siguen siendo manuales.
- **El dato se captura con formulario, no en la conversación.** El asistente conversa, educa y filtra; el formulario de registro es el que guarda. Esta decisión evita depender de que la IA extraiga datos limpios del chat.
Pendiente derivado: definir si es un número API por mercado o uno compartido (ver 7.2).
### 3.3 Los dos mercados en fase 1
Una sola subcuenta, base de contactos unificada con campos `idioma` y `mercado`, y **dos pipelines separados** porque el proceso de cierre difiere. Plantillas, correos y páginas duplicados por idioma mediante réplica, no mediante construcción nueva.
---
## 4 · Estado comercial
### 4.1 Precios cerrados
| Concepto | Precio | Nota |
|---|---|---|
| Fase 1 — El arranque | **$2.100 USD** | $2.250 menos los $150 de la consultoría ya pagada |
| Fase 2 — Sistema completo | **$1.950 USD** | Sin descuento adicional |
| Paquete completo | **$4.050 USD** | $4.200 menos los $150 |
Sin mensualidad, sin permanencia. Pago 50% al confirmar y 50% contra entrega, en ambas fases. Treinta días de soporte tras cada entrega.
### 4.2 Links de pago (Live mode, ya creados)
| Link | Cobra | URL |
|---|---|---|
| ESB Fase 1 Arranque | $1.050 (primer 50%) | `https://link.fastpaydirect.com/payment-link/6a6e953b7b99151a54041c28` |
| ESB Sistema Completo | $2.025 (primer 50%) | `https://link.fastpaydirect.com/payment-link/6a6e9619a655fa0b802a7755` |
**Los segundos pagos no están automatizados.** Se enviaron como links del 50%, no como Split Payments. Hay que agendar manualmente el cobro del saldo contra la entrega — candidato claro a tarea en ClickUp atada al hito de entrega.
### 4.3 Publicación
El estimado se sube como paso de funnel GHL: nombre `Estimado`, URL `/estimado`. Recomendado cambiar a una ruta menos adivinable (`/estimado-escuela-sanacion`) y marcar noindex.
---
## 5 · El mapa técnico
Referencia completa del roadmap. La división en fases está en la sección 6.
### 5.1 Campos personalizados
**Atribución**
| Campo | Tipo | Valores / nota |
|---|---|---|
| `idioma` | Desplegable | ES / IT — bifurca casi todos los workflows |
| `mercado` | Desplegable | Perú-LATAM / Italia |
| `pais` | Texto | |
| `fuente_contacto` | Desplegable | Meta Ads / TikTok / IG orgánico / Telegram / Referido / Base histórica |
| `utm_campaign`, `utm_adset`, `utm_ad` | Texto | Alimentan el reporte por anuncio |
| `estado_ia` | Desplegable | Activa / Pausada / Escalada a humano |
**Calificación**
| Campo | Tipo | Valores / nota |
|---|---|---|
| `cluster_sintoma` | Desplegable | Dolores articulares / Digestivo / Ansiedad-pánico-depresión / Piel / Otro |
| `sintoma_declarado` | Texto largo | En palabras del contacto |
| `tiempo_con_sintoma` | Desplegable | <6 meses / 6-24 meses / +2 años / +5 años |
| `intentos_previos` | Desplegable | Medicina tradicional / Terapias / Ambos / Ninguno |
| `nivel_calificacion` | Desplegable | Califica / A educar / No califica |
| `motivo_descalificacion` | Desplegable | Busca pastillas o medicina / Curiosidad / Sin capacidad de pago / Fuera de mercado |
**Evento**
| Campo | Tipo | Valores / nota |
|---|---|---|
| `lanzamiento` | Texto | Código del lanzamiento semanal, ej. `LNZ-2026-W32-ES` |
| `modalidad_evento` | Desplegable | Online / Presencial (full day Perú) |
| `fecha_evento` | Fecha | |
| `asistio_evento` | Casilla | Se marca desde la página propia del evento |
| `vio_replay` | Casilla | |
**Venta y entrega**
| Campo | Tipo | Valores / nota |
|---|---|---|
| `producto_comprado` | Selección múltiple | Escuela / 21 días / 5 leyes / Dispersión / Reflexología / Libro |
| `plan_pago` | Desplegable | Contado / 2 cuotas / 3 cuotas |
| `cuota_actual` | Número | |
| `estado_pago` | Desplegable | Al día / Fallido / En mora / Completado |
| `cohorte` | Texto | Grupo 1 IT, Grupo 2 IT, Grupo 1 ES… |
| `alta_systemio` | Casilla | Confirma que la API creó el acceso |
| `bono_llamada_christie` | Casilla | Solo pago de contado |
### 5.2 Custom values
Links de formularios, links de registro por mercado, link del aula en System.io, links de pago Stripe por plan, trigger links, zona horaria por mercado, nombre del lanzamiento vigente.
### 5.3 Pipelines
| Pipeline | Etapas |
|---|---|
| Lanzamiento Semanal — ES/Perú | Lead nuevo → Calificado → Registrado → Asistió → Postuló → Llamada agendada → Llamada realizada → Ganado / Perdido / No califica |
| Lanzamiento Semanal — IT/Italia | Idénticas |
| Escalera de Valor (low ticket) | Interés → Checkout iniciado → Comprado → Upsell ofrecido → Upsell comprado |
| Alumnos activos (entrega) | Matriculado → Onboarding → Cursando → Cuota pendiente → En mora → Graduado / Baja |
### 5.4 Calendarios
- Llamada de cierre — Luca / Italia (Europa-Roma, 30 min)
- Llamada de cierre — Luca / Perú (América-Lima, 30 min)
- Sesión bono 40 min — Christie (acceso solo por link tras pago de contado)
### 5.5 Formularios y encuestas
| Código | Nombre | Nota |
|---|---|---|
| F01 / F02 | Registro al evento (ES / IT) | **Punto de captura del negocio.** Nombre, WhatsApp, email, país, cluster, tiempo con el síntoma |
| F03 | Postulación a la escuela | Post-evento, califica antes de gastar una llamada de Luca |
| F04 | Order form low ticket | Uno por producto |
| E01 | Resultado de llamada | Interna, 15 segundos, la llena Luca |
| E02 | Cierre de cohorte + testimonio | Alimenta prueba social |
### 5.6 Funnels y páginas
- Landing de registro al evento (ES + IT)
- Página de gracias con instrucciones y acceso al grupo
- **Página propia del evento en vivo** — YouTube no listado embebido, contador, botón de postulación. Crítico: transmitir en YouTube abierto elimina la medición de asistencia, el CTA y la urgencia.
- Página de replay con caducidad
- Cinco páginas de venta low ticket + order forms + gracias
- Página de postulación
### 5.7 Workflows
Roadmap completo, 29 workflows. En construcción real se consolidan en ~15 (ver 6.2).
**Captación — LS**
| Código | Nombre | Disparador |
|---|---|---|
| LS01 | Origen y atribución | Contacto creado |
| LS02 | Entrada por WhatsApp | Mensaje entrante de número desconocido |
| LS03 | Registro al evento | F01/F02 enviado |
| LS04 | Orgánico y trigger links | Click en trigger link |
| LS05 | Rescate de base histórica | Importación manual |
**Agente de WhatsApp — IA**
| Código | Nombre | Disparador |
|---|---|---|
| IA01 | Calificación y educación | Mensaje entrante |
| IA02 | Escalada a humano | La IA no resuelve o el contacto lo pide |
| IA03 | Reactivación | Sin respuesta a las 24 h |
**Ventas — SP**
| Código | Nombre | Disparador |
|---|---|---|
| SP01 | Confirmación de registro | Formulario enviado |
| SP02 | Recordatorios pre-evento | Programado sobre `fecha_evento` |
| SP03 | Asistencia y no-show | Visita a la página del evento |
| SP04 | Postulación post-evento | Click en botón del evento o F03 |
| SP05 | Agenda de llamada | Cita agendada |
| SP06 | Resultado de llamada | E01 enviada |
| SP07 | Cobro y confirmación | Pago recibido en Stripe |
| SP08 | Ventana de cierre viernes-sábado | Etiqueta "asistió sin comprar" |
| SP09 | Nurturing largo | Oportunidad perdida |
**Entrega — AP**
| Código | Nombre | Disparador |
|---|---|---|
| AP01 | Alta de alumno | Pago confirmado → API System.io |
| AP02 | Onboarding de cohorte | Alta completada |
| AP03 | Recordatorios de encuentros | Programado por cohorte |
| AP04 | **Gestión de cuotas** | Cobro programado / pago fallido |
| AP05 | Cierre de cohorte | Fin del programa |
**Prueba social — PS**
| Código | Nombre | Disparador |
|---|---|---|
| PS01 | Solicitud de testimonio | Fin de cohorte o sesión con Christie |
| PS02 | Registro de testimonio | Testimonio recibido |
**Escalera de valor — EV** *(prefijo propio, extensión a la nomenclatura estándar)*
| Código | Nombre | Disparador |
|---|---|---|
| EV01 | Venta automática low ticket | Order form enviado |
| EV02 | Order bump y upsell | Compra registrada |
| EV03 | Carrito abandonado | Checkout iniciado sin pago |
| EV04 | Campaña a base fría | Manual por campaña |
| EV05 | Ruta del no califica | `nivel_calificacion` = No califica |
### 5.8 Integraciones
| Sistema | Rol | Estado |
|---|---|---|
| Stripe | Cobro | Nativo con GHL. Planes contado / 2 / 3 cuotas con reintentos |
| System.io | Aula | API pública y webhooks confirmados. Alta de alumno + sync inverso |
| Hotmart | Producto suelto | Solo webhook de compra → contacto en GHL. No se migra |
| Meta píxel + CAPI | Medición | **Bloqueado** hasta resolver el admin del portafolio |
| WhatsApp API | Canal | Número nuevo, plantillas de recordatorio y cobro |
| YouTube | Emisión | Video no listado embebido en página propia |
---
## 6 · Corte de fases y realidad de horas
### 6.1 El problema a resolver antes de ejecutar
El precio se cerró contra la capacidad de pago del cliente, no contra el alcance. Eso deja un desajuste que hay que administrar en la ejecución:
| Fase | Precio | Alcance tal como está escrito | Tarifa implícita |
|---|---|---|---|
| Fase 1 | $2.100 | 79 h si se construye todo | **$27/h** |
| Fase 1 recortada | $2.100 | 50 h | $42/h |
| **Fase 1 mínima viable** | $2.100 | **30–36 h** | **$58–70/h** |
| Fase 2 | $1.950 | 68–90 h tal como está listada | **$22–29/h** |
Referencias propias: Termycal cerró a ~$74/h. Jubilando a Perú, $1.951 por una migración completa con chatbot.
**Conclusión operativa:** la Fase 1 es viable si se ejecuta recortada. **La Fase 2 está mal dimensionada** — el alcance listado en el estimado no cabe en $1.950 a ninguna tarifa sana. Es el punto más importante a resolver en Claude Code antes de empezar a construir.
Opciones para la Fase 2, en orden de preferencia:
1. Sacar la escalera de valor (5 páginas + EV01-EV05) a una Fase 3 cotizada aparte. Fase 2 baja a ~40 h → $49/h.
2. Reducir las 5 páginas de venta a una plantilla + 4 réplicas de copy, y automatizar solo 2 productos en la Fase 2.
3. Asumir la tarifa baja como inversión de entrada a un cliente recurrente. Solo si hay expectativa real de un tercer proyecto.
Si el estimado ya fue enviado con el alcance actual, la opción 2 es la única que no requiere renegociar.
### 6.2 Fase 1 — mínimo viable propuesto
Objetivo único: **que desde el primer jueves ninguna persona se pierda**.
- 1 pipeline con campo `mercado` en lugar de 2 pipelines separados
- 4 workflows consolidados en vez de 7:
  - `WF1` Captación y atribución (fusiona LS01 + LS02 + LS04)
  - `WF2` Registro y confirmación (fusiona LS03 + SP01)
  - `WF3` Recordatorios de evento (SP02)
  - `WF4` Asistencia, postulación y agenda (fusiona SP03 + SP04 + SP05)
- Landing de registro + página de evento, con réplica al italiano
- Calendarios de Luca por zona horaria
- Stripe conectado con los tres planes de pago
- Píxel + CAPI con los eventos de registro, asistencia, postulación y compra
- 1 sesión de capacitación
**Fuera de la Fase 1 mínima:** SP06 resultado de llamada, SP08 ventana de cierre, SP09 nurturing, reportes y dashboards. Pasan a Fase 2.
Advertencia: el estimado enviado al cliente menciona la ventana de cierre dentro de la **Fase 2**, así que el recorte es consistente con lo prometido. Verificar antes de construir.
### 6.3 Fase 2 — contenido comprometido en el estimado
Asistente IA bilingüe con escalada a humano · conexión con System.io y alta automática de alumno · entrega de bonos · recordatorios de encuentros · cobro y control de cuotas con reintentos y retiro de acceso · ventana de cierre viernes-sábado · escalera de los 5 productos con páginas de venta · upsell y carrito abandonado · recuperación de base histórica · campañas a base propia · testimonios automáticos · 2 sesiones de capacitación.
---
## 7 · Bloqueantes y dependencias del cliente
### 7.1 Admin del portafolio de Meta — BLOQUEANTE CRÍTICO
Luca no controla quién administra el portafolio. Sin acceso de administrador no se puede instalar píxel ni API de conversiones, y se cae la mitad del valor del proyecto. Si no se resuelve, hay que crear portafolio nuevo y empezar la medición desde cero — con la pérdida de histórico que eso implica.
**Este punto debe estar resuelto antes de facturar el segundo 50%.**
### 7.2 Número de WhatsApp para la API
Uno por mercado o uno compartido. Define cómo se separan Italia y Perú en el enrutamiento y cuántos bots hay que entrenar. Si son dos números, son dos bots → costo adicional no contemplado en el estimado.
### 7.3 Precios finales de los productos
Los 5 low tickets y el high ticket, por mercado y moneda. Sin esto no se arman order forms ni la escalera.
### 7.4 Idioma de cada activo
Los cursos están en italiano y el sistema se construye en español. Falta definir qué productos ya existen en español, cuáles hay que traducir y **quién escribe el copy del embudo en italiano**. La traducción está declarada fuera de alcance en el estimado; si el cliente asume que la hacemos, hay conflicto.
### 7.5 Cierre del full day de Lima
Fechas, aforo, precio de entrada y si el cierre ocurre en sala o con llamada posterior. Define una rama completa del flujo.
### 7.6 Materiales pendientes
- API key de System.io + export de contactos y compradores
- Export de compradores de Hotmart
- Cuenta(s) de Stripe y dominio
- **Contenido de la aplicación de síntomas** — es la base de conocimiento del bot IA. Luca ya ofreció pasarlo.
- Guion del evento del jueves y del pitch
- Disponibilidad real de Luca con zona horaria
- El funnel anterior que no convirtió
---
## 8 · Riesgos técnicos conocidos
1. **Los grupos de WhatsApp no son administrables por API.** Siguen siendo manuales. Si el cliente espera que el sistema los gestione, hay que aclararlo antes de construir.
2. **La página del evento depende de que acepten no transmitir en YouTube abierto.** Si insisten en el canal directo, se pierde asistencia, CTA y urgencia — y varios workflows quedan sin disparador.
3. **Cuenta publicitaria frágil.** Nicho de salud con promesas de sanación: riesgo real de restricción de cuenta. Refuerza el valor de la base propia, pero también implica que el tráfico puede cortarse durante la implementación.
4. **Doble idioma en el bot.** Entrenar y validar en italiano requiere alguien que valide las respuestas. Ni Henry ni el equipo hablan italiano con soltura — depende de Luca.
5. **Sincronización System.io ↔ GHL.** La API está confirmada pero no probada. Vale la pena una prueba de concepto temprana antes de comprometer AP01 en la Fase 2.
6. **Cobro del segundo 50%.** No automatizado. Riesgo puramente operativo, pero real.
---
## 9 · Convenciones y pipeline de ejecución
### 9.1 Cadena de skills
```
transcripción → ghl-onboarding-mapper → ghl-cotizador
             → ghl-clickup-task-builder → ghl-playwright-builder
             → n8n-workflow-builder
```
Estado actual: mapper y cotizador ya ejecutados. **El siguiente paso natural es `ghl-clickup-task-builder`** para convertir el roadmap de la sección 5.7 en subtareas atómicas (1 subtarea = 1 nodo del builder), y de ahí a `ghl-playwright-builder` para construir en la UI.
### 9.2 Convenciones fijas
- Nomenclatura de workflows: prefijos `LS` / `SP` / `AP` / `RP` / `PS`. `IA` y `EV` son extensiones propias de este proyecto.
- HTML para GHL: layout wide obligatorio, reset del builder con `!important`, `.page` full-bleed, clases con prefijo `pt-`, tokens de marca bloqueados. Skill `ghl-html-wide`.
- Mapas de cara al cliente: estilo del board VN SKCB, lenguaje de negocio, sin códigos técnicos. Solo entra como pendiente lo que cambia lo que se construye.
- La subcuenta de este cliente **aún no existe**. El Location ID que aparece en las notas de la CLI corresponde a otra cuenta. *(Desactualizado: la subcuenta ya existe, en la agencia de Jaime — ver deltas.)*
### 9.3 Nota sobre el cotizador
La tabla de precios de `ghl-cotizador` está descalibrada hacia arriba y produce números impresentables para clientes de LATAM directo. Dos correcciones pendientes:
- **Decaimiento por volumen:** el workflow 15 no cuesta lo mismo que el 4. Sugerido: los primeros 3 a precio pleno, del 4 al 8 al 50%, del 9 en adelante al 33%.
- **Precio de réplica:** una página o secuencia clonada a otro idioma debe costar ~30-35% de la unidad nueva, no el 100%.
Con esas dos correcciones, este proyecto habría salido cerca de $5.500 en la tabla, en lugar de $11.855.
---
## 10 · Punto a revisar antes de enviar
El estimado dice "válido 30 días" en el encabezado y en el pie. Es un marco de caducidad, y el criterio actual es redactar los términos en tono de relación continuada en lugar de cotización con vencimiento. Vale la pena decidir si se quita o se suaviza antes de publicar el funnel.
También: el `.pt-header` del estimado usa la línea de marca en texto en lugar del logo PNG que ya está fijado en la skill `ghl-html-wide`. Si se quiere consistencia con las demás propuestas, hay que sustituirlo.
---
## 11 · Activos generados
| Archivo | Contenido |
|---|---|
| `mapeo-ghl-escuela-sanacion-v1.md` | Roadmap técnico interno completo, 29 workflows |
| `Mapeo de Operacion - Escuela de Sanacion Biologica.pdf` | Documento explicativo de cara al cliente, 11 páginas |
| `prompt-claude-design-mapa-escuela-sanacion.md` | Prompt del board visual v1 |
| `correcciones-board-v2-claude-design.md` | Las 9 correcciones aplicadas al board |
| `estimado-escuela-sanacion-GHL.html` | Estimado wide con links de pago Live |
| Board Claude Design v2 | 14 secciones, 1600×4400 px |
Placeholders pendientes en el HTML del estimado: `PON_AQUI_TU_EMAIL` y `PON_AQUI_TU_WEB`.
---
## 12 · Preguntas abiertas para resolver en Claude Code
1. ¿Se re-escopea la Fase 2 antes de enviar el estimado, o se asume la tarifa baja? (sección 6.1)
2. ¿Un número de WhatsApp API o dos? Define arquitectura de enrutamiento y número de bots.
3. ¿Prueba de concepto temprana de la API de System.io antes de comprometer AP01?
4. ¿El bot IA se construye con Conversation AI nativo de GHL o con n8n como orquestador? El contenido de la app de síntomas puede ser grande para la KB nativa.
5. ¿Cómo se maneja la validación del italiano en el bot? Depende de Luca y es un riesgo de cronograma.
6. ¿Se generan las tareas en ClickUp para las dos fases desde ya, o solo la Fase 1?
7. ¿El full day de Lima requiere su propio flujo de venta de entradas, o entra como evento sin cobro?
