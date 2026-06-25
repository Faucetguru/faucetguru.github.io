
const fs = require('fs');
const path = require('path');

const inputDir = '/home/salmarina/Faucetguru_site/blog-content-final';
const outputDir = '/home/salmarina/Faucetguru_site/blogger-export/html-posts';

// Ensure output directory exists
if (!fs.existsSync(outputDir)){
    fs.mkdirSync(outputDir, { recursive: true });
}

// Minimal Markdown to HTML converter
function mdToHtml(md) {
  let html = md
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\[(.*)\]\((.*)\)/gim, '<a href="$2">$1</a>')
    .replace(/^\* (.*$)/gim, '<ul><li>$1</li></ul>')
    .replace(/\n/g, '<br>');
  // Cleanup lists
  html = html.replace(/<\/ul><br><ul>/g, '');
  return html;
}

const files = fs.readdirSync(inputDir).filter(file => file.endsWith('.md'));

files.forEach((file) => {
  const filePath = path.join(inputDir, file);
  const content = fs.readFileSync(filePath, 'utf-8');
  
  // Basic front-matter parsing
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  let title = file.replace(/.md$/, '');
  let body = content;
  
  if (fmMatch) {
    const fm = fmMatch[1];
    body = fmMatch[2];
    const titleMatch = fm.match(/title: "(.*)"/);
    if (titleMatch) title = titleMatch[1];
  }

  const htmlBody = mdToHtml(body);
  
  // Wrap in a simple HTML document structure for Blogger compatibility
  const htmlContent = `<html>
<head>
  <title>${title}</title>
</head>
<body>
  ${htmlBody}
</body>
</html>`;
  
  const outputFilePath = path.join(outputDir, file.replace(/.md$/, '.html'));
  fs.writeFileSync(outputFilePath, htmlContent);
  console.log(`Generated ${outputFilePath}`);
});

console.log(`Finished generating HTML posts in ${outputDir}`);
