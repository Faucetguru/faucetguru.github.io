#!/usr/bin/env python3
"""Generar bloque 'Posts relacionados' con interlinking para todos los posts.
- Blogger -> Blogger: 2-3 URLs reales de otros posts del blog.
- Ext link: siempre faucetguru.github.io + web oficial si trustScore>=3.0.
Excluye scams (trustScore < 3.0) del ext link.
Escribe el bloque inyectado en blog/posts/*.html (al pie, antes de </body>).
NO publica; solo prepara los locales. Luego se publica/actualiza por API.
"""
import re, json, pickle
from pathlib import Path
from googleapiclient.discovery import build

ROOT = Path("/home/salma/faucetguru.github.io")
POSTS = ROOT / "blog/posts"
BLOG_ID = "8989148619439472689"

# ---- 1) Mapa slug_local -> URL real Blogger (de los ya publicados) ----
# Obtenido del audit. Para los faltantes se completa al publicar.
BLOGGER_URLS = {
    "que-son-los-faucets-y-por-que-usarlos-en-2026": "https://cryptofuente.blogspot.com/2026/06/que-son-los-faucets-y-por-que-usarlos.html",
    "gui-a-completa-como-usar-el-faucet-de-monad-para-ganar-tokens-gratis-en-2026": "https://cryptofuente.blogspot.com/2026/06/guia-completa-como-usar-el-faucet-de.html",
    "gui-sonic-blaze-testnet-como-reclamar-tokens-gratis-para-ganar-sat-y-probar-la-blockchain": "https://cryptofuente.blogspot.com/2026/06/guia-sonic-blaze-testnet-como-reclamar.html",
    "berachain-faucet-guide-2026-como-obtener-tokens-de-prueba-gratis-artiosepolia": "https://cryptofuente.blogspot.com/2026/06/berachain-faucet-guide-2026-como.html",
    "como-usar-el-sui-faucet-2026-obten-sui-testnet-gratis-para-probar-la-blockchain": "https://cryptofuente.blogspot.com/2026/06/como-usar-el-sui-faucet-2026-obten-sui.html",
    "backpack-wallet-review-2026-es-la-mejor-wallet-para-solana-monad-y-berachain": "https://cryptofuente.blogspot.com/2026/06/backpack-wallet-review-2026-es-la-mejor.html",
    "autofaucet-dutchycorp-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-autofaucet-dutchycorp-es.html",
    "freetron-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-freetron-es-confiable-para.html",
    "faucetwallet-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-faucetwallet-es-confiable.html",
    "faucetcrypto-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-faucetcrypto-es-la-plataforma.html",
    "faucetpay-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-faucetpay-es-confiable-para.html",
    "easytrx-io-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-easytrxio-es-confiable-para.html",
    "99faucet-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-99faucet-es-confiable-para.html",
    "gamehag-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-gamehag-ganar-crypto-jugando.html",
    "freebtcco-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-freebtcco-es-confiable-para.html",
    "earnbonk-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-earnbonk-es-confiable-para.html",
    "cointiply-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-cointiply-es-confiable-para.html",
    "coinpayu-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-coinpayu-es-confiable-para.html",
    "cashmonster-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-cashmonster-es-la-mejor.html",
    "bnbfaucet-doge-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-bnbfaucet-doge-es-confiable.html",
    "gemifaucet-telegram-faucet-crypto-argentina": "https://cryptofuente.blogspot.com/2026/06/gemifaucet-la-faucet-de-telegram-que.html",
    "tangem-wallet-en-argentina-la-mejor": "https://cryptofuente.blogspot.com/2026/06/tangem-wallet-en-argentina-la-mejor.html",
    "aci-airdrop-guia-como-participar-desde-argentina": "https://cryptofuente.blogspot.com/2026/06/aci-airdrop-como-participar-desde.html",
    "abc-mining-reseña": "https://cryptofuente.blogspot.com/2026/06/resena-de-abc-mining-es-confiable-para.html",
    "como-retirar-satoshis-desde-argentina-de-forma-segura": "https://cryptofuente.blogspot.com/2026/06/como-retirar-satoshis-desde-argentina_09642586.html",
    "faucets-btc-vs-usdt-vs-tron": "https://cryptofuente.blogspot.com/2026/06/btc-vs-usdt-vs-tron-description-cual.html",
    "earncrypto-reseña": "https://cryptofuente.blogspot.com/2026/07/resena-de-earncrypto-es-confiable-para.html",
    "faucets-criptomonedas-argentina-guia-2026": "https://cryptofuente.blogspot.com/2026/07/faucets-de-criptomonedas-en-argentina.html",
}

# ---- 2) Categorías para relacionar posts ----
def categorize(slug):
    s = slug.lower()
    if any(k in s for k in ["wallet", "cwallet", "billetera"]): return "wallet"
    if any(k in s for k in ["mining", "miner", "multiminer", "grass", "farm"]): return "mining"
    if any(k in s for k in ["airdrop"]): return "airdrop"
    if any(k in s for k in ["guia", "gui-", "tutorial", "como", "testnet", "faucet-"]): return "guia"
    if any(k in s for k in ["faucet", "reseña", "review"]): return "faucet"
    return "general"

