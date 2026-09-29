from bs4 import BeautifulSoup

file_path = 'C:/Users/nihal/OneDrive/Desktop/revision-hub/subjects/os/cheat-sheet.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

skeleton = soup.find(id='pureSkeleton')
if skeleton:
    cards = skeleton.find_all('div', class_='cheat-card')
    count = 0
    for card in cards:
        card.extract()
        count += 1
    
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Removed {count} cheat-cards from pureSkeleton.")
    else:
        print("No cheat-cards found in pureSkeleton.")
else:
    print("pureSkeleton not found.")
