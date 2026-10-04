import glob
import json
import os
import re
import random
from bs4 import BeautifulSoup

with open('title_map.json', 'r', encoding='utf-8') as f:
    title_map = json.load(f)

def clean_text_for_sidebar(text):
    text = re.sub(r'CO\d$', '', text)
    text = re.sub(r'U\d$', '', text)
    
    return text.strip()

transitions = [
    "Having established the core principles of {prev}, we now turn our attention to {next}.",
    "Building on our understanding of {prev}, let's dive into {next}.",
    "Now that we have a solid grasp of {prev}, the natural next step is to explore {next}.",
    "With {prev} in mind, we can see why {next} becomes crucial in this context.",
    "Transitioning from {prev}, we now examine {next}, which builds upon these foundational rules.",
    "While {prev} gives us the theoretical background, {next} provides the next layer of complexity.",
    "To fully appreciate {next}, we must apply what we just learned about {prev}.",
    "Moving forward from {prev}, let's break down the mechanics of {next}."
]

unit_names = {
    "daa": {"I": "Introduction & Sorting", "II": "Divide & Conquer", "III": "Dynamic Programming", "IV": "Advanced Graph Algorithms", "V": "NP-Completeness"},
    "dbms": {"I": "Introduction & ER Modeling", "II": "Relational Algebra & SQL", "III": "Advanced SQL & Transactions", "IV": "Concurrency Control", "V": "NoSQL & MongoDB"},
    "java": {"I": "Java Basics & OOP", "II": "Inheritance & Interfaces", "III": "Exception Handling", "IV": "Multithreading", "V": "Collections Framework"},
    "maths": {"I": "Logic & Proofs", "II": "Combinatorics", "III": "Graph Theory", "IV": "Trees & Algorithms", "V": "Algebraic Structures"},
    "ml": {"I": "Introduction to ML", "II": "Regression Models", "III": "Classification", "IV": "Clustering", "V": "Advanced Concepts"},
    "os": {"I": "Fundamentals & Bootstrapping", "II": "Process Management", "III": "Concurrency & Deadlocks", "IV": "Memory Management", "V": "Storage & I/O Systems"}
}

for json_file in glob.glob('data/*/*_questions.json'):
    subject = json_file.split(os.sep)[1]
    
    with open(json_file, 'r', encoding='utf-8') as f:
        q_data = json.load(f)
        
    units_map = {}
    for q in q_data:
        u = q.get('unit', 'I')
        original_title = q.get('title', 'Topic')
        title = title_map.get(original_title, original_title)
        
        # Manually fix specific long titles if map failed
        
            
        html = q.get('answer_html', '')
        html = re.sub(r'<div class="concept-heading">(.*?)</div>', r'<h5 style="margin-top: 1.5rem; color: var(--subject-color, var(--text-light)); font-size: 1rem; margin-bottom: 0.5rem;">\1</h5>', html)
        
        if u not in units_map: units_map[u] = []
        units_map[u].append({"title": title, "original_title": original_title, "content_html": html})
        
    out_data = []
    for u in ['I', 'II', 'III', 'IV', 'V']:
        if u in units_map:
            u_title = unit_names.get(subject, {}).get(u, f"Unit {u}")
            out_data.append({"unit": u, "unit_title": f"Unit {u}: {u_title}", "topics": units_map[u]})
                
    # Build the HTML
    html_file = f"subjects/{subject}/comprehensive-report.html"
    if not os.path.exists(html_file): continue
    
    # We don't use BeautifulSoup to parse the whole file because it destroys format and we have 2c36f73
    # Actually, using BeautifulSoup to replace sidebar and main is fine if we save it back.
    with open(html_file, 'r', encoding='utf-8') as f: 
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    sidebar_ul = soup.find('aside', class_='report-sidebar').find('ul')
    main_content = soup.find('div', id='realContentWrapper')
    
    # Remove the old Q&A section if it exists below main
    if main_content:
        for sibling in main_content.find_next_siblings():
            if sibling.name != 'script' and sibling.get('id') != 'assistantModal' and not (sibling.name == 'button' and 'fab-main' in sibling.get('class', [])):
                sibling.decompose()
            
    sidebar_ul.clear()
    main_content.clear()
    
    for u_idx, unit_data in enumerate(out_data):
        u_num = unit_data.get('unit', str(u_idx+1))
        u_title = unit_data.get('unit_title', f"Unit {u_num}")
        topics = unit_data.get('topics', [])
        
        unit_li = soup.new_tag('li', attrs={'class': 'unit-link'})
        unit_a = soup.new_tag('a', href=f"#unit{u_num}")
        unit_a.string = clean_text_for_sidebar(u_title)
        unit_li.append(unit_a)
        sidebar_ul.append(unit_li)
        
        unit_div = soup.new_tag('div', attrs={'class': 'unit-section', 'id': f"unit{u_num}"})
        unit_h3 = soup.new_tag('h3', attrs={'class': 'unit-heading'})
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
            
            card_div = soup.new_tag('div', attrs={'class': 'article-card'})
            card_h4 = soup.new_tag('h4', id=t_id)
            card_h4.string = t_title
            card_div.append(card_h4)
            card_div.append(BeautifulSoup(topic.get('content_html', ''), 'html.parser'))
            unit_div.append(card_div)
            
            if t_idx < len(topics) - 1:
                next_title = clean_text_for_sidebar(topics[t_idx+1].get('title', ''))
                curr_title = clean_text_for_sidebar(t_title)
                trans_text = random.choice(transitions).format(prev=f"<strong>{curr_title}</strong>", next=f"<strong>{next_title}</strong>")
                trans_div = soup.new_tag('div', attrs={'class': 'presenter-transition'})
                trans_div['style'] = "font-style: italic; color: var(--text-light); margin: 1rem 0 2.5rem 1rem; border-left: 2px solid rgba(255,255,255,0.1); padding-left: 1rem; font-size: 1.05rem;"
                trans_div.append(BeautifulSoup(trans_text, 'html.parser'))
                unit_div.append(trans_div)
                
        main_content.append(unit_div)
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Rebuilt {subject} perfectly.")


