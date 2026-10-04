with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the nested padding line in the last block
css = css.replace(
    '.layout-wrapper, .report-wrapper, .report-container, .report-main, .unit-section, .article-card {\n        display: block !important;\n        width: 100% !important;\n        max-width: 100% !important;\n        min-width: 0 !important;\n        margin-left: 0 !important;\n        margin-right: 0 !important;\n        padding-left: 1rem !important;\n        padding-right: 1rem !important;',
    '.layout-wrapper, .report-wrapper, .report-container, .report-main, .unit-section, .article-card {\n        display: block !important;\n        width: 100% !important;\n        max-width: 100% !important;\n        min-width: 0 !important;\n        margin-left: 0 !important;\n        margin-right: 0 !important;\n        padding-left: 0 !important;\n        padding-right: 0 !important;'
)

# And explicitly add padding ONLY to the report container
css += "\n@media (max-width: 768px) { .report-container { padding-left: 1rem !important; padding-right: 1rem !important; } }\n"

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
