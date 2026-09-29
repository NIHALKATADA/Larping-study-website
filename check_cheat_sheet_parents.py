from bs4 import BeautifulSoup
with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/subjects/os/cheat-sheet.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

cards = soup.find_all('div', class_='cheat-card')
for c in cards:
    h4 = c.find('h4')
    if h4 and ('Process State Transition' in h4.text or 'Concurrency & Traps' in h4.text):
        print(f"Found: {h4.text}")
        curr = c
        path = []
        while curr.parent:
            curr = curr.parent
            if curr.name:
                name = curr.name
                if curr.get('id'):
                    name += f"#{curr.get('id')}"
                if curr.get('class'):
                    name += f".{'.'.join(curr.get('class'))}"
                path.append(name)
        print("Path:", " > ".join(reversed(path)))
