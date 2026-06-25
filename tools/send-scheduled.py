#!/usr/bin/env python3
"""
Enviar un post pendiente cada 5 minutos a Blogger via email.
Ejecutar con: python3 tools/send-scheduled.py
STOP_FILE para detener: tocar tools/.stop-scheduled para detener
"""

import os
import re
import smtplib
import time
import signal
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

EMAIL_USER = os.getenv("EMAIL_USER", "polakenfold@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "ghca olpq vdav pllw")
BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL", "polakenfold.crypto666@blogger.com")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = PROJECT_ROOT / "blog" / "posts"
CHECKLIST = PROJECT_ROOT / "blogposted.md"
STOP_FILE = PROJECT_ROOT / ".stop-scheduled"
INTERVAL_SECONDS = 300  # 5 minutos

running = True

def signal_handler(signum, frame):
    global running
    running = False
    print("\n🛑 Señal recibida, continuando hasta el final del post actual...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def extract_title(html_path):
    txt = html_path.read_text(encoding='utf-8')
    m = re.search(r'<title>(.*?)</title>', txt, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return html_path.stem.replace('_', ' ')

def strip_links(html):
    return re.sub(r'<a\s+[^>]*>(.*?)</a>', r'\1', html, flags=re.IGNORECASE | re.DOTALL)

def send_post(html_path, recipient):
    subject = extract_title(html_path)
    body = strip_links(html_path.read_text(encoding='utf-8'))
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

def get_pending():
    with open(CHECKLIST, encoding='utf-8') as f:
        lines = f.readlines()
    pending = []
    for line in lines:
        line = line.strip()
        if line.startswith('- [ ]'):
            title = re.sub(r'^- \[ \] ', '', line)
            pending.append(title)
    return pending, lines

def mark_sent(lines, title):
    for i, line in enumerate(lines):
        if title in line and '- [ ]' in line:
            lines[i] = line.replace('- [ ]', '- [x]')
            break
    with open(CHECKLIST, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    print(f"🚀 Iniciando envío programado cada {INTERVAL_SECONDS}s")
    print(f"Para detener: touch {STOP_FILE}")
    print("-" * 50)

    while running:
        if STOP_FILE.exists():
            print("🛑 Archivo .stop-scheduled detectado, terminando...")
            STOP_FILE.unlink()
            break

        pending, lines = get_pending()
        if not pending:
            print("🎉 ¡Todos los posts han sido publicados!")
            break

        title = pending[0]
        html_file = None
        for f in POSTS_DIR.glob("*.html"):
            content = f.read_text(encoding='utf-8')
            if title in content or title.lower() in content.lower():
                html_file = f
                break

        if not html_file:
            print(f"⚠️ No se encontró HTML para: {title}")
            mark_sent(lines, title)
            continue

        if send_post(html_file, BLOGGER_EMAIL):
            mark_sent(lines, title)

        pending, _ = get_pending()
        if pending:
            print(f"⏳ Esperando {INTERVAL_SECONDS}s... (faltan {len(pending)} posts)")
            for _ in range(INTERVAL_SECONDS):
                if not running or STOP_FILE.exists():
                    return
                time.sleep(1)

if __name__ == "__main__":
    main()