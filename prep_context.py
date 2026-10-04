import json

with open('data/dbms/dbms_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create a clean text representation of the question bank to feed the LLM
out = []
for q in data:
    u = q.get('unit', 'Unknown')
    title = q.get('title', '')
    ans = q.get('answer_html', '')
    
    # Strip HTML from answer for the prompt to save tokens, or keep it so the LLM sees the depth
    # We will keep it but clean it slightly
    out.append(f"--- UNIT {u} ---")
    out.append(f"TOPIC: {title}")
    out.append(f"NOTES: {ans}\n")

with open('data/dbms/dbms_full_context.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out))
print("Created full context file.")
