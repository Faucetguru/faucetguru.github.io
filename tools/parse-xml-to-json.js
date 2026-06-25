
const fs = require('fs');

const xmlContent = fs.readFileSync('blogger-export/faucetguru-all-entries.xml', 'utf-8');

const entryRegex = /<ns0:entry>([\s\S]*?)<\/ns0:entry>/g;
const titleRegex = /<ns0:title type="html">(.*?)<\/ns0:title>/;
const contentRegex = /<ns0:content type="html">([\s\S]*?)<\/ns0:content>/;
// Use &lt; and &gt; to match escaped HTML
const trustScoreRegex = /Trust Score:&lt;\/strong&gt; ([\d\.]+)\/5\.0/;
const refLinkRegex = /href="([^"]+)"/;

const entries = [];
let match;
while ((match = entryRegex.exec(xmlContent)) !== null) {
  const entryXml = match[1];
  const titleMatch = entryXml.match(titleRegex);
  const contentMatch = entryXml.match(contentRegex);
  
  if (titleMatch && contentMatch) {
    const title = titleMatch[1].replace(" - Resena completa", "");
    const content = contentMatch[1];
    
    const trustScoreMatch = content.match(trustScoreRegex);
    const refLinkMatch = content.match(refLinkRegex);
    
    entries.push({
      id: title,
      trustScore: trustScoreMatch ? parseFloat(trustScoreMatch[1]) : null,
      referralLink: refLinkMatch ? refLinkMatch[1] : null
    });
  }
}

fs.writeFileSync('js/parsed-sites.json', JSON.stringify(entries, null, 2));
console.log(`Parsed ${entries.length} sites.`);
