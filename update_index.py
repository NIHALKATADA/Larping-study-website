import json
import re
from pathlib import Path

BASE_DIR = Path('C:/Users/nihal/OneDrive/Desktop/revision-hub')
DATA_DIR = BASE_DIR / 'data'
SUBJECTS = ['dbms', 'java', 'os', 'daa', 'ml', 'maths']

def normalize_unit(unit):
    if not isinstance(unit, str):
        unit = str(unit)
    unit_norm = unit.strip().lower()
    mapping = {
        '1': 'I', 'unit 1': 'I', 'unit i': 'I', 'i': 'I',
        '2': 'II', 'unit 2': 'II', 'unit ii': 'II', 'ii': 'II',
        '3': 'III', 'unit 3': 'III', 'unit iii': 'III', 'iii': 'III',
        '4': 'IV', 'unit 4': 'IV', 'unit iv': 'IV', 'iv': 'IV',
        '5': 'V', 'unit 5': 'V', 'unit v': 'V', 'v': 'V'
    }
    return mapping.get(unit_norm, unit_norm)

midterm_required = {}

for subject in SUBJECTS:
    json_path = DATA_DIR / subject / f"{subject}_questions.json"
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        ids = []
        for q in questions:
            unit = normalize_unit(q.get('unit', ''))
            if q.get('important') and unit in ['I', 'II', 'III']:
                ids.append(q.get('id'))
        midterm_required[subject] = ids

index_path = BASE_DIR / 'index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# find const midtermRequiredIds = {...};
pattern = r'const midtermRequiredIds = \{.*?\};'
replacement = f'const midtermRequiredIds = {json.dumps(midterm_required)};'

new_content = re.sub(pattern, replacement, content)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated index.html with new midtermRequiredIds')
