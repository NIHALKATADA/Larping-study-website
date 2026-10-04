import glob
from bs4 import BeautifulSoup

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    body = soup.find('body')
    if body:
        classes = body.get('class', [])
        if 'report-page' not in classes:
            classes.append('report-page')
            body['class'] = classes
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Added report-page class to {filepath}")
