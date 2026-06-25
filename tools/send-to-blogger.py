#!/usr/bin/env python3
"""
Enviar posts HTML a Blogger via email posting.
Uso: python3 tools/send-to-blogger.py

Requiere configurar:
- EMAIL_USER: tu email (ej: tuaccount@gmail.com)
- EMAIL_PASS: tu app password (no el password normal)
- BLOGGER_EMAIL: la dirección única de Blogger (te la da Blogger al configurar email posting)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Configuración - editar antes de usar
EMAIL_USER = os.getenv("EMAIL_USER", "polakenfold@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "ghca olpq vdav pllw")
BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL", "polakenfold.crypto666@blogger.com")

# Directorio de posts
POSTS_DIR = Path(__file__).parent.parent / "blog" / "posts"

# Posts a publicar (ajustar nombres según necesites)
POSTS_TO_PUBLISH = [
    "que-son-los-faucets-y-por-que-usarlos-en-2026.html",
    "gui-a-completa-como-usar-el-faucet-de-monad-para-ganar-tokens-gratis-en-2026.html",
    "gui-sonic-blaze-testnet-como-reclamar-tokens-gratis-para-ganar-sat-y-probar-la-blockchain.html",
    "berachain-faucet-guide-2026-como-obtener-tokens-de-prueba-gratis-artiosepolia.html",
    "como-usar-el-sui-faucet-2026-obten-sui-testnet-gratis-para-probar-la-blockchain.html",
    "backpack-wallet-review-2026-es-la-mejor-wallet-para-solana-monad-y-berachain.html",
]

def extract_title(html_path):
    """Extraer título del archivo HTML."""
    content = html_path.read_text(encoding='utf-8')
    import re
    match = re.search(r'<title>(.*?)</title>', content)
    if match:
        return match.group(1)
    match = re.search(r'<h1>(.*?)</h1>', content)
    if match:
        return match.group(1)
    return html_path.stem

def send_post(post_path, blogger_email):
    """Enviar un post a Blogger por email."""
    subject = extract_title(post_path)
    body = post_path.read_text(encoding='utf-8')
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = blogger_email
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
    parser = argparse.ArgumentParser(description="Publicar posts a Blogger via email")
    parser.add_argument("--email", default=BLOGGER_EMAIL, help="Dirección de email de Blogger")
    parser.add_argument("--user", default=EMAIL_USER, help="Email remitente (gmail)")
    parser.add_argument("--pass", dest="password", default=EMAIL_PASS, help="App password")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar sin enviar")
    args = parser.parse_args()
    
    if args.dry_run:
        print("=== DRY RUN - Posts a publicar ===")
        for post in POSTS_TO_PUBLISH:
            path = POSTS_DIR / post
            if path.exists():
                print(f"- {extract_title(path)}")
        return
    
    for post in POSTS_TO_PUBLISH:
        path = POSTS_DIR / post
        if path.exists():
            send_post(path, args.email)
        else:
            print(f"⚠️ No encontrado: {post}")

if __name__ == "__main__":
    main()