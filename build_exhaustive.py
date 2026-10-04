import glob
import json
import os
import re
import random
from bs4 import BeautifulSoup

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

def clean_text(text):
    text = re.sub(r'CO\d$', '', text)
    text = re.sub(r'U\d$', '', text)
    text = re.sub(r'ER Diagram$', ' (ER Diagram)', text)
    text = re.sub(r'Applied Concept$', ' (Applied Concept)', text)
    return text.strip()

for json_file in glob.glob('data/*/*_exhaustive_report.json'):
    subject = json_file.split(os.sep)[1]
    
    html_file = f"subjects/{subject}/comprehensive-report.html"
    if not os.path.exists(html_file): continue
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    sidebar_ul = soup.find('aside', class_='report-sidebar').find('ul')
    main_content = soup.find('main', class_='report-main')
    
    # Clear existing content
    sidebar_ul.clear()
    main_content.clear()
    
    for u_idx, unit_data in enumerate(data):
        u_num = unit_data.get('unit', str(u_idx+1))
        u_title = unit_data.get('unit_title', f"Unit {u_num}")
        topics = unit_data.get('topics', [])
        
        # Add Unit to Sidebar
        unit_li = soup.new_tag('li', attrs={'class': 'unit-link'})
        unit_a = soup.new_tag('a', href=f"#unit{u_num}")
        unit_a.string = clean_text(u_title)
        unit_li.append(unit_a)
        sidebar_ul.append(unit_li)
        
        # Add Unit to Main
        unit_div = soup.new_tag('div', attrs={'class': 'unit-section', 'id': f"unit{u_num}"})
        unit_h3 = soup.new_tag('h3', attrs={'class': 'unit-heading'})
        unit_h3.string = u_title
        unit_div.append(unit_h3)
        
        for t_idx, topic in enumerate(topics):
            t_title = topic.get('title', 'Topic')
            t_id = f"sub_{u_num}_{t_idx}"
            
            # Add Topic to Sidebar
            sub_li = soup.new_tag('li', attrs={'class': 'sub-link'})
            sub_a = soup.new_tag('a', href=f"#{t_id}")
            sub_a.string = clean_text(t_title)
            sub_li.append(sub_a)
            sidebar_ul.append(sub_li)
            
            # Add Topic Card to Main
            card_div = soup.new_tag('div', attrs={'class': 'article-card'})
            card_h4 = soup.new_tag('h4', id=t_id)
            card_h4.string = t_title
            card_div.append(card_h4)
            
            content_html = topic.get('content_html', '')
            parsed_content = BeautifulSoup(content_html, 'html.parser')
            card_div.append(parsed_content)
            
            unit_div.append(card_div)
            
            # Add presenter transition after card if it's not the last one
            if t_idx < len(topics) - 1:
                next_title = clean_text(topics[t_idx+1].get('title', ''))
                curr_title = clean_text(t_title)
                
                template = random.choice(transitions)
                trans_text = template.format(prev=f"<strong>{curr_title}</strong>", next=f"<strong>{next_title}</strong>")
                
                trans_div = soup.new_tag('div', attrs={'class': 'presenter-transition'})
                trans_div['style'] = "font-style: italic; color: #94a3b8; margin: 1rem 0 2.5rem 1rem; border-left: 2px solid rgba(255,255,255,0.1); padding-left: 1rem; font-size: 1.05rem;"
                
                trans_parsed = BeautifulSoup(trans_text, 'html.parser')
                trans_div.append(trans_parsed)
                unit_div.append(trans_div)
                
        main_content.append(unit_div)
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Rebuilt exhaustive report for {subject}")
