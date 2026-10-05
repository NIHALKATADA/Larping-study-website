import json
import os

out = []
for i in [1, 2, 3]:
    fname = f"data/ml/unit_{i}_dedup.json"
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            unit_data = json.load(f)
            out.append(unit_data)

with open("data/ml/ml_dedup_report.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print(f"Combined into ml_dedup_report.json with {len(out)} units.")
