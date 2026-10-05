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

unit_names = {
    "daa": {"I": "Introduction & Sorting", "II": "Divide & Conquer", "III": "Greedy & Dynamic", "IV": "Backtracking", "V": "NP-Hard"},
    "dbms": {"I": "Introduction, ER Modeling, and Normalization", "II": "Relational Algebra, SQL, and Query Processing", "III": "Advanced SQL and Transaction Management", "IV": "Concurrency Control and Recovery", "V": "NoSQL Databases and MongoDB"},
    "java": {"I": "Java Basics & Data Types", "II": "Object-Oriented Programming (OOP) Concepts", "III": "Inheritance, Interfaces, & Exception Handling", "IV": "Multithreading & Concurrency", "V": "Collections Framework & Generics"},
    "maths": {"I": "Logic, Propositions, & Proofs", "II": "Combinatorics & Counting Principles", "III": "Graph Theory Fundamentals", "IV": "Trees & Graph Algorithms", "V": "Algebraic Structures & Group Theory"},
    "ml": {"I": "Introduction to Machine Learning", "II": "Regression Models & Cost Functions", "III": "Classification Algorithms", "IV": "Clustering & Unsupervised Learning", "V": "Advanced Machine Learning Concepts"},
    "os": {"I": "Fundamentals & Bootstrapping", "II": "Process Management & Threads", "III": "Concurrency & Deadlocks", "IV": "Memory Management", "V": "Storage & I/O Systems"}
}

for subject in ["daa", "dbms", "java", "maths", "ml", "os"]:
    html_file = f"{subject}/comprehensive-report.html"
    if not os.path.exists(html_file):
        continue
        
    print(f"Building {subject}...")
    
    # Use Exhaustive Report to get full depth back, or Questions as fallback
    out_data = None
    if os.path.exists(f"data/{subject}/{subject}_perfect_report.json"):\n        print(f"  Using PERFECT report for {subject}")\n        with open(f"data/{subject}/{subject}_perfect_report.json", "r", encoding="utf-8") as f:\n            out_data = json.load(f)\n    elif os.path.exists(f"data/{subject}/{subject}_exhaustive_report.json"):
        print(f"  Using exhaustive report for {subject}")
        with open(f"data/{subject}/{subject}_exhaustive_report.json", 'r', encoding='utf-8') as f:
            out_data = json.load(f)
    elif os.path.exists(f"data/{subject}/{subject}_questions.json"):
        print(f"  Using questions report for {subject}")
        with open(f"data/{subject}/{subject}_questions.json", 'r', encoding='utf-8') as f:
            q_data = json.load(f)
            units_map = {}
            for q in q_data:
                u = q.get('unit', 'I')
                title = clean_title(q.get('title', 'Topic'))
                html = q.get('answer_html', '')
                html = re.sub(r'<div class="concept-heading">(.*?)</div>', r'<h5 style="margin-top: 1.5rem; color: var(--subject-color, var(--text-light)); font-size: 1rem; margin-bottom: 0.5rem;">\1</h5>', html)
                if u not in units_map: units_map[u] = []
                units_map[u].append({"title": title, "content_html": html})
            
            out_data = []
            for u in ['I', 'II', 'III', 'IV', 'V']:
                if u in units_map:
                    u_title = unit_names.get(subject, {}).get(u, f"Unit {u}")
                    out_data.append({
                        "unit": u,
                        "unit_title": f"Unit {u}: {u_title}",
                        "topics": units_map[u]
                    })
    
    if not out_data:
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
        
    # Inject JS to open details on hash change
    js_script = """
    <script>
    document.addEventListener('DOMContentLoaded', () => {
        const openHashDetails = () => {
            if(window.location.hash) {
                const targetId = window.location.hash.substring(1);
                const el = document.getElementById(targetId);
                if(el && el.tagName === 'DETAILS') {
                    el.open = true;
                    setTimeout(() => el.scrollIntoView({behavior: 'smooth', block: 'start'}), 100);
                }
            }
        };
        window.addEventListener('hashchange', openHashDetails);
        openHashDetails();
    });
    </script>
    """
    if 'openHashDetails' not in html_content:
        main_content.append(BeautifulSoup(js_script, 'html.parser'))
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Rebuilt {subject} successfully with accordion.")


