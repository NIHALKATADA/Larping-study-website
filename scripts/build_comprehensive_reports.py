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
    text = re.sub(r'ER Diagram$', ' (ER Diagram)', text)
    text = re.sub(r'Applied Concept$', ' (Applied Concept)', text)
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
    "dbms": {"I": "Intro & ER", "II": "Relational Algebra & SQL", "III": "Advanced SQL & Transactions", "IV": "Concurrency & Recovery", "V": "NoSQL & MongoDB"},
    "java": {"I": "Java Basics", "II": "OOP Concepts", "III": "Inheritance & Exceptions", "IV": "Multithreading", "V": "Collections"},
    "maths": {"I": "Logic & Proofs", "II": "Combinatorics", "III": "Graph Theory", "IV": "Trees", "V": "Algebraic Structures"},
    "ml": {"I": "Intro to ML", "II": "Regression", "III": "Classification", "IV": "Clustering", "V": "Advanced ML"},
    "os": {"I": "Intro to OS", "II": "Process Management", "III": "Concurrency", "IV": "Memory", "V": "Storage & I/O"}
}

for json_file in glob.glob('data/*/*_questions.json'):
    subject = json_file.split(os.sep)[1]
    
    with open(json_file, 'r', encoding='utf-8') as f:
        q_data = json.load(f)
        
    units_map = {}
    for q in q_data:
        u = q.get('unit', 'I')
        title = clean_title(q.get('title', 'Topic'))
        html = q.get('answer_html', '')
        
        # Clean concept-headings to adapt to W3Schools flow
        html = re.sub(r'<div class="concept-heading">(.*?)</div>', r'<h5 style="margin-top: 1.5rem; color: var(--subject-color, var(--text-light)); font-size: 1rem; margin-bottom: 0.5rem;">\1</h5>', html)
        
        if u not in units_map: units_map[u] = []
        units_map[u].append({"title": title, "content_html": html})
        
    out_data = []
    for u in ['I', 'II', 'III', 'IV', 'V']:
        if u in units_map:
            u_title = unit_names.get(subject, {}).get(u, f"Unit {u}")
            
            # Special override for DBMS Unit I manual depth
            if subject == 'dbms' and u == 'I':
                out_data.append({
                    "unit": "I",
                    "unit_title": "Unit I: Intro & ER",
                    "topics": [
                        {
                            "title": "Introduction to DBMS",
                            "content_html": "<p>A <strong>Database Management System (DBMS)</strong> is a powerful software system that allows users to create, maintain, and manage databases efficiently. It serves as a secure interface between the end-user and the raw data, ensuring that data is consistently organized and easily accessible.</p><p>Before the invention of DBMS, organizations relied on <strong>File-Based Systems</strong> where data was stored in flat files (like CSVs or text files). This older approach suffered from severe limitations, which modern DBMS architecture solves.</p>"
                        },
                        {
                            "title": "DBMS vs File System",
                            "content_html": "<p>The transition from file systems to DBMS was driven by the need to handle large, complex datasets securely. Here is a detailed comparison of the two approaches:</p><table border=\"1\"><tr><th>Feature</th><th>File-Processing System</th><th>Database Management System (DBMS)</th></tr><tr><td><strong>Data Redundancy</strong></td><td>High. The same data is often duplicated across multiple files, wasting storage.</td><td>Minimal. Data is centralized and normalized, eliminating unnecessary duplication.</td></tr><tr><td><strong>Data Inconsistency</strong></td><td>High. If data is updated in one file but not another, inconsistencies arise.</td><td>Low. Updates automatically propagate throughout the centralized database.</td></tr><tr><td><strong>Data Access</strong></td><td>Difficult. Requires writing custom application code for every new query.</td><td>Easy. Uses declarative query languages like SQL to retrieve data instantly.</td></tr><tr><td><strong>Data Independence</strong></td><td>None. Applications are tightly coupled to the physical structure of the file.</td><td>High. Applications are isolated from how the data is physically stored on disk.</td></tr><tr><td><strong>Concurrent Access</strong></td><td>Poor. Multiple users trying to edit a file simultaneously can corrupt it.</td><td>Excellent. Uses locks and transactions to allow safe simultaneous edits.</td></tr></table>"
                        },
                        {
                            "title": "Data Abstraction (3-Schema Architecture)",
                            "content_html": "<p>One of the primary advantages of a DBMS is <strong>Data Abstraction</strong>. Databases are incredibly complex internally, involving trees, hash tables, and pointers. However, end-users do not need to understand this complexity to use the database.</p><p>To achieve this, the ANSI-SPARC architecture divides the database into three levels of abstraction:</p><ul><li><strong>Physical Level (Internal Schema):</strong> The lowest level of abstraction. It describes exactly <em>how</em> the data is stored on the physical hardware (e.g., contiguous blocks, B+ trees). This level is managed by the Database Administrator (DBA).</li><li><strong>Logical Level (Conceptual Schema):</strong> The middle level. It describes <em>what</em> data is stored in the database and the relationships among that data. Programmers and developers operate at this level, viewing the data as tables and relationships without worrying about disk sectors.</li><li><strong>View Level (External Schema):</strong> The highest level. It describes only a specific portion of the database relevant to a particular user. For example, a university clerk might only have a view of the student names, while the payroll department has a view of the salary data. This hides unnecessary data and enforces security.</li></ul><div class=\"pro-tip\"><strong>Data Independence:</strong> This 3-schema architecture provides Data Independence. <strong>Logical Data Independence</strong> means you can change the logical schema (e.g., add a new column) without breaking the external views or applications. <strong>Physical Data Independence</strong> means you can change the physical storage (e.g., move data to a faster hard drive) without breaking the logical schema!</div>"
                        },
                        {
                            "title": "Schema and Instance",
                            "content_html": "<p>It is critical to understand the distinction between a database's structure and its data. These are formally known as the Schema and the Instance.</p><p>A <strong>Schema</strong> is the overall logical blueprint or structural design of the database. It defines the tables, the columns, the data types, and the constraints (like Primary Keys). A schema is established when the database is first created and changes very rarely. Think of the schema as the architectural blueprint of a house.</p><p>An <strong>Instance</strong> (or State) is the actual collection of data stored in the database at a specific moment in time. Every time you insert a new row, update a value, or delete a record, the instance changes. While the schema is static, the instance is highly dynamic. Think of the instance as the furniture and people currently inside the house.</p>"
                        }
                    ] + [t for t in units_map[u] if "DBMS vs File System" not in t["title"] and "Introduction to DBMS" not in t["title"] and "Schema and Instance" not in t["title"] and "Data Abstraction" not in t["title"]]
                })
            else:
                out_data.append({"unit": u, "unit_title": f"Unit {u}: {u_title}", "topics": units_map[u]})
                
    # Build the HTML
    html_file = f"subjects/{subject}/comprehensive-report.html"
    if not os.path.exists(html_file): continue
    with open(html_file, 'r', encoding='utf-8') as f: soup = BeautifulSoup(f.read(), 'html.parser')
    sidebar_ul = soup.find('aside', class_='report-sidebar').find('ul')
    main_content = soup.find('main', class_='report-main')
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
                trans_div['style'] = "font-style: italic; color: var(--text-light); margin: 1rem 0 2.5rem 1rem; border-left: 2px solid var(--text-light); padding-left: 1rem; font-size: 1.05rem;"
                trans_div.append(BeautifulSoup(trans_text, 'html.parser'))
                unit_div.append(trans_div)
                
        main_content.append(unit_div)
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Rebuilt {subject}.")
