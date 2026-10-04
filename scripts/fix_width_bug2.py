with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
css = re.sub(r'\.report-main\s*\{\s*width:\s*100%\s*!important;\s*max-width:\s*100%\s*!important;\s*box-sizing:\s*border-box\s*!important;\s*min-width:\s*0\s*!important;\s*/\*[^}]*\*/\s*\}',
             '.report-main { max-width: 100% !important; box-sizing: border-box !important; min-width: 0 !important; }', css)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
