new_css = """

/* =========================================
   CRITICAL MOBILE WIDTH FIX
   ========================================= */
@media (max-width: 768px) {
    html, body {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    
    .report-wrapper, .report-container, .report-main, .article-card {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .report-container {
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    .report-main p, .report-main ul, .report-main li, .report-main h4 {
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
