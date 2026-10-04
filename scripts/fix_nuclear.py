with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make god-mode text wrapping completely global (outside media queries)
new_css = """
/* =========================================
   ABSOLUTE NUCLEAR GLOBAL OVERFLOW PREVENTION
   ========================================= */
html, body {
    max-width: 100vw !important;
    overflow-x: hidden !important;
    width: 100% !important;
}

.report-container, .report-wrapper, .report-main {
    max-width: 100% !important;
    box-sizing: border-box !important;
}

/* Force ALL text on the entire site to wrap unconditionally */
p, h1, h2, h3, h4, h5, h6, li, span, div, .article-card *, .unit-heading {
    white-space: pre-wrap !important; 
    word-break: break-word !important;
    overflow-wrap: break-word !important;
    max-width: 100% !important;
}

/* Except tables and pre blocks which MUST scroll */
pre, table, .table-scroll-wrapper {
    white-space: normal !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    display: block !important;
}
pre code {
    white-space: pre !important;
    word-break: normal !important;
    overflow-wrap: normal !important;
}
table th, table td {
    white-space: nowrap !important;
    word-break: normal !important;
    overflow-wrap: normal !important;
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
