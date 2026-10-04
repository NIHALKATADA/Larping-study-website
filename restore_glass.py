with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

# Remove the rule that strips the article-card styling
css = re.sub(r'/\* Remove all boxed backgrounds \*/.*?\.report-main \.article-card \{.*?\}', 
    """/* Restore beautiful glass cards in single column */
.report-main .article-card {
    margin-bottom: 3.5rem;
    background: var(--card-bg) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
    padding: var(--space-6) !important;
    border-radius: 12px;
    width: 100%;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}""", css, flags=re.DOTALL)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Restored glass cards.")
