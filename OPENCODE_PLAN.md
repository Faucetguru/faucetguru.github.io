# PLAN OPENCODE: Blog FaucetGuru

## Objetivo
Automatizar la creación, optimización y publicación de contenido SEO para blog de faucets crypto en español (Argentina), usando OpenCode como orquestador principal.

## Estado Actual
- **40 entradas de blog** exportadas desde `faucetguru-all-entries.xml` (Blogger Atom format)
- Cada entrada contiene: trust score, bonus, resumen, estrategia, opiniones, link de referido
- Contenido a importar/regenerar en plataforma CMS

---

## ETAPAS DEL PLAN

### ETAPA 1: Parseo y Análisis de Contenido Actual
**Objetivo:** Extraer datos del XML y mapear necesidades de optimización

Tasks:
- [ ] **parse-xml**: Parsear `faucetguru-all-entries.xml` → tabla de 40 sitios
- [ ] **audit-seo**: Evaluar cada entrada contra criterios WORKPLAN
  - Longitud actual vs. mínimo (1200 palabras)
  - Presencia de estructura obligatoria (H2s, FAQs)
  - Metadata (title, description)
  - Cantidad de FAQs
- [ ] **detect-gaps**: Identificar qué falta en cada entrada
  - Interlinking (necesita 2 artículos + 1 guía + 1 categoría)
  - Keywords long-tail no cubiertas
  - Falta de tablas comparativas

---

### ETAPA 2: Expansión y Enriquecimiento de Contenido
**Objetivo:** Llevar cada entrada de blog a estándar WORKPLAN

Tasks:
- [ ] **expand-structure**: Para cada uno de 40 sitios:
  - Expandir introducción
  - Agregar "Qué es" (contexto sobre el tipo de site)
  - Escribir "Cómo funciona" (paso a paso)
  - Listar ventajas/desventajas (en tabla o bullets)
  - Crear tutorial completo
  - Generar 5+ FAQs temáticas
  - Escribir conclusión con CTA

- [ ] **add-keywords**: Inyectar long-tail keywords naturalmente
  - Keywords objetivo: "mejores faucets para argentinos", "faucets que pagan al instante", etc.
  - Evitar keyword stuffing

- [ ] **optimize-metadata**: Para cada entrada
  - Title: ≤60 caracteres + keyword principal
  - Meta description: ≤155 caracteres
  - Canonical URLs

---

### ETAPA 3: Generación de Contenido Complementario
**Objetivo:** Crear artículos estratégicos que no sean reseñas individuales

Tasks:
- [ ] **generate-comparison**: Crear 3-5 artículos comparativos
  - "Mejores faucets para argentinos 2026"
  - "Faucets que pagan al instante vs. retiro lento"
  - "Faucets BTC vs. USDT vs. TRON"
  
- [ ] **generate-rankings**: Crear rankings por categoría
  - "Top 10 Faucets por Trust Score"
  - "Mejores faucets por payout mínimo"
  - "Faucets más rápidas para ganar satoshis"

- [ ] **generate-tutorials**: Guías paso a paso
  - "Cómo retirar satoshis desde Argentina"
  - "Mejores wallets para recibir USDT 2026"
  - "Tutorial: Ganar bitcoin gratis desde celular"

- [ ] **generate-guides**: Guías principales (pilares)
  - "Guía completa: Ganar Bitcoin Gratis en Argentina"
  - "Faucets Crypto 2026: Todo lo que necesitas saber"

---

### ETAPA 4: Interlinking Automático
**Objetivo:** Conectar contenido estratégicamente

Tasks:
- [ ] **map-relationships**: Crear grafo de relaciones entre artículos
  - Cada reseña → 2 artículos relacionados
  - Cada reseña → 1 guía principal
  - Cada reseña → 1 categoría

- [ ] **inject-internal-links**: Inyectar links internos naturales
  - Anchor text con keywords long-tail
  - Máximo 3-4 links por artículo
  - Contextualmente relevantes

---

### ETAPA 5: Validación y Control de Calidad
**Objective:** Asegurar estándares WORKPLAN antes de publicación

Tasks:
- [ ] **validate-content**:
  - ✓ Cada artículo ≥1200 palabras
  - ✓ Estructura H1→H2s completa
  - ✓ Mínimo 5 FAQs
  - ✓ Metadata correcta
  - ✓ Sin contenido duplicado (Copyscape check si es posible)
  - ✓ Sin keyword stuffing (densidad natural)
  - ✓ Links internos funcionales
  - ✓ Lenguaje natural (no AI obviamente)

