
const fs = require('fs');

const xmlContent = fs.readFileSync('blogger-export/faucetguru-all-entries.xml', 'utf-8');

const entryRegex = /<ns0:entry>([\s\S]*?)<\/ns0:entry>/g;
const titleRegex = /<ns0:title type="html">(.*?)<\/ns0:title>/;
const contentRegex = /<ns0:content type="html">([\s\S]*?)<\/ns0:content>/;

const results = [];
let match;
while ((match = entryRegex.exec(xmlContent)) !== null) {
  const entryXml = match[1];
  const titleMatch = entryXml.match(titleRegex);
  const contentMatch = entryXml.match(contentRegex);
  
  if (titleMatch && contentMatch) {
    const title = titleMatch[1].replace(" - Resena completa", "");
    const content = contentMatch[1];
    
    // Simple word count (naive)
    const wordCount = content.split(/\s+/).length;
    
    // Check for H2s
    const h2Count = (content.match(/&lt;h2&gt;/g) || []).length;
    
    // Check for FAQ section
    const hasFAQ = content.includes("FAQ") || content.includes("Preguntas frecuentes");

    results.push({
      id: title,
      wordCount,
      h2Count,
      hasFAQ
    });
  }
}

// Generate report
console.log("Audit Report:");
console.log("--------------------------------------------------");
results.forEach(r => {
  console.log(`${r.id}:`);
  console.log(`  Words: ${r.wordCount} (Target: 1200+)`);
  console.log(`  H2s: ${r.h2Count} (Target: Structure)`);
  console.log(`  Has FAQ: ${r.hasFAQ}`);
});
