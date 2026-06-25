#!/usr/bin/env python3
"""
Enviar por email a Blogger só los posts que todavía no están marcados
como publicados en `blogposted.md`.
"""

import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Configuración
EMAIL_USER   = os.getenv("EMAIL_USER",   "polakenfold@gmail.com")
EMAIL_PASS   = os.getenv("EMAIL_PASS",   "ghca olpq vdav pllw")
BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL", "polakenfold.crypto666@blogger.com")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR    = PROJECT_ROOT / "blog" / "posts"
CHECKLIST    = PROJECT_ROOT / "blogposted.md"


def extract_title(html_path):
    txt = html_path.read_text(encoding='utf-8')
    m = re.search(r'<title>(.*?)</title>', txt, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return html_path.stem.replace('_', ' ')


def send_post(html_path, recipient):
    """Enviar un post a Blogger por email."""
    subject = extract_title(html_path)
    body = html_path.read_text(encoding='utf-8')
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
        print(f"✅ Publicado: {subject}")
        return True
    except Exception as e:
        print(f"❌ Error enviando {subject}: {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Publicar posts no subidos a Blogger via email")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar sin enviar")
    args = parser.parse_args()

    # Leer checklist
    with open(CHECKLIST, encoding='utf-8') as f:
        lines = f.readlines()

    pending = []
    for line in lines:
        line = line.strip()
        if line.startswith('- [ ]'):
            title = re.sub(r'^- \[ \] ', '', line)
            pending.append(title)

    print(f" Posts pending para publicar: {len(pending)}\n")

    for title in pending:
        # Buscar HTML file
        html_file = None
        for f in POSTS_DIR.glob("*.html"):
            content = f.read_text(encoding='utf-8')
            if title in content or title.lower() in content.lower():
                html_file = f
                break
        if not html_file:
            print(f"⚠️ No se encontró el archivo HTML para: {title}")
            continue
        if args.dry_run:
            print(f"[DRY RUN] would send: {html_file.name} -> {BLOGGER_EMAIL}")
        else:
            send_post(html_file, BLOGGER_EMAIL)


if __name__ == "__main__":
    main()