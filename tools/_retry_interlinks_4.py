#!/usr/bin/env python3
"""Reintenta interlinks SOLO para los 4 posts que fallaron por cuota (429).
Wrapper acotado sobre la logica de _push_interlinks.py para no re-tocar
los ~46 posts ya publicados. Pausa 8s entre llamadas para esquivar rate limit.
"""
import time, sys
sys.path.insert(0, "/home/salma/faucetguru.github.io/tools")
import _push_interlinks as P

FAILED = [
    "top69-crypto-casinos-reseña",
    "tronpayu-io-reseña",
    "tutorial-ganar-bitcoin-gratis-desde-celular",
    "vie-faucet-reseña",
]

def main():
    svc = P.build_service()
    bposts = P.list_blogger_posts(svc)
    print(f"Posts en Blogger: {len(bposts)}")
    print(f"Reintentando {len(FAILED)} posts que fallaron por 429...\n")
    ok, err = 0, 0
    for slug in FAILED:
        html = (P.POSTS / f"{slug}.html").read_text(encoding="utf-8")
        title = P.extract_title(html)
        match = P.match_local_to_blogger(slug, bposts)
        body = {"kind": "blogger#post", "title": title, "content": html, "isDraft": False}
        try:
            if match:
                res = svc.posts().update(blogId=P.BLOG_ID, postId=match["id"], body=body, publish=True).execute()
                print(f"  OK UPDATE {slug} -> {res.get('url')}")
            else:
                res = svc.posts().insert(blogId=P.BLOG_ID, body=body, isDraft=False).execute()
                print(f"  OK INSERT {slug} -> {res.get('url')}")
            ok += 1
        except Exception as e:
            print(f"  ERR {slug}: {str(e)[:200]}")
            err += 1
        time.sleep(8)
    print(f"\n=== FIN: {ok} OK, {err} ERR ===")

if __name__ == "__main__":
    main()
