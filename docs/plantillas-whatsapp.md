# Plantillas de WhatsApp para aprobación de Meta

Textos sacados de los workflows de la subcuenta y **repasados el 5-sep** en dos cosas.

**Género.** Ningún mensaje asume si quien lo lee es hombre o mujer. Nada de «ya estás
registrado», y tampoco «registrado/a» entre paréntesis, que se lee peor. De las 19 solo dos lo
tenían: la bienvenida en español pasó a *«tu registro está listo»*, y el no-show italiano de
*«ti sei perso»* a *«hai saltato»* — con *avere* el participio no concuerda, así que vale para
cualquiera.

**Acentos.** Los quince que salieron de nodos del builder venían sin ellos. Esto lo lee un
cliente en su teléfono: «Manana es la clase» y «el sintoma» se ven como un descuido.

> Los nodos de los workflows **siguen con el texto viejo** y no pasa nada: hoy son `sms` con el
> texto dentro, y al convertirlos a WhatsApp pasarán a referenciar la plantilla aprobada. Manda
> el texto de Meta. Al hacer esa conversión, copiar de aquí y no del nodo.

**7-sep.** Meta aprobó las 19 y quedan **cinco por mandar**: las de WF2-IT y las tres italianas
de WF4C, que no estaban en la lista original y sin las cuales esos cuatro nodos no se pueden
convertir. Están abajo, en sus secciones. Van 15 de 19 nodos convertidos; los ids que GHL guarda
para cada plantilla viven en `PLANTILLAS`, en `builders/esb_lib.py`, porque **no hay endpoint que
los liste**.

## Cómo funciona esto

Meta solo deja enviar mensajes libres dentro de las **24 h siguientes al último mensaje que
escribió la persona**. Fuera de esa ventana hace falta una **plantilla aprobada**. La aprobación
tarda entre 24 y 48 h, y es el único paso que depende de un tercero — por eso conviene mandarlas
cuanto antes.

Meta **no entiende** las variables de GHL (`{{contact.first_name}}`, `{{custom_values.…}}`): van
numeradas (`{{1}}`, `{{2}}`) y hay que dar un ejemplo de cada una para la revisión. Abajo está
cada mensaje ya convertido, con la correspondencia.

**Nombre de plantilla:** solo minúsculas, números y guiones bajos.

**El cuerpo no puede empezar ni terminar con una variable.** Es regla de Meta y GHL la aplica
al crear: *«Your body can't start or end with a variable»*. Y **un punto después de la variable no cuenta
como texto**: GHL lo rechaza igual. Diez de las diecinueve terminaban en variable o en variable
más punto, así que llevan una línea de cierre después — corta, neutra y que sume algo
(*«Te toma un minuto»*, *«Te esperamos dentro»*), no un punto pegado a la variable por cumplir.

---


## WF1 - Captacion y atribucion

### Link de registro IT

- **Nombre:** `respuesta_entrada_desconocido_it`
- **Idioma:** Italiano (it)
- **Categoría:** MARKETING
- **¿Necesita plantilla?** No siempre: responde a alguien que acaba de escribir, así que suele caer dentro de la ventana. Conviene tenerla igual por si contesta al día siguiente.

**Texto para Meta:**

```
Ciao {{1}}, iscriviti qui: {{2}}

Ci vuole un minuto.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{contact.first_name}}` | María |
| `{{2}}` | `{{custom_values.link_registro_it}}` | https://eventos.lanuovacoscienza.com/registro-it |

### Link de registro ES

- **Nombre:** `respuesta_entrada_desconocido_es`
- **Idioma:** Español (es)
- **Categoría:** MARKETING
- **¿Necesita plantilla?** No siempre: responde a alguien que acaba de escribir, así que suele caer dentro de la ventana. Conviene tenerla igual por si contesta al día siguiente.

**Texto para Meta:**

```
Hola {{1}}, regístrate aquí: {{2}}

Te toma un minuto.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{contact.first_name}}` | María |
| `{{2}}` | `{{custom_values.link_registro_es}}` | https://eventos.lanuovacoscienza.com/registro-es |


## WF2 - Registro y calificacion

### Bienvenida con link del grupo

