# Deltas — llamada técnica del 28-ago (86 min)

Grabación: https://fathom.video/share/_eZDWzzGxhx3qmBSzcaCQNUbLxwG_M_W
Asistentes: Jaime · Oliver · Germán · Henry (Profit) · Luca · Christie · Joaquín (cliente).

Sesión mixta: se ejecutaron las tres llaves técnicas en vivo **y** salieron decisiones de negocio
que cambian el alcance. Los compromisos nuevos se numeran `K10…K14` (siguen a los `K1…K9` de
`01-deltas-llamadas.md`).

---

## 1 · Lo que quedó hecho en la llamada

### Dominio — estaba en GoDaddy, no en Zoho

Se confirmó lo que sospechábamos: **Zoho Mail era el correo, no el dominio**. El dominio
`lanuovacoscienza.com` está en **GoDaddy**; Luca entró con OTP al correo porque no recordaba la
contraseña. Registros cargados y verificados en vivo:

| Tipo | Nombre | Valor | Para qué |
|---|---|---|---|
| CNAME | `eventos` | (valor de GHL) | **Subdominio de la página del evento** |
| TXT | `mail` | `v=spf1 …` | SPF del envío |
| TXT | `smtp` | `k=rsa; p=…` | DKIM |
| CNAME | `email.mail` | `mailgun.org` | Tracking de Mailgun |
| MX | `mail` (prio 0) | `mxa.mailgun.org` | Recepción |
| MX | `mail` (prio 0) | `mxb.mailgun.org` | Recepción |
| TXT | `_dmarc.mail` | política DMARC | Reputación de envío |

Todos verificados en la sesión. El subdominio de envío quedó en `mail.lanuovacoscienza.com`.

> ⚠️ **RIESGO ABIERTO — el dominio puede estar vencido.** Al buscarlo aparecía como *disponible*
> y pidiendo pago. Oliver les avisó de que lo renueven. **Si caduca, se cae la página del evento
> y el envío de correo de golpe.** Confirmar que la renovación se pagó, y ponerle renovación
> automática.

### Meta — portafolio recuperado y accesos dados

Joaquín **sí recuperó** el admin del portafolio (respondía a A1). En la llamada agregó a Germán
como **socio** del grupo de activos comerciales, con acceso total a: las 2 páginas de Facebook
(incluida «Salud Consciente»), la cuenta publicitaria y la cuenta de WhatsApp.

Nunca hubo píxel: **la cuenta publicitaria no tiene ningún activo conectado**. Germán lo crea él.

> ⚠️ **El Meta Business NO está verificado todavía.** Hay que subir los documentos de la empresa.
> Mientras siga en «pendiente», las plantillas de WhatsApp y los límites de mensajería quedan
> restringidos. **Es el bloqueo real que sigue vivo sobre los 13 mensajes.**

### WhatsApp — conectado en coexistencia

Número integrado: **986 199 020** (leído en la llamada; coincide con el del form de onboarding,
aunque Christie lo describió como «número nuevo» — **verificar cuál es**). Enlazado al portafolio
existente, con el dominio como sitio web. Luca vinculó el dispositivo desde WhatsApp Business
compartiendo todos los chats.

Hubo un bug de permisos de GHL con el usuario de Joaquín; Henry lo escaló a soporte y quedó
corregido en la sesión. Coste mencionado: **$30** del plan de coexistencia → va con Jaime.

### Stripe

Jaime quedó de conectarlo desde el modo agencia (Settings → Stripe). **Sin confirmar en la
llamada que se completara.**

---

## 2 · Decisiones que cambian el alcance

### K10 · Lanzamiento simultáneo IT + ES — se cae el «Perú primero» (`P-14`)

Christie lo decidió en la llamada: **se lanza en italiano y español a la vez**.

- **Italiano**: el público está listo, falta material — dos piezas y los videos publicitarios.
- **Español**: material, publicidad y lanzamiento listos, **falta el público**.

**Consecuencia directa:** la réplica italiana vuelve al camino crítico. Las 5 páginas, las 11
plantillas y los 7 emails en italiano dejan de poder diferirse, y **B4 (bloque de validación de
Luca) vuelve a ser urgente**.

