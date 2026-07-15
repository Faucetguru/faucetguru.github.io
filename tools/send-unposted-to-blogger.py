#!/usr/bin/env python3
"""
Publicar posts pendientes a Blogger, de a UNO por vez, vía email.

Flujo por post:
  1. Lee el primer título con '- [ ]' de blogposted.md (o todos si no --one).
  2. Busca su .html en blog/posts por <title> exacto (ignora index.html).
  3. Le quita los <a href> en MEMORIA (interlink queda como texto plano, sin tag
     anchor) — NO se toca el archivo fuente de gh-pages.
  4. Lo envía por mail a la dirección de Blogger (uno solo si --one).
  5. --mark lo marca como enviado en blogposted.md.
  6. --verify-rss cruza contra el feed público de Blogger (no requiere token).

Uso:
  python3 tools/send-unposted-to-blogger.py --one --mark      # enviar 1
  python3 tools/send-unposted-to-blogger.py --verify-rss     # revisar
"""

import os
import re
import smtplib
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

EMAIL_USER    = os.getenv("EMAIL_USER")    or "polakenfold@gmail.com"
EMAIL_PASS    = os.getenv("EMAIL_PASS")    or "ghca olpq vdav pllw"
BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL") or "polakenfold.crypto666@blogger.com"
BLOG_ID       = os.getenv("BLOGGER_BLOG_ID", "G-F7ZG182KN2")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR    = PROJECT_ROOT / "blog" / "posts"
CHECKLIST    = PROJECT_ROOT / "blogposted.md"

ANCHOR_OPEN = re.compile(r'<a\s+href="[^"]*"\s*([^>]*)>', re.IGNORECASE)


def strip_anchors(content):
    """Interlinking -> texto plano sin <a>. En memoria, no muta el archivo."""
    content = ANCHOR_OPEN.sub(r'<span\1>', content)
    content = re.sub(r'</a>', '', content, flags=re.IGNORECASE)
    return content


def get_title(html_path):
    txt = html_path.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<title>(.*?)</title>', txt, re.IGNORECASE)
    return m.group(1).strip() if m else html_path.stem.replace('_', ' ')


def load_pending():
    titles, seen = [], set()
    for line in CHECKLIST.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line.startswith('- [ ]'):
            t = re.sub(r'^- \[ \] ', '', line).strip()
            if t and t.lower() not in seen:
                seen.add(t.lower())
                titles.append(t)
    return titles


def find_html(title):
    want = title.strip().lower()
    for f in POSTS_DIR.glob('*.html'):
        if f.name == 'index.html':
            continue
        if get_title(f).strip().lower() == want:
            return f
    for f in POSTS_DIR.glob('*.html'):
        if f.name == 'index.html':
            continue
        if want in get_title(f).strip().lower():
            return f
    return None


def send_post(html_path, recipient, strip=True):
    subject = get_title(html_path)
    body = html_path.read_text(encoding='utf-8', errors='ignore')
    if strip:
        body = strip_anchors(body)
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Enviado (1 post): {subject}")
        return True
    except Exception as e:
        print(f"❌ Error enviando {subject}: {e}")
        return False


def mark_sent(sent_titles):
    if not sent_titles:
        return
    lines = CHECKLIST.read_text(encoding='utf-8').splitlines()
    done = set(t.lower() for t in sent_titles)
    out = []
    for l in lines:
        if l.strip().startswith('- [ ]'):
            tt = re.sub(r'^- \[ \] ', '', l).strip().lower()
            if tt in done:
                out.append(l.replace('- [ ]', '- [x]', 1))
                continue
        out.append(l)
    CHECKLIST.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f"📝 Marcados {len(sent_titles)} como enviado(s) en blogposted.md")


def verify_rss():
    """Cruza pendientes contra el feed público de Blogger (solo publicados)."""
    url = f"https://www.blogger.com/feeds/{BLOG_ID}/posts/default?max-results=500"
    try:
        data = urllib.request.urlopen(url, timeout=25).read().decode('utf-8', 'ignore')
    except Exception as e:
        print(f"❌ No se pudo leer el feed de Blogger: {e}")
        return
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(data)
    live = set(e.text.strip().lower() for e in root.findall('.//a:title', ns))
    print(f"📡 Blogger feed: {len(live)} posts publicados.")
    pending = load_pending()
    missing = [t for t in pending if t.strip().lower() not in live]
    if missing:
        print(f"❌ {len(missing)} pendientes NO aparecen en el feed (pueden estar en borrador o sin procesar):")
        for t in missing:
            print(f"   - {t}")
    else:
        print("✅ Todos los pendientes ya están publicados en Blogger.")


def main():
    ap = argparse.ArgumentParser(description="Publicar posts a Blogger, de a uno, vía email")
    ap.add_argument("--one", action="store_true", help="Enviar SOLO el primer pendiente")
    ap.add_argument("--dry-run", action="store_true", help="Mostrar sin enviar")
    ap.add_argument("--mark", action="store_true", help="Marcar enviados en blogposted.md")
    ap.add_argument("--verify-rss", action="store_true", help="Verificar contra feed RSS público")
    ap.add_argument("--no-strip", action="store_true", help="No quitar anchors")
    args = ap.parse_args()

    if args.verify_rss:
        verify_rss()
        return

    pending = load_pending()
    if args.one:
        total = len(pending)
        pending = pending[:1]
        print(f"📍 Modo UN POST: enviando solo el 1º de {total} pendientes.\n")

    sent = []
    for t in pending:
        hf = find_html(t)
        if not hf:
            print(f"⚠️ No se encontró HTML para: {t}")
            continue
        if args.dry_run:
            print(f"[DRY RUN] {hf.name} -> {BLOGGER_EMAIL}")
            continue
        if send_post(hf, BLOGGER_EMAIL, strip=not args.no_strip):
            sent.append(t)

    if args.mark and sent:
        mark_sent(sent)


if __name__ == "__main__":
    main()
