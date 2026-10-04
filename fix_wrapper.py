import glob
from bs4 import BeautifulSoup

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    layout = soup.find('div', class_='layout-wrapper')
    if layout:
        classes = layout.get('class', [])
        if 'layout-wrapper' in classes:
            classes.remove('layout-wrapper')
            classes.append('report-wrapper')
            layout['class'] = classes
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Fixed wrapper for {filepath}")
