from bs4 import BeautifulSoup

with open('ml/midterm-important.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

items = soup.select('.article-card')
print(f"Total important items: {len(items)}")
for i, item in enumerate(items[:5]):
    title = item.select_one('h3').get_text(strip=True) if item.select_one('h3') else "No Title"
    badge = item.select_one('.importance-badge')
    score = badge.get_text(strip=True) if badge else "No Score"
    print(f"{i+1}. {score} - {title}")
