import os
import glob
import re

meta_tag = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
html_files = glob.glob('**/*.html', recursive=True)

for html_file in html_files:
    # Skip node_modules
    if 'node_modules' in html_file: continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'name="viewport"' not in content:
        content = re.sub(r'(<head.*?>)', r'\1\n' + meta_tag, content, count=1, flags=re.IGNORECASE)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"Added viewport to {html_file}")
            
print("Done!")
