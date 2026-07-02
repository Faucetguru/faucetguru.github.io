# FaucetGuru Bet — Análisis completo de propuestas, conflictos y opciones

> Documento de referencia para la sección paralela `bet/`.
> Consolida todas las propuestas de la conversación, decisiones de diseño, riesgos de TOS y variaciones a analizar antes de ejecutar.

---

## 1. Propósito y alcance

### 1.1 Propósito oficial
Crear una sección paralela tipo blog, dedicada a reseñas y guías de casinos/bonos: bonus, drops, promociones, términos, confiabilidad y recomendaciones.

### 1.2 Alcance inicial
- Sitio propio: `faucetguru.github.io/bet/`
- Blog del sitio: `blog/` con artículos que enlacen a `/bet/`
- Blogger/WordPress: canal aparte, separado del sitio principal; para esta sección no se integra export automático desde `bet/`
- Pinterest: pins scam-warning y educacionales, no como destino final de contenido promocional

### 1.3 No alcance (por ahora)
- No publicar contenido promocional directo de casinos en Pinterest
- No habilitar afiliados agresivos sin revisión legal
- No modificar el flujo principal de faucets (`index.html`, `js/faucets.js`)
- No modificar el flujo principal de Blogger; se hará en un Blogger/WordPress aparte

---

## 2. Cambios y agregados propuestos

### 2.1 Estructura de carpetas nueva
**Propuesta:** crear `bet/` como sección paralela.

**Archivos/carpetas a agregar:**
- `bet/index.html`
- `bet/css/bet.css`
- `bet/js/bet-sites.js`
- `bet/js/bet-app.js`
- `bet/markdown/`
- `bet/posts/`
- `bet/posts-backup/`
- `bet/disclaimers/disclaimer-bet.md`
- `bet/disclaimers/disclaimer-blogger.md`
- `bet/disclaimers/disclaimer-pinterest.md`
- `bet/blogger-export/`
- `bet/secrets/keys.txt`

**Variaciones:**
- 1) Adaptar `blog/` y compartir assets (CSS/JS) en vez de duplicar
- 2) Usar una estructura similar a la principal de tarjetas, sin categorías tipo blog, ordenada por A-Z / scam rank

**Decisión tomada:**
- Se adopta variación 1 como base operativa.
- Se adopta variación 2 como criterio de presentación principal: sin categorías fijas de blog; ordenación por nombre o por score escamalidad.

### 2.2 Integración en home (`index.html`)
**Propuesta:** agregar un botón/vinculo en el nav hacia `bet/index.html`.

**Opciones:**
- A) Botón separado “Bet”
- B) Dropdown combinado “Blog / Bet”
- C) Link en footer solo, sin nav button

**Decisión electa:** A para máxima claridad; evita mezclar marcas si después querés separar.

### 2.3 Disclaimer global
**Propuesta:** disclaimer visible en hero/footer de `/bet/` y en cada post.

**Opciones:**
- A) Banner fijo en hero + inline al final de cada post
- B) Overlay modal al entrar a `/bet/`
- C) Footer ampliado con sección “Juego responsable”

**Decisión tomada:** A + C combinados. El modal puede generar fricción.

### 2.4 Disclaimer por post
**Propuesta:** cada reseña incluye texto corto de:
- 18+/21+
- Juego responsable
- Naturaleza informativa, no consejo financiero
- Divulgación de afiliados

**Opciones:**
- A) Bloque reusable insertado en template
- B) Texto hardcodeado por post
- C) Generado automáticamente desde markdown frontmatter

**Decisión tomada:** A.

### 2.5 Modelo de datos de reseñas
**Propuesta:** `bet/js/bet-sites.js` con objetos tipo `window.betSitesData`.

**Campos sugeridos:**
- `id`, `name`, `type`, `trustScore` (0-5)
- `summary`, `bonus`, `terms`
- `paymentMethods[]`, `pros[]`, `cons[]`
- `referralLink` o `#`
- `tags[]`
- `disclaimerNote`

