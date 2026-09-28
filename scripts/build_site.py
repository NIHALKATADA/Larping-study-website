import json
import re
import html
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

SUBJECT_META = {
    "dbms": "Database Management Systems",
    "java": "Object Oriented Programming using Java",
    "os": "Operating Systems",
    "daa": "Design and Analysis of Algorithms",
    "ml": "Machine Learning",
    "maths": "Discrete Mathematics"
}

def normalize_unit(unit):
    if not isinstance(unit, str):
        unit = str(unit)
    unit_norm = unit.strip().lower()
    mapping = {
        '1': 'I', 'unit 1': 'I', 'unit i': 'I', 'i': 'I',
        '2': 'II', 'unit 2': 'II', 'unit ii': 'II', 'ii': 'II',
        '3': 'III', 'unit 3': 'III', 'unit iii': 'III', 'iii': 'III',
        '4': 'IV', 'unit 4': 'IV', 'unit iv': 'IV', 'iv': 'IV',
        '5': 'V', 'unit 5': 'V', 'unit v': 'V', 'v': 'V'
    }
    if unit_norm in mapping:
        return mapping[unit_norm]
    raise ValueError(f"Invalid unit encountered: '{unit}'. Unit must be one of I, II, III, IV, V.")

def clean_html(html_str):
    if not html_str: return ""
    html_str = re.sub(r'<svg[^>]*>.*?</svg>', '', html_str, flags=re.IGNORECASE | re.DOTALL)
    # preserve code block contents
    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(1))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    html_str = re.sub(r'<pre><code>(.*?)</code></pre>', save_code, html_str, flags=re.IGNORECASE | re.DOTALL)
    
    html_str = re.sub(r'<(div|p|br|h[1-6]|li|tr|ul|ol)[^>]*>', '\n', html_str, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', html_str)
    text = html.unescape(text)
    
    for i, cb in enumerate(code_blocks):
        text = text.replace(f"__CODE_BLOCK_{i}__", "\n" + html.unescape(cb) + "\n")
        
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def chunk_html(html_str):
    parts = re.split(r'(<h[1-6][^>]*>.*?</h[1-6]>)', html_str, flags=re.IGNORECASE)
    chunks = []
    current_chunk = ""
    for part in parts:
        if re.match(r'<h[1-6]', part, flags=re.IGNORECASE):
            if current_chunk.strip():
                clean = clean_html(current_chunk)
                if clean: chunks.append(clean)
            current_chunk = part
        else:
            current_chunk += " " + part
    if current_chunk.strip():
        clean = clean_html(current_chunk)
        if clean: chunks.append(clean)
    
    final_chunks = []
    for c in chunks:
        words = c.split()
        if len(words) > 250:
            for i in range(0, len(words), 200):
                final_chunks.append(" ".join(words[i:i+200]))
        else:
            final_chunks.append(c)
    return final_chunks

def extract_course_data_chunks(course_data_path):
    chunks = []
    try:
        try:
            with open(course_data_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(course_data_path, 'r', encoding='utf-16') as f:
                content = f.read()
        
        units_match = re.search(r'units:\s*\[(.*?)\]\s*,\s*examScheme', content, re.DOTALL)
        if units_match:
            units_str = units_match.group(1)
            unit_objs = re.findall(r'\{(.*?)\}', units_str, re.DOTALL)
            for u in unit_objs:
                unit_num = re.search(r'unit:\s*"([^"]+)"', u)
                title = re.search(r'title:\s*"([^"]+)"', u)
                topics_match = re.search(r'topics:\s*\[(.*?)\]', u, re.DOTALL)
                
                chunk_text = []
                if unit_num and title:
                    chunk_text.append(f"Unit {unit_num.group(1)}: {title.group(1)}")
                if topics_match:
                    topics = re.findall(r'"([^"]+)"', topics_match.group(1))
                    chunk_text.extend(topics)
                if chunk_text:
                    chunks.append(" ".join(chunk_text))
    except Exception as e:
        print(f"Error parsing course data {course_data_path}:", e)
    return chunks

def build_subject(subject_dir, templates_dir, data_dir):
    subject_id = subject_dir.name
    questions_path = data_dir / subject_id / f"{subject_id}_questions.json"
    
    if not questions_path.exists():
        print(f"Skipping {subject_id}: {questions_path.name} not found.")
        return
        
    with open(questions_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
        
    for q in questions:
        if 'unit' in q:
            q['unit'] = normalize_unit(q['unit'])

    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template('question-bank-template.html')
    
    subject_code = subject_id.upper()
    subject_full_name = SUBJECT_META.get(subject_id, subject_code)

    output_html = template.render(
        questions=questions, 
        is_midterm=False, 
        subject_code=subject_code,
        subject_id=subject_id,
        subject_full_name=subject_full_name
    )
    with open(subject_dir / 'question-bank.html', 'w', encoding='utf-8') as f:
        f.write(output_html)
        
    print(f"[{subject_id}] Successfully rebuilt question-bank.html with {len(questions)} questions.")
    
    midterm_questions = [q for q in questions if q.get('important') and q.get('unit') in ['I', 'II', 'III']]
    output_midterm = template.render(
        questions=midterm_questions, 
        is_midterm=True, 
        subject_code=subject_code,
        subject_id=subject_id,
        subject_full_name=subject_full_name
    )
    with open(subject_dir / 'midterm-important.html', 'w', encoding='utf-8') as f:
        f.write(output_midterm)
        
    print(f"[{subject_id}] Successfully rebuilt midterm-important.html with {len(midterm_questions)} questions.")
    
    quiz_data_path = data_dir / subject_id / f"{subject_id}_quiz.json"
    if quiz_data_path.exists():
        with open(quiz_data_path, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
        quiz_template = env.get_template('quiz-template.html')
        quiz_html = quiz_template.render(
            quiz_data=quiz_data,
            subject_id=subject_id
        )
        with open(subject_dir / 'interactive-quiz.html', 'w', encoding='utf-8') as f:
            f.write(quiz_html)
        print(f"[{subject_id}] Successfully rebuilt interactive-quiz.html with {len(quiz_data)} questions.")

    # --- AI ASSISTANT INDEX GENERATION ---
    assistant_index = []
    
    # 1. Question Bank Items
    for q in questions:
        # q: {id, q_num, unit, marks, bloom, co, score, important, title, answer_html, ...}
        chunks = chunk_html(q.get('answer_html', ''))
        assistant_index.append({
            "id": q.get('id'),
            "q_num": q.get('q_num'),
            "unit": q.get('unit'),
            "marks": q.get('marks'),
            "bloom": q.get('bloom'),
            "co": q.get('co'),
            "score": q.get('score'),
            "important": q.get('important', False),
            "title": q.get('title', ''),
            "url": f"question-bank.html?open={q.get('id')}",
            "chunks": chunks,
            "type": "question"
        })
        
    # 2. Cheat Sheet Items
    cheat_sheet_path = subject_dir / 'cheat-sheet.html'
    if cheat_sheet_path.exists():
        with open(cheat_sheet_path, 'r', encoding='utf-8') as f:
            cheat_html = f.read()
            # Find body content
            body_match = re.search(r'<body[^>]*>(.*?)</body>', cheat_html, re.DOTALL | re.IGNORECASE)
            if body_match:
                cheat_html = body_match.group(1)
            chunks = chunk_html(cheat_html)
            assistant_index.append({
                "id": "cheat-sheet",
                "title": f"{subject_code} Cheat Sheet",
                "url": "cheat-sheet.html",
                "chunks": chunks,
                "type": "cheat"
            })
            
    # 3. Course Data (Syllabus) Items
    course_data_path = subject_dir / 'course-data.js'
    if course_data_path.exists():
        course_chunks = extract_course_data_chunks(course_data_path)
        if course_chunks:
            assistant_index.append({
                "id": "syllabus",
                "title": f"{subject_code} Syllabus & Topics",
                "url": "index.html",
                "chunks": course_chunks,
                "type": "syllabus"
            })
            
    # Save index
    index_out_path = subject_dir / 'assistant-index.json'
    with open(index_out_path, 'w', encoding='utf-8') as f:
        json.dump(assistant_index, f, indent=2)
    print(f"[{subject_id}] Successfully built assistant-index.json with {len(assistant_index)} items.")

def main():
    root_dir = Path(__file__).parent.parent
    subjects_dir = root_dir / 'subjects'
    data_dir = root_dir / 'data'
    templates_dir = root_dir / 'templates'
    
    if not subjects_dir.exists():
        print("Error: subjects directory not found.")
        return
        
    if not templates_dir.exists():
        print("Error: templates directory not found.")
        return
        
    global_index = []
    
    for subject_path in subjects_dir.iterdir():
        if subject_path.is_dir() and subject_path.name != 'global':
            build_subject(subject_path, templates_dir, data_dir)
            index_file = subject_path / 'assistant-index.json'
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    subject_data = json.load(f)
                    for item in subject_data:
                        # Copy the item to avoid mutating the original dict if needed, 
                        # but here we can just mutate and append
                        new_item = item.copy()
                        new_item['subject'] = subject_path.name
                        new_item['url'] = f"subjects/{subject_path.name}/{item['url']}"
                        global_index.append(new_item)
                        
    global_dir = subjects_dir / 'global'
    global_dir.mkdir(exist_ok=True)
    with open(global_dir / 'assistant-index.json', 'w', encoding='utf-8') as f:
        json.dump(global_index, f, indent=2)
    print(f"[global] Successfully built global assistant-index.json with {len(global_index)} items.")

if __name__ == '__main__':
    main()
