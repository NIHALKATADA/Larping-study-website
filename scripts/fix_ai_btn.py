import re

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Completely remove all .ask-ai-btn blocks to rewrite them
css = re.sub(r'(?s)\.ask-ai-btn\s*\{[^}]*\}', '', css)
css = re.sub(r'(?s)body\.report-page\s*\.ask-ai-btn\s*\{[^}]*\}', '', css)

# Append the intelligent responsive blocks
new_css = """
/* =========================================
   ASK AI WIDGET
   ========================================= */
.ask-ai-btn {
    position: fixed;
    bottom: calc(2rem + 70px + 1rem); /* Stack above quiz progress */
    right: 2rem;
    z-index: 9999;
    transition: all 0.3s ease;
}

body.report-page .ask-ai-btn {
    bottom: 2rem; /* No progress widget on reports, drop to corner */
    right: 2rem;
}

@media (max-width: 768px) {
    .ask-ai-btn {
        bottom: calc(1rem + 50px + 1rem);
        right: 1rem;
        left: auto;
    }
    
    body.report-page .ask-ai-btn {
        bottom: 1rem;
        right: 1rem;
    }
}
"""

css += new_css

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
