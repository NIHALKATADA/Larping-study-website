import json
import os

filepath = r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\ml\ml_perfect_report.json'
with open(filepath, 'r', encoding='utf-8') as f:
    d = json.load(f)

u1 = [u for u in d if u['unit'] == 'I'][0]

with open('u1_extract.txt', 'w', encoding='utf-8') as out:
    for i, t in enumerate(u1['topics']):
        out.write(f"--- TOPIC {i} ---\nTITLE: {t['title']}\nCONTENT: {t['content_html']}\n\n")

print("Done writing to u1_extract.txt")
