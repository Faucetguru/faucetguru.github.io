const faucets = window.faucetsData || [];

const faucetList = document.getElementById('faucet-list');
const faucetDetail = document.getElementById('faucet-detail');
const hero = document.getElementById('hero');
const navLinks = document.querySelector('.nav-links');

const TYPE_LABELS = {
    all: 'Todas',
    faucet: 'Faucets',
    mining: 'Minería',
    ptc: 'PTC',
    rewards: 'Recompensas',
    tasks: 'Tareas',
    contests: 'Concursos',
    investment: 'Inversión',
    referral: 'Referidos',
    autofaucet: 'AutoFaucet',
    service: 'Servicios',
    affiliate: 'Afiliados',
    cloud_mining: 'Cloud Mining',
    wallet: 'Wallet',
    microwallet: 'MicroWallet'
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
    return [...new Set(faucets.map(f => String(f.type || '').trim()).filter(Boolean))].sort();
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
        <button class="back-btn" id="back-to-list">← Volver al listado</button>
        <div id="blog-container" style="max-width: 900px; margin: 0 auto;">
            <p style="text-align: center; color: var(--text-dim);">Cargando blog...</p>
        </div>
    `;
    
    fetch('blog/blogger-export/html-posts/index.html')
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
    
    document.getElementById('back-to-list').onclick = () => {
        faucetDetail.classList.add('hidden');
        hero.classList.remove('hidden');
        faucetList.classList.remove('hidden');
    };
}

init();
