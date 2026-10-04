with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
# Remove overflow-x: hidden !important from html, body
css = re.sub(r'html,\s*body\s*\{\s*width:\s*100%\s*!important;\s*max-width:\s*100%\s*!important;\s*overflow-x:\s*hidden\s*!important;\s*\}', 
             'html, body { width: 100% !important; max-width: 100% !important; }', css)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
