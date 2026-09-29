const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/os/os_questions.json', 'utf8'));
const important = data.filter(q => q.important);
const content = fs.readFileSync('subjects/os/cheat-sheet.html', 'utf8');
const missing = important.filter(q => !content.includes(q.title.substring(0, 20)));

let html = '<div class="cheat-card">\n  <h2>Applied Examples &amp; Important Concepts</h2>\n';
missing.forEach(q => {
  html += `  <div class="concept-block">\n    <h3>${q.title}</h3>\n    ${q.answer_html}\n  </div>\n`;
});
html += '</div>\n';

const scriptIndex = content.lastIndexOf('<script');
const beforeScript = content.substring(0, scriptIndex);
const afterScript = content.substring(scriptIndex);

const finalContent = beforeScript + html + afterScript;
fs.writeFileSync('C:/Users/nihal/.gemini/antigravity/brain/855a76bf-d666-4067-81a1-95f8f5163051/scratch/new_sheet.html', finalContent);
