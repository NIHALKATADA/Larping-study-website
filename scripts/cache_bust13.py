import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'design-system.css' in content:
        content = re.sub(r'design-system\.css\?v=[0-9.]+', 'design-system.css?v=4.5', content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
