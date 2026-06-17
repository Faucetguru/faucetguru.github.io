# Blog Post Navigation Integration Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Add a navigation button to all blog post HTML pages that integrates them with the main index page (faucet listing) and provides a unified user experience.

**Status:** ✅ COMPLETED

**Architecture:** 
- Created a shared navigation bar that appears at the top of every blog post
- The nav includes buttons to return to the main site (index) and blog index
- Blog posts load the shared nav via a JavaScript file
- Main index's blog view updated to show proper "Back to Faucets" button

**Tech Stack:** Vanilla HTML, CSS, JavaScript (no framework)

---

## Current State Analysis

### Existing Structure
- Main site: `index.html` (faucet listings, filters, detail view)
- Blog posts: `blog/posts/*.html` (individual post files, ~30+ posts)
- Blog index: `blog/posts/index.html` (list of all posts)
- App logic: `js/app.js` (renders faucets, handles blog view via `showBlog()`)

### Current Blog Integration
- `js/app.js` `showBlog()` fetches `blog/posts/index.html` and injects into `#faucet-detail`
- Blog posts open as standalone HTML files
- No navigation back to main site from individual posts

---

## Proposed Approach

1. Create shared blog navigation JavaScript (`blog/posts/blog-nav.js`)
2. Add CSS styles for the navigation bar
3. Inject nav script into all blog post HTML files
4. Update main index's blog view to include proper nav
5. Update blog index links to use absolute paths

---

## Step-by-Step Implementation

### Task 1: Create shared blog navigation JavaScript

**Objective:** Create a reusable navigation component for blog posts.

**Files:**
- Create: `blog/posts/blog-nav.js`

**Implementation:**

```javascript
(function() {
    // Navigation bar HTML
    function createNav() {
        const nav = document.createElement('nav');
        nav.className = 'blog-nav';
        nav.innerHTML = `
            <div class="blog-nav-inner">
                <a href="/" class="blog-nav-link">⚡ Faucet Guru</a>
                <a href="/blog/posts/index.html" class="blog-nav-link">Blog Index</a>
                <div class="blog-nav-spacer"></div>
                <a href="/" class="blog-nav-link" id="back-to-main">← Volver a Faucets</a>
            </div>
        `;
        return nav;
    }

    // Inject navigation at the top of body
    function injectNav() {
        const nav = createNav();
        document.body.insertBefore(nav, document.body.firstChild);
    }

    // Run after DOM loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectNav);
    } else {
        injectNav();
    }
})();
```

---

### Task 2: Add CSS styles for blog navigation

**Objective:** Style the navigation bar to match the site's dark theme.

**Files:**
- Modify: `css/style.css`

**Add to `:root` and styles:**

```css
/* Blog Navigation */
.blog-nav {
    background: #1a1a1a;
    border-bottom: 1px solid #333;
    padding: 12px 0;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.blog-nav-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    gap: 20px;
}

.blog-nav-link {
    color: #ff7357;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
}

.blog-nav-link:hover {
    text-decoration: underline;
}

.blog-nav-spacer {
    flex: 1;
}
```

---

### Task 3: Add navigation script to blog post HTML files

**Objective:** Inject the shared navigation into all blog post HTML files.

**Files:**
- Modify: All files in `blog/posts/*.html` (approximately 30+ files)

**Implementation:**
Add before `</body>` in each HTML file:

```html
<script src="/blog/posts/blog-nav.js"></script>
</body>
```

**Note:** This can be done efficiently with a single shell command:

```bash
for file in /home/salmarina/faucetguru.github.io/blog/posts/*.html; do
    if ! grep -q "blog-nav.js" "$file"; then
        sed -i 's|</body>|<script src="/blog/posts/blog-nav.js"></script>\n</body>|' "$file"
    fi
done
```

---

### Task 4: Update main index blog view

**Objective:** Update `js/app.js` to show proper navigation when blog is loaded.

**Files:**
- Modify: `js/app.js`

**Changes to `showBlog()` function:**

```javascript
function showBlog() {
    hero.classList.add('hidden');
    faucetList.classList.add('hidden');
    faucetDetail.classList.remove('hidden');
    
    faucetDetail.innerHTML = `
        <button class="back-btn" id="back-to-main">← Volver a Faucets</button>
        <div id="blog-container" style="max-width: 900px; margin: 0 auto;">
            <p style="text-align: center; color: var(--text-dim);">Cargando blog...</p>
        </div>
    `;
    
    fetch('blog/posts/index.html')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.text();
        })
        .then(html => {
            const blogContainer = document.getElementById('blog-container');
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const bodyContent = doc.body.innerHTML;
            blogContainer.innerHTML = bodyContent;
            
            // Open external links in new tab
            blogContainer.querySelectorAll('a').forEach(link => {
                if (link.hostname && link.hostname !== window.location.hostname) {
                    link.setAttribute('target', '_blank');
                    link.setAttribute('rel', 'noopener noreferrer');
                }
            });
        })
        .catch(err => {
            const blogContainer = document.getElementById('blog-container');
            blogContainer.innerHTML = `<p style="color: var(--accent-orange);">Error cargando blog: ${escapeHtml(err.message)}</p>`;
        });
    
    document.getElementById('back-to-main').onclick = () => {
        faucetDetail.classList.add('hidden');
        hero.classList.remove('hidden');
        faucetList.classList.remove('hidden');
    };
}
```

---

### Task 5: Update blog index links to absolute paths

**Objective:** Ensure all blog index links work correctly from any entry point.

**Files:**
- Modify: `blog/posts/index.html`

**Changes:**
Replace relative links like `href="filename.html"` with absolute paths like `href="/blog/posts/filename.html"`

This is already correct in the current index.html - the links use `/blog/posts/` prefix.

---

### Task 6: Test the integration

**Objective:** Verify navigation works correctly.

**Verification Steps:**
1. Open `index.html` in browser
2. Click "Blog" button - should show blog index
3. Click a blog post link - should show post with nav bar
4. Click "← Volver a Faucets" in nav - should return to main site
5. Click "Blog Index" link - should return to blog index
6. Test "Back to Faucets" button on blog view in main site

---

## Files Summary

| File | Action |
|------|--------|
| `blog/posts/blog-nav.js` | Create |
| `css/style.css` | Modify (add nav styles) |
| `js/app.js` | Modify (update showBlog) |
| `blog/posts/*.html` | Modify (add script tag) |
| `blog/posts/index.html` | Verify links |

---

## Risks & Considerations

1. **Existing blog posts:** The `generate-blogger-html-posts.js` script may overwrite posts if rerun. Consider updating the script to include the nav script automatically.

2. **External links:** Blog posts with external affiliate links should open in new tabs (already handled in `showBlog()` for main site, but individual posts need manual review).

3. **Styling consistency:** The nav styles should match the existing dark theme. CSS variables from `:root` should be used where possible.

---

## Verification Commands

```bash
# Validate faucets.js schema (should still pass)
node tools/validate-faucets.js

# No build step needed - just open in browser
# Test by opening index.html
```