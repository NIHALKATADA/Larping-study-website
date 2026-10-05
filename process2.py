import json

with open('unit2_topics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

topics = data.get('topics', [])
with open('unit2_topics.txt', 'w', encoding='utf-8') as f:
    for i, t in enumerate(topics):
        f.write(f"Topic {i}: {t.get('title', 'Unknown')}\n")
        f.write(f"{t.get('content_html', '')}\n")
        f.write("-" * 40 + "\n")
