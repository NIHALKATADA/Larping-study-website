import os
import glob
from bs4 import BeautifulSoup
import re

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    subject = filepath.split(os.sep)[1]
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # We already restructured it in the previous step.
    # Now let's just add the mobile toggle button right before the sidebar.
    container = soup.find('div', class_='report-container')
    if container:
        # Check if toggle already exists
        if not container.find('button', class_='mobile-toc-toggle'):
            toggle = soup.new_tag('button', attrs={'class': 'mobile-toc-toggle', 'onclick': 'document.querySelector(".report-sidebar").classList.toggle("show-toc")'})
            toggle.string = "? Table of Contents"
            # Insert at the top of the container
            container.insert(0, toggle)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Added mobile TOC toggle to {filepath}")
