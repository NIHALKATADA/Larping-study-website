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
    
    # 1. Determine JSON source
    out_data = None
    if subject == "ml" and os.path.exists(f"data/ml/ml_condensed_report.json"):
        with open(f"data/ml/ml_condensed_report.json", 'r', encoding='utf-8') as f:
            out_data = json.load(f)
    elif os.path.exists(f"data/{subject}/{subject}_exhaustive_report.json"):
        with open(f"data/{subject}/{subject}_exhaustive_report.json", 'r', encoding='utf-8') as f:
            out_data = json.load(f)
    elif os.path.exists(f"data/{subject}/{subject}_questions.json"):
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
        print(f"No data for {subject}")
        continue
        
    # 2. Modify HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    sidebar = soup.find('aside', class_='report-sidebar')
    if sidebar:
        old_ul = sidebar.find('ul', class_='toc-list')
        if old_ul: old_ul.decompose()
        
        toc_ul = soup.new_tag('ul', attrs={'class': 'toc-list'})
        sidebar.append(toc_ul)
        sidebar_ul = toc_ul
    else:
        sidebar_ul = soup.new_tag('ul')
        
    main_content = soup.find('main', class_='report-main')
    if not main_content: continue
    
    # Remove old units
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
                trans_div['style'] = "font-style: italic; color: var(--text-light); margin: 1rem 0 2.5rem 1rem; border-left: 2px solid var(--text-light); padding-left: 1rem; font-size: 1.05rem;"
                trans_div.append(BeautifulSoup(trans_text, 'html.parser'))
                unit_div.append(trans_div)
                
        main_content.append(unit_div)
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Rebuilt {subject} successfully.")


