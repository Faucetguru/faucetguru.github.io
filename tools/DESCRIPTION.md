# Herramientas de FaucetGuru

## Validación

- `validate-faucets.js` – valida el esquema y reglas de `js/faucets.js`: requiere `id`, `name`, `type`, confirma que `referralLink` no esté vacío ni tenga placeholders como `TU_ID`/`#`, revisa rangos de `trustScore`, URLs de imágenes, y agrega warnings. Sale con código 1 si hay errores.
- `validate-seo-posts.py` – valida posts HTML bajo `blog/posts/`: H1 obligatoria, meta description entre 70 y 160 chars, meta keywords con al menos 3 palabras, contenido mínimo 300 chars, e imágenes con `alt`. Sale con error si hay problemas bloqueantes.

## Publicación y Blogger

- `send-to-blogger.py` – envía posts a Blogger por email posting SMTP. Tiene una lista fija `POSTS_TO_PUBLISH`, usa credenciales por defecto en el mismo script y soporta `--dry-run`.
- `send-post-email.py` – utilidad genérica de email HTML por consola: `<destinatario> <asunto> <archivo_html>`. Usa placeholders `YOUR_EMAIL@gmail.com`, así que hay que editar credenciales antes de usarla.
- `send-2-pending.py` – envía exactamente 1 post pendiente desde `blogposted.md` a Blogger por email, marca el checklist como enviado después.
- `send-scheduled.py` – envía posts pendientes cada 5 minutos usando email posting, con stop file `.stop-scheduled`. Relee `blogposted.md`, encuentra el HTML correspondiente, y sigue hasta que no queden pendientes o se pida parar.
- `scheduled-blogger-api.py` – publicador programador por API oficial de Blogger v3. Lee `blogposted.md`, busca HTML en `blog/posts/`, publica con la API, marca checklist como hecho cada 300 segundos y se detiene con `.stop-scheduled`.
- `post-to-blogger.py` – wrapper CLI simple para crear un post nuevo en Blogger v3 por API usando credenciales OAuth.
- `sync-blogger-posts.py` – sincroniza metadatos entre Blogger y posts locales. Obtiene posts por API, completa o corrige keywords/labels y description desde el archivo HTML local.
- `update-blogger-post.py` – actualiza un post existente en Blogger por API; recibe blogId/postId/title/content por argumentos.
- `update-blogger-metadata.py` – recorre posts en Blogger y actualiza labels/SEO cuando faltan metadatos.
- `list-blogger-posts.py` – lista posts de Blogger: título, id, URL, etiquetas, fecha.

## Edición y contenido

- `remove-anchors.py` – recorre `blog/posts/*.html` y convierte `<a href="...">...</a>` en `<span>...</span>`.
- `translate-post.py` – parece especializado en una traducción en español de un post sobre `coin-time.online`; hoy funciona más como fragmento hardcodeado que como herramienta genérica.
- `update-post-spanish.py` – actualiza contenido de un post específico de Blogger (`coin-time.online`) via API.

## Tokens y auth

- `get-blogger-token.py` – obtiene token OAuth para `token.pickle` mediante flujo de servidor local y redir con código manual.
- `generate-token-from-code.py` – variante “sin navegador” del token OAuth: pide la URL y luego pegar el código en consola.

## Generación / exportación

- `generate-blogger-html-posts.js` – convierte markdown a HTML simple para Blogger desde un directorio hardcodeado de entrada.
- `generate-blogger-xml.js` – genera un XML de exportación Blogger desde markdown en ruta hardcodeada.
- `parse-xml-to-json.js` – parsea `blogger-export/faucetguru-all-entries.xml` y extrae título, trust score y referral link hacia `js/parsed-sites.json`.
- `generate-markdown-templates.js` – genera markdowns de reseña plantilla a partir de `js/parsed-sites.json`.
- `generate-blog-index.js` – genera un `index.html` de blog leyendo posts HTML exportados y asignando fechas decrecientes.
- `audit-content.js` – audita contenido XML del blog exportado: conteo de palabras, cantidad de H2 y presencia de FAQ.
- `interlink_script.py` – inyecta sección de “Más contenido recomendado” con enlaces internos aleatorios entre reseñas/guías del directorio de markdown.
- `weekly_site_check.py` – load `js/faucets.js`, hace `curl` a cada `referralLink`, detecta caídas/scam keywords, y escribe un reporte markdown en la raíz.
- `batch-post-blogs.py` – postea archivos markdown con `post-to-blogger.py` en orden por trust score.
- `git-push.sh` – utilitario de git push.
- `seo-blog-posts.js` – optimiza SEO de posts HTML: genera/inyecta `title`, `description`, `keywords`, `og:title`, `og:description` y backupea archivos originales.
