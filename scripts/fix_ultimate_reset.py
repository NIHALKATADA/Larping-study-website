new_css = """

/* =========================================
   ULTIMATE MOBILE LAYOUT RESET
   ========================================= */
@media (max-width: 768px) {
    /* 1. Nuke any possible horizontal overflow at the root */
    html, body {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }
    
    /* 2. Constrain every single container block */
    .layout-wrapper, .report-wrapper, .report-container, .report-main, .unit-section, .article-card {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }
    
    /* 3. Force wrap on all text nodes */
    .article-card p, .article-card ul, .article-card li, .article-card h1, .article-card h2, .article-card h3, .article-card h4, .article-card h5, .article-card h6, .article-card span, .article-card div {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        box-sizing: border-box !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* 4. Ensure tables scroll but don't stretch */
    .report-main table {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
