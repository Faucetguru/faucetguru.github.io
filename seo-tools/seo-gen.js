const fs = require('fs');
const path = require('path');

// Basic configuration
const config = {
    baseUrl: 'https://faucetguru.github.io/',
    title: 'Faucet Guru - Reseñas y Estrategias',
    description: 'Encuentra las mejores faucets, PTC y minería de cripto. Reseñas reales, estrategias de juego y scripts.',
    keywords: 'faucets, cripto, minería, PTC, estrategias, scripts',
    ogImage: 'https://faucetguru.github.io/og-image.jpg' // Placeholder
};

// 1. Generate robots.txt
function generateRobotsTxt() {
    const content = `User-agent: *\nAllow: /\nSitemap: ${config.baseUrl}sitemap.xml`;
    fs.writeFileSync('robots.txt', content);
    console.log('robots.txt generated.');
}

// 2. Generate sitemap.xml
function generateSitemap() {
    const files = fs.readdirSync('.').filter(file => file.endsWith('.html'));
    let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;
    files.forEach(file => {
        xml += `  <url>\n    <loc>${config.baseUrl}${file}</loc>\n  </url>\n`;
    });
    xml += `</urlset>`;
    fs.writeFileSync('sitemap.xml', xml);
    console.log('sitemap.xml generated.');
}

// 3. Inject Meta Tags into index.html
function injectMetaTags() {
    let html = fs.readFileSync('index.html', 'utf8');
    
    // Add meta tags
    const metaTags = `
    <meta name="description" content="${config.description}">
    <meta name="keywords" content="${config.keywords}">
    <link rel="canonical" href="${config.baseUrl}">
    <meta property="og:title" content="${config.title}">
    <meta property="og:description" content="${config.description}">
    <meta property="og:url" content="${config.baseUrl}">
    <meta property="og:type" content="website">
    <meta property="og:image" content="${config.ogImage}">
    `;
    
    // Simple injection (replace existing description or just after head)
    html = html.replace(/<meta name="description".*?>/s, ''); // Remove old
    html = html.replace('<head>', `<head>${metaTags}`);
    
    fs.writeFileSync('index.html', html);
    console.log('Meta tags injected into index.html.');
}

generateRobotsTxt();
generateSitemap();
injectMetaTags();
