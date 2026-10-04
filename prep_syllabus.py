import glob
import json
import os

for json_file in glob.glob('data/*/*_questions.json'):
    subject = json_file.split(os.sep)[1]
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    unit_map = {}
    for q in data:
        u = q.get('unit', 'Unknown')
        if u not in unit_map: unit_map[u] = []
        unit_map[u].append(q.get('title'))
        
    # Write to a text file for subagent to read
    with open(f'data/{subject}/{subject}_syllabus_dump.txt', 'w', encoding='utf-8') as f:
        for u, titles in unit_map.items():
            f.write(f"=== UNIT {u} ===\n")
            for t in titles:
                f.write(f"- {t}\n")
            f.write("\n")
    print(f"Generated syllabus dump for {subject}")
