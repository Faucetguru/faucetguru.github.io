#!/usr/bin/env python3
"""Publicar/actualizar todos los posts con interlinking en Blogger.
CORREGIDO: matching local->blogger por palabra clave (no por slug exacto).
- Si el post local matchea un post existente en Blogger: posts.update.
- Si no: posts.insert.
Loop secuencial + pausa 3s. Dry-run por defecto.
"""
import re, time, sys, pickle
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = Path("/home/salma/faucetguru.github.io")
POSTS = ROOT / "blog/posts"
BLOG_ID = "8989148619439472689"

def get_creds():
    with open(ROOT / "tools/token.pickle", "rb") as f:
        return pickle.load(f)

def extract_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    return None

# Palabra clave que identifica cada post local -> debe aparecer en la URL de Blogger
KEYWORDS = {
    "99faucet-reseña": "99faucet",
    "abc-mining-reseña": "abc-mining",
    "aci-airdrop-guia-como-participar-desde-argentina": "aci-airdrop",
    "autofaucet-dutchycorp-reseña": "autofaucet-dutchycorp",
    "backpack-wallet-review-2026-es-la-mejor-wallet-para-solana-monad-y-berachain": "backpack-wallet",
    "berachain-faucet-guide-2026-como-obtener-tokens-de-prueba-gratis-artiosepolia": "berachain-faucet",
    "bnbfaucet-doge-reseña": "bnbfaucet-doge",
    "cashmonster-reseña": "cashmonster",
    "coinpayu-reseña": "coinpayu",
    "cointiply-reseña": "cointiply",
    "como-usar-el-sui-faucet-2026-obten-sui-testnet-gratis-para-probar-la-blockchain": "sui-faucet",
    "cómo-retirar-satoshis-desde-argentina-de-forma-segura": "retirar-satoshis",
    "earnbonk-reseña": "earnbonk",
    "earncrypto-reseña": "earncrypto",
    "easytrx-io-reseña": "easytrxio",
    "faucetcrypto-reseña": "faucetcrypto",
    "faucetpay-reseña": "faucetpay",
    "faucets-btc-vs-usdt-vs-tron": "btc-vs-usdt-vs-tron",
    "faucets-criptomonedas-argentina-guia-2026": "faucets-de-criptomonedas",
    "faucets-crypto-2026-todo-lo-que-necesitas-saber": "faucets-crypto-2026",
    "faucets-más-rápidas-para-ganar-satoshis": "faucets-mas-rapidas",
    "faucets-que-pagan-al-instante-vs-retiro-lento": "pagan-al-instante",
    "faucetwallet-reseña": "faucetwallet",
    "freebitcoin-reseña": "freebitcoin",
    "freebtcco-reseña": "freebtcco",
    "freetron-reseña": "freetron",
    "gamehag-reseña": "gamehag",
    "gemifaucet-telegram-faucet-crypto-argentina": "gemifaucet",
    "grass-reseña": "grass",
    "gui-a-completa-como-usar-el-faucet-de-monad-para-ganar-tokens-gratis-en-2026": "faucet-de-monad",
    "gui-sonic-blaze-testnet-como-reclamar-tokens-gratis-para-ganar-sat-y-probar-la-blockchain": "sonic-blaze",
    "guía-completa-ganar-bitcoin-gratis-en-argentina": "ganar-bitcoin-gratis",
    "keran-usdt-reseña": "keran-usdt",
    "litecoin-farm--alerta--reseña": "litecoin-farm",
    "litecoin-farm-online-reseña": "litecoin-farm-online",
    "litepick-reseña": "litepick",
    "ltcminer-reseña": "ltcminer",
    "luckywatch-reseña": "luckywatch",
    "makeyoutask-reseña": "makeyoutask",
    "mejores-faucets-para-argentinos-2026": "mejores-faucets-para-argentinos",
    "mejores-faucets-por-payout-mínimo": "mejores-faucets-por-payout",
    "mejores-wallets-para-recibir-usdt-2026": "mejores-wallets-para-recibir",
    "multiminer-reseña": "multiminer",
    "my-cwallet-reseña": "my-cwallet",
    "que-son-los-faucets-y-por-que-usarlos-en-2026": "que-son-los-faucets",
    "ready-wallet-starknet-guia-argentina": "ready-wallet",
    "realix-reseña": "realix",
    "rollercoin-reseña": "rollercoin",
    "scalevance-reseña": "scalevance",
    "tangem-wallet-argentina-billetera-hardware-segura": "tangem-wallet",
    "top-10-faucets-por-trust-score": "top-10-faucets",
    "top69-crypto-casinos-reseña": "top69-crypto-casinos",
    "tronpayu-io-reseña": "tronpayu",
    "tutorial-ganar-bitcoin-gratis-desde-celular": "ganar-bitcoin-gratis-desde",
    "vie-faucet-reseña": "vie-faucet",
    "wipter-reseña": "wipter",
}

def build_service():
    return build("blogger", "v3", credentials=get_creds())

def list_blogger_posts(svc):
    """Devuelve lista de (slug_blogger, id, url, title)."""
    out = []
    req = svc.posts().list(blogId=BLOG_ID, maxResults=50, fields="items(title,url,id),nextPageToken")
    while req:
        resp = req.execute()
        for p in resp.get("items", []):
            m = re.search(r"/(\d{4})/(\d{2})/([^.]+)\.html", p["url"])
            slug = m.group(3) if m else p["title"]
            out.append({"slug": slug, "id": p["id"], "url": p["url"], "title": p["title"]})
        req = svc.posts().list_next(req, resp)
    return out

def match_local_to_blogger(local_slug, blogger_posts):
    kw = KEYWORDS.get(local_slug)
    if not kw:
        return None
    for bp in blogger_posts:
        if kw in bp["slug"] or kw in bp["url"]:
            return bp
    return None

def main():
    dry = "--dry" in sys.argv
    svc = build_service()
    bposts = list_blogger_posts(svc)
    print(f"Posts en Blogger: {len(bposts)}")
    updates, inserts = 0, 0
    for p in sorted(POSTS.glob("*.html")):
        if p.name == "index.html":
            continue
        slug = p.stem
        html = p.read_text(encoding="utf-8")
        title = extract_title(html)
        match = match_local_to_blogger(slug, bposts)
        if match:
            print(f"  [UPDATE id={match['id'][:8]}..] {slug}")
            updates += 1
        else:
            print(f"  [INSERT] {slug}")
            inserts += 1
    print(f"\nRESÚMEN: {updates} updates + {inserts} inserts = {updates+inserts}")
    if dry:
        print("(DRY RUN - no se tocó Blogger)")
        return

    # --- Loop real con pausa ---
    print("\n=== EJECUTANDO ===")
    for p in sorted(POSTS.glob("*.html")):
        if p.name == "index.html":
            continue
        slug = p.stem
        html = p.read_text(encoding="utf-8")
        title = extract_title(html)
        match = match_local_to_blogger(slug, bposts)
        body = {"kind": "blogger#post", "title": title, "content": html, "isDraft": False}
        try:
            if match:
                res = svc.posts().update(blogId=BLOG_ID, postId=match["id"], body=body, publish=True).execute()
                print(f"  OK UPDATE {slug} -> {res.get('url')}")
            else:
                res = svc.posts().insert(blogId=BLOG_ID, body=body, isDraft=False).execute()
                print(f"  OK INSERT {slug} -> {res.get('url')}")
        except HttpError as e:
            print(f"  ERR {slug}: {str(e)[:200]}")
        time.sleep(3)
    print("=== FIN ===")

if __name__ == "__main__":
    main()
