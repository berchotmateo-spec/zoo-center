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
| Colores de marca | Violeta #5B2D8E, naranja/amarillo #F5A623, lila #EDE4F7, blanco. ⚠️ Aproximados. En la foto del cartel el naranja del gato y el perro se ve más tostado que #F5A623 (puede ser la luz de la foto): se dejó #F5A623 hasta ver el original | Mateo, 22/10/2026 |
| Tipografía | Baloo 2 (títulos, 700–800, MAYÚSCULAS) + Nunito (texto). Alternativa gratis a la letra de sus placas | decisión de diseño |
| Logo | **Réplica vectorial** hecha desde una foto del cartel del frente (Mateo no dijo de qué sucursal), a pedido de Mateo: `img/logo.svg` (el cartel, fondo violeta), `img/logo-chico.svg` (sin "PETSHOP & VETERINARIA", para la cabecera), `img/logo-blanco.svg` (sin fondo, para el pie). Letras: Sniglet ExtraBold ("ZOO", "CENTER") y Montserrat Bold (bajada); gato y perro redibujados sobre la foto. Se rehace con `herramientas/hacer-logo.py`. ⚠️ Pedir igual el original para confirmar | foto del cartel, 22/10/2026 |

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
- [ ] **Clave del local** para la agenda de turnos (el proyecto de Supabase ya está creado y conectado): la elige el dueño y se carga con `select public.fijar_clave('…')` en el SQL Editor (ver "Agenda de turnos"). Después, probar un turno de punta a punta en la web publicada.
- [ ] **Turnos**: cada cuánto se dan, cuánto dura cada uno (veterinaria y peluquería) y si la veterinaria atiende todo el horario de Alberti → `TURNOS` (tiene `horarios:[...]` para acotarlo). Explicarle cómo confirmar: el link que llega al final de cada pedido → "Confirmar el turno por WhatsApp".
- [ ] **¿Atienden urgencias?** La web NO dice que sí. Si el dueño lo confirma, recién ahí se agrega.
- [ ] **Veterinario**: nombre y matrícula, solo si quiere mostrarlos.
- [ ] **Texto sobre por qué vacunar**: solo si el veterinario lo revisa y aprueba (base: su posteo sobre vacunas) → `SERVICIOS[0].nota`. Nada de información médica sin su aprobación.
- [ ] **Logo original en vector** (SVG, AI o PDF), para confirmar la réplica y los colores exactos. Si llega, reemplaza `img/logo.svg`, `img/logo-chico.svg` e `img/logo-blanco.svg` (mismos nombres) y `img/og.jpg`.
- [ ] **Fotos del local** por dentro y por fuera (las dos sucursales) → `SUCURSALES[].foto`.
- [ ] **Permiso para usar fotos del Instagram**: antes y después de la peluquería (`ASI_QUEDARON`) y mascotas de clientes (`CLIENTES`). Sin fotos, esas galerías no se dibujan.
- [ ] **Fotos de productos** (reales, del local o del Instagram) → `f:` de cada producto en `CATALOGO`.
- [ ] **Coordenadas** de las dos sucursales (copiarlas de Google Maps) → `lat`/`lng` en `SUCURSALES` **y** `"geo"` en el JSON-LD del `<head>`.

## PROVISORIO (cargado, pero hay que confirmarlo)

