from googleapiclient.discovery import build
import pickle

with open("tools/token.pickle", "rb") as f:
    creds = pickle.load(f)
service = build("blogger", "v3", credentials=creds)

# Obtener blogs del usuario
blogs = service.blogs().listByUser(userId="self").execute()
for b in blogs.get("items", []):
    print("BLOG:", b["name"], "| id:", b["id"], "| url:", b.get("url"))
    blog_id = b["id"]
    # Listar posts (paginado)
    titles = []
    req = service.posts().list(blogId=blog_id, maxResults=50, fields="items(title,url),nextPageToken")
    while req:
        resp = req.execute()
        for p in resp.get("items", []):
            titles.append(p["title"])
        req = service.posts().list_next(req, resp)
    print(f"  TOTAL POSTS: {len(titles)}")
    for t in titles:
        print("   -", t)
