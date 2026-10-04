import os
import glob
import json
import re
from bs4 import BeautifulSoup
from collections import defaultdict

def extract_keywords(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    stop_words = {'what', 'is', 'the', 'of', 'and', 'a', 'to', 'in', 'how', 'discuss', 'explain', 'with', 'example', 'between', 'difference', 'write', 'for', 'are', 'on', 'give', 'briefly', 'types', 'various'}
    return set([w for w in text.split() if w not in stop_words and len(w) > 2])

report_missing = {}

for json_file in glob.glob('data/*/*_questions.json'):
    subject = json_file.split(os.sep)[1]
    
    html_file = f"subjects/{subject}/comprehensive-report.html"
    if not os.path.exists(html_file): continue
    
    with open(json_file, 'r', encoding='utf-8') as f:
        q_data = json.load(f)
        
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract topics and text from HTML per unit
    html_units = defaultdict(str)
    for unit_div in soup.find_all('div', class_='unit-section'):
        h3 = unit_div.find(['h3', 'h2'])
        if not h3: continue
        unit_title = h3.get_text()
        # Find which unit it is (I, II, III, IV, V)
        match = re.search(r'Unit (I{1,3}|IV|V)', unit_title, re.IGNORECASE)
        if match:
            u_num = match.group(1).upper()
            html_units[u_num] += unit_div.get_text(separator=' ')
            
    # Check questions
    missing = []
    for q in q_data:
        u = q.get('unit')
        title = q.get('title', '')
        q_keywords = extract_keywords(title)
        
        if u in html_units:
            html_text = html_units[u].lower()
            # Check how many keywords are in the HTML text
            found = 0
            for kw in q_keywords:
                if kw in html_text:
                    found += 1
                    
            if len(q_keywords) > 0:
                coverage = found / len(q_keywords)
                if coverage < 0.3: # Less than 30% keywords found
                    missing.append(title)
        else:
            missing.append(f"[Unit {u} entirely missing] {title}")
            
    if missing:
        report_missing[subject] = missing

for sub, misses in report_missing.items():
    print(f"--- {sub.upper()} ---")
    print(f"Total flagged: {len(misses)}")
    for m in misses[:5]:
        print(f" - {m}")
    if len(misses) > 5:
        print(f"   ...and {len(misses)-5} more.")
