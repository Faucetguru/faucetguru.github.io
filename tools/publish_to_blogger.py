#!/usr/bin/env python3
"""Publicar UN post a Blogger via API (INSERT o UPDATE si ya existe).

Regla del usuario: 1 post a la vez, sin lotes. Este script publica solo el
slug que le pases. Usa token.pickle (OAuth nativo) ya configurado.

Uso:
  python3 tools/publish_to_blogger.py <slug-sin-extension>
  python3 tools/publish_to_blogger.py <slug> --dry-run

El post debe existir en blog/posts/<slug>.html (ya con anchors quitados).
"""
import argparse, sys, time, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _push_interlinks as P

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    post_path = P.POSTS / f"{args.slug}.html"
    if not post_path.exists():
        print(f"ERROR: no existe {post_path}")
        sys.exit(1)

    html = post_path.read_text(encoding="utf-8")
    title = P.extract_title(html)
    if not title:
        print("ERROR: no se encontro <title> en el post")
        sys.exit(1)

    # Blogger espera solo el fragmento interior del <body>, no el documento
    # HTML completo (DOCTYPE + head lo rechaza en silencio en INSERT).
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S | re.I)
    content = m.group(1).strip() if m else html

    svc = P.build_service()
    bposts = P.list_blogger_posts(svc)
    match = P.match_local_to_blogger(args.slug, bposts)
    body = {"kind": "blogger#post", "title": title, "content": content, "isDraft": False}

    if args.dry_run:
        print(f"[DRY] {'UPDATE' if match else 'INSERT'} -> {title}")
        print(f"[DRY] match id: {match['id'][:8] if match else 'NONE'}")
        return

    try:
        if match:
            res = svc.posts().update(blogId=P.BLOG_ID, postId=match["id"], body=body, publish=True).execute()
            post_id = res.get("id")
            url = res.get("url")
            print(f"OK UPDATE {args.slug} -> {url}")
        else:
            res = svc.posts().insert(blogId=P.BLOG_ID, body=body, isDraft=False).execute()
            post_id = res.get("id")
            url = res.get("url")
            print(f"OK INSERT {args.slug} -> {url}")
        # Verificacion real: Blogger puede tardar en reflejar el list.
        # Hacemos un get por ID para confirmar que existe de verdad.
        try:
            chk = svc.posts().get(blogId=P.BLOG_ID, postId=post_id).execute()
            if chk.get("id") != post_id:
                print(f"WARN: get devolvio id distinto")
        except Exception as e:
            print(f"WARN: no se pudo verificar por ID: {str(e)[:120]}")
    except Exception as e:
        print(f"ERR {args.slug}: {str(e)[:200]}")
        sys.exit(1)
    time.sleep(3)  # pausa para no pegarle seguido a la API

if __name__ == "__main__":
    main()
