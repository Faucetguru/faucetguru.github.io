#!/usr/bin/env python3
"""
Enviar exactamente 1 post pendiente a Blogger via email.
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

def main():
    with open(CHECKLIST, encoding='utf-8') as f:
        lines = f.readlines()

    pending = []
    for line in lines:
        line = line.strip()
        if line.startswith('- [ ]'):
            title = re.sub(r'^- \[ \] ', '', line)
            pending.append(title)

    if not pending:
        print("🎉 No hay posts pendientes")
        return
            
    title = pending[0]
    html_file = None
    for f in POSTS_DIR.glob("*.html"):
        content = f.read_text(encoding='utf-8')
        if title in content or title.lower() in content.lower():
            html_file = f
            break
    
    if html_file:
        if send_post(html_file, BLOGGER_EMAIL):
            for i, line in enumerate(lines):
                if title in line and '- [ ]' in line:
                    lines[i] = line.replace('- [ ]', '- [x]')
                    break
            with open(CHECKLIST, 'w', encoding='utf-8') as f:
                f.writelines(lines)

if __name__ == "__main__":
    main()
