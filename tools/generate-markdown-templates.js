
const fs = require('fs');

const sites = JSON.parse(fs.readFileSync('js/parsed-sites.json', 'utf-8'));

sites.forEach(site => {
  if (site.id === "FreeBitco.in") return; // Already done

  const markdownContent = `---
title: "Reseña de ${site.id}: ¿Es confiable para ganar crypto en Argentina?"
description: "Analizamos ${site.id}. Descubre si paga, cómo optimizar tus ganancias y nuestra opinión honesta."
keywords: "${site.id} reseña, ganar crypto argentina, faucets confiables"
author: "FaucetGuru"
---

# Reseña de ${site.id}

[CONTENIDO EXPANDIDO AQUÍ: Debes usar la estructura del WORKPLAN: H1, Intro, H2 Qué es, H2 Cómo funciona, H2 Ventajas, H2 Desventajas, H2 Tutorial, H2 FAQ, Conclusión. Debes usar lenguaje natural y alcanzar 1200+ palabras.]

## Registro
[Registrate aquí en ${site.id}](${site.referralLink})
`;

  const fileName = `blog-content-final/${site.id.toLowerCase().replace(/[^a-z0-9]/g, '-')}-reseña.md`;
  fs.writeFileSync(fileName, markdownContent);
  console.log(`Created ${fileName}`);
});
