# Form de onboarding — respuesta del cliente (15/16-ago-2026)

Fuente: form submission de GHL (PDF en uploads). Logos extraídos a `assets/brand/`.
**Lo que este form responde ya NO se le pide al cliente.** Lo que abre de nuevo está marcado con ⚠️.

## Datos del negocio

| Campo | Valor | Nota |
|---|---|---|
| Nombre del negocio | **SALUD CONSCIENTE** | ⚠️ El dominio de email es `lanuovacoscienza.com` ("La Nuova Coscienza") → posible marca distinta por mercado (ES vs IT). Confirmar qué marca va en las páginas italianas → `P-11` |
| Responsable | Luca Stefanizzi | |
| Localidad / dirección | Perú · Calle Las Lilas 142 | |
| WhatsApp del negocio | **+51 986 199 020** | ⚠️ Confirmar si es el número actual (NO conectable a la API sin romper su uso en la app y los grupos) o el número nuevo destinado a la API → checklist A2 |
| Instagram | christie.salvatierra | |
| Facebook | Christie Salvatierra Bioterapeuta | |
| TikTok | christiesalvatierra | |
| Horario de atención | lun–vie 9:00–18:00 | Referencia general; para calendarios se necesitan franjas reales de Luca (checklist B5) |
| Email del negocio | info@lanuovacoscienza.com | Candidato a remitente; requiere DNS del dominio (checklist A3) |
| Moneda | $ Dólar | ⚠️ Declarada en genérico; el libro está en soles y falta confirmar EUR para Italia → `P-09` |
| Timezone del form | Europe/Rome (IP peruana) | Consistente con operación en doble huso |

## Productos y precios declarados

| Producto | Precio | Nota |
|---|---|---|
| Sesión personalizada | $70 | ⚠️ Las sesiones 1-a-1 están vivas y con precios de pack — no estaban en el alcance del estimado → `P-12` |
| 3 sesiones | $180 | |
| 6 sesiones | $299 | |
| **Escuela NCA Academy** (high ticket) | **$1.000** | Coincide con la "oferta de cierre" del handoff. ⚠️ Faltan: montos de 2 y 3 cuotas, y precio para Italia (¿EUR?) |
| Videocurso 5 Leyes Biológicas | $100 | |
| Libro "La Nueva Consciencia" | S/ 80 | En **soles** — mezcla de monedas confirmada |

⚠️ Sin precio aún: **21 días**, **dispersión del dolor**, **reflexología emocional** (checklist A6).

## Cobro

| Campo | Valor | Implicación |
|---|---|---|
| ¿Piden seña? | No | |
| Método de pago | **TRANSFERENCIA BANCARIA (IBAN, titular Luca Stefanizzi)** | **Refuerza D8 con fuerza:** la transferencia no es un caso borde — es el método que el cliente declara como principal. La ruta `pago-manual` de F1 debe ser de primera clase, y Stripe se posiciona como el camino automatizado que queremos que crezca. |

## Assets recibidos

- `assets/brand/logo-salud-consciente-vertical.png` (1000×1000)
- `assets/brand/logo-salud-consciente-horizontal.png` (1000×1000)
- Paleta: **oro sobre negro**. ⚠️ Ambos PNG traen el fondo negro **incrustado** (no transparente) → pedir versión transparente o vector (checklist B8); mientras tanto, las páginas se diseñan en tema oscuro donde el logo aparezca.