- **Nombre:** `bienvenida_registro_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Hola {{1}}, tu registro está listo. Únete al grupo para recibir el acceso: {{2}}

¡Nos vemos en el grupo!
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{contact.first_name}}` | María |
| `{{2}}` | `{{custom_values.link_grupo_whatsapp_es}}` | https://chat.whatsapp.com/XXXX |

### Contenido educativo (sin link de grupo)

- **Nombre:** `educativo_no_califica_es`
- **Idioma:** Español (es)
- **Categoría:** MARKETING
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Gracias por escribirnos. Te dejamos este contenido para entender la causa emocional del síntoma: {{1}}

Sin prisa: es para verlo cuando puedas.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_educativo_es}}` | https://go.hotmart.com/XXXX |


## WF2-IT - Registrazione e qualifica

Las dos que faltaban. WF2-IT se duplicó de WF2 el 4-sep y **quedó publicado y disparando** sin
que sus plantillas existieran en Meta: hasta que estas dos se aprueben, sus dos nodos siguen
como `sms`. Traducción provisional — la valida Luca (P-13/B4).

### Bienvenida con link del grupo

- **Nombre:** `bienvenida_registro_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Ciao {{1}}, la tua iscrizione è confermata. Entra nel gruppo per ricevere l'accesso: {{2}}

Ci vediamo nel gruppo!
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{contact.first_name}}` | Giulia |
| `{{2}}` | `{{custom_values.link_grupo_whatsapp_it}}` | https://chat.whatsapp.com/XXXX |

> «Sei registrato» era la traducción directa, pero en italiano concuerda en género: le habría
> dicho *registrato* a una mujer. `La tua iscrizione è confermata` no concuerda con nadie.

### Contenido educativo (sin link de grupo)

- **Nombre:** `educativo_no_califica_it`
- **Idioma:** Italiano (it)
- **Categoría:** MARKETING
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Grazie per averci scritto. Ti lasciamo questo contenuto per capire la causa emotiva del sintomo: {{1}}

Con calma: è da guardare quando puoi.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_educativo_it}}` | https://go.hotmart.com/XXXX |


## WF3-ES - Recordatorios de evento

### Recordatorio 24 h

- **Nombre:** `recordatorio_24h_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Mañana es la clase: {{1}} a las {{2}}.

Te avisamos por aquí cuando empecemos.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.fecha_evento_es}}` | jueves 18 de septiembre |
| `{{2}}` | `{{custom_values.hora_evento_pe}}` | 8:00 p. m. |

### Recordatorio 3 h

- **Nombre:** `recordatorio_3h_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Hoy es el día. En 3 horas comenzamos.
```

### Estamos en vivo (trigger link 1:1)

- **Nombre:** `en_vivo_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Estamos comenzando. Entra aquí: {{1}}

Te esperamos dentro.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{trigger_link.zsM5LP4jGLvvLbNG8hXy}}` | https://eventos.lanuovacoscienza.com/evento-es |

> **No es `link_evento_es`.** El enlace tiene que ser el *trigger link* `evento-es-en-vivo`, que
> es lo que dispara WF4A y marca la asistencia. Con el custom value entra igual, pero no queda
> registrado y le acaba llegando el mensaje de no-show. El valor de la variable se puede cambiar
> sin volver a pasar por Meta.

### Recuperacion de no-show (copy suave)

- **Nombre:** `no_show_es`
- **Idioma:** Español (es)
- **Categoría:** MARKETING
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Te perdiste la clase de hoy, pero te dejamos lo esencial.
```


## WF3-IT - Promemoria evento

### Recordatorio 24 h

- **Nombre:** `recordatorio_24h_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Domani è la lezione: {{1}} alle {{2}}.

Ti avvisiamo qui quando iniziamo.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.fecha_evento_it}}` | sabato 20 settembre |
| `{{2}}` | `{{custom_values.hora_evento_it}}` | 20:00 |

### Recordatorio 3 h

- **Nombre:** `recordatorio_3h_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Oggi è il giorno. Tra 3 ore iniziamo.
```

### Estamos en vivo (trigger link 1:1)

- **Nombre:** `en_vivo_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Stiamo iniziando. Entra qui: {{1}}

