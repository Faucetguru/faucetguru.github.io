#!/usr/bin/env python3
"""Auditar interlinking:
- Blogger real: listar posts con sus URLs reales.
- Locales: contar <a> por post y a donde apuntan.
"""
import re, pickle
from pathlib import Path
from googleapiclient.discovery import build

BLOG_ID = "8989148619439472689"
ROOT = Path("/home/salma/faucetguru.github.io")
POSTS = ROOT / "blog/posts"

def load_creds():
    with open(ROOT / "tools/token.pickle", "rb") as f:
        return pickle.load(f)

def list_blogger():
    creds = load_creds()
    svc = build("blogger", "v3", credentials=creds)
    out = {}
    req = svc.posts().list(blogId=BLOG_ID, maxResults=50, fields="items(title,url,id),nextPageToken")
    while req:
        resp = req.execute()
        for p in resp.get("items", []):
            title = p["title"]
            # slug aproximado desde la url
            m = re.search(r"/(\d{4})/(\d{2})/([^.]+)\.html", p["url"])
            slug = m.group(3) if m else title
            out[slug] = {"url": p["url"], "title": title, "id": p["id"]}
        req = svc.posts().list_next(req, resp)
    return out

def audit_local():
    res = {}
    for p in sorted(POSTS.glob("*.html")):
        if p.name == "index.html":
            continue
        html = p.read_text(encoding="utf-8")
        links = re.findall(r'<a\b[^>]*href="([^"]+)"', html, re.I)
        res[p.stem] = links
    return res

def main():
    print("=== LISTANDO BLOGGER ===")
    bgr = list_blogger()
    print(f"Posts en Blogger: {len(bgr)}")
    for slug, d in bgr.items():
        print(f"  {slug} -> {d['url']}")

    print("\n=== AUDIT LOCAL ===")
    local = audit_local()
    no_links = [s for s, ls in local.items() if not ls]
    print(f"Posts locales (sin index): {len(local)}")
    print(f"Posts locales SIN ningun <a>: {len(no_links)}")
    print("Slugs sin enlaces:")
    for s in no_links:
        print("  -", s)

if __name__ == "__main__":
    main()
