# Zoo Center — sitio web

Memoria del proyecto para cualquier sesión de Claude que lo retome. Se trabaja
con la skill `metodo-web-negocio-local`. **Este archivo está en un repo
público:** nada de montos del abono, contraseñas ni datos privados del dueño.

## Qué es

Web de una página para **Zoo Center**, petshop y veterinaria de Mar del Plata
con dos sucursales. Hasta ahora no tenía web: todo pasaba por Instagram
(@zoocentermdp) y un WhatsApp. La web junta servicios, catálogo, promos y
sucursales, y todo termina en un WhatsApp o en un pedido de turno.
Armada por Mateo Berchot en octubre de 2026 (todavía en etapa de demo para el dueño).

- Sitio: **sin dominio todavía** (ver "Estado técnico").
- Repo: `berchotmateo-spec/zoo-center`, rama de trabajo `claude/loving-dirac-spw1xn`.
- Vista previa (Artifact): https://claude.ai/artifact/NEuwdatvgBmHiN14FcLoWU
  - Agregando `#borrador` al final del link se ve lo pendiente marcado
    «A confirmar» / «Falta» (para revisarlo con el dueño).

## Datos del local

| Dato | Valor | Fuente y fecha |
|---|---|---|
| Nombre comercial | Zoo Center · bajada "Petshop & Veterinaria" | Mateo, 22/10/2026 |
| Frase de sus posteos | "Los mejores productos para tus mascotas" | Instagram |
| Sucursal 1 | **Alberti 1381** — veterinaria, peluquería canina y petshop | Mateo, 22/10/2026 |
| Sucursal 2 | **Catamarca 1951** — petshop | Mateo, 22/10/2026 |
| Coordenadas | ⚠️ FALTAN (la red de la sesión no llega a Google ni a OpenStreetMap) | — |
| Horario | Las dos: lunes a sábado de 9 a 20. Domingo cerrado | Mateo, 22/10/2026 |
| WhatsApp y teléfono | 223 691-9808 (wa.me/5492236919808) — contacto único para las dos | Mateo, 22/10/2026 |
| Email | zoocentermdq@gmail.com | Mateo, 22/10/2026 |
| Medios de pago | ⚠️ A CONFIRMAR | — |
| Delivery | Sin cargo. ⚠️ Zona, mínimo y días A CONFIRMAR | Mateo, 22/10/2026 |
| Redes que van | Instagram @zoocentermdp · Facebook "Zoo Center Mar del Plata" (facebook.com/p/Zoo-Center-Mar-del-Plata-100083610631017) | Mateo, 22/10/2026 |
| Colores de marca | Violeta #5B2D8E, naranja/amarillo #F5A623, lila #EDE4F7, blanco. ⚠️ Aproximados: confirmar con el logo | Mateo, 22/10/2026 |
| Tipografía | Baloo 2 (títulos, 700–800, MAYÚSCULAS) + Nunito (texto). Alternativa gratis a la letra de sus placas | decisión de diseño |
| Logo | ⚠️ FALTA el archivo vectorial. Mientras tanto el nombre va escrito en Baloo 2 (no se redibujó el logo) | — |

## PENDIENTES PARA EL DUEÑO (no publicar hasta confirmar)

En el código, lo pendiente lleva `pendiente:true` (o está vacío) y **no se ve**
en la web publicada; solo en la vista `#borrador`.

- [ ] **Guardería felina y acuario** en Alberti (los dice Facebook): ¿siguen? → `SERVICIOS` (pendiente) y `SUCURSALES[0].aConfirmar`.
- [ ] **Delivery**: zona, compra mínima y días. Hoy solo dice "sin cargo" y "escribinos y te contamos zona y días".
- [ ] **Medios de pago** → pregunta de `PREGUNTAS` (pendiente).
- [ ] **¿Hace falta turno o se puede ir sin turno?** → pregunta de `PREGUNTAS` (pendiente).
- [ ] **Marcas de alimento** que trabajan → categoría "Alimentos" del `CATALOGO`. NO inventar la lista.
- [ ] **Promos vigentes** → `PROMOS`. Las tres cargadas están `pendiente:true`:
  - BBVA (martes, jueves, viernes y sábados): falta **qué es** la promo (descuento, cuotas, tarjetas) y hasta cuándo.
  - Cuenta DNI (Banco Provincia, con topes por tipo de cliente): la última venció el 30/09/2026; quedó cargada con esa fecha y se oculta sola. Si hay una nueva, cargarla con su `vence`.
  - Bravecto → medallita GeoID con QR, solo en Alberti: falta confirmar si sigue y hasta cuándo.
- [ ] **¿Atienden urgencias?** La web NO dice que sí. Si el dueño lo confirma, recién ahí se agrega.
- [ ] **Veterinario**: nombre y matrícula, solo si quiere mostrarlos.
- [ ] **Texto sobre por qué vacunar**: solo si el veterinario lo revisa y aprueba (base: su posteo sobre vacunas) → `SERVICIOS[0].nota`. Nada de información médica sin su aprobación.
- [ ] **Logo en vector** (SVG o PDF) → `img/logo.svg` y `MARCA.logo = "img/logo.svg"`. Confirmar colores con ese archivo.
- [ ] **Fotos del local** por dentro y por fuera (las dos sucursales) → `SUCURSALES[].foto`.
- [ ] **Permiso para usar fotos del Instagram**: antes y después de la peluquería (`ASI_QUEDARON`) y mascotas de clientes (`CLIENTES`). Sin fotos, esas galerías no se dibujan.
- [ ] **Fotos de productos** (reales, del local o del Instagram) → `f:` de cada producto en `CATALOGO`.
- [ ] **Coordenadas** de las dos sucursales (copiarlas de Google Maps) → `lat`/`lng` en `SUCURSALES` **y** `"geo"` en el JSON-LD del `<head>`.

