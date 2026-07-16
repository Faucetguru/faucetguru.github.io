# KANBAN — Contenido Semanal FaucetGuru

Flujo: `ideas` → `investigando` → `escribiendo` → `listo-mail` → `publicado`

Reglas:
- 1 post por semana (cron domingo 10:00, job `66a0ceae9771`).
- El agente investiga BAJA competencia (research-topics.py + cache), escribe en
  criollo AR, valida SEO, quita anchors, publica a Blogger via API (1 a la vez),
  regenera blog/posts/index.html, commitea a main (--no-gpg-sign).
- Sin mail: publica directo. Blog = cryptofuente.blogspot.com. fg/blog = repo main.
- gh-pages se sirve desde main (deploy aparte).
- Para agregar temas/sitios: ponelos en `ideas` con `- [ ] TEMA`.

## ideas
- [ ] (agregar temas/sitios mientras investigás — un item por línea)

## investigando
- [ ] (el pipeline mueve acá el tema de la semana)

## escribiendo
- [ ] (en redacción)

## listo-mail
- [ ] (ya no usamos mail; flujo directo a Blogger)

## publicado
- [ ] faucet crypto argentina _(BAJA/DESCONOCIDA, publicado 2026-07-16)_
