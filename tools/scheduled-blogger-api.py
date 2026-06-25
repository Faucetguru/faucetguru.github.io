#!/usr/bin/env python3
"""
Blogger API v3 - Envia posts a Blogger usando API oficial.
Requiere: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
Requiere: tools/credentials.json (OAuth Desktop App credentials)
"""

import os
import re
import pickle
import sys
import time
import signal
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']
CREDENTIALS_FILE = 'tools/credentials.json'
TOKEN_FILE = 'tools/token.pickle'
BLOG_ID = os.getenv('BLOGGER_BLOG_ID', '')
PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = PROJECT_ROOT / "blog" / "posts"
CHECKLIST = PROJECT_ROOT / "blogposted.md"
STOP_FILE = PROJECT_ROOT / ".stop-scheduled"
INTERVAL_SECONDS = 300

running = True

def signal_handler(signum, frame):
    global running
    running = False
    print("\n🛑 Señal recibida, terminando...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

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

def strip_links(html):
    return re.sub(r'<a\s+[^>]*>(.*?)</a>', r'\1', html, flags=re.IGNORECASE | re.DOTALL)

def post_to_blogger(service, title, content):
    body = {
        'kind': 'blogger#post',
        'title': title,
        'content': strip_links(content)
    }
    result = service.posts().insert(blogId=BLOG_ID, body=body).execute()
    print(f"✅ Publicado: {title} (ID: {result['id']})")
    return True

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ {CREDENTIALS_FILE} no encontrado")
        print("   Ver BLOGGER_API_SETUP.md para crear credenciales OAuth Desktop App")
        sys.exit(1)

    if not BLOG_ID:
        print("❌ BLOGGER_BLOG_ID no configurado")
        print("   Usa: BLOGGER_BLOG_ID=TU_ID python3 tools/scheduled-blogger-api.py")
        sys.exit(1)

    print(f"🚀 Blogger API Scheduler - cada {INTERVAL_SECONDS}s")
    print(f"Blog ID: {BLOG_ID}")
    print(f"Para detener: touch {STOP_FILE}")
    print("-" * 50)

    while running:
        if STOP_FILE.exists():
            print("🛑 Detenido por archivo .stop-scheduled")
            STOP_FILE.unlink()
            break

        pending, lines = get_pending()
        if not pending:
            print("🎉 ¡Todos los posts publicados!")
            break

        title = pending[0]
        html_file = None
        for f in POSTS_DIR.glob("*.html"):
            content = f.read_text(encoding='utf-8')
            if title in content or title.lower() in content.lower():
                html_file = f
                break

        if not html_file:
            print(f"⚠️ No se encontró HTML: {title}")
            mark_sent(lines, title)
            continue

        try:
            creds = get_credentials()
            service = build('blogger', 'v3', credentials=creds)
            if post_to_blogger(service, title, html_file.read_text(encoding='utf-8')):
                mark_sent(lines, title)
        except Exception as e:
            print(f"❌ Error: {e}")

        pending, _ = get_pending()
        if pending and running:
            print(f"⏳ Esperando {INTERVAL_SECONDS}s... (faltan {len(pending)})")
            for _ in range(INTERVAL_SECONDS):
                if not running or STOP_FILE.exists():
                    return
                time.sleep(1)

if __name__ == "__main__":
    main()