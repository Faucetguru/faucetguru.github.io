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