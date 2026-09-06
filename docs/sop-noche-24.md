# SOP · La noche del 24 — cambiar de ciclo

Es la única operación del lanzamiento que **no avisa si se olvida**. Si no se hace, quien se
registre el 25 recibe recordatorios del webinar que ya pasó, y los que se registren esa misma
noche con la fecha vieja puesta reciben la cadena entera de golpe.

**Cuándo:** el jueves 24, en cuanto termine el webinar LATAM (empieza 20:00 Perú). **Esa
noche, no a la mañana siguiente.** El campo del evento se fija al entrar al workflow: cada
minuto con la fecha vieja es gente que entra apuntando al pasado.

**Cuánto tarda:** diez minutos. Tres comandos y tres pegados.

---

## 1 · Cargar el ciclo 2

```
python3 builders/valores.py ciclo 2 --aplicar
```

Cambia siete valores: las fechas de LATAM (jueves 1-oct) y de Italia (sábado 3-oct) en sus
tres formatos —texto, ISO para las páginas, y el de GHL para las esperas— y el nombre del
lanzamiento. Comprobar que la salida dice `→` en las siete líneas, no `=`.

## 2 · Regenerar y volver a pegar las tres páginas con fecha

```
python3 builders/previsualizar.py --ghl paginas/registro-es.html paginas/gracias-es.html paginas/evento-es.html
```

Las páginas llevan la fecha **escrita dentro** —GHL no sustituye merge fields—, así que las
tres que la muestran hay que regenerarlas y pegarlas de nuevo en su Custom Code:

| Página | Dónde aparece la fecha |
|---|---|
| `registro-es` | La ficha del evento y la barra fija de abajo |
| `gracias-es` | La ficha y el botón de «añadir al calendario» |
| `evento-es` | La cuenta atrás |

`agenda-es`, `postulacion-es` y `comienza-aqui` no llevan fecha: **no se tocan.**

## 3 · Comprobar

```
python3 builders/auditar.py
```

Y abrir `registro-page` en el navegador: la ficha tiene que decir **jueves 1 de octubre**.

---

## Lo que NO se hace esa noche

- **No se tocan los workflows.** Las esperas están ancladas a `fecha_evento_es_ghl`, que es uno
  de los siete valores del paso 1. Cambiar el valor las mueve solas.
- **No se tocan los calendarios.** La disponibilidad de cierre ya cubre las dos semanas
  (25-sep a 10-oct) desde el principio.
- **No se cambian las plantillas de WhatsApp.** Leen la fecha del custom value al enviar.

## Si algo sale mal

`valores.py ciclo 1 --aplicar` vuelve al estado anterior. Las páginas se regeneran igual.

## Después del 3 de octubre

Ya no hay ciclo 3. Los workflows siguen publicados y las páginas con la fecha del 1-oct; quien
se registre después recibe una espera anclada a una fecha pasada. **Antes del 4-oct hay que
decidir**: o despublicar WF3-ES/IT y WF6, o cargar las fechas del siguiente lanzamiento.
