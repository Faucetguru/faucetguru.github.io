import re
from googleapiclient.discovery import build
import pickle
from pathlib import Path

# 1) Posts remotos reales en CryptoFuente
with open("tools/token.pickle", "rb") as f:
    creds = pickle.load(f)
service = build("blogger", "v3", credentials=creds)
blog_id = "8989148619439472689"
remote_titles = []
req = service.posts().list(blogId=blog_id, maxResults=50, fields="items(title),nextPageToken")
while req:
    resp = req.execute()
    for p in resp.get("items", []):
        remote_titles.append(p["title"])
    req = service.posts().list_next(req, resp)

# 2) Archivos locales
root = Path("/home/salma/faucetguru.github.io")
posts_dir = root / "blog/posts"
html_files = sorted(p.name[:-5] for p in posts_dir.glob("*.html") if p.name != "index.html")

def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return set(s.split())

# Normalizar titulos remotos a slugs aproximados
def title_to_slug(t):
    t = t.lower()
    t = re.sub(r"^(reseña de |reseña: |guía |guia )", "", t)
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return re.sub(r"-+", "-", t).strip("-")

remote_slugs = set()
for t in remote_titles:
    remote_slugs.add(title_to_slug(t))

# Mapear archivos locales -> slug
def file_to_slug(f):
    f = f.lower()
    f = re.sub(r"-reseña$", "", f)
    return f

missing = []
for f in html_files:
    slug = file_to_slug(f)
    # match: el slug del archivo debe estar contenido en algun remote_slug o viceversa
    found = any(slug == rs or slug in rs or rs in slug for rs in remote_slugs)
    if not found:
        # match por palabras clave (>=3 palabras en comun)
        fw = norm(f)
        for rt in remote_titles:
            rw = norm(rt)
            if len(fw & rw) >= min(3, len(fw)):
                found = True
                break
    if not found:
        missing.append(f)

print("="*60)
print(f"Remoto CryptoFuente TOTAL: {len(remote_titles)} (incluye duplicados)")
print(f"Local HTML (sin index):    {len(html_files)}")
print(f"FALTANTES (no encontrados remoto): {len(missing)}")
print("-"*60)
for m in missing:
    print("  -", m)
