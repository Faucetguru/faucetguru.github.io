# Blog Post Navigation Integration Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Add navigation buttons to blog post HTML pages and integrate them with the main index page and frame principal.

**Architecture:** Create a shared navigation component that can be loaded on any blog post page, with links back to the main site and between blog posts. The navigation will be injected via a shared JavaScript file.

**Tech Stack:** Vanilla HTML, CSS, JavaScript (no framework)

---

### Task 1: Create shared blog navigation JavaScript

**Objective:** Create a reusable navigation component for blog posts.

**Files:**
- Create: `blog/posts/blog-nav.js`

**Step 1: Write the navigation script**

```javascript
(function() {
    const posts = [
        {
            title: "Ready Wallet (ex Argent X): la wallet inteligente de Starknet para Argentina",
            url: "ready-wallet-starknet-guia-argentina.html"
        },
        {
            title: "Tangem Wallet en Argentina: ¿la mejor billetera hardware para crypto?",
            url: "tangem-wallet-argentina-billetera-hardware-segura.html"
        },
        {
            title: "ACI Airdrop: cómo participar desde Argentina, guía paso a paso 2026",
            url: "aci-airdrop-guia-como-participar-desde-argentina.html"
        },
        {
            title: "Backpack Wallet review 2026: ¿Es la mejor wallet para Solana, Monad y Berachain?",
            url: "backpack-wallet-review-2026-es-la-mejor-wallet-para-solana-monad-y-berachain.html"
        },
        {
            title: "Reseña de ABC Mining: ¿Es confiable para ganar crypto en Argentina?",
            url: "abc-mining-reseña.html"
        }
    ];

    function getCurrentPostIndex() {
        const currentPath = window.location.pathname.split('/').pop();
        return posts.findIndex(post => post.url === currentPath);
    }

    function createNav() {
        const nav = document.createElement('nav');
        nav.className = 'blog-nav';
        nav.innerHTML = `
            <div class="blog-nav-inner">
                <a href="/" class="blog-nav-link">⚡ Faucet Guru</a>
                <a href="/blog/posts/index.html" class="blog-nav-link">Blog Index</a>
                <div class="blog-nav-spacer"></div>
                <a href="#" class="blog-nav-link" id="prev-post">← Anterior</a>
                <a href="#" class="blog-nav-link" id="next-post">Siguiente →</a>
            </div>
        `;
        return nav;
    }

    function setupPrevNext(nav) {
        const currentIndex = getCurrentPostIndex();
        const prevLink = nav.querySelector('#prev-post');
        const nextLink = nav.querySelector('#next-post');

        if (currentIndex <= 0) {
            prevLink.style.visibility = 'hidden';
        } else {
            prevLink.href = posts[currentIndex - 1].url;
        }

        if (currentIndex < 0 || currentIndex >= posts.length - 1) {
            nextLink.style.visibility = 'hidden';
        } else {
            nextLink.href = posts[currentIndex + 1].url;
        }
    }

    function injectNav() {
        const nav = createNav();
        document.body.insertBefore(nav, document.body.firstChild);
        setupPrevNext(nav);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectNav);
    } else {
        injectNav();
    }
})();
```

**Step 2: Add CSS styles**

Add to `css/style.css`:

```css
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
}

.blog-nav-link:hover {
    text-decoration: underline;
}

.blog-nav-spacer {
    flex: 1;
}
```

---

### Task 2: Add navigation to blog post HTML files

**Objective:** Inject the shared navigation into the 5 new blog post HTML files.

**Files:**
- Modify: `blog/posts/ready-wallet-starknet-guia-argentina.html`
- Modify: `blog/posts/tangem-wallet-argentina-billetera-hardware-segura.html`
- Modify: `blog/posts/aci-airdrop-guia-como-participar-desde-argentina.html`
- Modify: `blog/posts/backpack-wallet-review-2026-es-la-mejor-wallet-para-solana-monad-y-berachain.html`
- Modify: `blog/posts/abc-mining-reseña.html`

**Step 1: Add script reference to each HTML file**

For each file, add before `</body>`:

```html
<script src="/blog/posts/blog-nav.js"></script>
</body>
```

---

### Task 3: Update main index to integrate blog section

**Objective:** Update `js/app.js` to provide proper navigation between main site and blog.

**Files:**
- Modify: `js/app.js`

**Step 1: Update `showBlog()` function**

Add a "Back to Main Site" button in the blog view:

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

### Task 4: Update blog index links

**Objective:** Ensure all blog index links use absolute paths.

**Files:**
- Modify: `blog/posts/index.html`

**Step 1: Convert relative links to absolute**

Replace `href="filename.html"` with `href="/blog/posts/filename.html"`

---

### Task 5: Test and deploy

**Objective:** Verify navigation works and deploy.

**Step 1: Test locally**

1. Open `index.html` in browser
2. Click "Blog" button
3. Click a blog post link
4. Verify nav bar shows with correct links
5. Test Prev/Next buttons

**Step 2: Deploy**

```bash
git add .
git commit --no-gpg-sign -m "feat: add blog navigation"
git push origin main
git push origin gh-pages
```