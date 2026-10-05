import json
import re
from bs4 import BeautifulSoup

def process_html(html_content, topic_title):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text from the first paragraph or div
    first_p = soup.find('p')
    text = ""
    if first_p:
        text = first_p.get_text(separator=' ')
    else:
        text = soup.get_text(separator=' ')
        
    # Heuristic: Find sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    definition = ""
    if sentences:
        definition = sentences[0].replace('<strong>', '').replace('</strong>', '').strip()
        if definition.startswith(topic_title):
             pass
    
    # Remove strong/b tags from definition text
    definition = re.sub(r'<[^>]+>', '', definition)
    
    sub_concepts = []
    
    # Check if there is a ul
    ul = soup.find('ul')
    if ul:
        for li in ul.find_all('li'):
            b_tag = li.find(['b', 'strong'])
            if b_tag:
                title = b_tag.get_text(strip=True).strip(':')
                # Remove the title from li text
                b_tag.extract()
                desc = li.get_text(separator=' ').strip().strip(':').strip()
                sub_concepts.append((title, desc))
            else:
                sub_concepts.append(("Concept", li.get_text(separator=' ').strip()))
    else:
        # If no ul, use remaining sentences
        for sent in sentences[1:]:
            sent = sent.strip()
            if not sent: continue
            # Try to guess a sub-concept title (first 2-3 words)
            words = sent.split()
            if len(words) > 2:
                title = " ".join(words[:2]).title()
            else:
                title = "Detail"
            sub_concepts.append((title, sent))
            
    # Format
    out = f'<p><strong>Definition:</strong> {definition}</p>\n<ul class="revision-list">\n'
    for title, desc in sub_concepts:
        out += f'<li><strong>{title}:</strong> {desc}</li>\n'
    out += '</ul>'
    return out

with open(r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\ml_exhaustive_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for unit in data:
    for topic in unit.get("topics", []):
        topic["content_html"] = process_html(topic["content_html"], topic.get("title", ""))
        
with open(r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\ml_perfect_report.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done")
