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

def extract_keywords(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    stop_words = {'what', 'is', 'the', 'of', 'and', 'a', 'to', 'in', 'how', 'discuss', 'explain', 'with', 'example', 'between', 'difference', 'write', 'for', 'are', 'on', 'give', 'briefly', 'types', 'various'}
    return set([w for w in text.split() if w not in stop_words and len(w) > 2])

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

for json_file in glob.glob('data/*/*_questions.json'):
    subject = json_file.split(os.sep)[1]
    
    html_file = f"subjects/{subject}/comprehensive-report.html"
    if not os.path.exists(html_file): continue
    
    # 1. Load HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    # Force data-theme="dark" just in case
    if soup.find('html'): soup.find('html')['data-theme'] = 'dark'
    
    # 2. Fix specific DBMS topics with deep content
    if subject == 'dbms':
        intro_card = soup.find(lambda tag: tag.name == 'h4' and 'Architecture' in tag.text)
        if intro_card:
            intro_card = intro_card.parent
            # Replace the entire card content with the massive depth content
            intro_card.clear()
            intro_card.append(BeautifulSoup("""<h4 id="sub_I_0">Introduction to DBMS & Architecture</h4>
<p>A <strong>Database Management System (DBMS)</strong> is a powerful software system that allows users to create, maintain, and manage databases efficiently. It serves as a secure interface between the end-user and the raw data, ensuring that data is consistently organized and easily accessible.</p>
<p>Before the invention of DBMS, organizations relied on <strong>File-Based Systems</strong> where data was stored in flat files (like CSVs or text files). This older approach suffered from severe limitations.</p>

<h5 style="margin-top:2rem; font-size:1.2rem; color:var(--subject-color);">DBMS vs File System</h5>
<p>The transition from file systems to DBMS was driven by the need to handle large, complex datasets securely. Here is a detailed comparison of the two approaches:</p>
<table border="1">
    <tr>
        <th>Feature</th>
        <th>File-Processing System</th>
        <th>Database Management System (DBMS)</th>
    </tr>
    <tr>
        <td><strong>Data Redundancy</strong></td>
        <td>High. The same data is often duplicated across multiple files, wasting storage.</td>
        <td>Minimal. Data is centralized and normalized, eliminating unnecessary duplication.</td>
    </tr>
    <tr>
        <td><strong>Data Inconsistency</strong></td>
        <td>High. If data is updated in one file but not another, inconsistencies arise.</td>
        <td>Low. Updates automatically propagate throughout the centralized database.</td>
    </tr>
    <tr>
        <td><strong>Data Access</strong></td>
        <td>Difficult. Requires writing custom application code for every new query.</td>
        <td>Easy. Uses declarative query languages like SQL to retrieve data instantly.</td>
    </tr>
    <tr>
        <td><strong>Data Independence</strong></td>
        <td>None. Applications are tightly coupled to the physical structure of the file.</td>
        <td>High. Applications are isolated from how the data is physically stored on disk.</td>
    </tr>
    <tr>
        <td><strong>Concurrent Access</strong></td>
        <td>Poor. Multiple users trying to edit a file simultaneously can corrupt it.</td>
        <td>Excellent. Uses locks and transactions to allow safe simultaneous edits.</td>
    </tr>
</table>

<h5 style="margin-top:2rem; font-size:1.2rem; color:var(--subject-color);">Data Abstraction (3-Schema Architecture)</h5>
<p>One of the primary advantages of a DBMS is <strong>Data Abstraction</strong>. Databases are incredibly complex internally, involving trees, hash tables, and pointers. However, end-users do not need to understand this complexity to use the database.</p>
<p>To achieve this, the ANSI-SPARC architecture divides the database into three levels of abstraction:</p>
<ul>
    <li><strong>Physical Level (Internal Schema):</strong> The lowest level of abstraction. It describes exactly <em>how</em> the data is stored on the physical hardware.</li>
    <li><strong>Logical Level (Conceptual Schema):</strong> The middle level. It describes <em>what</em> data is stored in the database and the relationships among that data.</li>
    <li><strong>View Level (External Schema):</strong> The highest level. It describes only a specific portion of the database relevant to a particular user.</li>
</ul>
<div class="pro-tip"><strong>Data Independence:</strong> This 3-schema architecture provides Data Independence. Logical Data Independence means you can change the logical schema without breaking the external views. Physical Data Independence means you can change the physical storage without breaking the logical schema!</div>

<h5 style="margin-top:2rem; font-size:1.2rem; color:var(--subject-color);">Schema and Instance</h5>
<p>It is critical to understand the distinction between a database's structure and its data.</p>
<p>A <strong>Schema</strong> is the overall logical blueprint or structural design of the database. It defines the tables, the columns, the data types, and the constraints (like Primary Keys). A schema is established when the database is first created and changes very rarely. Think of the schema as the architectural blueprint of a house.</p>
<p>An <strong>Instance</strong> (or State) is the actual collection of data stored in the database at a specific moment in time. Every time you insert a new row, update a value, or delete a record, the instance changes. While the schema is static, the instance is highly dynamic. Think of the instance as the furniture and people currently inside the house.</p>
""", 'html.parser'))
            
    # 3. Inject Missing Questions
    with open(json_file, 'r', encoding='utf-8') as f:
        q_data = json.load(f)
        
    sidebar_ul = soup.find('aside', class_='report-sidebar').find('ul')
    if not sidebar_ul: continue
    
    # Track existing topics per unit to avoid duplicates
    html_units_text = {}
    unit_divs = soup.find_all('div', class_='unit-section')
    for udiv in unit_divs:
        # Extract unit number (I, II, etc)
        h3 = udiv.find(['h3', 'h2'])
        if h3:
            match = re.search(r'Unit (I{1,3}|IV|V)', h3.get_text(), re.IGNORECASE)
            if match:
                u_num = match.group(1).upper()
                html_units_text[u_num] = udiv.get_text(separator=' ').lower()
                
    appended_count = 0
    for q in q_data:
        u = q.get('unit')
        title = q.get('title', '')
        q_keywords = extract_keywords(title)
        
        if u in html_units_text and u in [match.group(1).upper() for match in re.finditer(r'Unit (I{1,3}|IV|V)', "".join([d.find(['h3','h2']).get_text() for d in unit_divs if d.find(['h3','h2'])]), re.IGNORECASE)]:
            html_text = html_units_text[u]
            found = sum(1 for kw in q_keywords if kw in html_text)
            coverage = found / len(q_keywords) if q_keywords else 1.0
            
            # If missing, inject it!
            if coverage < 0.35: # Needs to be added
                target_div = None
                for d in unit_divs:
                    h3 = d.find(['h3', 'h2'])
                    if h3 and re.search(r'Unit ' + u, h3.get_text(), re.IGNORECASE):
                        target_div = d
                        break
                        
                if target_div:
                    c_title = clean_title(title)
                    c_id = f"sub_added_{u}_{appended_count}"
                    
                    # Create the card
                    card = soup.new_tag('div', attrs={'class': 'article-card'})
                    card_h4 = soup.new_tag('h4', id=c_id)
                    card_h4.string = c_title
                    card.append(card_h4)
                    
                    ans_html = q.get('answer_html', '')
                    ans_html = re.sub(r'<div class="concept-heading">(.*?)</div>', r'<h5 style="margin-top: 1.5rem; color: var(--subject-color, var(--text-light)); font-size: 1rem; margin-bottom: 0.5rem;">\1</h5>', ans_html)
                    card.append(BeautifulSoup(ans_html, 'html.parser'))
                    
                    # Append it
                    target_div.append(card)
                    
                    # Append to sidebar under correct unit
                    # Find the unit link in sidebar
                    unit_link = None
                    for li in sidebar_ul.find_all('li', class_='unit-link'):
                        if re.search(r'Unit ' + u, li.get_text(), re.IGNORECASE):
                            unit_link = li
                            break
                            
                    if unit_link:
                        new_li = soup.new_tag('li', attrs={'class': 'sub-link'})
                        new_a = soup.new_tag('a', href=f"#{c_id}")
                        new_a.string = clean_text_for_sidebar(c_title)
                        new_li.append(new_a)
                        
                        # Insert after the last sub-link of this unit
                        next_sib = unit_link.find_next_sibling()
                        last_sub = unit_link
                        while next_sib and 'sub-link' in next_sib.get('class', []):
                            last_sub = next_sib
                            next_sib = next_sib.find_next_sibling()
                        last_sub.insert_after(new_li)
                        
                    appended_count += 1
                    
    # 4. Re-run Presenter Transitions
    for t in soup.find_all('div', class_='presenter-transition'):
        t.decompose() # Remove old ones
        
    for udiv in unit_divs:
        cards = udiv.find_all('div', class_='article-card')
        for i in range(len(cards) - 1):
            prev_card = cards[i]
            next_card = cards[i+1]
            prev_h4 = prev_card.find('h4')
            next_h4 = next_card.find('h4')
            if prev_h4 and next_h4:
                prev_title = clean_text_for_sidebar(prev_h4.get_text(strip=True))
                next_title = clean_text_for_sidebar(next_h4.get_text(strip=True))
                trans_text = random.choice(transitions).format(prev=f"<strong>{prev_title}</strong>", next=f"<strong>{next_title}</strong>")
                trans_div = soup.new_tag('div', attrs={'class': 'presenter-transition'})
                trans_div['style'] = "font-style: italic; color: var(--text-light); margin: 1rem 0 2.5rem 1rem; border-left: 2px solid var(--text-light); padding-left: 1rem; font-size: 1.05rem;"
                trans_div.append(BeautifulSoup(trans_text, 'html.parser'))
                prev_card.insert_after(trans_div)
                
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Restored and injected {appended_count} missing topics for {subject}.")
