import os
import glob
from bs4 import BeautifulSoup
import re

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    subject = filepath.split(os.sep)[1]
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # We will just fix the link text in the sidebar since we already processed the rest.
    nav_ul = soup.find('ul')
    if nav_ul:
        for a in nav_ul.find_all('a'):
            # The text has things like 'DBMSCO1' or 'IndependenceU1'.
            # We can use regex to remove 'CO[1-5]' or 'U[1-5]' or 'ER Diagram' if they got stuck.
            text = a.get_text()
            text = re.sub(r'CO\d$', '', text)
            text = re.sub(r'U\d$', '', text)
            text = re.sub(r'ER Diagram$', ' (ER Diagram)', text)
            text = re.sub(r'Applied Concept$', ' (Applied Concept)', text)
            a.string = text
            
    # Also let's check for stray pureSkeleton and remove it to clean up the DOM if it's there?
    # Actually pureSkeleton is just a div that might be toggled by JS. Let's see if it has id="pureSkeleton".
    skel = soup.find(id="pureSkeleton")
    if skel:
        skel.decompose()
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Fixed sidebar text for {filepath}")
