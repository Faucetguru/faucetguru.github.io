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

// For card background images: allow both absolute https and local relative paths (img/xxx.jpg)
function safeImg(url) {
    const raw = String(url ?? '').trim();
    if (!raw || raw === '#' || raw.includes('TU_ID')) return '#';
    if (/^https?:\/\//i.test(raw)) return raw;
    if (/^(?:img|blog\/img)\//.test(raw) || raw.startsWith('/')) return raw;
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

    navLinks.innerHTML = `${filterButtonsHtml}<button class="nav-btn" id="blog-link">Blog</button><button class="nav-btn" id="bet-link">Bet</button>`;
}

function init() {
    renderNavButtons();
    renderList(faucets);
    setupEventListeners();
}

async function initVisitCounter() {
    const counterEl = document.getElementById('visit-count');
    if (!counterEl) return;

    const LOCAL_KEY = 'faucetguru-local-count';
    const SESSION_KEY = 'faucetguru-session-counted';
    let loaded = false;

    const setCount = (value) => {
        if (!Number.isFinite(value)) return;
        counterEl.textContent = `${Number(value).toLocaleString()} visitas`;
        counterEl.style.visibility = 'visible';
        loaded = true;
    };

    const tryGenerate = async () => {
        if (loaded) return;
        try {
            const endpoint = 'https://api.countapi.xyz/hit/faucetguru.github.io/visits';
            const response = await fetch(endpoint);
            if (response.ok) {
                const data = await response.json();
                const value = Number(data.value);
                if (Number.isFinite(value) && value >= 0) {
                    localStorage.setItem(LOCAL_KEY, String(value));
                    localStorage.setItem(SESSION_KEY, 'true');
                    setCount(value);
                    return;
                }
            }
            throw new Error('countapi unavailable');
        } catch (error) {
            setTimeout(() => {
                if (!loaded) tryGenerate();
            }, 3000);
        }
    };

    tryGenerate();
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
    // 1.3x speed: movement is 1.3x faster
    const offset = progress * -200;
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
        const bg = safeImg(faucet.image);
        const bgStyle = bg && bg !== '#'
            ? `style="background-image: linear-gradient(rgba(10,11,16,0.82), rgba(10,11,16,0.92)), url('${escapeHtml(bg)}');"`
            : '';
        card.innerHTML = `
            <div class="card-bg" ${bgStyle}></div>
            <span class="card-tag">${escapeHtml(faucet.type)}</span>
            <h3 class="card-title">${escapeHtml(faucet.name)}</h3>
            <div class="trust-badge">
                <span class="rating-stars">${stars(faucet.trustScore)}</span>
                <span>${escapeHtml(faucet.trustScore)}</span>
            </div>
            <div class="card-bonus">${escapeHtml(faucet.bonus)}</div>
            ${faucet.comment ? `<div class="card-comment">💬 ${escapeHtml(faucet.comment.substring(0, 100))}${faucet.comment.length > 100 ? '…' : ''}</div>` : ''}
            <p style="color: var(--text-dim); font-size: 0.9rem;">${escapeHtml(String(faucet.summary || '').substring(0, 80))}...</p>
            ${(() => {
                const slug = String(faucet.id || '').replace(/_/g, '-').trim();
                if (!slug) return '';
                const href = `/blog/posts/${slug}-reseña.html`;
                return `<p style="margin-top:12px;"><a class="card-blog-link" href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">📝 Entrada del blog</a></p>`;
            })()}
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

    const commentHtml = faucet.comment
        ? `
            <div class="commentary-section">
                <h3><span style="color: var(--accent-orange);">💬</span> Comentario</h3>
                <p>${escapeHtml(faucet.comment)}</p>
            </div>
          `
        : '';

    // Comments section (user comments from Supabase)
    const commentsSectionHtml = `
        <div class="comments-section" id="comments-section">
            <h3>💬 Comentarios de Usuarios</h3>
            <div id="comments-list" class="comments-list">Cargando comentarios...</div>
            
            <!-- Add Comment Form -->
            <div class="comment-form-section">
                <h4>Deja tu opinión</h4>
                <form id="comment-form" class="comment-form">
                    <div class="form-group">
                        <label for="comment-name">Tu nombre <span class="required">*</span></label>
                        <input type="text" id="comment-name" name="name" required maxlength="50" placeholder="Ej: CriptoJuan" />
                    </div>
                    <div class="form-group">
                        <label for="comment-email">Email (opcional, para notificaciones)</label>
                        <input type="email" id="comment-email" name="email" maxlength="100" placeholder="tu@email.com" />
                    </div>
                    <div class="form-group">
                        <label>Tu calificación</label>
                        <div class="star-rating" id="comment-rating">
                            <span class="star" data-value="1">★</span>
                            <span class="star" data-value="2">★</span>
                            <span class="star" data-value="3">★</span>
                            <span class="star" data-value="4">★</span>
                            <span class="star" data-value="5">★</span>
                            <input type="hidden" name="rating" id="comment-rating-value" value="0" />
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="comment-text">Comentario <span class="required">*</span></label>
                        <textarea id="comment-text" name="comment" required maxlength="2000" rows="4" placeholder="Compartí tu experiencia... ¿Paga bien? ¿Es confiable? ¿Trucos?"></textarea>
                        <small class="char-count"><span id="comment-char-count">0</span>/2000 caracteres</small>
                    </div>
                    <button type="submit" class="submit-comment-btn">💬 Publicar comentario</button>
                </form>
                <div id="comment-form-message" class="form-message"></div>
            </div>
        </div>
    `;

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
                <img src="${escapeHtml(safeImg(faucet.image))}" alt="${escapeHtml(faucet.name)}" style="width:100%; height:100%; object-fit: cover; border-radius: 20px;">
            </div>
        </div>

        ${commentHtml}

        <div class="strategy-section">
            <h3>Estrategia Recomendada</h3>
            <p>${escapeHtml(faucet.strategies)}</p>
            ${scriptSnippet}
        </div>

        <div style="margin-top: 40px;">
            <h3>Opiniones de Usuarios (Reseñas)</h3>
            ${reviewsHtml}
        </div>

        ${commentsSectionHtml}
    `;

    document.getElementById('back-to-list').onclick = () => {
        faucetDetail.classList.add('hidden');
        hero.classList.remove('hidden');
        faucetList.classList.remove('hidden');
        // Preserve active filter
        const activeBtn = navLinks.querySelector('.nav-btn.active');
        if (activeBtn) {
            const filter = activeBtn.dataset.filter;
            const filteredData = filter === 'all' ? faucets : faucets.filter(f => f.type === filter);
            renderList(filteredData);
        } else {
            renderList(faucets);
        }
    };

    // Load comments from Supabase
    loadComments(faucet.id);
    
    // Setup comment form
    setupCommentForm(faucet.id);
}

function setupEventListeners() {
    navLinks.addEventListener('click', (event) => {
        const btn = event.target.closest('.nav-btn');
        if (!btn) return;

        if (btn.id === 'blog-link') {
            showBlog();
            // Remove active from all buttons, add to Blog
            navLinks.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            return;
        }

        if (btn.id === 'bet-link') {
            showBet();
            navLinks.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
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
            <h2 style="margin-bottom: 8px;">Blog</h2>
            <input type="search" id="blog-search" placeholder="Buscar posts..." autocomplete="off" style="
                width: 100%; padding: 12px 14px; border-radius: 10px; border: 1px solid #2b2d3a;
                background: #10111a; color: #e6e9f0;
                outline: none; font-size: 1rem;
            ">
            <div id="blog-search-results" style="
                margin-top: 10px; display: none;
                background: #11131f; border: 1px solid #2b2d3a; border-radius: 12px;
                max-height: 260px; overflow-y: auto;
            "></div>
            <p style="text-align: center; color: var(--text-dim);">Cargando blog...</p>
        </div>
    `;
    
    document.getElementById('blog-search').addEventListener('input', (event) => {
        const query = String(event.target.value || '').trim().toLowerCase();
        const resultsBox = document.getElementById('blog-search-results');
        if (!currentBlogPosts.length) {
            resultsBox.style.display = 'none';
            return;
        }

        if (!query) {
            resultsBox.style.display = 'none';
            return;
        }

        const matches = currentBlogPosts.filter(post =>
            (post.title || '').toLowerCase().includes(query)
        );

        if (!matches.length) {
            resultsBox.innerHTML = `<div style="padding:12px 14px; color: var(--text-dim);">Sin resultados</div>`;
            resultsBox.style.display = 'block';
            return;
        }

        resultsBox.innerHTML = matches.map(post => `
            <a href="${escapeHtml(post.href)}" target="_blank" rel="noopener noreferrer" style="display: block; padding: 10px 14px; color: #e6e9f0; text-decoration: none;">
                <div style="font-weight: 600;">${escapeHtml(post.title)}</div>
                <div style="font-size: 0.82rem; color: var(--text-dim); word-break: break-all;">${escapeHtml(post.href)}</div>
            </a>
        `).join('');
        resultsBox.style.display = 'block';
    });

    document.addEventListener('click', (event) => {
        const resultsBox = document.getElementById('blog-search-results');
        if (!resultsBox) return;
        if (!resultsBox.contains(event.target) && event.target.id !== 'blog-search') {
            resultsBox.style.display = 'none';
        }
    });
    
    fetch('blog/posts/index.html')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.text();
        })
        .then(html => {
            currentBlogPosts = extractBlogPosts(html);
            const blogContainer = document.getElementById('blog-container');
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const bodyContent = doc.body.innerHTML;
            blogContainer.innerHTML = bodyContent + `
                <div style="margin-top: 40px; padding: 20px; background: #0d0f18; border-radius: 14px; border: 1px solid #22242f;">
                    <h3 style="margin-bottom: 10px;">Navegación rápida</h3>
                    <ul style="padding-left: 20px; display: grid; gap: 8px;">
                        ${currentBlogPosts.slice(0, 20).map(post => `
                            <li><a href="${escapeHtml(post.href)}" target="_blank" rel="noopener noreferrer">${escapeHtml(post.title)}</a></li>
                        `).join('')}
                    </ul>
                    ${currentBlogPosts.length > 20 ? `<p style="color: var(--text-dim); font-size: 0.85rem;">Mostrando los primeros 20 posts. Usá el buscador para ver el resto.</p>` : ''}
                </div>
            `;
            
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
        currentBlogPosts = [];
        faucetDetail.classList.add('hidden');
        hero.classList.remove('hidden');
        faucetList.classList.remove('hidden');
    };
}