## PROVISORIO (cargado, pero hay que confirmarlo)

| Qué | Por qué hay duda | Desde |
|---|---|---|
| Para qué mascota es cada producto (`mascota` en `CATALOGO`) | Deducido del rubro, no confirmado. Indumentaria, pelotas y mordillos → perro; medallas y GeoID → perros y gatos; piedras y sanitarios → gato | 22/10/2026 |
| Peluches, higiene (shampoo, perfumes, repelente) y salud (pipetas, antiparasitarios, antiestrés) **sin mascota a propósito** | Algunos productos de perro son tóxicos para gatos (p. ej. repelentes y pipetas con permetrina). Que lo defina el dueño o el veterinario; hasta entonces aparecen solo en "Todos" | 22/10/2026 |
| Colores | Aproximados por Mateo; confirmar con el logo | 22/10/2026 |
| `img/og.jpg` (imagen al compartir) | Gráfica con el nombre escrito y motivos de sus placas. Reemplazar por una con el logo real o una foto del local | 22/10/2026 |

## Lo que NO va en la web

Al sacar algo, buscarlo en **todo** el `index.html`, incluido el JSON-LD del `<head>`.

- Precios inventados, productos o marcas no confirmados, horarios, reseñas o promos inventadas.
- Información médica o consejos médicos. No decir que atienden urgencias.
- `aggregateRating` en el JSON-LD.
- Fotos de stock, de IA o de otros comercios. Solo fotos reales del local y de sus clientes (con permiso).

## De dónde salen los precios

Hoy **no hay precios cargados**: todos los productos muestran "Consultar"
(abre WhatsApp con "Hola! Quería consultar por: [producto]").
Si el dueño quiere precios: que los pase él (no copiarlos de otro lado), cargar
`p:` en cada producto y **siempre** poner la fecha en `PRECIOS_AL` (o `act:` por
producto). La web muestra "Actualizado el dd/mm/aaaa · Precios sujetos a cambio".

## Decisiones tomadas (respetarlas)

- Un solo `index.html`, HTML/CSS/JS sin frameworks ni build. Fondo claro, mobile-first, probado a 390 px.
- Todo lo que cambia seguido está en arrays al principio del `<script>`: `SUCURSALES`, `HORARIOS`, `DIAS_ESPECIALES`, `SERVICIOS`, `CATALOGO`, `PROMOS`, `ASI_QUEDARON`, `CLIENTES`, `PREGUNTAS`. Un campo vacío no dibuja nada.
- Violeta para títulos y botones; naranja para acentos y para el ícono de WhatsApp/llamar (como "burbuja" con el dibujo violeta). Nunca texto naranja/amarillo sobre blanco.
- Productos y fotos nunca recortados: `object-fit:contain` o `height:auto`.
- Catálogo para mirar y consultar, no tienda: sin carrito ni pago online.
- Huellitas que cruzan la portada una sola vez al cargar; respetan "reducir movimiento".
- Barra fija arriba "Abierto ahora / Cerrado" calculada con la **hora de Argentina** (no la del visitante), con aviso editable en `DIAS_ESPECIALES`.
- Barra fija abajo en el celular: "WhatsApp" y "Pedir turno".
- "Pedir turno" abre un formulario que arma el mensaje y abre WhatsApp. Veterinaria: nombre, mascota, especie, motivo, día. Peluquería: nombre, perro (opcional), raza, tamaño, servicio, día. No deja elegir domingo ni días cerrados.
- Crédito al pie: "Sitio web diseñado por Mateo Berchot".

## Fotos

- Con foto: **0**. Faltan todas (ver pendientes). El sitio funciona sin fotos: lo que no tiene foto no muestra hueco.
- Cuando lleguen: a `fotos-originales/` con el nombre del producto → `python3 hacer-fotos.py` → `f:"nombre.webp"`.

## Estado técnico

- [ ] Dominio (NIC.ar) — cuando exista: poner URL absolutas en `og:image`, `canonical`, `url`/`image` del JSON-LD (con `publicar-cabecera.html`, ver la skill).
- [ ] GitHub Pages desde `main` / `docs` (`python3 publicar.py <dominio>`).
- [ ] Search Console y Perfil de Empresa de Google.
- [ ] QR entregado.

## Cómo se trabaja acá

1. Cambio en los datos del `<script>` de `index.html`.
   - Feriado o cierre: un objeto en `DIAS_ESPECIALES` (hay un ejemplo comentado). Ej.: el Día del Empleado de Comercio, `abiertas:{ alberti:"09:00-13:00" }` y un `aviso`.
   - Promo nueva: objeto en `PROMOS` con `vence`; sin `pendiente:true` recién cuando el dueño la confirmó.
   - Producto nuevo: objeto en `CATALOGO`; `nuevo:true` para la etiqueta "Nuevo ingreso".
2. Si cambia dirección, horario o teléfono: cambiarlo **también** en el JSON-LD del `<head>`.
3. Probar: `node verificar.mjs index.html` (de la skill) a 1366 y 390 px, sin errores ni desborde.
4. Commit + push → actualizar la vista previa.

## Registro de cambios

Una línea por pedido, la más nueva arriba.

- 22/10/2026 — Armado inicial desde cero con los datos que pasó Mateo (sucursales, horario, contacto, servicios, categorías del Instagram, promos que venían usando). Sin fotos ni logo todavía; promos, guardería/acuario y FAQ sin respuesta quedan como pendientes.
