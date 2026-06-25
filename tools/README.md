# Herramientas para Posts

## Validación y SEO
- `validate-seo-posts.py` - Valida posts HTML: H1, meta description (70-160 chars), keywords (mínimo 3), contenido (mínimo 300 chars), imágenes con alt

## Publicación
- `send-to-blogger.py` - Publica posts HTML a Blogger via email
- `send-post-email.py` - Envía post por email (configurar EMAIL_USER/EMAIL_PASS)

## Edición de contenido
- `remove-anchors.py` - Elimina `<a href=...>` de posts, reemplazándolos por `<span>`

## Traducción y actualización
- `translate-post.py` - Traduce posts
- `update-post-spanish.py` - Actualiza posts en español
- `update-blogger-post.py` - Actualiza posts en Blogger
- `update-blogger-metadata.py` - Actualiza metadatos SEO de posts publicados

## Sincronización
- `sync-blogger-posts.py` - Sincroniza posts entre Blogger y local
- `batch-post-blogs.py` - Procesa posts en lote

## Utilidades
- `weekly_site_check.py` - Verifica enlaces de referidos
- `list-blogger-posts.py` - Lista posts de Blogger
- `get-blogger-token.py` - Obtiene token de autenticación Blogger
- `generate-token-from-code.py` - Genera token desde código de autorización