import json

with open('data/daa/daa_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
important = [q for q in data if q.get('important')]

for q in important:
    if q['id'] == 'q27':
        mermaid_merge = '''
<div class="compact-svg" style="margin-top: 15px; margin-bottom: 15px;">
  <div class="mermaid">
    flowchart TD
      A("[38, 27, 43, 3, 9, 82, 10, 15, 21, 6]") --> B("[38, 27, 43, 3, 9]")
      A --> C("[82, 10, 15, 21, 6]")
      B --> D("[38, 27, 43]")
      B --> E("[3, 9]")
      C --> F("[82, 10, 15]")
      C --> G("[21, 6]")
      D --> H("[38, 27]")
      D --> I("[43]")
      F --> Q("[82, 10]")
      F --> R("[15]")
      G --> V("[21]")
      G --> W("[6]")
  </div>
</div>
'''
        q['answer_html'] = q['answer_html'] + mermaid_merge
        
    if q['id'] == 'q19': # Binary Search
        mermaid_bs = '''
<div class="compact-svg" style="margin-top: 15px; margin-bottom: 15px;">
  <div class="mermaid">
    flowchart LR
      S1("low=0, high=10, mid=5<br>arr[5]=37 < 45") --> S2("low=6, high=10, mid=8<br>arr[8]=64 > 45")
      S2 --> S3("low=6, high=7, mid=6<br>arr[6]=45 == 45")
      S3 --> Found("Found at index 6")
  </div>
</div>
'''
        q['answer_html'] = q['answer_html'] + mermaid_bs

out = '\n<div style=\"grid-column: 1 / -1; margin-top: 2rem;\"><h2 style=\"border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;\">Applied Examples &amp; Important Concepts</h2></div>\n'

for q in important:
    title = q['title']
    ans = q['answer_html']
    out += '    <div class=\"cheat-card\">\n        <h4>' + title + '</h4>\n        <div style=\"margin-top: 10px; font-size: 0.9rem;\">\n            ' + ans + '\n        </div>\n    </div>\n'

with open('payload.html', 'w', encoding='utf-8') as f:
    f.write(out)