**Variaciones:**
- A) Esquema minimalista: solo campos obligatorios
- B) Esquema extendido: `minDeposit`, `wagering`, `countryRestrictions`, `verifiedAt`
- C) Esquema mixto: base obligatoria + campos opcionales

**Decisión tomada:** C para empezar.
**Entregable esperado:** el usuario proveerá la información; se verificará y se corregirá; se crearán 3 registros de test.

### 2.6 Validación
**Propuesta:** nuevo validador `tools/validate-bet-sites.js` o reusar `validate-faucets.js` adaptado.

**Opciones:**
- A) Duplicar validador mantenible
- B) Parametrizar validador existente por schema
- C) Validación manual hasta tener volumen

**Decisión tomada:** A para MVP; migrar a B más adelante.

### 2.7 Export Blogger
**Propuesta:** generar HTML desde `bet/markdown/` hacia `bet/posts/` y luego exportar XML/HTML desde `bet/blogger-export/`.

**Opciones:**
- A) Reusar `tools/generate-blogger-html-posts.js` apuntando a `bet/`
- B) Script separado `bet/tools/generate-bet-blogger-posts.js`
- C) No exportar Blogger, solo sitio propio

**Decisión tomada:** No se integra Blogger automático desde `bet/`. Blogger/WordPress queda como canal aparte.

### 2.8 Interlinking interno
**Propuesta:** posts relacionados por tags y ID.

**Opciones:**
- A) Sección “Ver también” generada automáticamente
- B) Enlaces manuales dentro del markdown
- C) No interlinking inicial

**Decisión tomada:** A + B combinados; A reduce mantenimiento.

---

## 3. Estrategia por canal y variaciones

### 3.1 Sitio propio `/bet/`
**Objetivo:** hub central con disclaimer, ordenación por A-Z / scam rank, detalle y datos editables.

**Variaciones:**
- A) Página única con filtros/ordenación dinámica similar a `faucets.js`
- B) Multi-página: `index.html` + `posts/*.html` independientes
- C) Solo JSON + rendering estático generado en build

**Decisión tomada:** A.

### 3.2 Blog del sitio (`blog/`)
**Objetivo:** artículos editoriales hacia `/bet/` y `/blog/`.

**Variaciones:**
- A) Posts exclusivos de guía/estrategia con enlaces hacia `/bet/`
- B) Posts duplicados/resumidos desde `/bet/`
- C) Blog y `bet/` completamente desacoplados

**Decisión tomada:** B. No duplicar contenido exacto; usar blog como embudo editorial.

### 3.3 Blogger
**Objetivo:** sindicar contenido editorial a Blogger con compliance.

**Variaciones:**
- A) Export completo de `bet/posts/`
- B) Solo posts seleccionados del blog que enlacen a `/bet/`
- C) No usar Blogger por ahora

**Decisión tomada:** C.
**Aclaración:** Blogger/WordPress se maneja aparte; no se integra en el flujo automático de `bet/`.

### 3.4 Pinterest
**Objetivo:** descubrimiento orgánico hacia blog/sitio; no destino final gambling.

**Variaciones:**
- A) Solo pines de contenido editorial informativo
- B) Pines de infografías/resúmenes hacia blog
- C) No usar Pinterest para esta sección

**Decisión tomada:** A + B; priorizar contenido educativo/informativo.

---

## 4. Conflictos identificados

### 4.1 Cumplimiento y TOS
| Conflicto | Descripción | Mitigación |
|-----------|-------------|-----------|
| Pinterest gambling policy | Política prohíbe juego/azar/casinos | No publicar contenido promocional directo; solo contenido editorial/educativo |
| Blogger/YMYL | Contenido de dinero entra en Your Money or Your Life | E-E-A-T alto, disclaimer, fuentes/terms visibles, actualizaciones periódicas |
| GitHub Pages TOS | Prohibido spam, fraude, contenido dañino | Neutralidad editorial + disclaimer; evitar affiliate agresivo |
| Google/AdSense | No paga por contenido gambling/aff | No depender de AdSense en esta sección |
| FTC/afiliados | Requiere divulgación si hay links de referral | Disclaimer por post y global; transparencia con `referralLink` |
| Edad y jurisdicción | Restricción 18+/21+ según país | Disclaimer + bloqueo主张/no consulta legal explícita |

