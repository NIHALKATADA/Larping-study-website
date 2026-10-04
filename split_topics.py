import json
import re
from bs4 import BeautifulSoup

with open('data/dbms/dbms_exhaustive_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for unit in data:
    new_topics = []
    for topic in unit['topics']:
        html = topic['content_html']
        
        # Split on <h3>
        parts = re.split(r'<h3>(.*?)</h3>', html)
        
        # The first part is the original topic
        first_content = parts[0].strip()
        if first_content:
            new_topics.append({
                "title": topic['title'],
                "content_html": first_content
            })
            
        # The rest come in pairs: title, content
        for i in range(1, len(parts), 2):
            sub_title = parts[i].strip()
            sub_content = parts[i+1].strip() if i+1 < len(parts) else ""
            if sub_content:
                new_topics.append({
                    "title": sub_title,
                    "content_html": sub_content
                })
                
    unit['topics'] = new_topics

with open('data/dbms/dbms_exhaustive_report.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print("Split internal h3 tags into top-level topics.")
