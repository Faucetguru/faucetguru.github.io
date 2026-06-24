const faucets = window.faucetsData || [];

const faucetList = document.getElementById('faucet-list');
const faucetDetail = document.getElementById('faucet-detail');
const hero = document.getElementById('hero');
const navLinks = document.querySelector('.nav-links');
const searchInput = document.getElementById('nav-search');

const TYPE_LABELS = {
    all: 'Todas',
    faucet: 'Faucets',
    ptc: 'PTC',
    mining: 'Minería',
    tasks: 'Tareas',
    rewards: 'Recompensas',
    referral: 'Referidos',
    wallet: 'Wallet',
};

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>'"]/g, (char) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
    }[char]));
}

function safeUrl(url) {
    const raw = String(url ?? '').trim();
    if (!raw || raw === '#' || raw.includes('TU_ID')) return '#';
    if (/^https?:\/\//i.test(raw)) return raw;
    return '#';
}

function stars(score) {
    const safeScore = Number.isFinite(Number(score)) ? Number(score) : 0;
    return '★'.repeat(Math.max(0, Math.floor(safeScore)));
}

function getAvailableTypes() {
    const excludedTypes = new Set(['contests', 'affiliate', 'rewards', 'referral', 'autofaucet', 'microwallet', 'service', 'cloud_mining', 'tasks']);
    return [...new Set(faucets.map(f => String(f.type || '').trim()).filter(type => type && !excludedTypes.has(type)))].sort();
}

function renderNavButtons() {
    const availableTypes = getAvailableTypes();
    const orderedTypes = ['all', ...availableTypes];

    const filterButtonsHtml = orderedTypes.map((type, idx) => {
        const label = TYPE_LABELS[type] || type.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
        return `<button class="nav-btn ${idx === 0 ? 'active' : ''}" data-filter="${escapeHtml(type)}">${escapeHtml(label)}</button>`;
    }).join('');

    navLinks.innerHTML = `${filterButtonsHtml}<button class="nav-btn" id="blog-link">Blog</button>`;
}

function init() {
    renderNavButtons();
    renderList(faucets);
    setupEventListeners();
}

async function initVisitCounter() {
    const counterEl = document.getElementById('visit-count');
    if (!counterEl) return;

    // Local storage based visit counter (Option 2 fallback)
    const STORAGE_KEY = 'faucetguru-visits';
    const LOCAL_KEY = 'faucetguru-local-count';
    const SESSION_KEY = 'faucetguru-session-counted';
    
    // Try external API first
    try {
        const endpoint = 'https://api.countapi.xyz/hit/faucetguru.github.io/visits';
        const response = await fetch(endpoint);
        if (response.ok) {
            const data = await response.json();
            const value = Number(data.value);
            if (Number.isFinite(value)) {
                // Sync local storage with global count
                localStorage.setItem(LOCAL_KEY, value.toString());
                localStorage.setItem(SESSION_KEY, 'true');
                counterEl.textContent = value.toLocaleString();
                return;
            }
        }
        throw new Error('countapi error');
    } catch (error) {
        // Fallback to localStorage-based counting
        let localCount = Number(localStorage.getItem(LOCAL_KEY) || '0');
        const sessionCounted = localStorage.getItem(SESSION_KEY);
        
        // Increment only once per session
        if (!sessionCounted) {
            localCount++;
            localStorage.setItem(LOCAL_KEY, localCount.toString());
            localStorage.setItem(SESSION_KEY, 'true');
        }
        
        counterEl.textContent = `${localCount.toLocaleString()} visitas`;
    }
}

window.addEventListener('load', () => {
    initVisitCounter();
});

let ticking = false;
const bgWrapper = document.querySelector('.bg-wrapper');
let contentHeight = document.body.scrollHeight - window.innerHeight;

function updateParallax() {
    const scrollY = window.scrollY || window.pageYOffset || 0;
    const maxScroll = Math.max(1, contentHeight);
    const progress = scrollY / maxScroll;
    // Invertido: scroll down = move image up (negative offset)
    const offset = progress * -100;
    if (bgWrapper) bgWrapper.style.transform = `translateY(calc(25% + ${offset}px))`;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            updateParallax();
            ticking = false;
        });
        ticking = true;
    }
}, { passive: true });

