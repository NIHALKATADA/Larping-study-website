from bs4 import BeautifulSoup
with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/subjects/os/cheat-sheet.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

skeleton = soup.find(id='pureSkeleton')
if skeleton:
    print(skeleton.prettify())
