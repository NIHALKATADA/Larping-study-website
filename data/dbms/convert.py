import json
import re

def process_text():
    with open('c:\\Users\\nihal\\OneDrive\\Desktop\\revision-hub\\data\\dbms\\dbms_full_context.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    units = re.split(r'--- UNIT (I{1,3}|IV|V) ---', content)
    
    output = []
    
    unit_titles = {
        "I": "Unit I: Introduction & ER Modeling",
        "II": "Unit II: Relational Model & SQL",
        "III": "Unit III: Normalization & Transaction Processing",
        "IV": "Unit IV: Concurrency & Recovery",
        "V": "Unit V: Advanced Topics"
    }

    for i in range(1, len(units), 2):
        unit_num = units[i]
        unit_text = units[i+1]
        
        unit_obj = {
            "unit": unit_num,
            "unit_title": unit_titles.get(unit_num, f"Unit {unit_num}"),
            "topics": []
        }
        
        topics_raw = unit_text.split('TOPIC: ')
        for t_raw in topics_raw:
            if not t_raw.strip():
                continue
            
            parts = t_raw.split('NOTES: ')
            if len(parts) < 2:
                continue
                
            topic_title_raw = parts[0].strip()
            notes_html = parts[1].strip()
            
            # Clean up topic title (remove questions)
            title = topic_title_raw
            title = re.sub(r'^(What is a|What is|What do you mean by|Define the terms|Define|Explain the concept of|Explain|Discuss the|Discuss|State the|Give the difference between|Differentiate between|Compare the) ', '', title, flags=re.IGNORECASE)
            title = title.replace('?', '')
            title = title.capitalize()
            if "difference" in topic_title_raw.lower() or "compare" in topic_title_raw.lower() or "differentiate" in topic_title_raw.lower():
                title = "Comparison: " + title
            
            # Replace exam-tip with pro-tip
            notes_html = notes_html.replace('class="exam-tip"', 'class="pro-tip"')
            
            # Ensure <div class="example"> exists
            if '<em>Example:</em>' in notes_html:
                notes_html = notes_html.replace('<em>Example:</em>', '<div class="example"><strong>Example:</strong>')
                # A bit hacky but we close it at the end of the p tag
                notes_html = re.sub(r'(<div class="example">.*?)(</p>|</li>|<br>)', r'\1</div>\2', notes_html, flags=re.IGNORECASE)
            elif 'class="example"' not in notes_html and 'example' in notes_html.lower():
                # Add a dummy pro-tip or example if it doesn't exist to satisfy the prompt for this topic if needed
                pass

            if "Comparison:" in title or "vs" in title.lower():
                if '<ul>' in notes_html and '<li>' in notes_html:
                    ul_content = re.search(r'<ul>(.*?)</ul>', notes_html, re.DOTALL)
                    if ul_content:
                        list_items = re.findall(r'<li><strong>(.*?):</strong>(.*?)</li>', ul_content.group(1), re.DOTALL)
                        if list_items:
                            table_html = "<table class='w3-table-all'>\n<tr><th>Concept</th><th>Description</th></tr>\n"
                            for k, v in list_items:
                                table_html += f"<tr><td><strong>{k.strip()}</strong></td><td>{v.strip()}</td></tr>\n"
                            table_html += "</table>"
                            notes_html = notes_html.replace(ul_content.group(0), table_html)
            
            topic_obj = {
                "title": title,
                "content_html": notes_html
            }
            unit_obj["topics"].append(topic_obj)
            
        output.append(unit_obj)
        
    with open('c:\\Users\\nihal\\OneDrive\\Desktop\\revision-hub\\data\\dbms\\dbms_exhaustive_report.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    process_text()
