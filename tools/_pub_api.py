#!/usr/bin/env python3
"""Publicar UN post a Blogger por API (insert). Remove-anchors en memoria.
Uso: python3 tools/_pub_api.py <archivo.html>
El blog_id está hardcodeado para CryptoFuente.
"""
import sys, re, pickle
from pathlib import Path
from googleapiclient.discovery import build

BLOG_ID = "8989148619439472689"
ROOT = Path("/home/salma/faucetguru.github.io")
POSTS = ROOT / "blog/posts"

def load_creds():
    with open(ROOT / "tools/token.pickle", "rb") as f:
        return pickle.load(f)

def extract_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return None

def strip_anchors(html):
    # Quita las etiquetas <a> pero deja el texto interior (interlinking como texto plano)
    return re.sub(r"<a\b[^>]*>(.*?)</a>", r"\1", html, flags=re.S | re.I)

def publish(fname):
    path = POSTS / fname
    if not path.exists():
        print("NO_EXISTE", fname); return False
    html = path.read_text(encoding="utf-8")
    title = extract_title(html)
    if not title:
        print("NO_TITLE", fname); return False
    content = strip_anchors(html)
    creds = load_creds()
    service = build("blogger", "v3", credentials=creds)
    body = {"kind": "blogger#post", "title": title, "content": content, "isDraft": False}
    try:
        res = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=False).execute()
        pid = res.get("id")
        print(f"OK {fname} -> post id {pid} | url: {res.get('url')}")
        return True
    except Exception as e:
        print("ERR", fname, str(e)[:300])
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 tools/_pub_api.py <archivo.html>"); sys.exit(1)
    publish(sys.argv[1])
