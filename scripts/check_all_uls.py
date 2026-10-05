import glob
from bs4 import BeautifulSoup

for file in glob.glob('*/comprehensive-report.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    sidebar = soup.find('aside', class_='report-sidebar')
    if sidebar:
        uls = sidebar.find_all('ul')
        print(f"{file}: {len(uls)} ul(s) in sidebar")
        links = sidebar.find_all('a')
        print(f"  Total links: {len(links)}")
