#!/usr/bin/env python3
"""Agrega referral link a los posts de reseña de faucets/wallets del blog.

Mapea cada post *-reseña.html con su id en js/faucets.js y:
 - si ya tiene <h2>Registro</h2><br><span>Registrate aquí en X<br>  -> lo reemplaza por un <a href> real
 - si no tiene sección Registro -> la inserta antes del <script blog-nav.js>
Solo toca los posts que matchean con faucets.js. No borra nada mas.
"""
import re, glob, os

ROOT = "/home/salma/faucetguru.github.io"
js = open(os.path.join(ROOT, "js/faucets.js"), encoding="utf-8").read()
rows = re.findall(r'id:\s*"([^"]+)".*?name:\s*"([^"]+)".*?referralLink:\s*"([^"]+)"', js, re.S)
data = {i: (n, r) for i, n, r in rows}

POSTS = os.path.join(ROOT, "blog", "posts")

def slug_to_id(slug):
    base = re.split(r'-(reseña|review|guia|telegram|guide)', slug)[0]
    for i in data:
        if slug.startswith(i) or base.startswith(i.replace('_', '-')):
            return i
    return None

modified = 0
report = []
for p in sorted(glob.glob(os.path.join(POSTS, "*.html"))):
    slug = os.path.basename(p).replace(".html", "")
    i = slug_to_id(slug)
    if not i:
        continue
    name, ref = data[i]
    html = open(p, encoding="utf-8").read()

    # Caso 1: span roto existe
    pat = re.compile(r'<h2>Registro</h2><br><span[^>]*>Registrate aquí en ' + re.escape(name) + r'<br>')
    if pat.search(html):
        new = (f'<h2>Registro</h2><br><p>¿Listo para empezar? '
               f'<a href="{ref}" target="_blank" rel="noopener noreferrer">'
               f'Registrate aquí en {name}</a> con nuestro link de referido.</p>')
        html2 = pat.sub(new, html, count=1)
        if html2 != html:
            open(p, "w", encoding="utf-8").write(html2)
            modified += 1
            report.append(f'FIXED span: {os.path.basename(p)} -> {ref}')
        continue

    # Caso 2: no tiene Registro -> insertar antes del script
    if '<h2>Registro</h2>' not in html:
        block = (f'\n\n<h2>Registro</h2>\n'
                 f'<p>¿Listo para empezar? '
                 f'<a href="{ref}" target="_blank" rel="noopener noreferrer">'
                 f'Registrate aquí en {name}</a> con nuestro link de referido.</p>\n\n')
        marker = '<script src="/blog/posts/blog-nav.js"></script>'
        if marker in html:
            html2 = html.replace(marker, block + marker, 1)
            open(p, "w", encoding="utf-8").write(html2)
            modified += 1
            report.append(f'ADDED registro: {os.path.basename(p)} -> {ref}')
        else:
            report.append(f'SKIP (sin marker): {os.path.basename(p)}')
        continue

    report.append(f'NO MATCH PATTERN: {os.path.basename(p)}')

print(f'Modificados: {modified}')
for r in report:
    print(r)
