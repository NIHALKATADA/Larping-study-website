import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SUBJECTS = ["dbms", "java", "os", "daa", "ml", "maths"]

# Generalized Examiner's Predictive Matrix Rule Engine
def is_predictable_generalized(bloom, marks):
    """
    Applies the universal Outcome-Based Education (OBE) bias discovered:
    - 2 Mark (Short): K1/L1 (Remember) or K2/L2 (Understand)
    - 3 Mark (Medium): K2/L2 (Understand) or K3/L3 (Apply)
    - 5 Mark (Long): K3/L3 (Apply), K4/L4 (Analyze), or higher
    """
    bloom_level = str(bloom).upper().strip()
    
    if marks == 2:
        return bloom_level in ["L1", "K1", "L2", "K2"]
    elif marks == 3:
        return bloom_level in ["L2", "K2", "L3", "K3"]
    elif marks == 5:
        return bloom_level in ["L2", "K2", "L3", "K3", "L4", "K4", "L5", "K5", "L6", "K6"]
    
    return False

def process_subject(subject):
    json_path = DATA_DIR / subject / f"{subject}_questions.json"
    if not json_path.exists():
        print(f"Skipping {subject}, file not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    updated_count = 0
    for q in questions:
        # Evaluate based on the generalized matrix
        bloom = q.get("bloom", "")
        marks = q.get("marks", 0)
        score = q.get("score")
        if score is None: score = 0.0
        score = float(score)
        
        should_be_important = is_predictable_generalized(bloom, marks) and (score >= 9.0)
        
        if q.get("important") != should_be_important:
            q["important"] = should_be_important
            updated_count += 1

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4)

    print(f"[{subject.upper()}] Updated {updated_count} questions based on the Generalized Predictive Matrix.")

if __name__ == "__main__":
    print("Applying Generalized Examiner Predictive Matrix to ALL Question Banks...")
    for sub in SUBJECTS:
        process_subject(sub)
    print("Run `python scripts/build_site.py` to regenerate the important HTML files.")
