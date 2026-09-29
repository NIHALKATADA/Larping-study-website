import os
import json
import glob
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockerThreshold

# =====================================================================
# INSTRUCTIONS:
# 1. Install the Gemini SDK: pip install google-generativeai
# 2. Set the GEMINI_API_KEY environment variable.
# =====================================================================

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = os.environ.get("GEMINI_MODEL")

if not API_KEY or not MODEL_NAME:
    print("ERROR: Please set the GEMINI_API_KEY and GEMINI_MODEL environment variables before running.")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME, generation_config={"response_mime_type": "application/json"})

PROMPT = """
You are an expert professor. I will give you a JSON array of long-form exam questions and their answers.
I want you to convert EVERY SINGLE question into an interactive quiz format.
For each question, decide whether it makes the most sense as a Multiple Choice Question ("mcq") or a Short Answer/One-Word Question ("short").
If it's code related, you can make it "code" (where the user types a snippet).

Return a JSON array of objects with the exact following schema:
[
  {
    "id": "original_q_id",
    "type": "mcq", // or "short" or "code"
    "question": "The newly formulated clear question.",
    "options": ["Option A", "Option B", "Option C", "Option D"], // ONLY if type is mcq, otherwise omit
    "correct_answer": "The exact string of the correct option, or the expected short answer",
    "explanation": "Brief explanation of why this is correct based on the original answer."
  }
]
Ensure you map the "id" properly.
"""

def generate_for_subject(json_path):
    print(f"Processing {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process in batches of 20 to avoid token limits
    batch_size = 20
    all_quizzes = []
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        print(f"  Sending batch {i//batch_size + 1}...")
        
        # Strip HTML from answers to save tokens
        clean_batch = []
        for q in batch:
            clean_batch.append({
                "id": q["id"],
                "title": q["title"],
                "answer_text": q["answer_html"][:500] # send just enough context
            })
            
        try:
            response = model.generate_content(
                PROMPT + "\\n\\nInput Data:\\n" + json.dumps(clean_batch),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockerThreshold.BLOCK_NONE
                }
            )
            batch_result = json.loads(response.text)
            all_quizzes.extend(batch_result)
        except Exception as e:
            print(f"  Error on batch {i//batch_size + 1}: {e}")
            
        time.sleep(2) # rate limit prevention
        
    out_path = json_path.replace('_questions.json', '_quiz.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_quizzes, f, indent=4)
    print(f"Saved {len(all_quizzes)} quiz questions to {out_path}")

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for filepath in sorted(glob.glob(os.path.join(root, 'data', '*', '*_questions.json'))):
        generate_for_subject(filepath)
    print("All subjects processed! You can now run build_site.py.")
