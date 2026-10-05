import glob
import json
import os
import re
import random
from bs4 import BeautifulSoup

def clean_text_for_sidebar(text):
    text = re.sub(r'CO\d$', '', text)
    text = re.sub(r'U\d$', '', text)
    if len(text) > 40: text = text[:37] + "..."
    return text.strip()

transitions = [
    "Moving forward from {prev}, let's examine {next}.",
    "Building on {prev}, we now turn to {next}.",
    "Having established {prev}, let's explore {next}."
]

for subject in ["daa", "dbms", "java", "maths", "ml", "os"]:
    # Determine which JSON to use
    json_path = None
    if subject == "ml":
        if os.path.exists(f"data/ml/ml_condensed_report.json"):
            json_path = f"data/ml/ml_condensed_report.json"
        else:
            print("Warning: ml_condensed_report.json not ready yet. Skipping ML for now.")
            continue
    elif os.path.exists(f"data/{subject}/{subject}_exhaustive_report.json"):
        json_path = f"data/{subject}/{subject}_exhaustive_report.json"
    else:
        json_path = f"data/{subject}/{subject}_questions.json"
        
    print(f"Building {subject} using {json_path}")
