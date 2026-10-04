import glob
import random
import re
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

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # First, remove any existing transitions if we run this multiple times
    for t in soup.find_all('div', class_='presenter-transition'):
        t.decompose()
    
    units = soup.find_all('div', class_='unit-section')
    for unit in units:
        cards = unit.find_all('div', class_='article-card')
        for i in range(len(cards) - 1):
            prev_card = cards[i]
            next_card = cards[i+1]
            
            prev_h4 = prev_card.find('h4')
            next_h4 = next_card.find('h4')
            
            if prev_h4 and next_h4:
                prev_title = clean_text(prev_h4.get_text(strip=True))
                next_title = clean_text(next_h4.get_text(strip=True))
                
                # Pick a random transition format
                template = random.choice(transitions)
                transition_text = template.format(prev=f"<strong>{prev_title}</strong>", next=f"<strong>{next_title}</strong>")
                
                # Create the transition element
                trans_div = soup.new_tag('div', attrs={'class': 'presenter-transition'})
                trans_div['style'] = "font-style: italic; color: #94a3b8; margin: 1rem 0 2.5rem 1rem; border-left: 2px solid rgba(255,255,255,0.1); padding-left: 1rem; font-size: 1.05rem;"
                
                # Parse the HTML string into a tag and append
                parsed_text = BeautifulSoup(transition_text, 'html.parser')
                trans_div.append(parsed_text)
                
                # Insert it after the prev_card
                prev_card.insert_after(trans_div)
                
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Cleaned presenter transitions for {filepath}")
