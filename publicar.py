# -*- coding: utf-8 -*-
"""
============================================================
  Arma la carpeta docs/ para GitHub Pages
------------------------------------------------------------
  GitHub Pages sirve los archivos tal cual están commiteados en
  main/docs. Este script deja esa carpeta lista:

    - copia index.html y las carpetas de imágenes (fotos/, img/)
    - si existe publicar-cabecera.html, la pone en lugar de todo
      lo que hay antes de <style> en index.html (título largo,
      descripción, Open Graph, JSON-LD con URL absolutas)
    - escribe CNAME (si se le da el dominio), robots.txt,
      sitemap.xml con la fecha de hoy y .nojekyll
    - controla que exista cada imagen referenciada con ruta
      relativa, y avisa si quedó algún data: URI pesado

  Uso (copiarlo a la raíz del proyecto del cliente):
      python3 publicar.py pizzerialanieve.com.ar
      python3 publicar.py                      (sin dominio propio todavía)

  docs/ NO se edita a mano: se regenera con esto. Editarla a mano
  es la forma más común de perder el CNAME y tirar el dominio.
============================================================
"""
import datetime
import pathlib
import re
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
DESTINO = RAIZ / "docs"
PAGINA = RAIZ / "index.html"
CABECERA = RAIZ / "publicar-cabecera.html"

# Carpetas y archivos sueltos que viajan a docs/ tal cual.
CARPETAS = ["fotos", "img"]
SUELTOS = ["og.jpg", "icono.png", "favicon.ico", "logo.png"]


def armar_html():
    html = PAGINA.read_text(encoding="utf-8")
    if CABECERA.exists():
        corte = html.find("<style")
        if corte < 0:
            sys.exit("No encuentro <style> en index.html: no sé dónde termina la cabecera.")
        html = CABECERA.read_text(encoding="utf-8").rstrip() + "\n\n" + html[corte:]
    if "</html>" not in html.lower():
        html = html.rstrip() + "\n</body>\n</html>\n"
    return html


def revisar(html):
    """Avisa de imágenes referenciadas que no existen y de data URI pesados."""
    problemas = 0
    rutas = set(re.findall(r'''(?:src|href)=["']([^"'#?]+\.(?:webp|jpe?g|png|svg|gif|ico))["']''', html, re.I))
    rutas |= set(re.findall(r'''["']([\w./-]+\.(?:webp|jpe?g|png|svg))["']''', html, re.I))
    for r in sorted(rutas):
        if r.startswith(("http:", "https:", "//", "data:")):
            continue
        if not (DESTINO / r).exists() and not (DESTINO / "fotos" / r).exists():
            print("  ✗ falta el archivo:", r)
            problemas += 1
    for uri in re.findall(r"data:image/[a-z+]+;base64,[A-Za-z0-9+/=]{20000,}", html):
        print("  ⚠ data URI de %d KB embebido: mejor como archivo suelto" % (len(uri) // 1000))
    return problemas


def main():
    dominio = sys.argv[1].strip().removeprefix("https://").strip("/") if len(sys.argv) > 1 else ""
    DESTINO.mkdir(exist_ok=True)

    for nombre in CARPETAS:
        origen = RAIZ / nombre
        if origen.is_dir():
            shutil.copytree(origen, DESTINO / nombre, dirs_exist_ok=True)
    for nombre in SUELTOS:
        if (RAIZ / nombre).is_file():
            shutil.copy2(RAIZ / nombre, DESTINO / nombre)

    html = armar_html()
    (DESTINO / "index.html").write_text(html, encoding="utf-8")
    (DESTINO / ".nojekyll").write_text("", encoding="utf-8")

    if dominio:
        sitio = "https://" + dominio
        # Sin este archivo GitHub Pages deja de servir el dominio propio.
        (DESTINO / "CNAME").write_text(dominio + "\n", encoding="utf-8")
        (DESTINO / "robots.txt").write_text(
            "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % sitio, encoding="utf-8")
        (DESTINO / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            "  <url>\n    <loc>%s/</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n  </url>\n</urlset>\n"
            % (sitio, datetime.date.today().isoformat()), encoding="utf-8")
    elif (DESTINO / "CNAME").exists():
        print("⚠ docs/CNAME existe y no pasaste dominio: lo dejo como está.")

    print("docs/index.html: %d KB" % (len(html.encode("utf-8")) // 1000))
    problemas = revisar(html)
    print("Listo." if not problemas else "%d archivo(s) faltan: revisar antes de commitear." % problemas)
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
