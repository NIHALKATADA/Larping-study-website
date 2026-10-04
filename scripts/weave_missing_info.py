import os
import json
import glob
import sys
try:
    import google.generativeai as genai
except ImportError:
    print("Please install google-generativeai: pip install google-generativeai")
    sys.exit(1)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Please set the GEMINI_API_KEY environment variable.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')

def weave_missing_information():
    for json_file in glob.glob('data/*/*_questions.json'):
        subject = json_file.split(os.sep)[1]
        html_file = f"subjects/{subject}/comprehensive-report.html"
        
        if not os.path.exists(html_file):
            continue
            
        with open(json_file, 'r', encoding='utf-8') as f:
            q_data = json.load(f)
            
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        print(f"Processing {subject}...")
        
        prompt = f"""
        You are an expert textbook editor. 
        I have a highly-curated HTML cheat sheet for the subject '{subject}'.
        I also have a JSON array of questions and answers that represent the complete syllabus.
        
        Your task is to cross-reference the HTML with the JSON. 
        Identify any INFORMATION from the JSON that is missing or not covered with enough depth in the HTML.
        DO NOT paste the raw questions. Instead, seamlessly WEAVE the missing information into the HTML.
        - Add new paragraphs to existing sections where appropriate.
        - Create new <div class="article-card"> sections ONLY if it's a completely new topic.
        - Keep the output as valid HTML. Do not alter the overarching UI structure.
        
        Here is the JSON Question Bank:
        {json.dumps(q_data)}
        
        Here is the current HTML:
        {html_content}
        
        Return ONLY the fully updated HTML code.
        """
        
        try:
            response = model.generate_content(prompt)
            updated_html = response.text.replace("```html", "").replace("```", "").strip()
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            print(f"Successfully updated {subject}.")
        except Exception as e:
            print(f"Failed to process {subject}: {e}")

if __name__ == "__main__":
    weave_missing_information()
