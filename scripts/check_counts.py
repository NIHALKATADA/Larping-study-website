import json
with open('data/ml/ml_exhaustive_report.json', 'r', encoding='utf-8') as f:
    ex = json.load(f)
print("Exhaustive report units:", len(ex))
for u in ex:
    print(u['unit_title'], len(u['topics']), "topics")

with open('data/ml/ml_questions.json', 'r', encoding='utf-8') as f:
    qs = json.load(f)
print("Questions json total questions:", len(qs))
