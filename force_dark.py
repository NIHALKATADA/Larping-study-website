import glob
from bs4 import BeautifulSoup

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    html_tag = soup.find('html')
    if html_tag:
        html_tag['data-theme'] = 'dark'
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
