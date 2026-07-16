# KANBAN — Contenido Semanal FaucetGuru

Flujo: `ideas` → `investigando` → `escribiendo` → `publicado`

Reglas:
- 1 post por semana (cron domingo 10:00, job `66a0ceae9771`).
- El agente investiga BAJA competencia (research-topics.py + cache), escribe en
  criollo AR, valida SEO, publica a Blogger via API CON LINKS (1 a la vez,
  anchors NO se remueven), regenera blog/posts/index.html, commitea a main
  (--no-gpg-sign).
- Los posts llevan <a href> reales (interlinks internos y/o referrals) — Blogger
  API los acepta. No usar remove-anchors en este flujo.
- Blog = cryptofuente.blogspot.com. fg/blog = repo main. gh-pages se sirve
  desde main (deploy aparte).
- Para agregar temas/sitios: ponelos en `ideas` con `- [ ] TEMA`.

## ideas
- [ ] (agregar temas/sitios mientras investigás — un item por línea)

## investigando
- [ ] (el pipeline mueve acá el tema de la semana)

## escribiendo
- [ ] (en redacción)

## publicado
- [ ] faucet crypto argentina  _(publicado)_