Ti aspettiamo dentro.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{trigger_link.Y5dtDFxPynXgvi9hqp91}}` | https://eventos.lanuovacoscienza.com/evento-it |

> El trigger link italiano (`evento-it-en-vivo`) se creó el 7-sep: hasta entonces solo existía el
> español, así que en Italia **no se marcaba la asistencia de nadie**.

### Recuperacion de no-show (copy suave)

- **Nombre:** `no_show_it`
- **Idioma:** Italiano (it)
- **Categoría:** MARKETING
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Hai saltato la lezione di oggi, ma ti lasciamo l'essenziale.
```


## WF4B - Postulacion

### Enviar calendario Italia

- **Nombre:** `postulacion_agenda_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Prenota la tua chiamata: {{1}}

Scegli l'orario che preferisci.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_calendario_cierre_it}}` | https://api.leadconnectorhq.com/widget/booking/XXXX |

### Enviar calendario Peru

- **Nombre:** `postulacion_agenda_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Agenda tu llamada de cierre: {{1}}

Elige el horario que mejor te venga.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_calendario_cierre_pe}}` | https://api.leadconnectorhq.com/widget/booking/XXXX |


## WF4C - Cita agendada

### Confirmacion de cita

- **Nombre:** `confirmacion_cita_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Tu llamada quedó agendada. Te esperamos.
```

### Recordatorio cita 24 h

- **Nombre:** `recordatorio_cita_24h_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Mañana es tu llamada de cierre.
```

### Recordatorio cita 1 h + Zoom

- **Nombre:** `recordatorio_cita_1h_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
En 1 hora es tu llamada. Enlace: {{1}} (instala Zoom antes para no perder tiempo).
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_zoom_llamada_es}}` | https://zoom.us/j/XXXXXXXXX |

> Antes apuntaba a `{{appointment.address}}`, que **no está en el selector** de la plantilla
> (ofrece contacto y custom values, no campos de la cita) y que además **resolvía a nada**: la
> ubicación de reunión de los calendarios está vacía. El Zoom de Joaquín vive en
> `link_zoom_llamada_es`, que hoy está en `PENDIENTE` — checklist **B9**, sin cerrar.


### Confirmacion de cita — Italia

- **Nombre:** `confirmacion_cita_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY

**Texto para Meta:**

```
La tua chiamata è fissata. Ti aspettiamo.
```

### Recordatorio cita 24 h — Italia

- **Nombre:** `recordatorio_cita_24h_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY

**Texto para Meta:**

```
Domani è la tua chiamata.
```

### Recordatorio cita 1 h + Zoom — Italia

- **Nombre:** `recordatorio_cita_1h_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY

**Texto para Meta:**

```
Tra 1 ora è la tua chiamata. Link: {{1}} (installa Zoom prima, per non perdere tempo).
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_zoom_llamada_it}}` | https://zoom.us/j/XXXXXXXXX |

> Las tres son de **WF4C, que hoy no filtra por mercado**: su trigger es `customer_appointment`
> sin condición, así que un italiano que agenda recibe los tres mensajes en español con el Zoom
> de Perú. Con estas aprobadas se le añade la bifurcación por `Mercado`, como la de WF4B.

---

## Cierre manual — no salen de un workflow

Las 17 de arriba están sacadas de nodos de workflow. **Estas dos no**: las manda una persona
desde la conversación, al terminar la llamada de cierre. Aun así necesitan aprobación, porque
casi siempre salen fuera de la ventana de 24 h.

Van con acentos, a diferencia del resto. Las otras vienen de los nodos del builder, que se
escribieron sin ellos; estas se redactan ahora y las lee alguien justo antes de mover $1.000.

⚠️ **Los datos bancarios van en el cuerpo, no como variable.** WhatsApp rechaza parámetros
que contengan saltos de línea, tabulaciones o cuatro espacios seguidos, y el bloque bancario
son cinco líneas. Solo el nombre va como `{{1}}`.

Eso tiene un precio: **una plantilla aprobada no se edita**. Si cambia la cuenta hay que crear
otra y volver a esperar. Se asume porque una cuenta bancaria no cambia en mitad de un
lanzamiento, y la alternativa —un CCI de 20 dígitos tipeado a mano en cada cierre— falla mucho
más seguido.

> **La italiana ya se puede mandar.** Joaquín confirmó el 4-sep que la cuenta es de Luca a
> título personal. La peruana espera una sola cosa: si la razón social lleva S o no. Como el
> nombre queda escrito dentro de la plantilla y después no se edita, se aprueba con el dato
> bueno o no se aprueba.

### Datos de pago - Perú

- **Nombre:** `datos_pago_pe`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h
- **La manda:** Joaquín, al cerrar la llamada

**Texto para Meta:**

```
Hola {{1}}, estos son los datos para la transferencia:

