import os
import glob
from bs4 import BeautifulSoup

def clean_stray_headings(main_content):
    # Find all h2, h3 and remove them if they have no text content after them until the next heading
    headings = main_content.find_all(['h2', 'h3'])
    for h in headings:
        has_content = False
        for sibling in h.parent.find_next_siblings():
            if sibling.name in ['h2', 'h3']:
                break
            if sibling.get_text(strip=True):
                has_content = True
                break
        
        # If it's inside a div, check siblings of the div
        if not has_content:
            parent = h.parent
            if parent.name == 'div' and len(parent.contents) == 1:
                # The div only contains the heading
                for sibling in parent.find_next_siblings():
                    if sibling.name in ['h2', 'h3', 'div']:
                        if sibling.get_text(strip=True):
                            has_content = True
                            break
            else:
                # Heading has siblings in the same div
                for sibling in h.find_next_siblings():
                    if sibling.name in ['h2', 'h3']:
                        break
                    if sibling.get_text(strip=True):
                        has_content = True
                        break
                        
        if not has_content:
            # print(f"Removing stray heading: {h.get_text(strip=True)}")
            if h.parent.name == 'div' and len(h.parent.find_all()) == 1:
                h.parent.decompose()
            else:
                h.decompose()

for filepath in glob.glob('subjects/*/comprehensive-report.html'):
    subject = filepath.split(os.sep)[1]
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    if body:
        body['data-subject'] = subject
        
    layout = soup.find('div', class_='layout-wrapper')
    if not layout: continue
    
    # Remove old quick jump
    controls = layout.find('div', class_='controls')
    if controls: controls.decompose()
    
    # Get all content
    content_elements = layout.contents[:]
    
    # Create new structure
    layout.clear()
    layout['style'] = '' # remove display: block
    
    container = soup.new_tag('div', attrs={'class': 'report-container'})
    sidebar = soup.new_tag('aside', attrs={'class': 'report-sidebar'})
    main_content = soup.new_tag('main', attrs={'class': 'report-main'})
    
    for el in content_elements:
        main_content.append(el)
        
    # Process main content
    # 1. Change cheat-grid to normal div
    for grid in main_content.find_all('div', class_='cheat-grid'):
        grid['class'] = [c for c in grid.get('class', []) if c != 'cheat-grid']
        grid['style'] = '' # remove margin-bottom etc.
        
    # 2. Change cheat-card to article-card
    for card in main_content.find_all('div', class_='cheat-card'):
        classes = card.get('class', [])
        classes = ['article-card' if c == 'cheat-card' else c for c in classes]
        card['class'] = classes
        
    # 3. Clean stray headings
    clean_stray_headings(main_content)
    
    # 4. Generate Sidebar Navigation
    nav_ul = soup.new_tag('ul')
    
    # We will look for .unit-section h3, or loose h2
    sections = main_content.find_all(['h2', 'h3'])
    
    sidebar_title = soup.new_tag('h3')
    sidebar_title.string = "Table of Contents"
    sidebar.append(sidebar_title)
    
    for sec in sections:
        sec_id = sec.parent.get('id') if sec.parent.get('id') else sec.get('id')
        if not sec_id:
            sec_id = "sec_" + "".join(c for c in sec.get_text() if c.isalnum()).lower()
            sec['id'] = sec_id
            
        li = soup.new_tag('li', attrs={'class': 'unit-link'})
        a = soup.new_tag('a', href=f"#{sec_id}")
        a.string = sec.get_text(strip=True).replace(' CO1', '').replace(' CO2', '').replace(' CO3', '')
        li.append(a)
        nav_ul.append(li)
        
        # Now find h4s under this section
        if sec.parent.name == 'div' and 'unit-section' in sec.parent.get('class', []):
            h4s = sec.parent.find_all('h4')
            for h4 in h4s:
                h4_id = h4.get('id')
                if not h4_id:
                    h4_id = "sub_" + "".join(c for c in h4.get_text() if c.isalnum()).lower()
                    h4['id'] = h4_id
                sub_li = soup.new_tag('li', attrs={'class': 'sub-link'})
                sub_a = soup.new_tag('a', href=f"#{h4_id}")
                # clean up U1, U2 badges from text
                h4_text = h4.get_text(strip=True)
                if ' U1' in h4_text: h4_text = h4_text.replace(' U1', '')
                if ' U2' in h4_text: h4_text = h4_text.replace(' U2', '')
                if ' U3' in h4_text: h4_text = h4_text.replace(' U3', '')
                if ' U4' in h4_text: h4_text = h4_text.replace(' U4', '')
                if ' U5' in h4_text: h4_text = h4_text.replace(' U5', '')
                sub_a.string = h4_text
                sub_li.append(sub_a)
                nav_ul.append(sub_li)
                
    sidebar.append(nav_ul)
    
    # 5. Fix up styling on h3
    for h3 in main_content.find_all('h3'):
        classes = h3.get('class', [])
        if 'unit-heading' not in classes:
            classes.append('unit-heading')
        h3['class'] = classes

    container.append(sidebar)
    container.append(main_content)
    layout.append(container)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Processed {filepath}")
