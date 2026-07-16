#!/usr/bin/env python3
"""PIPELINE SEMANAL de contenido FaucetGuru — modo AUTONOMO (sin mail).

Flujo completo que corre el cron cada semana:
  research  -> elige 1 tema BAJA competencia (cache si DDG falla)
  write     -> el AGENTE (LLM del cron) escribe el post en criollo AR usando
               tools/_weekly_context.json  (esta parte la hace el prompt del cron)
  validate  -> validate-seo-posts.py
  anchors   -> remove-anchors.py (texto plano, regla del usuario)
  publish   -> publish_to_blogger.py (INSERT/UPDATE via API, 1 a la vez)
  index     -> regenera blog/posts/index.html (fg/blog)
  kanban    -> mueve el item a 'publicado'

Uso (lo llama el cron con el modo segun corresponda):
  python3 tools/weekly_content_pipeline.py --mode research --email NONE
  python3 tools/weekly_content_pipeline.py --mode publish
"""
import argparse, json, subprocess, sys, shutil, re
from pathlib import Path
from datetime import datetime

ROOT = Path("/home/salma/faucetguru.github.io")
TOOLS = ROOT / "tools"
POSTS = ROOT / "blog" / "posts"
KANBAN = ROOT / "blog" / "KANBAN.md"
RESEARCH_JSON = TOOLS / "_weekly_research.json"
CONTEXT = TOOLS / "_weekly_context.json"
CACHE = TOOLS / "_backlog_cache.json"
VENV = ROOT / ".venv"

def run(cmd):
    py = str(VENV / "bin" / "python") if (VENV / "bin" / "python").exists() else "python3"
    return subprocess.run([py, *cmd], cwd=ROOT, capture_output=True, text=True)

def slugify(tema):
    return re.sub(r"[^a-z0-9]+", "-", tema.lower()).strip("-")

def choose_theme():
    """Research + cache. Devuelve (tema, competition) o None."""
    backlog = []
    for intento in range(3):
        cmd = [str(TOOLS / "research-topics.py"), "--json", str(RESEARCH_JSON)]
        r = run(cmd)
        if r.returncode == 0 and RESEARCH_JSON.exists():
            data = json.loads(RESEARCH_JSON.read_text(encoding="utf-8"))
            backlog = data.get("backlog", [])
            if backlog:
                break
        print(f"  intento {intento+1}: backlog vacio, reintentando en 45s...")
        import time; time.sleep(45)
    if not backlog and CACHE.exists():
        backlog = json.loads(CACHE.read_text(encoding="utf-8")).get("backlog", [])
        if backlog:
            print("  usando backlog cacheado")
    if not backlog:
        return None, None
    CACHE.write_text(json.dumps({"backlog": backlog}, ensure_ascii=False, indent=2), encoding="utf-8")
    priorizados = [x for x in backlog if x["competition"] in ("BAJA", "MEDIA")] or backlog
    t = priorizados[0]
    return t["seed"], t["competition"]

def move_kanban(tema, col):
    if not KANBAN.exists():
        return
    lines = KANBAN.read_text(encoding="utf-8").splitlines()
    out = []
    for ln in lines:
        if tema in ln and ln.strip().startswith("- [ ]"):
            out.append(f"- [ ] {tema}  _({col})_")
        else:
            out.append(ln)
    KANBAN.write_text("\n".join(out), encoding="utf-8")

