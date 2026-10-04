with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Aggressively strip 100vw
css = css.replace('100vw', '100%')

# Add the most aggressive word-wrap to literally everything inside report-main
new_css = """
@media (max-width: 768px) {
    /* Absolute nuke on horizontal overflow */
    .report-main, .report-main * {
        max-width: 100% !important;
        box-sizing: border-box !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: pre-wrap !important; /* Force wrap even for pre-formatted, unless overridden */
    }
    
    /* Except for code and tables which MUST scroll */
    .report-main pre, .report-main pre *, .report-main table, .report-main table * {
        white-space: normal !important;
    }
    .report-main pre code {
        white-space: pre !important;
    }
    .report-main table th, .report-main table td {
        white-space: nowrap !important;
    }
    .report-main pre, .report-main table {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        display: block !important;
        width: 100% !important;
    }
    
    /* Make sure body cannot possibly be wider than screen */
    html, body {
        width: 100% !important;
        max-width: 100% !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
