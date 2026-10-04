import os
import glob

html_files = glob.glob('**/*.html', recursive=True)
count = 0

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'design-system.css' in content:
        # Replace any existing versioning first to be safe
        import re
        content = re.sub(r'design-system\.css(\?v=[0-9.]+)?', 'design-system.css?v=2.5', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Cache-busted CSS in {count} HTML files.")
