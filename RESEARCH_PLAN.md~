# RESEARCH PLAN: Descubrimiento de Temas con Baja Competencia

## Objetivo
Descubrir y priorizar temas relacionados a crypto/faucets/wallets con baja competencia y alto potencial de tráfico orgánico, usando herramientas de investigación, y luego generar contenido siguiendo los estándares SEO de WORKPLAN.

---

## ETAPA 1: Investigación de Keywords y Temas

### Fuentes de datos

#### 1. Google Search Console (GSC)
- Exportar queries con impresiones > 100 pero CTR < 5% (oportunidades de mejora)
- Exportar queries en posición 5-15 (fáciles de escalar)
- Identificar páginas existentes con impresiones pero sin clics
- Analizar tendencias de 12 meses

#### 2. AnswerThePublic / AlsoAsked
- Input seeds: "bitcoin gratis", "faucet", "wallet crypto", "usdt argentina", "ganar crypto"
- Extraer preguntas reales de usuarios (formato PAA: People Also Ask)
- Categorizar por embudo: informacional vs. transaccional

#### 3. Google Trends
- Comparar volumen relativo de términos en Argentina (LATAM7)
- Identificar temas en ascenso: "sonic testnet", "berachain", "monad", "depin projects"
- Estacionalidad: picos de búsqueda por mes

#### 4. Análisis de competencia
- Extraer H2/H3 de top 5 resultados de Google para keywords core
- Detectar patrones que Google premia (estructura, FAQs, tablas)
- Identificar "content gaps": preguntas sin respuesta en top 10

---

## ETAPA 2: Filtrado y Priorización

### Criterios de baja competencia

| Criterio | Peso | Métrica |
|----------|------|---------|
| Keyword Difficulty (KD) < 20 | 30% | Ahrefs / Ubersuggest API |
| Autoridad dominio competidor < 40 | 25% | DR / DA estimado |
| Contenido pobre en top 3 (sin FAQs, sin tablas, <800 palabras) | 20% | Análisis manual o scraping |
| Tendencia estable o creciente (12 meses) | 15% | Google Trends |
| Intención informacional clara | 10% | Clasificación manual |

Score mínimo para pasar: **60/100**

### Categorías de temas

```
informacion/           # Baja competencia, alto volumen
  - "cómo funciona X"
  - "qué es X"         
  - "X vs Y"
  - "X es seguro"

herramientas/          # Media competencia
  - "mejores wallets"
  - "faucets activas 2026"
  - "exchanges sin verificacion"

tutoriales/            # Alta intención, poca competencia
  - "paso a paso X"
  - "tutorial X desde celular"
  - "retirar X en argentina"

actualidad/            # Ventana de oportunidad corta
  - "nuevo faucet X"
  - "airdrop Y fecha"
  - "testnet Z como participar"
```

---

## ETAPA 3: Generación de Contenido (siguiendo WORKPLAN)

### Estructura obligatoria por artículo

```text
H1 (keyword principal, ≤50 caracteres)
Introducción (2-3 párrafos, hook + qué vas a aprender)
H2 ¿Qué es [tema]?
H2 ¿Cómo funciona [tema]?
  - Paso a paso numerado
  - Captura/imagen si aplica
H2 Ventajas
  - Tabla o bullets
H2 Desventajas / Riesgos
  - Tabla o bullets
H2 Tutorial: Cómo empezar
  - 1. Registro / requisitos
  - 2. Configuración
  - 3. Uso diario
  - 4. Retiro / resultados
H2 FAQ (mínimo 5 preguntas)
  - Preguntas reales de AnswerThePublic/AlsoAsked
Conclusión (CTA + resumen)
```

### Metadata SEO

| Campo | Regla |
|-------|-------|
| Title | ≤50 caracteres, keyword al inicio |
| Meta description | ≤99 caracteres, incluye keyword + beneficio |
| URL slug | keyword principal con guiones |
| H1 | ≤60 caracteres, única por página |

### Especificaciones de contenido

- **Idioma:** Español argentino natural
- **Tono:** Semi-informal + técnico simple
- **Mínimo:** 1200 palabras (ideal 1800-2500)
- **FAQs:** Mínimo 5 (ideales 7-10)
- **Tablas:** Al menos 1 comparativa o resumen
- **Links internos:** 2 artículos relacionados + 1 guía principal + 1 categoría

---

## ETAPA 4: Herramientas para Ejecutar Research

### Script propuesto: `tools/research-topics.js`

```javascript
// Pseudocódigo de tool opcional
// 1. Leer seeds de js/faucets.js (tipos, monedas)
// 2. Para cada seed:
//    - Google Trends API → tendencia 12m
//    - GSC API → queries existentes con oportunidad
//    - Scraping top 3 resultados → estructura, longitud, FAQs
// 3. Scorear cada tema potencial
// 4. Output: lista priorizada de temas
```

API keys necesarias (configurables vía `.env`):
- `GSC_API_KEY` — Google Search Console
- `TRENDS_API_KEY` — Google Trends (opcional)
- `KEYWORDS_API_KEY` — Ubersuggest / DataForSEO

### Alternativa sin APIs (manual/asistido)

Si no hay APIs configuradas, el research se hace mediante:

1. **Búsqueda manual en Google:**
   - Buscar keyword + "para argentinos" / "en argentina"
   - Analizar top 10: ¿Hay contenido pobre? ¿FAQs ausentes?
2. **AnswerThePublic web:**
   - Navegar a `answerthepublic.com` y buscar seeds
3. **Google "People Also Ask":**
   - Extraer preguntas del SERP manualmente
4. **Trends explorar:**
   - `trends.google.com` → comparar términos

---

## ETAPA 5: Pipeline de Publicación

```
Research (Etapa 1-2)
  ↓
Scoreo y selección de tema (Etapa 2)
  ↓
Generación de contenido WORKPLAN (Etapa 3)
  ↓
Interlinking automático (tool: interlink_script.py)
  ↓
Validación (check_content.js / check_blog_content.py)
  ↓
Exportación a HTML (generate-blogger-html-posts.js)
  ↓
### /* Publicación a Blogger (send-2-pending.py) */
  ↓
Monitoreo de resultados (GSC a 30 días)
```

---

## MÉTRICAS DE ÉXITO

| Métrica | Objetivo | Plazo |
|---------|----------|-------|
| Temas descubiertos por ronda | ≥10 | Cada research |
| Contenido generado de baja competencia | ≥5 artículos/semana | Semanal |
| Nuevas keywords posicionadas en top 10 | ≥20 | 90 días |
| Crecimiento de impresiones GSC | +30% | 90 días |
| CTR promedio | ≥3% | 90 días |

---

## ARCHIVOS INVOLUCRADOS

| Archivo | Rol |
|---------|-----|
| `js/faucets.js` | Seeds de datos (tipos, monedas, nombres) |
| `tools/research-topics.js` | **(por crear)** Script de investigación |
| `workplneo.md` | Estándares SEO y estructura |
| `blog/posts/` | Output: artículos HTML generados |
| `blogposted.md` | Checklist de publicación |
| `.env` | API keys (no commiteado) |

---

## NOTAS

- Priorizar temas con intención informacional (cómo, qué, tutorial)
- Evitar temas ultrasaturados: "ganar bitcoin rápido", "bitcoin a 1 millón"
- Aprovechar ventanas de oportunidad: testnets, airdrops, nuevos proyectos
- Keywords LATAM7 tienen menor competencia que ES genérico
- Reciclar contenido existente optimizándolo vs. crear desde cero cuando sea posible