| Qué | Por qué hay duda | Desde |
|---|---|---|
| Para qué mascota es cada producto (`mascota` en `CATALOGO`) | Deducido del rubro, no confirmado. Indumentaria, pelotas y mordillos → perro; medallas y GeoID → perros y gatos; piedras y sanitarios → gato | 22/10/2026 |
| Peluches, higiene (shampoo, perfumes, repelente) y salud (pipetas, antiparasitarios, antiestrés) **sin mascota a propósito** | Algunos productos de perro son tóxicos para gatos (p. ej. repelentes y pipetas con permetrina). Que lo defina el dueño o el veterinario; hasta entonces aparecen solo en "Todos" | 22/10/2026 |
| Colores | Aproximados por Mateo; el naranja del cartel se ve más tostado en la foto | 22/10/2026 |
| Logo (`img/logo*.svg`) | Es una réplica hecha a partir de una foto (no el archivo original): la letra es la misma (Sniglet), pero el gato, el perro y los colores son aproximados | 22/10/2026 |
| Turnos (`TURNOS`) | Cada 30 min para veterinaria y peluquería; duración 30 min (veterinaria) y 60 min (peluquería, para la agenda); 1 hora de anticipación para turnos de hoy; dentro del horario de Alberti (9 a 20). Todo a confirmar con el dueño (¿el veterinario atiende todo ese horario?) | 23/10/2026 |
| `img/og.jpg` (imagen al compartir) | Gráfica con la réplica del logo y los datos. Mejor con una foto real del local cuando haya | 22/10/2026 |

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
- **Turnos** (sin servidor ni costo, todo por WhatsApp):
  1. El cliente toca "Pedir turno", elige **día y hora** (solo horarios dentro del horario de Alberti, según `TURNOS`; nada de domingos, días cerrados ni horas que ya pasaron) y deja su WhatsApp. Veterinaria: nombre, WhatsApp, mascota, especie, motivo. Peluquería: nombre, WhatsApp, perro (opcional), raza, tamaño, servicio.
  2. Se abre WhatsApp con el pedido para el local y, al final, un **link para el local** (`<sitio>#t-…`, el pedido va codificado en el link; no se guarda en ningún lado).
  3. El dueño toca el link → **panel del turno**: "Confirmar el turno por WhatsApp" (abre el chat del cliente con la confirmación lista: un toque y le llega), "Proponer otro horario", "Mandar recordatorio" y "Agendar en Google Calendar". Puede corregir el número del cliente.
  - No es automático: el que manda la confirmación es el dueño, con un toque. Que salga sola necesita la API oficial de WhatsApp Business (paga por mensaje, con verificación de Meta) y un servidor; anotado como posible mejora.
  - **Con la agenda de Supabase conectada** (`AGENDA` con url y clave publicable; ver "Agenda de turnos" abajo), dos clientes no pueden pedir el mismo horario: el formulario muestra solo horarios libres y el cliente primero toca "Reservar horario" y después manda el WhatsApp. Sin agenda (o si no responde), todo sigue andando por WhatsApp, sin bloquear horarios.
- Logo: el cartel completo en la portada; la versión sin bajada en la cabecera (solo en la compu: en el celular esa fila no se muestra, porque el logo grande ya abre la página y el WhatsApp está en la barra de abajo); la versión blanca en el pie. Las imágenes van directo en el HTML (`<img>`), sin JS.
- Crédito al pie: "Sitio web diseñado por Mateo Berchot".

## Fotos

- Con foto: **0**. Faltan todas (ver pendientes). El sitio funciona sin fotos: lo que no tiene foto no muestra hueco.
- Cuando lleguen: a `fotos-originales/` con el nombre del producto → `python3 hacer-fotos.py` → `f:"nombre.webp"`.

## Estado técnico

- [ ] Dominio (NIC.ar) — cuando exista: poner URL absolutas en `og:image`, `canonical`, `url`/`image`/`logo` del JSON-LD (con `publicar-cabecera.html`, ver la skill).
- [ ] GitHub Pages desde `main` / `docs` (`python3 publicar.py <dominio>`).
- [x] Agenda en Supabase — proyecto `ebkfuvvbhsztenbkyvyw` (cuenta de Mateo), conectada en `AGENDA` el 23/10/2026. En el HTML solo la clave publicable. ⚠️ Falta probarla de punta a punta en la web publicada (desde la sesión de Claude no se llega a supabase.co).
- [ ] Con dominio: poner la dirección en `CONTACTO.sitio` (es la que va en el link de cada pedido de turno). En la vista previa (Artifact) se publica con la del Artifact.
- [ ] Search Console y Perfil de Empresa de Google.
- [ ] QR entregado.

## Agenda de turnos (Supabase) — para que no se pisen los horarios

Estado: **proyecto creado y conectado** (`ebkfuvvbhsztenbkyvyw`, 23/10/2026). Falta probarla en la web publicada y que el dueño tenga su clave del local.

Qué hace:
- El formulario lee los horarios ocupados (sin datos de nadie) y no los ofrece. Al tocar "Reservar horario" la base guarda el pedido **solo si ese horario sigue libre** (si dos tocan a la vez, entra uno; el otro ve "ese horario se acaba de ocupar").
- Un pedido de la web **reserva el horario 24 horas**. Si el local no lo confirma en ese tiempo, se libera solo (por si el cliente nunca mandó el WhatsApp).
- **Panel del turno** (el link que llega en cada pedido): con la clave del local, "Confirmar el turno en la agenda" → recién ahí aparece "Confirmar el turno por WhatsApp". También "Pasar el turno a este horario" y "Liberar el horario".
- **Agenda** (`<sitio>#agenda`, para guardar en la pantalla de inicio del celular del dueño): turnos de los próximos 30 días y **"Ocupar un horario"** para los que da por teléfono o en el local.
- La duración de cada turno sale de `TURNOS` (veterinaria y peluquería no se pisan entre sí).

