import json

with open("title_map.json", "r", encoding="utf-8") as f:
    data = json.load(f)

long_titles = [v for v in data.values() if len(v.split()) > 7]
print(f"Total long titles: {len(long_titles)}")
for t in long_titles[:20]:
    print("-", t)
