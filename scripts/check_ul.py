from bs4 import BeautifulSoup

with open('ml/comprehensive-report.html', 'r', encoding='utf-8') as f:
    html = f.read()
    
soup = BeautifulSoup(html, 'html.parser')
sidebar = soup.find('aside', class_='report-sidebar')

uls = sidebar.find_all('ul')
print(f"Total ul in sidebar: {len(uls)}")
for i, ul in enumerate(uls):
    print(f"  ul {i} class: {ul.get('class')}")
