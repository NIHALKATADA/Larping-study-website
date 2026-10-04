with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make the table scrolling fix apply to ALL screen sizes
new_css = """
/* =========================================
   GLOBAL OVERFLOW & TABLE FIX (Applies to Desktop too)
   ========================================= */
.report-main table {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    white-space: nowrap !important; /* or normal, but usually nowrap is better for data tables to prevent vertical squishing, allowing horizontal scroll */
}

html, body {
    max-width: 100% !important;
    overflow-x: hidden !important; /* safe on desktop, maybe risky on mobile but we'll see */
}

/* Let's remove overflow-x: hidden on body just in case it breaks pinch zoom, but use it on the wrapper */
.layout-wrapper, .report-wrapper, .report-container, .report-main {
    max-width: 100% !important;
    box-sizing: border-box !important;
}

/* Force text to wrap globally, not just on mobile */
.report-main p, .report-main ul, .report-main li, .report-main h1, .report-main h2, .report-main h3, .report-main h4, .report-main h5, .report-main h6, .article-card {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    white-space: pre-wrap !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}
.report-main pre code {
    white-space: pre !important;
}
.report-main pre {
    max-width: 100% !important;
    overflow-x: auto !important;
    display: block !important;
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