### 4.2 Marca y SEO
- Marca “FaucetGuru” + contenido de casinos puede generar confusión de expectativa
- Riesgo de canibalización entre `blog/` y `bet/`
- URLs duplicadas o thin content si se replica demasiado

### 4.3 Mantenimiento
- Cada post nuevo implica actualizar: markdown, HTML, JSON, Blogger export, backup
- Si no hay automatización, la carga editorial crece rápido

### 4.4 Legal local
- Depende de jurisdicción del usuario final
- No hay acuerdo explícito de asesoramiento legal en este plan
- Riesgo de responsabilidad por información desactualizada o errónea

---

## 5. Opciones y elecciones tomadas

### 5.1 Nivel de exposición comercial
| Opción | Descripción | Riesgo |
|--------|-------------|--------|
| Conservadora | Solo reseñas editoriales; pocos o ningún referral link activo | Bajo |
| Moderada | Reviews con enlaces `#` o homepage; disclaimer claro | Medio |
| Agresiva | Afiliados activos, CTAs fuertes, comparativas pagas | Alto |

**Elección tomada:** Conservadora.

### 5.2 Naming y branding
| Opción | Descripción |
|--------|-------------|
| 1 | `faucetguru.github.io/bet` — ligado a FaucetGuru |
| 2 | Subdominio separado `bet.faucetguru.github.io` |
| 3 | Dominio/repo separado para desvincular marca |

**Elección tomada:** Opción 3: dominio/repo separado para desvincular marca.

### 5.3 Modelo de gobernanza editorial
| Opción | Descripción |
|--------|-------------|
| A | Un solo revisor antes de publicar |
| B | Checklist automatizada + humano |
| C | Solo publicación manual sin automatización |

**Elección tomada:** B.

---

## 6. Decisiones de diseño registradas

1. Sección paralela `bet/` réplica de `blog/` para MVP
2. Disclaimer obligatorio global + por post
3. Pinterest: solo contenido editorial educativo; no destino final gambling
4. Blogger/WordPress queda como canal aparte; no se integra export automático desde `bet/`
5. Estructura de datos inspirada en `faucets.js` con campos específicos de casinos/bonos
6. Ordenación principal por A-Z / scam rank, sin categorías fijas tipo blog
7. No modificar flujo principal de faucets en `index.html`
8. `secrets/keys.txt` para claves de afiliados; no trackeado
9. Validación local antes de commit
10. Nivel comercial: conservador
11. Naming/estrategia hacia dominio/repo separado
12. Gobernanza editorial con checklist automatizada + humano

---

## 7. Próximas decisiones necesarias

- Entregar datos verificados para `bet/js/bet-sites.js` y crear 3 registros de test
- Definir país o países de foco inicial
- Definir quién ejecuta la checklist automatizada y quién hace la revisión humana
- Definir Blogger/WordPress aparte: plataforma, dominio/URL y proceso de publicación

---

## 8. Riesgos residuales

- Baneo de Pinterest si se cruza a contenido promocional directo
- Penalización SEO/YMYL si Blogger/indexa contenido delgado o sin E-E-A-T
- Takedown en GitHub si se interpreta como spam/aff agresivo
- Responsabilidad legal local si no se cumple edad/disclosure/terms
- Desactualización de términos de bono generando desconfianza
- Riesgo de canibalización si `blog/` y `bet/` se solapan demasiado

---

*Documento generado a partir de la conversación sobre la sección `bet/`.  
No se realizaron cambios en el sitio; esto es análisis y decisiones pendientes.*
