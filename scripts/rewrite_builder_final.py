import glob
import json
import os
import re
import random
from bs4 import BeautifulSoup

def clean_title(text):
    text = re.sub(r'^(What is the difference between|What is the difference|What do you mean by|What is meant by|What is|What are|Define|Explain the concept of|Explain how|Explain|Discuss|Differentiate between|Distinguish between|Compare and contrast|Compare|Write a note on|Write short notes on|State and prove|State|Describe)\s+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^(the|an|a)\s+', '', text, flags=re.IGNORECASE)
    text = text.split('.')[0].split('?')[0].split(' with ')[0].split(' using ')[0]
    if len(text) > 0: text = text[0].upper() + text[1:]
    return text.strip()

def clean_text_for_sidebar(text):
    text = re.sub(r'CO\d$', '', text)
    text = re.sub(r'U\d$', '', text)
    if len(text) > 40: text = text[:37] + "..."
    return text.strip()

for subject in ["daa", "dbms", "java", "maths", "ml", "os"]:
    html_file = f"{subject}/comprehensive-report.html"
    if not os.path.exists(html_file):
        continue
        
    print(f"Building {subject}...")
    
    out_data = None
    is_perfect = False
    
    if os.path.exists(f"data/{subject}/{subject}_dedup_report.json"):
        print(f"  Using DEDUP report for {subject}")
        with open(f"data/{subject}/{subject}_dedup_report.json", "r", encoding="utf-8") as f:
            out_data = json.load(f)
            is_perfect = True
    elif os.path.exists(f"data/{subject}/{subject}_perfect_report.json"):
        print(f"  Using PERFECT report for {subject}")
        with open(f"data/{subject}/{subject}_perfect_report.json", "r", encoding="utf-8") as f:
            out_data = json.load(f)
            is_perfect = True
    elif os.path.exists(f"data/{subject}/{subject}_exhaustive_report.json"):
        print(f"  Using EXHAUSTIVE report for {subject}")
        with open(f"data/{subject}/{subject}_exhaustive_report.json", "r", encoding="utf-8") as f:
            out_data = json.load(f)
    else:
        continue
        
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    sidebar = soup.find('aside', class_='report-sidebar')
    if sidebar:
        for old in sidebar.find_all('ul'):
            old.decompose()
        toc_ul = soup.new_tag('ul', attrs={'class': 'toc-list'})
        sidebar.append(toc_ul)
        sidebar_ul = toc_ul
    else:
        sidebar_ul = soup.new_tag('ul')
        
    main_content = soup.find('main', class_='report-main')
    if not main_content: continue
    
    for el in main_content.find_all('div', class_='unit-section'):
        el.decompose()
        
    for unit_obj in out_data:
        u_num = unit_obj.get('unit', 'I')
        u_title = unit_obj.get('unit_title', f"Unit {u_num}")
        topics = unit_obj.get('topics', [])
        
        unit_li = soup.new_tag('li', attrs={'class': 'unit-link'})
        unit_a = soup.new_tag('a', href=f"#unit_{u_num}")
        unit_a.string = u_title
        unit_li.append(unit_a)
        sidebar_ul.append(unit_li)
        
        unit_div = soup.new_tag('div', attrs={'class': 'unit-section'})
        unit_h3 = soup.new_tag('h3', id=f"unit_{u_num}", attrs={'class': 'unit-heading'})
        unit_h3.string = u_title
        unit_div.append(unit_h3)
        
        for t_idx, topic in enumerate(topics):
            t_title = topic.get('title', 'Topic')
            t_id = f"sub_{u_num}_{t_idx}"
            
            sub_li = soup.new_tag('li', attrs={'class': 'sub-link'})
            sub_a = soup.new_tag('a', href=f"#{t_id}")
            sub_a.string = clean_text_for_sidebar(t_title)
            sub_li.append(sub_a)
            sidebar_ul.append(sub_li)
            
            if is_perfect:
                card_div = soup.new_tag('div', attrs={'class': 'article-card', 'id': t_id, 'style': 'margin-bottom: 1.5rem; background: var(--card-bg, rgba(255,255,255,0.03)); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1.5rem;'})
                card_h4 = soup.new_tag('h4', attrs={'style': 'margin-top: 0; color: var(--subject-color, var(--primary-teal)); font-size: 1.25rem; margin-bottom: 1rem;'})
                card_h4.string = t_title
                content_div = soup.new_tag('div')
                content_div.append(BeautifulSoup(topic.get('content_html', ''), 'html.parser'))
                card_div.append(card_h4)
                card_div.append(content_div)
            else:
                card_div = soup.new_tag('div', attrs={'class': 'article-card', 'style': 'margin-bottom: 1rem; padding: 0; background: transparent; border: none; box-shadow: none;'})
                details = soup.new_tag('details', id=t_id, attrs={'style': 'background: var(--card-bg, rgba(255,255,255,0.03)); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 0.5rem 1rem; transition: all 0.3s ease;'})
                summary = soup.new_tag('summary', attrs={'style': 'font-size: 1.15rem; font-weight: 600; cursor: pointer; padding: 0.5rem 0; outline: none; list-style-position: inside;'})
                summary.string = t_title
                content_div = soup.new_tag('div', attrs={'style': 'padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 0.5rem;'})
                content_div.append(BeautifulSoup(topic.get('content_html', ''), 'html.parser'))
                details.append(summary)
                details.append(content_div)
                card_div.append(details)
                
            unit_div.append(card_div)
                
        main_content.append(unit_div)
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Rebuilt {subject} successfully.")
