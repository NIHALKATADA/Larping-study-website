import json
from bs4 import BeautifulSoup
import re

def get_keywords(text):
    stop = {'of', 'and', 'the', 'to', 'in', 'is', 'a', 'system', 'systems'}
    words = re.findall(r'\b\w+\b', text.lower())
    return set(w for w in words if w not in stop)

with open('data/os/os_questions.json', 'r', encoding='utf-8') as f:
    q_data = json.load(f)

with open('subjects/os/comprehensive-report.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for card in soup.find_all('div', class_='article-card'):
    h4 = card.find('h4')
    if not h4: continue
    
    title = h4.get_text(strip=True)
    title_kw = get_keywords(title)
    
    best_match = None
    best_score = 0
    
    for q in q_data:
        q_title = q['title']
        q_kw = get_keywords(q_title)
        
        # Calculate intersection
        score = len(title_kw.intersection(q_kw))
        if score > best_score:
            best_score = score
            best_match = q
            
    if best_match and best_score >= len(title_kw) * 0.5:
        print(f"Match: '{title}' => '{best_match['title']}' (Score: {best_score})")
    else:
        print(f"NO MATCH: '{title}'")
