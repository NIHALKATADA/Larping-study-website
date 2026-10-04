with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
# Strip everything after "GOD-MODE TEXT WRAP" or "GLOBAL OVERFLOW" or "STRICT MOBILE"
match = re.search(r'/\* =========================================\n\s*(GOD-MODE|GLOBAL OVERFLOW|STRICT MOBILE|ABSOLUTE NUCLEAR|QUESTION BANK RESTORATION)', css)
if match:
    css = css[:match.start()]

# Now, we apply ONLY the absolutely safe, targeted fixes:
safe_fixes = """
/* =========================================
   SAFE MOBILE OPTIMIZATIONS & FIXES
   ========================================= */

/* 1. Global table constraint so desktop tables don't blow up the layout */
table {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    white-space: nowrap !important;
}

/* 2. Global SVG/Mermaid constraint */
.mermaid svg, img, svg {
    max-width: 100% !important;
    height: auto !important;
}

/* 3. Safe document bounds to prevent panning bugs */
html, body {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
}

/* Fix Glow BG sizing */
.glow-bg {
    width: 100% !important;
    max-width: 100% !important;
}

/* Mobile specific overrides */
@media (max-width: 768px) {
    /* Hide desktop sidebar */
    .report-sidebar { display: none !important; }
    
    /* Ensure main report container fits 100% with padding */
    .report-container, .report-main {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }
    
    /* Give main content safe padding so text doesn't touch edges */
    .report-main {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }
    
    /* Ensure inner cards don't break out */
    .unit-section, .article-card {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* Force text to wrap ONLY inside the report to prevent breaking other UI */
    .report-main p, .report-main h1, .report-main h2, .report-main h3, .report-main h4, .report-main h5, .report-main h6, .report-main li, .report-main span, .report-main div {
        white-space: pre-wrap !important; 
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
    }
    
    /* Except code blocks which must scroll */
    .report-main pre {
        white-space: normal !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        display: block !important;
    }
    .report-main pre code {
        white-space: pre !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
    }
    
    /* Topbar mobile adjustments */
    .smart-topbar button[onclick="downloadPDF()"] { display: none !important; }
    
    /* FAB adjustments - Ensure no overlap */
    .fab-container {
        bottom: 1rem !important;
        left: 1rem !important;
        right: auto !important;
    }
    
    body:not(.report-page) .ask-ai-btn {
        bottom: 95px !important; /* Clear progress widget */
        right: 1rem !important;
        left: auto !important;
    }
    
    body.report-page .ask-ai-btn {
        bottom: 1rem !important;
        right: 1rem !important;
        left: auto !important;
    }
    
    /* Tighter margins for mobile density */
    .report-main .unit-section { margin-bottom: 2.5rem !important; }
    .report-main .unit-section h3.unit-heading { font-size: 1.8rem !important; margin-bottom: 1.5rem !important; padding-bottom: 0.75rem !important; }
    .report-main .article-card { margin-bottom: 2rem !important; }
    .report-main .article-card h4 { font-size: 1.3rem !important; margin-bottom: 0.75rem !important; }
    .presenter-transition { margin: 1rem 0 1.5rem 0.5rem !important; padding-left: 0.75rem !important; font-size: 0.95rem !important; }
    .report-main p, .report-main ul, .report-main div { margin-bottom: 0.75rem !important; font-size: 1rem !important; }
    .report-main li { margin-bottom: 0.5rem !important; }
}
"""

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css + safe_fixes)
