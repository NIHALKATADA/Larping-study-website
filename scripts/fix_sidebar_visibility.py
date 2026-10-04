with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
# We want to find `.report-sidebar { ... display: none !important; ... }` and remove the display line.
# Be careful not to touch `.report-sidebar:not(.show-toc) { display: none !important; }`

def repl(match):
    # If this is the :not(.show-toc) rule, leave it alone.
    if ':not(.show-toc)' in match.group(0):
        return match.group(0)
    
    # Otherwise, remove the display: none line
    block = match.group(0)
    block = re.sub(r'display:\s*none\s*!important;', '', block)
    return block

css = re.sub(r'\.report-sidebar\s*\{[^}]+\}', repl, css)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