function showBet() {
    hero.classList.add('hidden');
    faucetList.classList.add('hidden');
    faucetDetail.classList.remove('hidden');
    
    faucetDetail.innerHTML = `
        <button class="back-btn" id="back-to-main">← Volver a Faucets</button>
        <div id="bet-container" style="max-width: 1200px; margin: 0 auto;">
            <p style="text-align: center; color: var(--text-dim);">Cargando Bet...</p>
        </div>
    `;
    
    fetch('bet/')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.text();
        })
        .then(html => {
            const betContainer = document.getElementById('bet-container');
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const bodyContent = doc.body.innerHTML;
            betContainer.innerHTML = bodyContent;
            
            betContainer.querySelectorAll('a').forEach(link => {
                if (link.hostname && link.hostname !== window.location.hostname) {
                    link.setAttribute('target', '_blank');
                    link.setAttribute('rel', 'noopener noreferrer');
                }
            });
        })
        .catch(err => {
            const betContainer = document.getElementById('bet-container');
            betContainer.innerHTML = `<p style="color: var(--accent-orange);">Error cargando Bet: ${escapeHtml(err.message)}</p>`;
        });
    
    document.getElementById('back-to-main').onclick = () => {
        faucetDetail.classList.add('hidden');
        hero.classList.remove('hidden');
        faucetList.classList.remove('hidden');
    };
}