- [ ] **detect-scams**: Marcar faucets sospechosos
  - Si tiene historial de "no pagan"
  - Exceso de ads (⚠️)
  - Captchas abusivos (⚠️)
  - Mala reputación en foros

- [ ] **format-check**:
  - ✓ Markdown válido
  - ✓ Tablas bien formateadas
  - ✓ Listas claras
  - ✓ Subtítulos coherentes

---

### ETAPA 6: Exportación y Entrega
**Objetivo:** Generar contenido listo para publicación

Tasks:
- [ ] **generate-markdown**: Exportar todo en formato Markdown estructurado
  - Carpeta: `blog-content-final/`
  - Nombre: `{slug}-{tipo}.md`
  - Incluir frontmatter (title, meta-description, keywords, author)

- [ ] **generate-xml**: Re-exportar en Blogger Atom XML (opcional)
  - Para importación directa

- [ ] **generate-report**: Reporte final
  - Total artículos: 40 reseñas + X complementarios
  - Promedio palabras
  - Keywords cubiertas
  - SEO score promedio (estimado)
  - Links rotos detectados (0 si todo OK)

---

## PARAMETROS OPENCODE

### Modelo
- **Claude Haiku 4.5** (velocidad + calidad balanceada)

### Instrucciones Base para OpenCode
```
Eres un experto en SEO y copywriting español argentino.

Genera contenido que:
1. Sea útil, claro, confiable, humano
2. Cumpla estructuras WORKPLAN
3. Use keywords naturalmente
4. Evite keyword stuffing, spam, clickbait
5. Sea evergreen (válido en 2026+)
6. Enlace internamente cuando sea relevante

Idioma: Español argentino
Tono: Semi-informal + técnico simple
Min. palabras: 1200 (ideal 1800-2500)
FAQs: Mínimo 5
Metadata: Title ≤60 chars, Description ≤155 chars
```

---

## FLUJO OPENCODE

1. **INPUT**: Datos de 40 sitios (extraído de XML)
2. **PROCESSO**: Para cada sitio:
   - Expandir estructura (etapa 2)
   - Generar FAQs (etapa 2)
   - Inyectar keywords (etapa 2)
   - Optimizar metadata (etapa 2)
3. **GENERACIÓN PARALELA** (etapa 3):
   - Comparativas
   - Rankings
   - Tutoriales
   - Guías pilares
4. **INTERLINKING** (etapa 4):
   - Mapear relaciones
   - Inyectar links contextuales
5. **VALIDACIÓN** (etapa 5):
   - Control de calidad automático
6. **OUTPUT** (etapa 6):
   - Markdown + XML + Reporte

---

## DEPENDENCIAS Y ORDEN

```
Etapa 1 (Parse) 
  ↓
Etapa 2 (Expand Reseñas) 
  ↓
Etapa 3 (Generate Content Complementario) [paralelo con Etapa 2]
  ↓
Etapa 4 (Interlinking) 
  ↓
Etapa 5 (Validación) 
  ↓
Etapa 6 (Export)
```

---

## MÉTRICAS DE ÉXITO

- ✓ 40 reseñas expandidas a 1200+ palabras c/u
- ✓ 0 errores de estructura (H1/H2s)
- ✓ 0 duplicados detectados
- ✓ 100% FAQ coverage (5+ c/reseña)
- ✓ Metadata optimizada para CTR
- ✓ Interlinking estratégico (2+1+1 = 4 links c/reseña)
- ✓ 5-10 artículos complementarios (comparativas, rankings, tutoriales)
- ✓ Reporte SEO generado

---

## ARCHIVOS INVOLUCRADOS

| Archivo | Rol |
|---------|-----|
| `blogger-export/faucetguru-all-entries.xml` | INPUT: 40 sitios datos |
| `WORKPLAN.md` | SPEC: Criterios SEO y estructura |
| `blog-content-final/` | OUTPUT: Markdown + metadata |
| OpenCode Workflow | Orquestador principal |

---

## NOTAS

- OpenCode debe respetar el WORKPLAN.md como "constitution"
- Cada generación debe ser verificable (metadata, estructura)
- Evitar cualquier parecido a contenido AI obvio
- Keywords LATAM7 prioritarias
- El blog resultante debe tener tráfico orgánico sostenible (evergreen)