Titular: Nueva Consciencia Formación
Banco: BCP · cuenta en soles
Cuenta: 1937405302029
CCI: 00219300740530202918

Cuando la hagas, mándanos el comprobante por aquí y te confirmamos el acceso.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{contact.first_name}}` | María |

**Se llama `datos_pago_pe`, no `datos_pago_es`, a propósito.** Lleva la cuenta del BCP en soles
escrita en el cuerpo, así que sirve para Perú y **solo** para Perú. Fuera de Perú el resto de
Latinoamérica cobra por giro, y esos datos los escribe a mano el que cierra (ver
`docs/sop-cierre.md`). El nombre del archivo es lo único que evita que alguien se la mande a un
colombiano por descuido.

⚠️ El titular sigue **pendiente de confirmar en un punto**: el 4-sep Joaquín cerró que la razón
social es «Nueva Consciencia Formación» **sin «SAC»** —«sin saco», dijo—, y eso ya está aplicado.
Lo que el transcript no distingue es la **S** de «Con**s**ciencia»: Fathom normaliza la ortografía.
Va la grafía del mensaje escrito del cliente. No bloquea el cobro —el CCI encamina por el número
de cuenta— pero una vez aprobada la plantilla no se corrige, así que conviene mirar el mensaje
original antes de mandarla.

### Dati di pagamento - Italia

- **Nombre:** `datos_pago_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h
- **La manda:** Luca, al cerrar la llamada

**Texto para Meta:**

```
Ciao {{1}}, questi sono i dati per il bonifico:

Intestatario: Luca Stefanizzi
Banca: Intesa Sanpaolo
IBAN: IT98L0306979654100000006623

Quando l'hai fatto, mandaci la ricevuta qui e ti confermiamo l'accesso.
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{contact.first_name}}` | Giulia |

El intestatario lo confirmó Joaquín el 4-sep: en Italia no hay empresa, la cuenta es de Luca a
título personal. Ya estaba escrito desde el onboarding —`docs/fuentes/02-form-onboarding.md:40`
dice «titular Luca Stefanizzi»— y no lo habíamos conectado. Importa que esté: desde octubre de
2025 los bancos de la UE verifican el nombre del beneficiario contra el IBAN antes del bonifico.

Copy provisional por P-13, como el resto del italiano: lo valida Luca.


---

## Antes de mandarlas

- **22 de 24** salen fuera de la ventana: sin plantilla aprobada **no se envían**.
- Los **enlaces en el cuerpo** hacen que Meta revise con más lupa. Si rechaza alguna suele ser por
  eso, y la salida es sacar el enlace a un **botón de URL** de la plantilla en vez de dejarlo en el texto.
- Las de **MARKETING** se rechazan más que las UTILITY. Van clasificadas por lo que hace cada
  mensaje; si Meta discute alguna, se puede reargumentar como UTILITY cuando responde de verdad a
  una acción de la persona.
- **El copy italiano es provisional** — lo produce y valida Luca (P-13). Mejor no mandar esas a
  aprobación hasta que él las revise: **una plantilla aprobada no se edita**, hay que crear otra.
- **De las dos de cobro, la italiana ya está lista** (llamada del 4-sep: intestatario Luca
  Stefanizzi). La peruana espera un solo dato, y por eso es pregunta de hoy: los datos bancarios
  van escritos en el cuerpo, así que se aprueba bien o se aprueba mal, no hay arreglo después.

  | Falta | Plantilla | Sin eso |
  |---|---|---|
  | ¿«Consciencia» o «Conciencia»? | `datos_pago_pe` | Cobra igual, pero el comprador lee un nombre que no es el del banco |
