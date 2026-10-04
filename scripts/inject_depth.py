import json
import glob
import re
from bs4 import BeautifulSoup

def get_keywords(text):
    stop = {'of', 'and', 'the', 'to', 'in', 'is', 'a', 'system', 'systems', 'what', 'define', 'explain'}
    words = re.findall(r'\b\w+\b', text.lower())
    return set(w for w in words if w not in stop)

with open('title_map.json', 'r', encoding='utf-8') as f:
    title_map = json.load(f)

roman_map = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V'}

for html_file in glob.glob('subjects/*/comprehensive-report.html'):
    subject = html_file.split('\\')[1] if '\\' in html_file else html_file.split('/')[1]
    
    with open(f'data/{subject}/{subject}_questions.json', 'r', encoding='utf-8') as f:
        q_data = json.load(f)
        
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    used_questions = set()
    upgraded = 0
    appended = 0
        
    # Upgrade existing topics
    for card in soup.find_all('div', class_='article-card'):
        h4 = card.find('h4')
        if not h4: continue
        
        title = h4.get_text(strip=True)
        if subject == 'dbms' and title in ['Introduction to DBMS', 'DBMS vs File System', 'Data Abstraction (3-Schema Architecture)', 'Schema and Instance']:
            continue
            
        title_kw = get_keywords(title)
        
        best_match = None
        best_score = 0
        
        for q in q_data:
            q_title = q['title']
            q_kw = get_keywords(q_title)
            score = len(title_kw.intersection(q_kw))
            if score > best_score:
                best_score = score
                best_match = q
                
        # Relaxed matching
        if best_match and best_score >= max(1, len(title_kw) * 0.3):
            used_questions.add(best_match['id'])
            
            elements_to_keep = []
            for child in card.children:
                if getattr(child, 'name', None) in ['h4', 'svg']:
                    elements_to_keep.append(child)
                    
            card.clear()
            for el in elements_to_keep:
                card.append(el)
                
            rich_html = best_match['answer_html']
            rich_html = re.sub(r'<div class="concept-heading">(.*?)</div>', r'<h5 style="margin-top: 1.5rem; color: var(--subject-color, var(--text-light)); font-size: 1rem; margin-bottom: 0.5rem;">\1</h5>', rich_html)
            card.append(BeautifulSoup(rich_html, 'html.parser'))
            upgraded += 1
            
    # Add missing topics
    units = soup.find_all('div', class_='unit-section')
    for unit in units:
        unit_id = unit.get('id', '')
        u_num_arabic = unit_id.replace('unit', '')
        u_num_roman = roman_map.get(u_num_arabic, u_num_arabic)
        
        missing_qs = [q for q in q_data if q.get('unit') == u_num_roman and q['id'] not in used_questions]
        
        for q in missing_qs:
            used_questions.add(q['id'])
            short_title = title_map.get(q['title'], q['title'])
            if len(short_title) > 60: short_title = short_title[:57] + '...'
            
            card_div = soup.new_tag('div', attrs={'class': 'article-card', 'style': 'margin-top: 2rem; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 2rem;'})
            card_h4 = soup.new_tag('h4')
            card_h4.string = short_title
            card_div.append(card_h4)
            
            rich_html = q['answer_html']
            rich_html = re.sub(r'<div class="concept-heading">(.*?)</div>', r'<h5 style="margin-top: 1.5rem; color: var(--subject-color, var(--text-light)); font-size: 1rem; margin-bottom: 0.5rem;">\1</h5>', rich_html)
            card_div.append(BeautifulSoup(rich_html, 'html.parser'))
            
            unit.append(card_div)
            appended += 1
            
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"{subject}: Upgraded {upgraded} existing cards, Appended {appended} missing concepts. Total coverage: {len(used_questions)}/{len(q_data)}")
