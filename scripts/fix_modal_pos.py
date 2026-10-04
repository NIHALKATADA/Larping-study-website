import re

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the desktop .ask-ai-widget positioning
css = re.sub(
    r'\.ask-ai-widget\s*\{[^}]*left:\s*2rem;[^}]*\}', 
    r'.ask-ai-widget {\n    position: fixed;\n    bottom: calc(2rem + 70px + 60px);\n    right: 2rem;\n    left: auto;\n    z-index: 2000;\n    width: 400px;\n    max-width: calc(100vw - 4rem);\n    height: 600px;\n    max-height: calc(100vh - 120px);\n}', 
    css
)

# Append dynamic overrides at the very end to ensure they take precedence
new_css = """

/* =========================================
   ASK AI WIDGET ALIGNMENT FIX
   ========================================= */
.ask-ai-widget {
    right: 2rem !important;
    left: auto !important;
    bottom: calc(2rem + 70px + 60px) !important;
}

body.report-page .ask-ai-widget {
    bottom: calc(2rem + 60px) !important;
}

@media (max-width: 768px) {
    .ask-ai-widget {
        right: 1rem !important;
        left: 1rem !important;
        width: calc(100vw - 2rem) !important;
        bottom: calc(1rem + 50px + 60px) !important;
    }
    
    body.report-page .ask-ai-widget {
        bottom: calc(1rem + 60px) !important;
    }
}
"""

css += new_css

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
