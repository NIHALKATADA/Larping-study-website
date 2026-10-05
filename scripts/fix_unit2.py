import json
with open("data/ml/unit_2_dedup.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for topic in data.get("topics", []):
    if "topic_name" in topic:
        topic["title"] = topic.pop("topic_name")

with open("data/ml/unit_2_dedup.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
