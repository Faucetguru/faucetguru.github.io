#!/usr/bin/env python3
"""Publicar UN post a Blogger por API, CON interlinking (related posts).
Uso: python3 tools/_pub_api_link.py <archivo.html> [--related slug1 slug2 ...]
Inyecta al final un bloque 'Posts relacionados' con URLs reales de Blogger.
"""
import sys, re, pickle
from pathlib import Path
from googleapiclient.discovery import build

BLOG_ID = "8989148619439472689"
ROOT = Path("/home/salma/faucetguru.github.io")
POSTS = ROOT / "blog/posts"

# Mapa slug_local -> URL real en Blogger (de los ya publicados)
RELATED_URLS = {
    "que-son-los-faucets-y-por-que-usarlos-en-2026": "https://cryptofuente.blogspot.com/2026/07/que-son-los-faucets-y-por-que-usarlos.html",
    "gui-a-completa-como-usar-el-faucet-de-monad-para-ganar-tokens-gratis-en-2026": "https://cryptofuente.blogspot.com/2026/07/guia-completa-como-usar-el-faucet-de.html",
    "gui-sonic-blaze-testnet-como-reclamar-tokens-gratis-para-ganar-sat-y-probar-la-blockchain": "https://cryptofuente.blogspot.com/2026/07/guia-sonic-blaze-testnet-como-reclamar.html",
    "berachain-faucet-guide-2026-como-obtener-tokens-de-prueba-gratis-artiosepolia": "https://cryptofuente.blogspot.com/2026/07/berachain-faucet-guide-2026-como.html",
    "como-usar-el-sui-faucet-2026-obten-sui-testnet-gratis-para-probar-la-blockchain": "https://cryptofuente.blogspot.com/2026/07/como-usar-el-sui-faucet-2026-obten-sui.html",
    "backpack-wallet-review-2026-es-la-mejor-wallet-para-solana-monad-y-berachain": "https://cryptofuente.blogspot.com/2026/07/backpack-wallet-review-2026-es-la-mejor.html",
    "cointiply-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-cointiply-es-confiable-para.html",
    "freebitcoin-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-freebitcoin-es-la-faucet-mas.html",
    "rollercoin-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-rollercoin-es-el-mejor.html",
    "coinpayu-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-coinpayu-es-confiable-para.html",
    "faucetpay-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-faucetpay-es-confiable-para.html",
    "faucetcrypto-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-faucetcrypto-es-la.html",
    "earncrypto-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-earncrypto-es-confiable-para.html",
}

def load_creds():
    with open(ROOT / "tools/token.pickle", "rb") as f:
        return pickle.load(f)

def extract_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    return None

def related_block(slugs):
    items = []
    for s in slugs:
        if s in RELATED_URLS:
            items.append(f'  <li><a href="{RELATED_URLS[s]}">{s}</a></li>')
    if not items:
        return ""
    return "\n<h3>Posts relacionados</h3>\n<ul>\n" + "\n".join(items) + "\n</ul>\n"

def publish(fname, related_slugs=None):
    path = POSTS / fname
    if not path.exists():
        print("NO_EXISTE", fname); return False
    html = path.read_text(encoding="utf-8")
    title = extract_title(html)
    if not title:
        print("NO_TITLE", fname); return False
    # Conservar los <a> originales (NO borrarlos)
    content = html
    if related_slugs:
        content = content.rstrip() + "\n" + related_block(related_slugs)
    creds = load_creds()
    service = build("blogger", "v3", credentials=creds)
    body = {"kind": "blogger#post", "title": title, "content": content, "isDraft": False}
    try:
        res = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=False).execute()
        print(f"OK {fname} -> id {res.get('id')} | {res.get('url')}")
        return True
    except Exception as e:
        print("ERR", fname, str(e)[:300]); return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 tools/_pub_api_link.py <archivo.html> [slugs relacionados...]"); sys.exit(1)
    fname = sys.argv[1]
    related = sys.argv[2:]
    publish(fname, related)