### K11 · Luca no cierra en español — hacen falta dos calendarios

**Luca cierra en italiano. Joaquín cierra en español.** Lo dijo Christie explícitamente.

**Rompe lo construido:** hoy existe un único calendario «Llamada de cierre - Perú»
(`yCYC1PwGWrYRxifCIvBX`), pensado para Luca. Hay que:

1. Reasignarlo a **Joaquín** (es el de español), o crearlo de nuevo a su nombre.
2. Crear un **segundo calendario en italiano asignado a Luca**.
3. Cargar los dos links en `link_calendario_cierre_pe` y `link_calendario_cierre_it`.

WF4B ya bifurca por mercado y manda el calendario que toca, así que la estructura aguanta: solo
cambian los destinos.

### K12 · El evento vende, y cae en día distinto por mercado (`P-10`, `P-01`)

Es **masterclass con venta**, no webinar informativo. Y cada mercado tiene su día:

| Mercado | Masterclass | Ventana de venta |
|---|---|---|
| Italiano | **Sábado** | sábado → martes |
| Español | **Jueves** | jueves → lunes |

> La transcripción está entrecortada en esta parte. **Confirmar por escrito** los días y el cierre
> exacto de la ventana antes de programar WF3.

**Rompe lo construido:** hoy hay un único custom value `fecha_evento_vigente` con
`hora_evento_pe` / `hora_evento_it`. Con dos días distintos por mercado hace falta
**fecha por mercado**, no una sola fecha con dos horas. WF3 ancla los recordatorios a ese valor.

Además hay **dos pases diarios** del evento (mediodía y 20:00), no uno.

### K13 · Pase VIP — página de checkout nueva, concedida como bono

Propuesta de Joaquín y Christie: tras registrarse, antes del evento, una **página opcional de
checkout** con un «pase VIP»: repeticiones de las clases + PDFs + bonos. Los eventos son en vivo
y **no quedan grabados ni publicados**, así que la repetición es el gancho real.

Contenido: **4 videos de ~1 h (≈4,5 h en total) + PDF** del material de cada clase.
Motivo de negocio: hoy responden a mano a miles de personas pidiendo la repetición.

**Henry lo aprobó como bono** — dejó dicho que no estaba en el presupuesto. Joaquín manda
referencias de páginas parecidas.

### K14 · El pase VIP es también el destino del no-calificado (`P-05` cambia)

Joaquín lo planteó y quedó aceptado: quien **no califica** para la escuela puede comprar el pack
de videos. Reflexología y Dispersión del dolor **no le sirven — están dirigidos a operadores, no
a personas enfermas**.

**Cambia `P-05`:** la rama del no-calificado deja de ser solo contenido educativo + link al
21 Días; ahora ofrece el pack VIP. Es la primera monetización real de esa rama.

### El link de Zoom cambia en cada llamada

Confirmado por Christie: **no es fijo**. El custom value `link_zoom_llamada` como valor único
**no sirve**. Hay que sacar el link de la cita del calendario, no de un valor global.

---

## 3 · Sigue pendiente del cliente

Lo que Germán quedó de mandar «en limpio» por formulario:

- **Fecha y hora exactas del primer evento** — se dejó para después, es lo único que sigue
  frenando los custom values.
- **Franjas horarias de cierre**: Luca tiene que entrar él mismo a configurar su calendario;
  Joaquín puede configurar el suyo ya.
- **Datos de cobro**: Yape / Plin / transferencia, cuenta y CCI exactos.
- **Logos en fondo transparente.**
- **Legales**: política de privacidad, términos y descargo médico — su abogado.
- **Contenido del no-calificado** + links de compra actuales de 21 Días y Reflexología.

## 4 · Nota de alcance para Henry

Christie apuntó que **son cinco productos**, no los que están contemplados. Reflexología y
Dispersión del dolor son **para operadores**, no para el público enfermo — segmento distinto,
con embudo distinto. Queda para Fase 2, pero conviene que entre en la propuesta de F2.
