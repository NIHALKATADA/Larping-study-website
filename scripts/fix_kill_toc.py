with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add display: none !important to all .mobile-toc-toggle references
import re
css = re.sub(r'(\.mobile-toc-toggle\s*\{[^}]*)\}', r'\1 display: none !important; }', css)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