Seguridad:
- En el HTML va **solo la clave publicable** (`sb_publishable_…`). Nunca la secret / service_role.
- La tabla tiene RLS sin políticas: la página solo puede llamar a 5 funciones. Cualquiera ve qué horarios están ocupados; nombres y teléfonos solo con la **clave del local** (se pide una vez por celular y queda guardada en ese navegador; "Salir de la agenda" la borra).
- La clave del local se fija desde el SQL Editor con `select public.fijar_clave('…')`. **No va en el repo ni en el chat.**
- Freno a abusos: 40 pedidos por hora en total y hasta 3 turnos vigentes por número de WhatsApp.

Alta (Mateo, una sola vez):
1. supabase.com → New project (región São Paulo). La contraseña de la base la guarda Mateo.
2. SQL Editor → pegar entero `supabase/turnos.sql` → Run (se puede volver a correr sin perder turnos).
3. Nueva consulta: `select public.fijar_clave('la-clave-que-elija-el-dueño');` (8 caracteres o más).
4. Settings → API Keys → *Project URL* y clave **publishable** → van a `AGENDA = { url, clave }`.
5. Probar en la web publicada (el visor de Artifacts no deja salir a Supabase): pedir un turno, abrir el link, ver `#agenda`.

Ojo: Supabase gratis pausa los proyectos sin uso por ~1 semana. Si pasa, la web sigue tomando pedidos por WhatsApp (sin bloquear) y el panel avisa; se reactiva entrando a supabase.com.

Cómo se probó (23/10/2026): el SQL en un PostgreSQL 16 con los roles de Supabase (anon, extensiones, permisos por defecto): reservas, choques, permisos, clave, vencimiento y dos reservas simultáneas. La página, con Playwright contra una imitación de la API de Supabase que usa esa misma base.

## Logo: cómo se rehace

`python3 herramientas/hacer-logo.py <carpeta-con-fuentes>` (pip install fonttools). Necesita los .ttf de
Sniglet ExtraBold y Montserrat Bold (Google Fonts). Las medidas, el gato y el perro están en el script,
medidos sobre la foto del cartel enderezada. La foto del frente que mandó Mateo no se publicó: tiene un círculo rojo
dibujado encima y no sabemos de qué sucursal es. Sin la marca y sabiendo cuál es, puede ir como foto de esa sucursal.

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

- 23/10/2026 — Mateo creó el proyecto de Supabase (con la extensión de Chrome) y pasó la URL y la clave publicable → cargadas en `AGENDA`.
- 23/10/2026 — Mateo preguntó cómo evitar que pidan el mismo horario → agenda en Supabase (`supabase/turnos.sql` + `AGENDA` en el `index.html`): solo se ofrecen horarios libres, "Reservar horario" antes del WhatsApp, reserva de 24 h hasta que el local confirme, panel con clave del local (confirmar, pasar de horario, liberar) y `#agenda` con "Ocupar un horario". Falta crear el proyecto en Supabase; mientras tanto la web funciona como antes.
- 23/10/2026 — Mateo pidió mejorar los turnos y que al cliente le llegue el turno confirmado por WhatsApp → el cliente elige día y hora reales y deja su WhatsApp; al local le llega el pedido con un link a un panel para confirmar en un toque (le llega al cliente), proponer otro horario, mandar recordatorio y agendar en Google Calendar. Sin servidor ni costo; no es envío automático (eso necesita la API paga de WhatsApp).
- 22/10/2026 — Mateo mandó una foto del frente del local y pidió replicar el logo del cartel para usarlo en la web (antes la idea era esperar el vector) → réplica en `img/logo.svg`, `logo-chico.svg` y `logo-blanco.svg` (`herramientas/hacer-logo.py`), usada en la portada, la cabecera, el pie y la imagen para compartir. En el celular se ocultó la fila de la cabecera para no repetir el logo.
- 22/10/2026 — Armado inicial desde cero con los datos que pasó Mateo (sucursales, horario, contacto, servicios, categorías del Instagram, promos que venían usando). Sin fotos ni logo todavía; promos, guardería/acuario y FAQ sin respuesta quedan como pendientes.