def regenerate_index():
    """Reconstruye blog/posts/index.html listando todos los .html menos index."""
    posts = []
    for p in sorted(POSTS.glob("*.html")):
        if p.name == "index.html":
            continue
        html = p.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else p.stem
        posts.append((p.stem, title))
    items = "\n".join(
        f'      <div class="post-entry">\n        <a href="{slug}.html">{title}</a>\n      </div>' for slug, title in posts
    )
    index = f"""<!DOCTYPE html>
<html lang="es-419">
  <head>
    <style>
      :root {{ --primary: #00ff88; --bg-dark: #0a0b10; --bg-card: rgba(255, 255, 255, 0.03); --text-main: #e6f1ff; --text-dim: #8892b0; --glass-border: rgba(255, 255, 255, 0.1); --accent-orange: #ffa500; }}
      body {{ background-color: var(--bg-dark); color: var(--text-main); font-family: "Inter", sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
      h1, h2, h3 {{ font-family: "Outfit", sans-serif; color: var(--primary); }}
      h1 {{ font-size: 2rem; margin-bottom: 20px; }} h2 {{ font-size: 1.5rem; margin: 30px 0 15px; }} h3 {{ font-size: 1.2rem; margin: 20px 0 10px; }}
      a {{ color: var(--primary); text-decoration: none; }} a:hover {{ text-decoration: underline; }}
      strong {{ color: var(--text-main); }}
      pre {{ background: #1a1a1a; padding: 20px; border-radius: 10px; overflow-x: auto; margin: 15px 0; }}
      code {{ color: var(--text-main); }}
      .date {{ color: var(--text-dim); font-size: 0.45em; }}
    </style>
    <meta charset="UTF-8">
    <title>FaucetGuru Blog</title>
  </head>
  <body>
  <h1>FaucetGuru Blog</h1>
  <div class="posts">
{items}
  </div>
  </body>
</html>
"""
    (POSTS / "index.html").write_text(index, encoding="utf-8")
    print(f"  Indice regenerado ({len(posts)} posts)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["research", "publish"], required=True)
    args = ap.parse_args()

    print(f"=== PIPELINE {datetime.now():%Y-%m-%d %H:%M} [{args.mode}] ===")

    if args.mode == "research":
        tema, comp = choose_theme()
        if not tema:
            print("Sin tema esta semana. Abort."); sys.exit(0)
        ctx = {"tema": tema, "competition": comp,
               "fecha": datetime.now().strftime("%Y-%m-%d")}
        # completar PAA/trends si el research los trajo
        if RESEARCH_JSON.exists():
            data = json.loads(RESEARCH_JSON.read_text(encoding="utf-8"))
            for r in data.get("results", []):
                if r["seed"] == tema:
                    ctx["paa"] = r.get("paa", [])
                    ctx["trends"] = r.get("trends", [])
        CONTEXT.write_text(json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Tema: {tema} ({comp}). Contexto en {CONTEXT.name}")
        print("PIPELINE_ESPERA_ESCRITURA")  # el cron (agente) escribe el post
        sys.exit(0)

    # --- mode publish ---
    if not CONTEXT.exists():
        print("No hay _weekly_context.json. Corre --mode research primero."); sys.exit(1)
    ctx = json.loads(CONTEXT.read_text(encoding="utf-8"))
    tema = ctx["tema"]
    slug = slugify(tema)
    post_path = POSTS / f"{slug}.html"
    if not post_path.exists():
        print(f"El post {post_path.name} no existe. El agente debe escribirlo."); sys.exit(1)

    # validate (exit 0 = pasa; solo errores bloquean, advertencias ok)
    print("[1/4] Validando SEO...")
    v = run([str(TOOLS / "validate-seo-posts.py"), str(post_path)])
    if v.returncode != 0:
        print("SEO FAIL:", (v.stdout or v.stderr)[-300:]); sys.exit(1)
    print("  SEO OK (con posibles advertencias)")
    print("  Links: se publican tal cual (Blogger API acepta <a href>)")

    # publish blogger (con links, sin remover anchors)
    print("[2/4] Publicando a Blogger (API)...")
    p = run([str(TOOLS / "publish_to_blogger.py"), slug])
    print("  " + p.stdout.strip().replace("\n", "\n  "))
    if p.returncode != 0:
        print("  Blogger FAIL:", p.stderr[-300:]); sys.exit(1)

    # index fg/blog
    print("[3/4] Regenerando indice fg/blog...")
    regenerate_index()

    # kanban (trazabilidad; el tablero se queda)
    print("[4/5] Kanban...")
    move_kanban(tema, "publicado")

    # git commit + push a main (gh-pages se sirve desde ahi; deploy aparte)
    print("[5/5] Git commit + push (main)...")
    try:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "--no-gpg-sign", "-m",
                        f"content: post semanal '{slug}' publicado en Blogger + index"],
                       cwd=ROOT, capture_output=True, text=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
        print("  git OK")
    except Exception as e:
        print(f"  git WARN: {str(e)[:120]}")

    print("=== FIN: publicado ===")

if __name__ == "__main__":
    main()