# ---- 3) Mapa slug -> trustScore de la faucet reseñada (para ext link) ----
# Extraido de faucets.js (id -> trustScore). Se hace match por nombre en el titulo.
FAUCET_TRUST = {
    "freebitco": 4.9, "rollercoin": 4.7, "cointiply": 4.6, "faucetpay": 4.5,
    "coinpayu": 4.4, "faucetcrypto": 4.3, "freebtcco": 4.2, "freetron": 4.1,
    "faucetwallet": 4.0, "99faucet": 3.9, "gamehag": 3.8, "earnbonk": 3.7,
    "earncrypto": 3.6, "autofaucet-dutchycorp": 3.5, "easytrx": 3.4, "cashmonster": 3.3,
    "bnbfaucet-doge": 3.2, "gemifaucet": 3.1, "tangem": 4.8, "backpack": 4.6,
    "sui": 4.0, "monad": 4.0, "berachain": 4.0, "sonic": 4.0, "abc-mining": 1.0,
    "ltcminer": 1.0, "litecoin-farm": 1.0, "litepick": 2.0, "multiminer": 2.0,
    "my-cwallet": 2.5, "keran-usdt": 2.8, "luckywatch": 2.0, "makeyoutask": 2.5,
    "realix": 2.0, "scalevance": 2.5, "vie-faucet": 2.0, "wipter": 2.0,
}

# Mapa slug -> URL oficial (solo si trustScore>=3.0 se usa como ext link)
FAUCET_OFFICIAL = {
    "freebitco": "https://freebitco.in", "rollercoin": "https://rollercoin.com",
    "cointiply": "https://cointiply.com", "faucetpay": "https://faucetpay.io",
    "coinpayu": "https://coinpayu.com", "faucetcrypto": "https://faucetcrypto.com",
    "freebtcco": "https://freebtcco.com", "freetron": "https://fretron.com",
    "faucetwallet": "https://faucetwallet.com", "99faucet": "https://99faucet.com",
    "gamehag": "https://gamehag.com", "earnbonk": "https://earnbonk.com",
    "earncrypto": "https://earncrypto.com", "autofaucet-dutchycorp": "https://autofaucet.dutchycorp.com",
    "easytrx": "https://easytrx.io", "cashmonster": "https://cashmonster.com",
    "bnbfaucet-doge": "https://bnbfaucet.com", "gemifaucet": "https://gemifaucet.com",
    "tangem": "https://tangem.com", "backpack": "https://backpack.exchange",
    "sui": "https://sui.io", "monad": "https://monad.xyz", "berachain": "https://berachain.com",
    "sonic": "https://sonic.game",
}

EXT_SITE = "https://faucetguru.github.io"

def trust_for(slug):
    for k, v in FAUCET_TRUST.items():
        if k in slug:
            return v
    return None

def official_for(slug):
    for k, v in FAUCET_OFFICIAL.items():
        if k in slug:
            return v
    return None

def related_slugs(slug):
    cat = categorize(slug)
    # Todos los slugs excepto el actual, priorizando misma categoria
    others = [s for s in BLOGGER_URLS if s != slug]
    same_cat = [s for s in others if categorize(s) == cat]
    diff_cat = [s for s in others if categorize(s) != cat]
    # Tomar 3 de misma cat, completar con diff
    picked = (same_cat + diff_cat)[:3]
    return picked

def build_block(slug):
    rel = related_slugs(slug)
    items = []
    for s in rel:
        url = BLOGGER_URLS.get(s, "#")
        label = s.replace("-", " ").title()
        items.append(f'    <li><a href="{url}">{label}</a></li>')
    block = '<h3>Posts relacionados</h3>\n<ul>\n' + "\n".join(items) + "\n</ul>\n"
    # Ext links
    ext_items = [f'    <li><a href="{EXT_SITE}">FaucetGuru - Directorio de faucets</a></li>']
    t = trust_for(slug)
    off = official_for(slug)
    if off and (t is None or t >= 3.0):
        ext_items.append(f'    <li><a href="{off}" rel="nofollow">Sitio oficial</a></li>')
    block += '<h3>Enlaces útiles</h3>\n<ul>\n' + "\n".join(ext_items) + "\n</ul>\n"
    return block

def inject(html, slug):
    block = build_block(slug)
    # Insertar antes de </body>
    if "</body>" in html:
        return html.replace("</body>", block + "</body>", 1)
    return html.rstrip() + "\n" + block

def main():
    done = 0
    for p in sorted(POSTS.glob("*.html")):
        if p.name == "index.html":
            continue
        slug = p.stem
        html = p.read_text(encoding="utf-8")
        if '<h3>Posts relacionados</h3>' in html:
            print("YA TIENE:", slug); continue
        new = inject(html, slug)
        p.write_text(new, encoding="utf-8")
        done += 1
        print("INYECTADO:", slug)
    print(f"\nTotal inyectados: {done}")

if __name__ == "__main__":
    main()
