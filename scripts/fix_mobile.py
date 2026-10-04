import os
import glob
import re

# Fix design-system.css Ask AI button
css_path = 'shared/design-system.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'\.ask-ai-btn\s*\{\s*position:\s*fixed;\s*bottom:\s*2rem;\s*left:\s*2rem;\s*\}',
             '.ask-ai-btn {\n    position: fixed;\n    bottom: calc(2rem + 70px + 1rem + 60px);\n    right: 2rem;\n    z-index: 9999;\n}', css)

css = re.sub(r'\.ask-ai-btn\s*\{\s*bottom:\s*calc\(1rem \+ 48px \+ 1rem\);\s*/\* Stacked above 3-dots FAB \*/\s*left:\s*1rem;\s*\}',
             '.ask-ai-btn {\n        bottom: calc(1rem + 48px + 1rem);\n        right: 1rem;\n        left: auto;\n        z-index: 9999;\n    }', css)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# Inject viewport meta tag into all HTML files
meta_tag = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
html_files = glob.glob('**/*.html', recursive=True)

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'name="viewport"' not in content:
        content = re.sub(r'(<head.*?>)', r'\1\n' + meta_tag, content, count=1, flags=re.IGNORECASE)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"Added viewport to {html_file}")
            
print("Done!")
