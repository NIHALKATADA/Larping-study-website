import json
with open("data/ml/ml_perfect_report.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for unit in data:
    titles = [t["title"] for t in unit["topics"]]
    print(f"{unit['unit_title']} has {len(titles)} topics")
    
    # Simple deduplication based on first 3 words to see obvious duplicates
    seen = {}
    for t in titles:
        key = " ".join(t.lower().split()[:3])
        if key not in seen:
            seen[key] = []
        seen[key].append(t)
        
    for k, v in seen.items():
        if len(v) > 1:
            print(f"  Duplicate cluster '{k}':")
            for t in v:
                print(f"    - {t}")
