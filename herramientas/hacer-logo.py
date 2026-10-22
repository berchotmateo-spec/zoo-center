# -*- coding: utf-8 -*-
"""
============================================================
  Réplica vectorial del logo de Zoo Center (img/logo*.svg)
------------------------------------------------------------
  Hecha a partir de una foto del cartel del frente del local (22/10/2026),
  porque todavía no tenemos el archivo original del dueño. Cuando
  llegue el vector original, reemplaza a estos archivos.

  - "ZOO" y "CENTER": Sniglet ExtraBold (Google Fonts, licencia OFL),
    que es la letra del cartel. La Z va un poco ensanchada, como allá.
  - "PETSHOP & VETERINARIA": Montserrat Bold, espaciada.
  - Las dos O: círculos con el gato (mirando a la derecha) y el perro
    (mirando a la izquierda, con la oreja marcada con una línea).
  - Las letras quedan convertidas a trazos: el SVG no depende de
    ninguna fuente instalada.

  Uso:  python3 herramientas/hacer-logo.py  <carpeta-con-las-fuentes>
        (necesita Sniglet ExtraBold y Montserrat Bold en .ttf, con
         "sniglet" y "montserrat-700" o "montserrat-bold" en el nombre,
         y pip install fonttools)

  Medidas tomadas del cartel (foto enderezada 2,6°), en unidades donde
  el radio de las O es 100.

  Escribe:
    img/logo.svg          el cartel: fondo violeta, letras blancas
    img/logo-chico.svg    igual, sin "PETSHOP & VETERINARIA" (cabecera)
    img/logo-blanco.svg   sin fondo, letras blancas (sobre violeta)
============================================================
"""
import pathlib
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FUENTES = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")

VIOLETA = "#5B2D8E"
NARANJA = "#F5A623"
BLANCO = "#FFFFFF"

R = 100              # radio de las O (todo lo demás se mide contra esto)
ALTO_Z = 204         # tinta de la Z: del alto de las O
ANCHO_Z = 218        # y más ancha que la de la fuente
SEP_Z, SEP_O = 7, 18     # Z–O y O–O
SEP_CENTER = 9           # de la fila ZOO a CENTER
ALTO_CENTER = 105        # tinta de CENTER
ANCHO_CENTER = 666
SEP_BAJADA = 25
ALTO_BAJADA = 26.5       # tinta de PETSHOP & VETERINARIA
BAJADA_X = (10, 682)


def fuente(*nombres):
    for nombre in nombres:
        for f in sorted(FUENTES.glob("*.ttf")):
            if nombre in f.name.lower():
                return TTFont(f)
    sys.exit("No encuentro la fuente %r en %s" % (nombres, FUENTES))


