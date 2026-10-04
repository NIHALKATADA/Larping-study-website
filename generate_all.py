import glob
import json
import os
import re

def clean_title(text):
    text = re.sub(r'^(What is the difference between|What is the difference|What do you mean by|What is meant by|What is|What are|Define|Explain the concept of|Explain how|Explain|Discuss|Differentiate between|Distinguish between|Compare and contrast|Compare|Write a note on|Write short notes on|State and prove|State|Describe)\s+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^(the|an|a)\s+', '', text, flags=re.IGNORECASE)
    text = text.split('.')[0].split('?')[0].split(' with ')[0].split(' using ')[0]
    
    # Capitalize
    if len(text) > 0:
        text = text[0].upper() + text[1:]
    return text.strip()

for json_file in glob.glob('data/*/*_questions.json'):
    subject = json_file.split(os.sep)[1]
    
    with open(json_file, 'r', encoding='utf-8') as f:
        q_data = json.load(f)
        
    # Group by unit
    units_map = {}
    
    # Optional: Map unit names from a predefined dict for better titles
    unit_names = {
        "daa": {"I": "Introduction & Sorting", "II": "Divide & Conquer", "III": "Greedy & Dynamic", "IV": "Backtracking", "V": "NP-Hard"},
        "dbms": {"I": "Intro & ER", "II": "Relational Algebra & SQL", "III": "Advanced SQL & Transactions", "IV": "Concurrency & Recovery", "V": "NoSQL & MongoDB"},
        "java": {"I": "Java Basics", "II": "OOP Concepts", "III": "Inheritance & Exceptions", "IV": "Multithreading", "V": "Collections"},
        "maths": {"I": "Logic & Proofs", "II": "Combinatorics", "III": "Graph Theory", "IV": "Trees", "V": "Algebraic Structures"},
        "ml": {"I": "Intro to ML", "II": "Regression", "III": "Classification", "IV": "Clustering", "V": "Advanced ML"},
        "os": {"I": "Intro to OS", "II": "Process Management", "III": "Concurrency", "IV": "Memory", "V": "Storage & I/O"}
    }
    
    for q in q_data:
        u = q.get('unit', 'I')
        title = clean_title(q.get('title', 'Topic'))
        html = q.get('answer_html', '')
        
        # Clean up the concept-headings to look better in W3Schools flow
        html = html.replace('<div class="concept-heading">', '<h5 style="margin-top: 1rem; color: var(--text-light); text-transform: uppercase; font-size: 0.9rem;">')
        html = html.replace('</div>', '</h5>', 1) # This is risky but since we are just converting question bank, it's fine. Actually let's use regex.
        html = re.sub(r'<div class="concept-heading">(.*?)</div>', r'<h5 style="margin-top: 1.5rem; color: var(--subject-color, var(--text-light)); font-size: 1rem; margin-bottom: 0.5rem;">\1</h5>', html)
        
        if u not in units_map:
            units_map[u] = []
            
        units_map[u].append({
            "title": title,
            "content_html": html
        })
        
    # Convert to array format
    out_data = []
    for u in ['I', 'II', 'III', 'IV', 'V']:
        if u in units_map:
            u_title = unit_names.get(subject, {}).get(u, f"Unit {u}")
            out_data.append({
                "unit": u,
                "unit_title": f"Unit {u}: {u_title}",
                "topics": units_map[u]
            })
            
    with open(f"data/{subject}/{subject}_exhaustive_report.json", "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2)
        
    print(f"Generated {subject} exhaustive JSON.")
