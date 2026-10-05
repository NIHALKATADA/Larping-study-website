import json
for i in [1, 2, 3]:
    with open(f"data/ml/unit_{i}_dedup.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        topics = data.get("topics", [])
        if topics:
            print(f"Unit {i} first topic keys: {list(topics[0].keys())}")
