# SEO Post Verification Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Validate SEO quality of blog posts in `blog/posts/` directory against established SEO criteria.

**Architecture:** Run the existing `tools/validate-seo-posts.py` script against HTML blog posts, generate a report of failing posts with actionable fixes.

**Tech Stack:** Python script with regex/HTML parsing for SEO validation (H1, meta description, keywords, content length, alt attributes).

---

## Current Context

From `AGENTS.md`, the project uses:
- `tools/validate-seo-posts.py` - validates HTML posts for SEO: H1, meta description (70-160 chars), keywords min 3, content min 300 chars, images with alt
- `blog/posts/` - contains individual HTML blog posts
- Static site, no build step

## Tool: `tools/validate-seo-posts.py`

This is the primary SEO verification tool. It checks:
1. **H1 tag presence** - exactly one H1 per post
2. **Meta description** - length between 70-160 characters
3. **Keywords** - minimum 3 keywords in meta tag
4. **Content length** - minimum 300 characters of actual content
5. **Image alt attributes** - all images must have alt text

---

## Pautas SEO Oficiales (extraídas del proyecto)

### Requisitos de `tools/validate-seo-posts.py`:
1. **H1 obligatorio** - etiqueta `<h1>` debe existir
2. **Meta description** - 70-160 caracteres exactos
3. **Meta keywords** - mínimo 3 palabras (cada palabra ≥3 caracteres)
4. **Contenido** - mínimo 300 caracteres de texto
5. **Imágenes** - atributo `alt` obligatorio

### Keywords SEO sugeridas (de `tools/seo-blog-posts.js`):
- faucet: 'faucet, cripto argentina, bitcoin gratis, ethereum, reseña'
- bitcoin: 'bitcoin, cripto argentina, faucet, blockchain, btc'
- ethereum: 'ethereum, cripto argentina, faucet, reseña'
- wallet: 'wallet, billetera cripto, seguridad, argentina, reseña'
- mining: 'mining, minería cripto, bitcoin, gpu, cpu'
- ptc: 'ptc, ganar dinero, clic, cripto argentina, reseña'
- tutorial/guia: 'tutorial, guía, cripto argentina, cómo hacer, paso a paso'
- airdrop: 'airdrop, tokens gratis, cripto argentina, ganar, reseña'

### Template `blog/template-post.html`:
- Usa placeholders: `TITLE_PLACEHOLDER`, `KEYWORDS_PLACEHOLDER`, `DESCRIPTION_PLACEHOLDER`
- Estructura: `<h1>` dentro de `<header>`, contenido en `<main>`

---

## Step-by-Step Plan

### Task 1: Inspect the SEO validation tool

**Objective:** Understand the current validation logic and output format.

**Files:**
- Inspect: `tools/validate-seo-posts.py`

**Step 1: Read the validation script**

```bash
cat tools/validate-seo-posts.py
```

**Step 2: Identify validation rules**

Look for functions checking:
- `h1` tag count
- `meta description` length
- `keywords` count
- Content character count
- Image `alt` attribute presence

### Task 2: List blog posts to verify

**Objective:** Get a complete inventory of HTML posts in blog/posts/.

**Files:**
- Inspect: `blog/posts/` directory

**Step 1: List all HTML files**

```bash
ls -la blog/posts/*.html | head -20
```

**Step 2: Count total posts**

```bash
ls blog/posts/*.html | wc -l
```

### Task 3: Run initial SEO validation

**Objective:** Run the validation script and capture all failures.

**Files:**
- Execute: `tools/validate-seo-posts.py`

**Step 1: Run validation**

```bash
python3 tools/validate-seo-posts.py
```

**Step 2: Capture output to file**

```bash
python3 tools/validate-seo-posts.py > seo-validation-report.md 2>&1
```

**Expected output format:** Should list each post with validation status (PASS/FAIL) and specific issues.

### Task 4: Analyze validation failures

