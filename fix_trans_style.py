import glob
from bs4 import BeautifulSoup

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    for t in soup.find_all('div', class_='presenter-transition'):
        t['style'] = "font-style: italic; color: var(--text-light); margin: 1rem 0 2.5rem 1rem; border-left: 2px solid var(--text-light); padding-left: 1rem; font-size: 1.05rem;"
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
