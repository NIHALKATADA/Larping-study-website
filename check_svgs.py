from bs4 import BeautifulSoup
import glob

for html_file in glob.glob('subjects/*/comprehensive-report.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    svgs = soup.find_all('svg')
    
    # Filter out UI SVGs (width/height < 50)
    content_svgs = []
    for s in svgs:
        try:
            h = int(s.get('height', 0))
            if h > 50:
                content_svgs.append(s)
        except:
            if s.has_attr('viewBox') or s.has_attr('viewbox'):
                vb = s.get('viewBox', s.get('viewbox', ''))
                if '24 24' not in vb:
                    content_svgs.append(s)
                    
    if content_svgs:
        print(f"{html_file} has {len(content_svgs)} content SVGs.")
