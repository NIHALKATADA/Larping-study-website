import json
with open('data/daa/daa_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
important = [q for q in data if q.get('important')]
out = '\n<h3 style=\"margin-top: 3rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;\">Applied Examples &amp; Important Concepts <span class=\"badge unit-1\">Review</span></h3>\n<div class=\"cheat-grid\">\n'
for q in important:
    title = q['title']
    ans = q['answer_html']
    out += '    <div class=\"cheat-card\">\n        <h4>' + title + '</h4>\n        <div style=\"margin-top: 10px; font-size: 0.95rem; color: #ccc;\">\n            ' + ans + '\n        </div>\n    </div>\n'
out += '</div>\n'
with open('payload.html', 'w', encoding='utf-8') as f:
    f.write(out)
