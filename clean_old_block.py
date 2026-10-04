import glob
import os
from bs4 import BeautifulSoup

for html_file in glob.glob('subjects/*/comprehensive-report.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    main_content = soup.find('main', class_='report-main')
    
    # 1. Delete the explicit section if it exists
    old_section = soup.find(lambda tag: tag.name in ['section', 'div'] and tag.find(lambda t: t.name in ['h2', 'h3'] and 'Applied Examples' in t.text))
    if old_section and old_section.name != 'main':
        old_section.decompose()
        
    # 2. Also blindly delete anything after <main> except the assistant script
    if main_content:
        for sibling in main_content.find_next_siblings():
            if sibling.name != 'script':
                sibling.decompose()
                
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Cleaned {html_file}")
