
const fs = require('fs');
const path = require('path');

const inputDir = '/home/salmarina/Faucetguru_site/blog/blogger-export/html-posts';
const outputFilePath = path.join(inputDir, 'index.html');

// Read files, get titles, sort newest first
const files = fs.readdirSync(inputDir)
  .filter(file => file.endsWith('.html') && file !== 'index.html')
  .map(file => {
    const content = fs.readFileSync(path.join(inputDir, file), 'utf-8');
    const titleMatch = content.match(/<title>(.*)<\/title>/);
    return {
      file: file,
      title: titleMatch ? titleMatch[1] : file
    };
  });

// Sort to have newest first, date assignment
// Assign dates: newest = today, oldest = 50 weeks ago
const now = new Date();
const postsWithDates = files.map((post, index) => {
  const date = new Date(now.getTime() - index * 7 * 24 * 60 * 60 * 1000);
  return { ...post, date: date.toISOString().split('T')[0] };
});

// HTML Generation
const html = `<!DOCTYPE html>
<html lang="es-419">
<head>
  <meta charset="UTF-8">
  <title>FaucetGuru Blog</title>
  <style>
    body { background-color: #000; color: #fff; font-family: 'Open Sans', sans-serif; padding: 20px; }
    h1 { font-family: 'Lora', serif; color: #ff7357; }
    .post-entry { margin-bottom: 15px; }
    .date { color: #ccc; font-size: 0.9em; margin-right: 10px; }
    a { color: #ff7357; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>FaucetGuru Blog</h1>
  <div class="posts">
    ${postsWithDates.map(p => `
      <div class="post-entry">
        <span class="date">${p.date}</span>
        <a href="${p.file}">${p.title}</a>
      </div>
    `).join('')}
  </div>
</body>
</html>`;

fs.writeFileSync(outputFilePath, html);
console.log(`Generated ${outputFilePath}`);
