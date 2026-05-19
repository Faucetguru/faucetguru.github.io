const fs = require('fs');
const path = require('path');

const directoryPath = '/home/salmarina/Faucetguru_site/blog-content-final';
const files = fs.readdirSync(directoryPath);

files.forEach(file => {
  if (!file.endsWith('.md')) return;

  const filePath = path.join(directoryPath, file);
  const content = fs.readFileSync(filePath, 'utf-8');

  // Check metadata
  const hasMetadata = content.startsWith('---') && content.split('---')[1].includes('title:') && content.split('---')[1].includes('description:') && content.split('---')[1].includes('keywords:') && content.split('---')[1].includes('author:');

  // Check FAQ
  const faqMatch = content.match(/## (FAQ|Preguntas frecuentes)/i);
  let faqCount = 0;
  if (faqMatch) {
    const faqSection = content.substring(faqMatch.index);
    const questions = faqSection.match(/\d+\./g) || [];
    faqCount = questions.length;
  }

  // Check Conclusión
  const hasConclusion = /## Conclusión/i.test(content);

  console.log(`${file}:`);
  console.log(`  Metadata: ${hasMetadata}`);
  console.log(`  FAQ Count: ${faqCount}`);
  console.log(`  Has Conclusión: ${hasConclusion}`);
});
