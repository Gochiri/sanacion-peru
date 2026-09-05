# Plantillas de WhatsApp para aprobación de Meta

Textos sacados **directamente de los workflows** de la subcuenta, no reescritos.

## Cómo funciona esto

Meta solo deja enviar mensajes libres dentro de las **24 h siguientes al último mensaje que
escribió la persona**. Fuera de esa ventana hace falta una **plantilla aprobada**. La aprobación
tarda entre 24 y 48 h, y es el único paso que depende de un tercero — por eso conviene mandarlas
cuanto antes.

Meta **no entiende** las variables de GHL (`{{contact.first_name}}`, `{{custom_values.…}}`): van
numeradas (`{{1}}`, `{{2}}`) y hay que dar un ejemplo de cada una para la revisión. Abajo está
cada mensaje ya convertido, con la correspondencia.

**Nombre de plantilla:** solo minúsculas, números y guiones bajos.

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
Hola {{1}}, registrate aqui: {{2}}
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
Hola {{1}}! Ya estas registrado. Unete al grupo para recibir el acceso: {{2}}
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
Gracias por escribirnos. Te dejamos este contenido para entender la causa emocional del sintoma: {{1}}
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_educativo_es}}` | https://go.hotmart.com/XXXX |


## WF3-ES - Recordatorios de evento

### Recordatorio 24 h

- **Nombre:** `recordatorio_24h_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Manana es la clase: {{1}} a las {{2}}.
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
Hoy es el dia. En 3 horas comenzamos.
```

### Estamos en vivo (trigger link 1:1)

- **Nombre:** `en_vivo_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Estamos comenzando. Entra aqui: {{1}}
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_evento_es}}` | https://eventos.lanuovacoscienza.com/evento-es |

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
Domani e la lezione: {{1}} alle {{2}}.
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
Oggi e il giorno. Tra 3 ore iniziamo.
```

### Estamos en vivo (trigger link 1:1)

- **Nombre:** `en_vivo_it`
- **Idioma:** Italiano (it)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Stiamo iniziando. Entra qui: {{1}}
```

| Meta | GHL | Ejemplo para la revisión |
|---|---|---|
| `{{1}}` | `{{custom_values.link_evento_it}}` | https://eventos.lanuovacoscienza.com/evento-it |

### Recuperacion de no-show (copy suave)

- **Nombre:** `no_show_it`
- **Idioma:** Italiano (it)
- **Categoría:** MARKETING
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Ti sei perso la lezione di oggi, ma ti lasciamo l'essenziale.
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
Tu llamada quedo agendada. Te esperamos.
```

### Recordatorio cita 24 h

- **Nombre:** `recordatorio_cita_24h_es`
- **Idioma:** Español (es)
- **Categoría:** UTILITY
- **¿Necesita plantilla?** **Sí** — sale fuera de la ventana de 24 h

**Texto para Meta:**

```
Manana es tu llamada de cierre.
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
| `{{1}}` | `{{appointment.address}}` | https://zoom.us/j/XXXXXXXXX |


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

- **17 de 19** salen fuera de la ventana: sin plantilla aprobada **no se envían**.
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
