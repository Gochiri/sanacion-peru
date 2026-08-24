# Formularios a crear en la UI

El API no permite crearlos (público: *"route not supported by the IAM Service"*; interno: 404/403),
así que van a mano. Aquí está la especificación exacta.

**Solo hacen falta los de español**: el cliente confirmó que arranca con Perú (`P-14`).
La réplica italiana (F02) queda para cuando Italia entre al plan.

> ⚠️ **Lo más importante:** cada pregunta debe mapear al campo personalizado que ya existe.
> Los workflows leen esos campos por su `fieldKey` — si se crea un campo nuevo en vez de usar
> el existente, WF2 no encuentra la calificación y **todo el ruteo se cae**.
> En el builder: *Add Element → Custom Fields* y elegir el que ya está, **no crear uno nuevo**.

---

## F01 · Registro al evento (español)

**Tipo:** Encuesta (Survey), no formulario simple — hace falta la lógica de descalificación.
**Dónde va:** embebida en la página `/registro-es`.
**Es el punto de captura del negocio**: hoy los leads se pierden porque nadie los guarda.

### Paso 1 — Datos

| Campo | Tipo | Obligatorio | Mapea a |
|---|---|---|---|
| Nombre | Standard: First Name | Sí | — |
| Apellido | Standard: Last Name | No | — |
| WhatsApp | Standard: Phone | Sí | — |
| Email | Standard: Email | Sí | — |
| País | **`contact.pais`** (Pais) | Sí | campo existente |

### Paso 2 — Consentimientos (obligatorios)

Dos casillas separadas. **No son opcionales**: la encuesta captura datos de salud de personas
en la UE (Italia), que el RGPD trata como categoría especial (Art. 9), y Meta exige poder
demostrar el opt-in para mensajes iniciados por el negocio.

- ☑ *"Acepto la política de privacidad y el tratamiento de mis datos de salud"* → enlazar la política
- ☑ *"Acepto recibir información por WhatsApp y correo"*

### Reparto en slides

| Slide | Contenido |
|---|---|
| 1 | Datos + los 2 consentimientos |
| 2 | Q1 cluster · Q1b síntoma en texto · Q2 tiempo |
| **3** | **Q3 — la eliminatoria** (último slide) |

### Paso 3 — Calificación

**Q1 · ¿Cuál de estos describe mejor lo que vives hoy?** → **`contact.cluster_sintoma`**
Opciones (exactas, ya existen en el campo):
`Dolores articulares` · `Digestivo` · `Ansiedad-panico-depresion` · `Piel` · `Otro`
*(segmenta el cluster, no descalifica)*

**Q1b · Cuéntanos en una frase qué vives** → **`contact.sintoma_declarado`** (texto largo, opcional)
*(pregunta aparte: la opción "Otro" de Q1 no escribe en un segundo campo)*

**Q2 · ¿Hace cuánto buscas solución?** → **`contact.tiempo_con_sintoma`**
`Menos de 6 meses` · `6-24 meses` · `Mas de 2 anos` · `Mas de 5 anos`

**Q3 · ¿Qué esperas encontrar en esta clase?** → **`contact.nivel_calificacion`** — la eliminatoria

Es la última pregunta del survey. **Arrastrar el campo personalizado `Nivel calificacion`**: sus
opciones ya vienen con el texto correcto y **el builder no deja editarlas desde el formulario**
(se editan en el campo, cosa que ya está hecha).

| Opción que ve el visitante | Qué significa internamente |
|---|---|
| Entender por que mi cuerpo enfermo y como sanarlo | **Califica** → va al grupo |
| Un medicamento o tratamiento medico | **No califica** → ruta educativa |
| Solo tengo curiosidad | **A educar** → ruta educativa |

*(sin tildes: GHL las elimina y rompería la coincidencia con lo que lee WF2)*

### Q4 se elimina

La pregunta de inversión ("¿estarías dispuesto/a a invertir?") **no va en el formulario**.

Motivo: al arrastrar un campo personalizado, **cada pregunta muestra TODAS las opciones del campo**.
Como Q3 y Q4 escribían en `nivel_calificacion`, el campo habría necesitado las 3 opciones de Q3 más
las 2 de Q4, y ambas preguntas mostrarían las 5 mezcladas. Separarlas en dos campos tampoco
resuelve: GHL no admite bifurcaciones anidadas ni encadenadas (verificado), así que WF2 solo puede
rutear por una.

