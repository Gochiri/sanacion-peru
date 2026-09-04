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

## Antes de mandarlas

- **15 de 17** salen fuera de la ventana: sin plantilla aprobada **no se envían**.
- Los **enlaces en el cuerpo** hacen que Meta revise con más lupa. Si rechaza alguna suele ser por
  eso, y la salida es sacar el enlace a un **botón de URL** de la plantilla en vez de dejarlo en el texto.
- Las de **MARKETING** se rechazan más que las UTILITY. Van clasificadas por lo que hace cada
  mensaje; si Meta discute alguna, se puede reargumentar como UTILITY cuando responde de verdad a
  una acción de la persona.
- **El copy italiano es provisional** — lo produce y valida Luca (P-13). Mejor no mandar esas a
  aprobación hasta que él las revise: **una plantilla aprobada no se edita**, hay que crear otra.
