#!/usr/bin/env python3
"""
FaucetGuru — Research de temas con BAJA COMPETENCIA para el blog.

Fuentes (sin credenciales, vía DuckDuckGo + Google Trends):
  - DuckDuckGo SERP (region ar-es): detecta dominios competidores en top resultados
  - DuckDuckGo "People Also Ask" / related questions (long-tail real de usuarios)
  - Google Trends (pytrends, geo=AR): temas en ascenso

Filtro de competencia:
  - Marca como ALTA competencia si el top-N SERP esta dominado por sitios grandes
    (CryptoNews, Cointelegraph, BeInCrypto, CoinDesk, etc.).
  - Devuelve solo temas de BAJA/MEDIA competencia (huecos de contenido).

Uso:
  python3 tools/research-topics.py            # imprime backlog priorizado
  python3 tools/research-topics.py --json out.json
  python3 tools/research-topics.py --seed "usdt argentina"   # una sola seed

Requiere: uv venv con ddgs + pytrends  (ver setup en RESEARCH_PLAN.md)
"""
import argparse
import json
import re
import sys
import time
import warnings

warnings.filterwarnings("ignore")  # silencia el rename warning de ddgs

# --- Seeds del RESEARCH_PLAN.md (ETAPA 1) ---
DEFAULT_SEEDS = [
    "faucet crypto argentina",
    "ganar crypto gratis",
    "usdt argentina",
    "wallet crypto",
    "bitcoin gratis",
    "faucet de criptomonedas",
    "como conseguir usdt",
    "mejor faucet 2026",
    "criptomonedas para principiantes argentina",
    "retirar crypto a pesos",
]

# Dominios "grandes" que indican SERP dominada (alta competencia)
BIG_DOMAINS = {
    "cryptonews.com", "cointelegraph.com", "es.cointelegraph.com",
    "beincrypto.com", "es.beincrypto.com", "coindesk.com", "coinmarketcap.com",
    "binance.com", "coinbase.com", "investing.com", "wikipedia.org",
    "reddit.com", "youtube.com", "medium.com", "forbes.com", "bbc.com",
}

REGION = "ar-es"
TRENDS_GEO = "AR"


def extract_domain(url: str) -> str:
    m = re.search(r"https?://([^/]+)/?", url or "")
    return m.group(1).lower().replace("www.", "") if m else ""


def _ddgs():
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS
    return DDGS()


def ddg_serp(seed: str, max_results: int = 10, retries: int = 3):
    """SERP vía html.duckduckgo.com (más estable que el wrapper para búsquedas directas)."""
    import time
    import requests
    from bs4 import BeautifulSoup
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "es-AR,es;q=0.9",
    }
    for i in range(retries):
        try:
            resp = requests.post(url, data={"q": seed}, headers=headers, timeout=20)
            soup = BeautifulSoup(resp.text, "html.parser")
            links = soup.select("a.result__a")
            out = []
            for a in links[:max_results]:
                href = a.get("href", "")
                # DDG redirige via //duckduckgo.com/l/?uddg=URL
                m = re.search(r"uddg=([^&]+)", href)
                real = requests.utils.unquote(m.group(1)) if m else href
                out.append({"title": a.get_text(strip=True), "href": real})
            return out
        except Exception:
            time.sleep(3 * (i + 1))
    return []


def ddg_related(seed: str, max_results: int = 8, retries: int = 3):
    """People Also Ask / preguntas relacionadas (long-tail real de usuarios)."""
    import time
    out = []
    queries = [f"{seed} preguntas frecuentes", f"cómo {seed}", f"{seed} opiniones"]
    for q in queries:
        for i in range(retries):
            try:
                with _ddgs() as ddgs:
                    for r in ddgs.text(q, region=REGION, max_results=max_results):
                        t = r.get("title", "").strip()
                        # filtrar ruido irrelevante (Google Wallet, dict, login)
                        if t and not re.search(r"google wallet|diccionario|traducir|log ?in|iniciar ses", t, re.I):
                            out.append(t)
                break
            except Exception:
                time.sleep(2 * (i + 1))
        time.sleep(1)
    # dedupe preservando orden
    seen, uniq = set(), []
    for t in out:
        if t.lower() not in seen:
            seen.add(t.lower())
            uniq.append(t)
    return uniq[:max_results]


