with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
# Strip out the previous SAFE MOBILE OPTIMIZATIONS block
match = re.search(r'/\* =========================================\n\s*SAFE MOBILE OPTIMIZATIONS', css)
if match:
    css = css[:match.start()]

# Now append a flawless, globally resilient fix scoped strictly to reports.
flawless_fix = """
/* =========================================
   FLAWLESS REPORT LAYOUT FIX (GLOBAL)
   ========================================= */

/* 1. Global table constraint so desktop tables don't blow up the layout */
table {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    white-space: nowrap !important;
    -webkit-overflow-scrolling: touch;
}

/* 2. Global SVG/Mermaid constraint */
.mermaid svg, img, svg {
    max-width: 100% !important;
    height: auto !important;
}

/* 3. Safe document bounds */
html, body {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
}

.glow-bg {
    width: 100% !important;
    max-width: 100% !important;
}

/* 4. FORCE REPORT TO NEVER EXCEED SCREEN (APPLIES TO DESKTOP MODE TOO) */
.report-container, .report-wrapper {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    min-width: 0 !important;
}

.report-main {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    min-width: 0 !important;
    /* Don't force margin: 0 here or it breaks desktop centering */
}

/* 5. FORCE TEXT WRAPPING GLOBALLY (BUT SCOPED TO REPORT ONLY) */
.report-main p, .report-main h1, .report-main h2, .report-main h3, .report-main h4, .report-main h5, .report-main h6, .report-main li, .report-main span, .report-main div, .article-card *, .unit-heading {
    white-space: pre-wrap !important; 
    word-break: break-word !important;
    overflow-wrap: break-word !important;
    max-width: 100% !important;
}

/* 6. CODE BLOCKS SCROLL INSTEAD OF WRAP */
.report-main pre {
    white-space: normal !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    display: block !important;
    -webkit-overflow-scrolling: touch;
}
.report-main pre code {
    white-space: pre !important;
    word-break: normal !important;
    overflow-wrap: normal !important;
}

/* =========================================
   MOBILE-ONLY OVERRIDES
   ========================================= */
@media (max-width: 768px) {
    /* Hide desktop sidebar */
    .report-sidebar { display: none !important; }
    
    /* On mobile, remove margin/flex and force block */
    .report-container, .report-wrapper, .report-main {
        display: block !important;
        margin: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Give main content safe padding */
    .report-main {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }
    
    /* Inner cards */
    .unit-section, .article-card {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* Tighter margins for mobile density */
    .report-main .unit-section { margin-bottom: 2.5rem !important; }
    .report-main .unit-section h3.unit-heading { font-size: 1.8rem !important; margin-bottom: 1.5rem !important; padding-bottom: 0.75rem !important; }
    .report-main .article-card { margin-bottom: 2rem !important; }
    .report-main .article-card h4 { font-size: 1.3rem !important; margin-bottom: 0.75rem !important; }
    .presenter-transition { margin: 1rem 0 1.5rem 0.5rem !important; padding-left: 0.75rem !important; font-size: 0.95rem !important; }
    .report-main p, .report-main ul, .report-main div { margin-bottom: 0.75rem !important; font-size: 1rem !important; }
    .report-main li { margin-bottom: 0.5rem !important; }
    
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
}
"""

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css + flawless_fix)
