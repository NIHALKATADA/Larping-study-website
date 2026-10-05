from bs4 import BeautifulSoup

with open('ml/comprehensive-report.html', 'r', encoding='utf-8') as f:
    html = f.read()
    
soup = BeautifulSoup(html, 'html.parser')
sidebar = soup.find('aside', class_='report-sidebar')

ul = sidebar.find('ul')
links = ul.find_all('a')
print(f"Total links in TOC: {len(links)}")
for a in links[:10]:
    print(f"  {a.string}")