def trends_related(seed: str):
    """Temas en ascenso via Google Trends (pytrends, geo=AR)."""
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="es-419", tz=360)
        pytrends.build_payload([seed], geo=TRENDS_GEO, timeframe="today 12-m")
        related = pytrends.related_queries()
        res = []
        if seed in related:
            for kind in ("top", "rising"):
                qs = related[seed].get(kind)
                if qs is not None:
                    for _, row in qs.head(5).iterrows():
                        res.append((row["query"], kind, int(row.get("value", 0))))
        return res
    except Exception as e:
        return [("TRENDS_ERROR: " + str(e)[:80], "err", 0)]


def competition_score(serp_domains: list) -> tuple:
    """Retorna (nivel, pct_big). nivel: 'ALTA'|'MEDIA'|'BAJA'."""
    if not serp_domains:
        return ("DESCONOCIDA", 0)
    big = sum(1 for d in serp_domains if d in BIG_DOMAINS)
    pct = big / len(serp_domains)
    if pct >= 0.5:
        return ("ALTA", round(pct * 100))
    if pct >= 0.2:
        return ("MEDIA", round(pct * 100))
    return ("BAJA", round(pct * 100))


def research(seed: str) -> dict:
    serp = ddg_serp(seed)
    domains = [extract_domain(r.get("href", "")) for r in serp]
    level, pct = competition_score(domains)
    related = ddg_related(seed)
    trends = trends_related(seed)
    return {
        "seed": seed,
        "competition": level,
        "big_pct": pct,
        "serp_domains": domains[:10],
        "paa": related[:8],
        "trends": trends[:8],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", action="append", help="seed (repetible); si se omite usa DEFAULT_SEEDS")
    ap.add_argument("--json", help="ruta de salida JSON")
    ap.add_argument("--top", type=int, default=10, help="max resultados a imprimir")
    args = ap.parse_args()

    seeds = args.seed if args.seed else DEFAULT_SEEDS
    print(f"=== Research FaucetGuru | {len(seeds)} seeds | region {REGION} ===\n")

    results = []
    for i, s in enumerate(seeds):
        try:
            r = research(s)
            results.append(r)
            flag = {"ALTA": "🔴", "MEDIA": "🟡", "BAJA": "🟢", "DESCONOCIDA": "⚪"}.get(r["competition"], "?")
            print(f"{flag} [{r['competition']} {r['big_pct']}%] {s}")
            if r["paa"]:
                print(f"    PAA: {r['paa'][0][:75]}")
        except Exception as e:
            print(f"⚠️  {s}: {e}")
        # backoff entre seeds para evitar rate-limit de DDG
        if i < len(seeds) - 1:
            time.sleep(4)

    # Backlog priorizado: BAJA primero, luego MEDIA
    order = {"BAJA": 0, "MEDIA": 1, "DESCONOCIDA": 2, "ALTA": 3}
    backlog = sorted([r for r in results if r["competition"] in ("BAJA", "MEDIA")],
                     key=lambda r: (order[r["competition"]], r["big_pct"]))

    print(f"\n=== BACKLOG DE BAJA COMPETENCIA ({len(backlog)}) ===")
    for r in backlog[:args.top]:
        print(f"🟢 {r['seed']}  (competencia {r['competition']})")
        for p in r["paa"][:3]:
            print(f"     • {p[:70]}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"results": results, "backlog": backlog}, f, ensure_ascii=False, indent=2)
        print(f"\n✔️  Guardado en {args.json}")


if __name__ == "__main__":
    main()
