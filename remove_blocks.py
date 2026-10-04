with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
css = re.sub(r'/\* Restore beautiful glass cards in single column \*/.*?\.report-main \.article-card \{.*?\}',
"""/* Clean, open sections without boxed backgrounds (W3Schools style) */
.report-main .article-card {
    margin-bottom: 3.5rem;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    width: 100%;
}""", css, flags=re.DOTALL)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Removed block backgrounds.")
