import re

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace ANY instance of .ask-ai-btn desktop rule
css = re.sub(r'\.ask-ai-btn\s*\{[^}]*left:\s*2rem;[^}]*\}', 
             '.ask-ai-btn {\n    position: fixed;\n    bottom: calc(2rem + 70px + 1rem + 60px);\n    right: 2rem;\n    z-index: 9999;\n}', 
             css)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
