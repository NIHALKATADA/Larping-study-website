import json
import random

random.seed(42)

with open(r'data\maths\maths_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions:
    if 'score' not in q:
        q['score'] = round(random.uniform(5.5, 9.8), 1)

with open(r'data\maths\maths_questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=4)
print("Scores added.")
