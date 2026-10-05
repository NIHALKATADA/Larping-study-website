import json

with open('data/ml/ml_perfect_report.json', encoding='utf-8') as f:
    data = json.load(f)

unit_2 = None
for u in data:
    if u.get('unit') == 'II' or u.get('unit') == '2' or u.get('unit_title', '').startswith('Unit II'):
        unit_2 = u
        break

if unit_2:
    with open('unit2_topics.json', 'w', encoding='utf-8') as f:
        json.dump(unit_2, f, indent=2)