def trazo(font, texto, alto, x, arriba, ancho=None, ancho_letra=None):
    """Texto → path SVG con la tinta empezando en (x, arriba).
    alto = alto de la tinta · ancho = ancho total a lograr (ajusta el espaciado)
    ancho_letra = estira en horizontal para lograr ese ancho (una sola letra, como la Z)."""
    gs, cm = font.getGlyphSet(), font.getBestCmap()
    nombres = [cm[ord(c)] for c in texto]
    adv = [font["hmtx"][n][0] for n in nombres]
    bp = BoundsPen(gs)
    for n in nombres:
        gs[n].draw(bp)
    s = alto / (bp.bounds[3] - bp.bounds[1])
    escala_x = ancho_letra / ((bp.bounds[2] - bp.bounds[0]) * s) if ancho_letra else 1.0

    def armar(track):
        pos, cx = [], 0.0
        for n, a in zip(nombres, adv):
            pos.append(cx)
            cx += a * s * escala_x + track
        return pos

    def tinta(pos):
        bp = BoundsPen(gs)
        for n, p in zip(nombres, pos):
            gs[n].draw(TransformPen(bp, (s * escala_x, 0, 0, -s, p, 0)))
        return bp.bounds

    track = 0.0
    if ancho:
        b = tinta(armar(0))
        track = (ancho - (b[2] - b[0])) / max(1, len(texto) - 1)
    pos = armar(track)
    b = tinta(pos)
    base = arriba - b[1]
    pen = SVGPathPen(gs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
    for n, p in zip(nombres, pos):
        gs[n].draw(TransformPen(pen, (s * escala_x, 0, 0, -s, x - b[0] + p, base)))
    return pen.getCommands(), (x, arriba, x + b[2] - b[0], arriba + b[3] - b[1])


# --- el gato y el perro, dibujados con el centro del círculo en (0,0) y radio 100 ---
GATO = ("M-69 130 L-70 60 C-69 40 -64 18 -55 4 C-46 -10 -30 -24 -14 -31 "
        "L3 -39 C6 -40 8.5 -38.5 8.8 -35 L9.5 -16 "
        "C25 -13 39 -1 47 16 C51 26 57 35 62.5 42 C64.5 45 62 49.5 57 51.5 "
        "C49 55 39 59 31 61.5 C31 72 36 83 47 96 L60 130 Z")
OJO_GATO = (29.5, 20.5, 3.9)
PERRO = ("M-86 -13.5 C-80 -17.5 -71 -21.5 -62 -26 C-57 -29 -54 -32.5 -52.5 -37 "
         "C-53 -50 -44 -62 -27 -66 C-8 -69.5 18 -66.5 33 -60 "
         "C50 -52 70 -40 86 -26 L140 0 L140 140 L24 140 L24 96 "
         "C23 72 20 52 12 38 C6 30 -4 23 -22 21 C-38 19.5 -56 14 -68 8 "
         "C-77 4.5 -83 3 -87 0.5 C-90.5 -2 -90.5 -11 -86 -13.5 Z")
OREJA_PERRO = "M13 -40 C15 -27 18 -14 24 -6 C29 0 37 0 43 -6 C50 -14 55 -24 59 -34"
OJO_PERRO = (-32, -32, 3.9)


def logo(fondo=None, letras=BLANCO, circulos=BLANCO, animales=NARANJA, bajada=True, margen=(64, 52)):
    sni, mon = fuente("sniglet"), fuente("montserrat-700", "montserrat-bold")
    # ZOO: la Z y las dos O, apoyadas en la misma línea
    z, zb = trazo(sni, "Z", ALTO_Z, 0, 2 * R - ALTO_Z + 2, ancho_letra=ANCHO_Z)
    o1 = (zb[2] + SEP_Z + R, R)
    o2 = (o1[0] + 2 * R + SEP_O, R)
    # CENTER y la bajada, alineadas a la izquierda con la Z
    c, cb = trazo(sni, "CENTER", ALTO_CENTER, 5, 2 * R + SEP_CENTER, ancho=ANCHO_CENTER)
    alto_total = cb[3]
    b = ""
    if bajada:
        b, bb = trazo(mon, "PETSHOP & VETERINARIA", ALTO_BAJADA, BAJADA_X[0], cb[3] + SEP_BAJADA,
                      ancho=BAJADA_X[1] - BAJADA_X[0])
        alto_total = bb[3]
    ancho_zoo = o2[0] + R

    def o(id_, centro, animal, extra):
        cx, cy = centro
        return (f'<clipPath id="{id_}"><circle r="{R}"/></clipPath>'
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R}" fill="{circulos}"/>'
                f'<g clip-path="url(#{id_})" transform="translate({cx:.1f} {cy:.1f})">'
                f'<path d="{animal}" fill="{animales}"/>{extra}</g>')

    gato = o("o-gato", o1, GATO, '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (*OJO_GATO, circulos))
    perro = o("o-perro", o2, PERRO,
              '<path d="%s" fill="none" stroke="%s" stroke-width="3.4" stroke-linecap="round"/>'
              '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (OREJA_PERRO, circulos, *OJO_PERRO, circulos))
    ancho = max(ancho_zoo, cb[2], BAJADA_X[1] if bajada else 0)
    arriba = min(0, zb[1])
    mx, my = margen
    vb = (-mx, arriba - my, ancho + 2 * mx, alto_total - arriba + 2 * my)
    caja = (f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]:.1f}" height="{vb[3]:.1f}" rx="{min(vb[2], vb[3]) * 0.09:.1f}" fill="{fondo}"/>'
            if fondo else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]:.1f} {vb[3]:.1f}" '
            f'role="img" aria-label="Zoo Center, Petshop &amp; Veterinaria">'
            f'<title>Zoo Center · Petshop &amp; Veterinaria</title>{caja}'
            f'<g fill="{letras}"><path d="{z}"/><path d="{c}"/>' + (f'<path d="{b}"/>' if b else "") + '</g>'
            f'{gato}{perro}</svg>\n'), vb


def main():
    img = RAIZ / "img"
    for nombre, kw in [
        ("logo.svg", dict(fondo=VIOLETA)),
        ("logo-chico.svg", dict(fondo=VIOLETA, bajada=False, margen=(46, 40))),
        ("logo-blanco.svg", dict(margen=(4, 4))),
    ]:
        svg, vb = logo(**kw)
        (img / nombre).write_text(svg, encoding="utf-8")
        print("  ✓ img/%-16s %4.0f × %3.0f  (%d bytes)" % (nombre, vb[2], vb[3], len(svg.encode())))


if __name__ == "__main__":
    main()
