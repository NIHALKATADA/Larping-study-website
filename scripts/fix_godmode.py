new_css = """

/* =========================================
   GOD-MODE TEXT WRAP & LAYOUT RESET
   ========================================= */
@media (max-width: 768px) {
    /* Stop any centering overflow */
    .report-main, .unit-section, .article-card {
        margin-left: 0 !important;
        margin-right: 0 !important;
        float: none !important;
    }
    
    /* Force flex items to shrink */
    .report-container, .report-wrapper, .report-main {
        flex: 1 1 0% !important;
        min-width: 0 !important;
        width: 100vw !important;
        max-width: 100vw !important;
        display: block !important; /* KILL FLEXBOX ENTIRELY just to be safe */
    }
    
    /* God-mode word wrapping */
    p, h1, h2, h3, h4, h5, h6, li, span, div, .article-card * {
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
    }
    
    /* Let pre and table scroll, but restrict their width */
    pre, table {
        max-width: 100vw !important;
        overflow-x: auto !important;
        display: block !important;
    }
    pre *, table * {
        white-space: normal; /* Let them wrap if possible, except code */
    }
    pre code {
        white-space: pre !important;
    }
    table th, table td {
        white-space: nowrap !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
