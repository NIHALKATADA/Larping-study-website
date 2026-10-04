from bs4 import BeautifulSoup
with open("subjects/os/comprehensive-report.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
    
for child in soup.body.children:
    if child.name:
        print(child.name, child.get('id', ''), child.get('class', ''))
