import re

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the ugly mobile TOC FAB styles
css = re.sub(r'/\* Turn TOC into a Floating Action Button on the left \*/.*?/\* Swap text for an icon \*/', '', css, flags=re.DOTALL)
css = re.sub(r'\.mobile-toc-toggle\s*\{[^}]*font-size:\s*0\s*!important;[^}]*\}', '', css)
css = re.sub(r'\.mobile-toc-toggle::after\s*\{[^}]*\}', '', css)

# Fix the overlap between Ask AI and Fab container
css = re.sub(
    r'\.ask-ai-btn\s*\{[^}]*z-index:\s*9999;\s*transition:\s*all\s*0\.3s\s*ease;\s*\}',
    r'.ask-ai-btn {\n    position: fixed;\n    bottom: calc(2rem + 70px + 60px); /* Stack above quiz progress and fab */\n    right: 2rem;\n    z-index: 9999;\n    transition: all 0.3s ease;\n}',
    css
)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
