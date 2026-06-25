
const fs = require('fs');
const path = require('path');

const inputDir = '/home/salmarina/Faucetguru_site/blog/markdown';
const outputFilePath = '/home/salmarina/Faucetguru_site/blog/blogger-export/final-blog-export.xml';

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

let entriesXml = '';

files.forEach((file, index) => {
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

  const htmlBody = mdToHtml(body).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  entriesXml += `
  <ns0:entry>
    <ns0:id>tag:blogger.com,1999:blog-faucetguru-export.post-${1000000000000000000 + index}</ns0:id>
    <ns0:published>${new Date().toISOString()}</ns0:published>
    <ns0:updated>${new Date().toISOString()}</ns0:updated>
    <ns0:category scheme="http://www.blogger.com/atom/ns#" term="post" />
    <ns0:title type="html">${title}</ns0:title>
    <ns0:content type="html">${htmlBody}</ns0:content>
    <ns0:author>
      <ns0:name>FaucetGuru</ns0:name>
    </ns0:author>
  </ns0:entry>`;
});

const finalXml = `<?xml version='1.0' encoding='UTF-8'?>
<ns0:feed xmlns:ns0="http://www.w3.org/2005/Atom">
  <ns0:title type="text">FaucetGuru Blog</ns0:title>
  <ns0:generator version="7.00" uri="http://www.blogger.com">Blogger</ns0:generator>
  ${entriesXml}
</ns0:feed>`;

fs.writeFileSync(outputFilePath, finalXml);
console.log(`Generated ${outputFilePath}`);
