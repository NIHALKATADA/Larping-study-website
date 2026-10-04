import json
import re

# We will regenerate from the ORIGINAL titles using the JSON files directly to avoid re-shortening already shortened strings in title_map.json
import glob
data = {}
for file in glob.glob("data/*/*_questions.json"):
    with open(file, "r", encoding="utf-8") as f:
        q_data = json.load(f)
        for q in q_data:
            data[q['title']] = q['title']

def shorten_title(t):
    original = t
    
    # Very specific patterns first
    if "Find the time complexity" in t: return "Time Complexity Example"
    if "Perform a complete dry run of Bubble Sort" in t: return "Bubble Sort Dry Run"
    if "Apply Selection Sort" in t: return "Selection Sort Example"
    if "Perform a complete dry run of Insertion Sort" in t or "Apply Insertion Sort" in t: return "Insertion Sort Example"
    if "Construct a Max Heap" in t or "Heap Sort" in t: return "Heap Sort Example"
    if "Counting Sort" in t: return "Counting Sort Example"
    if "Radix Sort" in t: return "Radix Sort Example"
    
    # Generic replacements
    t = re.sub(r'^(?:Explain, in brief, why|Explain, in brief,|Explain briefly|Explain why|Explain the|Explain|Describe the|Describe|Discuss the|Discuss|What is the difference between|What is the|What is|What are the|What are|How does the|How does|How do|Why is the|Why is|Why do|Differentiate between|Compare and contrast|Compare|Define the|Define|State the|State) ', '', t, flags=re.IGNORECASE)
    
    # Truncate at punctuation
    t = re.split(r'[\?\.\|:]', t)[0]
    
    # Fix vs/difference questions
    t = re.sub(r' difference between (.*?) and (.*)', r'\1 vs \2', t, flags=re.IGNORECASE)
    t = re.sub(r'(.*?) more efficient than (.*)', r'\1 vs \2', t, flags=re.IGNORECASE)
    
    # Clean up trailing words
    t = re.sub(r'(?:with an example|with one suitable example|with suitable examples|with a diagram|with a neat diagram|in terms of.*|highlighting one.*|and justify.*|and explain.*|and mention.*|and briefly.*).*$', '', t, flags=re.IGNORECASE)
    
    # Capitalize
    t = t.strip()
    if t:
        t = t[0].upper() + t[1:]
        
    return t.strip()

new_data = {}
for k, v in data.items():
    new_data[k] = shorten_title(k)

with open("title_map.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=4)

print("Title map updated!")