// Recalculate on content load
window.addEventListener('load', () => {
    contentHeight = document.body.scrollHeight - window.innerHeight;
    updateParallax();
});

function renderList(data) {
    faucetList.innerHTML = '';
    data.forEach(faucet => {
        const card = document.createElement('div');
        card.className = 'faucet-card';
        card.innerHTML = `
            <span class="card-tag">${escapeHtml(faucet.type)}</span>
            <h3 class="card-title">${escapeHtml(faucet.name)}</h3>
            <div class="trust-badge">
                <span class="rating-stars">${stars(faucet.trustScore)}</span>
                <span>${escapeHtml(faucet.trustScore)}</span>
            </div>
            <div class="card-bonus">${escapeHtml(faucet.bonus)}</div>
            <p style="color: var(--text-dim); font-size: 0.9rem;">${escapeHtml(String(faucet.summary || '').substring(0, 80))}...</p>
        `;
        card.onclick = () => showDetail(faucet);
        faucetList.appendChild(card);
    });
}

function showDetail(faucet) {
    hero.classList.add('hidden');
    faucetList.classList.add('hidden');
    faucetDetail.classList.remove('hidden');

    const cleanedReviews = Array.isArray(faucet.reviews) ? faucet.reviews : [];
    const reviewsHtml = cleanedReviews.map(r => `
        <div style="background: var(--bg-card); padding: 15px; border-radius: 10px; margin-top: 10px;">
            <strong>${escapeHtml(r.user)}</strong> <span style="color: gold;">${stars(r.rating)}</span>
            <p style="color: var(--text-dim);">${escapeHtml(r.text)}</p>
        </div>
    `).join('');

    const referral = safeUrl(faucet.referralLink);
    const scriptSnippet = faucet.script && faucet.script !== 'N/A'
        ? `
            <h4 style="margin-top: 20px;">Script / Código Útil:</h4>
            <pre><code>${escapeHtml(faucet.script)}</code></pre>
          `
        : '';

    faucetDetail.innerHTML = `
        <button class="back-btn" id="back-to-list">← Volver al listado</button>
        <div class="detail-header">
            <div class="detail-info">
                <span class="card-tag">${escapeHtml(faucet.type)}</span>
                <h2>${escapeHtml(faucet.name)}</h2>
                <div class="trust-badge">
                    <span class="rating-stars" style="font-size: 1.5rem;">${stars(faucet.trustScore)}</span>
                    <span style="font-size: 1.5rem;">${escapeHtml(faucet.trustScore)} / 5</span>
                </div>
                <p>${escapeHtml(faucet.summary)}</p>
                <div class="card-bonus" style="margin-top: 20px;">
                    <strong>BONUS EXCLUSIVO:</strong> ${escapeHtml(faucet.bonus)}
                </div>
                <a href="${escapeHtml(referral)}" target="_blank" rel="noopener noreferrer" class="cta-btn">¡Regístrate y Gana Ahora!</a>
            </div>
            <div class="screenshot-container">
                <img src="${escapeHtml(safeUrl(faucet.image))}" alt="${escapeHtml(faucet.name)}" style="width:100%; height:100%; object-fit: cover; border-radius: 20px;">
            </div>
        </div>

        <div class="strategy-section">
            <h3>Estrategia Recomendada</h3>
            <p>${escapeHtml(faucet.strategies)}</p>
            ${scriptSnippet}
        </div>

        <div style="margin-top: 40px;">
            <h3>Opiniones de Usuarios</h3>
            ${reviewsHtml}
        </div>
    `;

    document.getElementById('back-to-list').onclick = () => {
        faucetDetail.classList.add('hidden');
        hero.classList.remove('hidden');
        faucetList.classList.remove('hidden');
    };
}

function setupEventListeners() {
    navLinks.addEventListener('click', (event) => {
        const btn = event.target.closest('.nav-btn');
        if (!btn) return;

        if (btn.id === 'blog-link') {
            showBlog();
            return;
        }

        navLinks.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.dataset.filter;
        const filteredData = filter === 'all' ? faucets : faucets.filter(f => f.type === filter);
        renderList(filteredData);

        faucetDetail.classList.add('hidden');
        hero.classList.remove('hidden');
        faucetList.classList.remove('hidden');
    });

    document.getElementById('home-link').onclick = () => {
        location.reload();
    };
}

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

init();