// ============================================
// COMMENT SYSTEM FUNCTIONS (Supabase)
// ============================================

let currentCommentRating = 0;

async function loadComments(faucetId) {
    const commentsList = document.getElementById('comments-list');
    if (!commentsList) return;
    
    if (!window.SupabaseComments || !window.SupabaseComments.fetchComments) {
        commentsList.innerHTML = '<p style="color: var(--text-dim); text-align: center; padding: 20px;">Sistema de comentarios no configurado. Configura Supabase en <code>js/supabase-client.js</code></p>';
        return;
    }
    
    try {
        commentsList.innerHTML = '<p style="text-align: center; color: var(--text-dim);">Cargando comentarios...</p>';
        
        const comments = await window.SupabaseComments.fetchComments(faucetId);
        
        if (comments.length === 0) {
            commentsList.innerHTML = '<p style="text-align: center; color: var(--text-dim); padding: 20px;">Sé el primero en comentar 👇</p>';
            return;
        }
        
        commentsList.innerHTML = comments.map(comment => `
            <div class="comment-item" data-comment-id="${escapeHtml(comment.id)}">
                <div class="comment-header">
                    <span class="comment-author">${escapeHtml(comment.user_name)}</span>
                    <span class="comment-date">${window.SupabaseComments.formatCommentDate(comment.created_at)}</span>
                </div>
                <div class="comment-rating">
                    ${'★'.repeat(comment.rating || 0)}${'☆'.repeat(5 - (comment.rating || 0))}
                </div>
                <div class="comment-text">${escapeHtml(comment.text)}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading comments:', error);
        commentsList.innerHTML = '<p style="color: var(--accent-orange); text-align: center;">Error cargando comentarios</p>';
    }
}

function setupCommentForm(faucetId) {
    const form = document.getElementById('comment-form');
    if (!form) return;
    
    // Star rating interaction
    const stars = document.querySelectorAll('#comment-rating .star');
    const ratingInput = document.getElementById('comment-rating-value');
    
    stars.forEach(star => {
        star.addEventListener('click', () => {
            currentCommentRating = parseInt(star.dataset.value);
            ratingInput.value = currentCommentRating;
            updateStarDisplay(stars, currentCommentRating);
        });
        
        star.addEventListener('mouseenter', () => {
            updateStarDisplay(stars, parseInt(star.dataset.value), true);
        });
        
        star.addEventListener('mouseleave', () => {
            updateStarDisplay(stars, currentCommentRating, false);
        });
    });
    
    // Character counter
    const textarea = document.getElementById('comment-text');
    const charCount = document.getElementById('comment-char-count');
    
    textarea.addEventListener('input', () => {
        charCount.textContent = textarea.value.length;
    });
    
    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('.submit-comment-btn');
        const messageDiv = document.getElementById('comment-form-message');
        
        const name = form.name.value.trim();
        const email = form.email.value.trim();
        const text = form.comment.value.trim();
        const rating = currentCommentRating;
        
        if (!name || !text) {
            showFormMessage(messageDiv, 'Por favor completá tu nombre y comentario', 'error');
            return;
        }
        
        if (rating === 0) {
            showFormMessage(messageDiv, 'Por favor seleccioná una calificación (estrellas)', 'error');
            return;
        }
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Publicando...';
        messageDiv.textContent = '';
        messageDiv.className = 'form-message';
        
        try {
            if (!window.SupabaseComments || !window.SupabaseComments.postComment) {
                throw new Error('Sistema de comentarios no configurado');
            }
            
            const result = await window.SupabaseComments.postComment(faucetId, text, name);
            
            if (result.error) {
                throw new Error(result.error);
            }
            
            showFormMessage(messageDiv, '¡Comentario publicado! 🎉', 'success');
            form.reset();
            currentCommentRating = 0;
            ratingInput.value = '0';
            updateStarDisplay(stars, 0, false);
            charCount.textContent = '0';
            
            // Reload comments to show the new one
            await loadComments(faucetId);
            
        } catch (error) {
            console.error('Error posting comment:', error);
            showFormMessage(messageDiv, `Error: ${error.message}`, 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = '💬 Publicar comentario';
        }
    });
}

function updateStarDisplay(stars, rating, isHover = false) {
    stars.forEach(star => {
        const value = parseInt(star.dataset.value);
        if (value <= rating) {
            star.classList.add('active');
            star.style.color = '#ffd700';
        } else {
            star.classList.remove('active');
            star.style.color = isHover ? '#444' : 'var(--text-dim)';
        }
    });
}

function showFormMessage(div, message, type) {
    div.textContent = message;
    div.className = `form-message ${type}`;
    if (type === 'success') {
        setTimeout(() => {
            div.textContent = '';
            div.className = 'form-message';
        }, 5000);
    }
}

init();
