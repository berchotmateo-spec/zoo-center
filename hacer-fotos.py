# -*- coding: utf-8 -*-
"""
============================================================
  Prepara las fotos de producto para la carta
------------------------------------------------------------
  Las fotos salen del celular pesando 3 o 4 MB cada una. Sesenta
  de esas son 200 MB: la página no cargaría nunca en la calle,
  con datos móviles.

  Este script las deja en ~150 KB sin que se note la diferencia
  en pantalla: las achica para que entren en un cuadro de 900 px
  y las guarda en WebP.

  NO RECORTA NADA. Regla de la casa: la comida nunca puede quedar
  cortada. Se respeta la proporción con la que se sacó la foto,
  sea horizontal o vertical, y la carta se acomoda a eso.

  Uso (copiarlo a la raíz del proyecto del cliente):
      python3 hacer-fotos.py

  Las HEIC del iPhone necesitan  pip install pillow-heif

  Lee todo lo que haya en  fotos-originales/
  y escribe el resultado en  fotos/

  El nombre del archivo se mantiene: si entra "muzzarella.jpg",
  sale "muzzarella.webp", y en la carta el producto lleva
  f:"muzzarella.webp".

  Además escribe las medidas de cada foto dentro de index.html,
  en el bloque MEDIDAS. El navegador las necesita ANTES de bajar
  la imagen para reservarle el lugar: sin eso la carta pega un
  salto cuando cada foto termina de cargar.
============================================================
"""
import io
import pathlib
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Falta Pillow. Instalalo con:  pip install pillow")

try:  # opcional: abre las HEIC del iPhone
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

RAIZ = pathlib.Path(__file__).parent
ORIGEN = RAIZ / "fotos-originales"
DESTINO = RAIZ / "fotos"
PAGINA = RAIZ / "index.html"

LADO = 900      # la foto entra en un cuadro de 900x900, sin recortar
CALIDAD = 82    # arriba de esto el archivo crece y la foto no mejora

EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp", ".heic"}

ABRE = "  /* MEDIDAS-EMPIEZA */"
CIERRA = "  /* MEDIDAS-TERMINA */"


def escribir_medidas(medidas):
    """Vuelca el ancho y alto de cada foto en el bloque MEDIDAS de index.html."""
    html = io.open(PAGINA, encoding="utf-8").read()
    if ABRE not in html or CIERRA not in html:
        print("\n⚠ No encuentro el bloque MEDIDAS en index.html; no lo toco.")
        return
    cuerpo = "\n".join('    "%s": [%d, %d],' % (n, w, h)
                       for n, (w, h) in sorted(medidas.items()))
    nuevo = re.sub(
        re.escape(ABRE) + r".*?" + re.escape(CIERRA),
        ABRE + "\n" + cuerpo + "\n" + CIERRA,
        html, flags=re.S)
    io.open(PAGINA, "w", encoding="utf-8").write(nuevo)
    print("Medidas de %d fotos escritas en index.html." % len(medidas))


def main():
    if not ORIGEN.is_dir():
        ORIGEN.mkdir()
        sys.exit("Creé la carpeta %s. Poné ahí las fotos y volvé a correrme." % ORIGEN.name)

    DESTINO.mkdir(exist_ok=True)
    fotos = sorted(f for f in ORIGEN.iterdir() if f.suffix.lower() in EXTENSIONES)
    if not fotos:
        sys.exit("No hay fotos en %s." % ORIGEN.name)

    pesaban = pesan = 0
    medidas = {}

    for foto in fotos:
        salida = DESTINO / (foto.stem + ".webp")
        try:
            with Image.open(foto) as img:
                # Respeta la orientación con la que se sacó la foto: sin esto,
                # las verticales del celular salen acostadas.
                img = ImageOps.exif_transpose(img)
                img = img.convert("RGB")
                # thumbnail achica para que entre en el cuadro y mantiene la
                # proporción. Nunca agranda y nunca corta.
                img.thumbnail((LADO, LADO), Image.LANCZOS)
                img.save(salida, "WEBP", quality=CALIDAD, method=6)
                medidas[salida.name] = img.size
        except Exception as e:
            print("  ✗ %s — %s" % (foto.name, e))
            continue

        antes, ahora = foto.stat().st_size, salida.stat().st_size
        pesaban += antes
        pesan += ahora
        w, h = medidas[salida.name]
        forma = "vertical  " if h > w else ("horizontal" if w > h else "cuadrada  ")
        print("  ✓ %-28s %s %4dx%-4d %6.1f MB → %5.0f KB"
              % (salida.name, forma, w, h, antes / 1e6, ahora / 1e3))

    print("\n%d fotos · %.1f MB → %.1f MB" % (len(medidas), pesaban / 1e6, pesan / 1e6))
    # Las medidas se toman de TODO fotos/, no sólo de lo recién procesado:
    # fotos-originales/ no está en el repo, así que en un clone nuevo sólo
    # están las fotos que acaban de llegar, y el bloque perdería las demás.
    for webp in DESTINO.glob("*.webp"):
        if webp.name not in medidas:
            with Image.open(webp) as img:
                medidas[webp.name] = img.size
    escribir_medidas(medidas)
    print('Acordate de agregar  f:"<archivo>.webp"  al producto en la CARTA.')


if __name__ == "__main__":
    main()
