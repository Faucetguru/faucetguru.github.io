const fs = require('fs');
const path = require('path');

const postsDir = path.join(__dirname, '..', 'blog', 'posts');
const backupDir = path.join(__dirname, '..', 'blog', 'posts-backup');

const SEO_KEYWORDS = {
    'faucet': 'faucet, cripto argentina, bitcoin gratis, ethereum, reseña',
    'bitcoin': 'bitcoin, cripto argentina, faucet, blockchain, btc',
    'ethereum': 'ethereum, cripto argentina, faucet, reseña',
    'tron': 'tron, trx, cripto argentina, inversiones, reseña',
    'wallet': 'wallet, billetera cripto, seguridad, argentina, reseña',
    'mining': 'mining, minería cripto, bitcoin, gpu, cpu',
    'ptc': 'ptc, ganar dinero, clic, cripto argentina, reseña',
    'reseña': 'reseña, review, cripto argentina, faucet, reseña',
    'tutorial': 'tutorial, guía, cripto argentina, cómo hacer, paso a paso',
    'guia': 'guía, tutorial, cripto argentina, cómo hacer, paso a paso',
    'cripto': 'criptomonedas, bitcoin, ethereum, argentina, inversión',
    'satoshis': 'satoshis, bitcoin, faucet, ganar gratis, micropagos',
    'testnet': 'testnet, tokens gratis, blockchain, prueba, reseña',
    'airdrop': 'airdrop, tokens gratis, cripto argentina, ganar, reseña',
    'payout': 'payout, retiros, pagos, cripto argentina, faucet'
};

function extractTitle(html) {
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    return titleMatch ? titleMatch[1].trim() : null;
}

function extractDescription(html) {
    const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["']/i);
    return descMatch ? descMatch[1] : null;
}

function extractKeywords(html) {
    const kwMatch = html.match(/<meta[^>]*name=["']keywords["'][^>]*content=["']([^"']+)["']/i);
    return kwMatch ? kwMatch[1] : null;
}

function generateDescription(title, content) {
    const sentences = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
    const desc = sentences.substring(0, 150).replace(/\s+$/, '');
    return desc.endsWith('.') ? desc : desc + '.';
}

function generateKeywords(title, content) {
    const titleLower = title.toLowerCase();
    let keywords = ['cripto argentina', 'faucet', 'criptomonedas'];
    
    for (const [key, kw] of Object.entries(SEO_KEYWORDS)) {
        if (titleLower.includes(key) || content.toLowerCase().includes(key)) {
            keywords.push(...kw.split(', '));
        }
    }
    
    return [...new Set(keywords)].join(', ');
}

function updateHtmlMeta(html, title, description, keywords) {
    let headMatch = html.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
    if (!headMatch) return html;
    
    let headContent = headMatch[1];
    
    const titleRegex = /<title[^>]*>[^<]*<\/title>/i;
    headContent = headContent.replace(titleRegex, `<title>${title}</title>`);
    
    const descRegex = /<meta[^>]*name=["']description[""][^>]*>/i;
    const descTag = `<meta name="description" content="${description}">`;
    headContent = descRegex.test(headContent) 
        ? headContent.replace(descRegex, descTag) 
        : headContent.replace(/<\/title>/i, `</title>\n    ${descTag}`);
    
    const kwRegex = /<meta[^>]*name=["']keywords[""][^>]*>/i;
    const kwTag = `<meta name="keywords" content="${keywords}">`;
    headContent = kwRegex.test(headContent) 
        ? headContent.replace(kwRegex, kwTag) 
        : headContent.replace(/<\/title>/i, `</title>\n    ${kwTag}`);
    
    const ogTitleRegex = /<meta[^>]*property=["']og:title[""][^>]*>/i;
    const ogTitleTag = `<meta property="og:title" content="${title}">`;
    headContent = ogTitleRegex.test(headContent) 
        ? headContent.replace(ogTitleRegex, ogTitleTag) 
        : headContent.replace(/<\/title>/i, `</title>\n    ${ogTitleTag}`);
    
    const ogDescRegex = /<meta[^>]*property=["']og:description[""][^>]*>/i;
    const ogDescTag = `<meta property="og:description" content="${description}">`;
    headContent = ogDescRegex.test(headContent) 
        ? headContent.replace(ogDescRegex, ogDescTag) 
        : headContent.replace(/<\/title>/i, `</title>\n    ${ogDescTag}`);
    
    return html.replace(/<head[^>]*>[\s\S]*?<\/head>/i, `<head>\n    ${headContent}\n  </head>`);
}

function processPosts() {
    if (!fs.existsSync(backupDir)) {
        fs.mkdirSync(backupDir, { recursive: true });
    }
    
    const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.html'));
    let processed = 0;
    let updated = 0;
    
    for (const file of files) {
        const filePath = path.join(postsDir, file);
        const html = fs.readFileSync(filePath, 'utf8');
        processed++;
        
        const title = extractTitle(html) || file.replace('.html', '');
        const existingDesc = extractDescription(html);
        const existingKw = extractKeywords(html);
        
        const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
        const bodyContent = bodyMatch ? bodyMatch[1] : '';
        
        const description = existingDesc || generateDescription(title, bodyContent);
        const keywords = existingKw || generateKeywords(title, bodyContent);
        
        if (!existingDesc || !existingKw) {
            const updatedHtml = updateHtmlMeta(html, title, description, keywords);
            
            fs.writeFileSync(path.join(backupDir, file), html);
            fs.writeFileSync(filePath, updatedHtml);
            updated++;
            
            console.log(`✓ ${file}`);
            console.log(`  Title: ${title}`);
            console.log(`  Desc: ${description.substring(0, 60)}...`);
        } else {
            console.log(`✓ ${file} (SEO OK)`);
        }
    }
    
    console.log(`\nProcessed: ${processed} posts, Updated: ${updated} posts`);
}

processPosts();