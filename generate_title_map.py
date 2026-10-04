import json
import glob
import re

out = {}
for json_file in glob.glob('data/*/*_questions.json'):
    with open(json_file, 'r', encoding='utf-8') as f:
        q_data = json.load(f)
    for q in q_data:
        title = q['title']
        
        # Heuristic to shorten
        t = re.sub(r'^(What is the difference between|What is the difference|What do you mean by|What is meant by|What is|What are|Define|Explain the concept of|Explain how|Explain|Discuss|Differentiate between|Distinguish between|Compare and contrast|Compare|Write a note on|Write short notes on|State and prove|State|Describe)\s+', '', title, flags=re.IGNORECASE)
        t = re.sub(r'^(the|an|a)\s+', '', t, flags=re.IGNORECASE)
        t = t.split('.')[0].split('?')[0]
        
        # Split by common connectors and take the first part
        t = re.split(r'\s+(in terms of|using|and explain|and describe|giving one|highlighting|with example|with an example|with one example|with the help of|in detail)', t, flags=re.IGNORECASE)[0]
        
        if len(t) > 0: t = t[0].upper() + t[1:]
        out[title] = t.strip()

with open('title_map.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)
print("Title map created")
