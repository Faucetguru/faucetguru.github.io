/**
 * bet-app.js
 * Render básico del hub de reseñas.
 */

window.betSitesData = window.betSitesData || [];

const defaultRank = (site) => site.trustScore ?? 0;

const text = (value) => {
  const safe = document.createElement("span");
  safe.textContent = value == null ? "" : String(value);
  return safe;
};

const escHtml = (value) => {
  return value
    ? String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
    : "";
};

const escapeHtml = (value) => {
  return value
    ? String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
    : "";
};

const safeUrl = (url) => {
  if (!url || url === "#") return "#";
  const u = String(url).trim();
  if (!/^https?:\/\//i.test(u)) return "#";
  return u;
};

function renderBetList(data) {
  const list = document.getElementById("bet-list");
  if (!list) return;
  const sorted = [...data].sort((a, b) => (b.trustScore ?? 0) - (a.trustScore ?? 0));
  list.innerHTML = "";
  if (!sorted.length) {
    list.innerHTML = `<div class="empty">No hay reseñas aún.</div>`;
    return;
  }
  sorted.forEach((site) => {
    const card = document.createElement("article");
    card.className = "card";
    const name = escHtml(site.name);
    const summary = escHtml(site.summary);
    const bonus = escHtml(site.bonus);
    const trust = Number(site.trustScore ?? 0);
    const stars = "★".repeat(Math.max(0, Math.min(5, trust))) + "☆".repeat(Math.max(0, 5 - Math.min(5, trust)));
    const url = safeUrl(site.referralLink);
    const cta = url && url !== "#" ? `<a href="${url}" rel="noopener noreferrer">Ver oferta</a>` : `<span class="muted">Sin enlace de referido</span>`;
    card.innerHTML = `
      <h3>${name}</h3>
      <p class="meta">${stars} / Trust ${trust}</p>
      <p>${summary}</p>
      ${bonus ? `<p class="highlight">Bono: ${bonus}</p>` : ""}
      <div class="actions">${cta}</div>
    `;
    list.appendChild(card);
  });
}

function initBetApp(data) {
  if (!document.getElementById("bet-list")) return;
  renderBetList(data);
}
