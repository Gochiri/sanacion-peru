# Mapa visual de la Fase 1

**https://claude.ai/code/artifact/65a295a1-24fb-4d21-b298-e43e5f7e6c70**

Recorrido completo de un lead por el sistema, construido leyendo el estado real de la subcuenta
por API (no el diseño teórico). Cada parada muestra la automatización, su disparador real, las
etiquetas que pone o lee, la etapa del CRM y los campos que escribe.

Sirve para dos cosas: que el equipo vea el sistema entero de una vez, y **enseñárselo al cliente en
la llamada** — cambia la conversación de "nos piden cosas" a "esto ya está armado".

## Qué muestra

Las 8 paradas del recorrido: entrada de tráfico → WF1 captación → survey F01 → WF2 calificación
→ WF3 recordatorios → evento y WF4A asistencia → F03 y WF4B postulación → WF4C cita → cierre manual
de Luca → WF5 cobro.

Las tres bifurcaciones reales se dibujan, no se describen: idioma por prefijo (WF1), calificado vs
descalificado (WF2), primer pago vs cuota (WF5).

## Lo que el mapa deja a la vista

- **13 mensajes de WhatsApp** escritos y colocados, esperando la conexión del número
- **4 eventos hacia Meta** que ni siquiera se pueden crear sin el permiso del portafolio
- **WF4A sin disparador**: espera la página del evento, que espera el dominio
- **13 de 23 datos** por completar (fecha del evento, links de pago, Zoom…)
- **La etapa «Calificado» está huérfana**: ningún flujo la usa, los registrados pasan directo de
  *Lead nuevo* a *Registrado*. Conviene eliminarla o darle uso para que el embudo no muestre una
  columna siempre vacía.

## Regenerarlo

El volcado del flujo real sale de recorrer los workflows por API (triggers, pasos, condiciones,
tags y etapas). Si cambia el sistema, releerlo y republicar el mismo archivo mantiene la URL.