**Objective:** Categorize and count the types of SEO issues found.

**Files:**
- Read: `seo-validation-report.md` (generated)
- Parse: Count failures by type

**Step 1: Extract failure categories**

```bash
grep -E "(FAIL|ERROR|MISSING)" seo-validation-report.md | sort | uniq -c
```

**Step 2: List posts failing validation**

```bash
grep -B2 -E "(FAIL|ERROR)" seo-validation-report.md | grep "blog/posts" | sort -u
```

### Task 5: Fix missing H1 tags

**Objective:** Ensure each post has exactly one H1 tag.

**Files:**
- Modify: Each post in `blog/posts/*.html` missing H1

**Step 1: For each failing post, read the file**

```bash
# Identify which posts need H1 fixes
grep -l "H1" blog/posts/??-??-????.html
```

**Step 2: Add H1 after opening body tag**

Add inside `<body>`:
```html
<h1>Post Title Here</h1>
```

### Task 6: Fix meta description length

**Objective:** Ensure meta descriptions are 70-160 characters.

**Files:**
- Modify: Posts with description too short/long

**Step 1: Find posts with meta description issues**

```bash
grep -E "(meta description|description)" seo-validation-report.md
```

**Step 2: Edit each post to adjust description**

Update `<meta name="description" content="...">` to be 70-160 chars.

### Task 7: Fix missing keywords

**Objective:** Add meta keywords tag with minimum 3 keywords.

**Files:**
- Modify: Posts missing meta keywords

**Step 1: Check for keywords meta tag**

```bash
grep -L "meta name=\"keywords\"" blog/posts/*.html
```

**Step 2: Add keywords meta tag**

Inside `<head>`:
```html
<meta name="keywords" content="keyword1, keyword2, keyword3">
```

### Task 8: Fix content length

**Objective:** Ensure posts have minimum 300 characters of content.

**Files:**
- Modify: Posts with insufficient content

**Step 1: Check character counts**

```bash
# Use the script to identify short posts
python3 tools/validate-seo-posts.py 2>&1 | grep -E "[0-9]+ chars"
```

**Step 2: Add placeholder content if needed**

Add relevant content to meet the 300 character minimum.

### Task 9: Fix image alt attributes

**Objective:** Add alt attributes to all images.

**Files:**
- Modify: Posts with images missing alt

**Step 1: Find images without alt**

```bash
grep -E "<img[^>]*src=" seo-validation-report.md
```

**Step 2: Add alt to each image**

Change:
```html
<img src="image.jpg">
```
To:
```html
<img src="image.jpg" alt="Descriptive alt text">
```

### Task 10: Re-run validation and verify all pass

**Objective:** Confirm all SEO issues are resolved.

**Files:**
- Execute: `tools/validate-seo-posts.py`

**Step 1: Run final validation**

```bash
python3 tools/validate-seo-posts.py
```

**Step 2: Confirm zero failures**

```bash
python3 tools/validate-seo-posts.py | grep -c "FAIL"
# Should return 0
```

### Task 11: Commit SEO fixes

**Objective:** Commit all SEO improvements.

**Step 1: Stage changes**

```bash
git add blog/posts/*.html
git add seo-validation-report.md
```

**Step 2: Commit**

```bash
git commit --no-gpg-sign -m "seo: fix validation issues in blog posts"
```

---

## Risks and Tradeoffs

| Risk | Mitigation |
|------|------------|
| Scripts may be outdated | Inspect script before running, verify it works |
| Posts may have custom title/H1 logic | Each fix must be done per-post, no bulk replace |
| Alt text may require manual description | Review each image contextually |
| Meta descriptions may impact SEO | Keep descriptions accurate to post content |

## Open Questions

1. ¿Quieres que incluya la validación automática de los posts actuales?
2. ¿Prefieres ejecutar los fixes manualmente o dejar que los subagentes los apliquen?