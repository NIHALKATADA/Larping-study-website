import re

with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/scripts/build_site.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_clean_html = re.search(r'def clean_html\(html_str\):.*?return text\n\n', content, re.DOTALL)
if old_clean_html:
    new_clean_html = '''def clean_html(html_str):
    if not html_str: return ""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_str, "html.parser")
    for tag in soup(["script", "style"]):
        tag.extract()
    for el in soup.select(".ask-ai-widget, .ask-ai-btn, .fab-main, #assistantModal"):
        el.extract()
    text = soup.get_text(separator=" ")
    text = re.sub(r'\\s+', ' ', text).strip()
    return text

'''
    content = content.replace(old_clean_html.group(0), new_clean_html)
    with open('C:/Users/nihal/OneDrive/Desktop/revision-hub/scripts/build_site.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated clean_html")
else:
    print("Could not find clean_html")
