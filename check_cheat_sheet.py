from bs4 import BeautifulSoup
with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/subjects/os/cheat-sheet.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

cards = soup.find_all('div', class_='cheat-card')
print(f"Total cheat-cards: {len(cards)}")
for c in cards:
    parent_id = c.parent.get('id') if c.parent else 'None'
    print(f"- {c.find('h4').text if c.find('h4') else 'No H4'} (Parent: {parent_id})")