Q3 ya filtra lo que de verdad duele —el que busca pastillas y el curioso—, que es el dolor que
describió Luca. El matiz "no quiero invertir" se recupera en Fase 2, cuando el asistente califique
en conversación. Además el formulario queda más corto, que ayuda a la conversión.

### Cómo se escribe el resultado

**`contact.nivel_calificacion`** lo escribe Q3 directamente. Es el campo por el que WF2 rutea todo
el registro.

⚠️ **WF2 compara contra la frase completa**, no contra la palabra `Califica`:
`nivel_calificacion == "Entender por que mi cuerpo enfermo y como sanarlo"`.
Si alguien edita el texto de esa opción en el campo, **hay que ajustar WF2 o el ruteo se cae**.

**`contact.motivo_descalificacion`** queda **sin llenar en Fase 1**, a propósito.

La idea era que WF2 lo dedujera del nivel, pero eso exige una bifurcación dentro de otra y
**GHL no admite bifurcaciones anidadas** (probado: rechaza el workflow entero). Escribir un valor
fijo para toda la rama descalificada contaminaría el reporte, porque ahí caen tanto los que buscan
medicina como los curiosos.

No se pierde nada relevante: **`nivel_calificacion` ya distingue los dos grupos** —`No califica`
son los que buscan medicina, `A educar` los curiosos y los de "solo gratis"—, que es lo que hace
falta para el reporte de Fase 1. El matiz curiosidad-vs-solo-gratis se recupera en Fase 2, cuando
el asistente califique en conversación.

### Campos ocultos (hidden)

`contact.utm_campaign` · `contact.utm_adset` · `contact.utm_ad` · `contact.fuente_contacto` ·
`contact.idioma` (valor fijo `ES`) · `contact.mercado` (valor fijo `Peru-LATAM`)

Sin estos, el reporte por anuncio de Joaquín no funciona.

### Al enviar

- **Califica** → redirigir a `/gracias-es`
- **No califica / A educar** → redirigir a `/comienza-aqui-es`

⚠️ **Prueba obligatoria antes de dar por bueno:** rellenar la encuesta eligiendo la opción
descalificadora de Q3 y verificar que **el contacto queda creado igual y con sus respuestas
guardadas**. Si al descalificar no se registra el contacto, la secuencia educativa de WF2 nunca
corre y **esos leads se pierden en silencio** — que es justo lo contrario del objetivo. Si eso
pasa, avísame: hay un plan B (encuesta sin descalificación y que el ruteo lo haga entero WF2).

⚠️ **Comprobar el valor guardado:** tras enviar, abrir la ficha del contacto y verificar que
`Nivel calificacion` contiene la frase completa. Es lo que compara WF2.

---

## F03 · Postulación a la escuela (español)

**Tipo:** Formulario simple, corto.
**Dónde va:** página `/postulacion-es`, a la que lleva el botón de la página del evento.
**Su envío es el disparador de WF4B**, que mueve a *Postuló* y manda el link del calendario.

| Campo | Tipo | Obligatorio |
|---|---|---|
| Nombre | Standard: First Name | Sí |
| WhatsApp | Standard: Phone | Sí — reconfirmar, es por donde se le escribe |
| Email | Standard: Email | Sí |
| *"¿Qué te gustaría resolver con la escuela?"* | Texto largo → **`contact.sintoma_declarado`** | No |
| *"¿En qué franja te viene mejor la llamada?"* | Desplegable: Mañana / Tarde / Noche | Sí |

**Al enviar:** mensaje de confirmación (*"te escribimos por WhatsApp para agendar"*).
El link del calendario **no va en la página**: lo manda WF4B 1:1 por WhatsApp, para que quede
trazado quién agendó.

---

## Después de crearlos

Pásame los **IDs de los dos formularios** (salen en la URL del builder o con `./ghl forms list`)
y yo:
1. conecto los triggers de WF2 y WF4B, que hoy están sin disparador;
2. lleno los custom values `link_registro_es` y los de las páginas;
3. ajusto WF2 según cómo hayas resuelto el mapeo de Q3/Q4.
