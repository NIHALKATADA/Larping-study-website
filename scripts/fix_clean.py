with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Completely nuke the chaotic resets I added at the end of the file.
# I will find everything after "/* =========================================\n   STRICT MOBILE UI FIXES"
import re
match = re.search(r'/\* =========================================\n\s*STRICT MOBILE UI FIXES', css)
if match:
    css = css[:match.start()]

# Now, append a SINGLE, CLEAN, CORRECT block.
clean_reset = """
/* =========================================
   STRICT MOBILE UI FIXES & LAYOUT RESET
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

/* 3. Global document constraint */
html, body {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
}

/* 4. Fix Glow BG sizing */
.glow-bg {
    width: 100% !important;
    max-width: 100% !important;
}

/* 5. Mobile specific overrides */
@media (max-width: 768px) {
    /* Hide desktop sidebar */
    .report-sidebar { display: none !important; }
    
    /* Reset containers to block and ensure they fit 100% */
    .layout-wrapper, .report-wrapper, .report-container, .report-main {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }
    
    /* Give main content safe padding so text doesn't touch edges */
    .report-main {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }
    
    /* Remove padding/margin from inner cards so they fit the main container */
    .unit-section, .article-card {
        width: 100% !important;
        max-width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        box-sizing: border-box !important;
    }
    
    /* Force text to wrap unconditionally */
    p, h1, h2, h3, h4, h5, h6, li, span, div, .article-card *, .unit-heading {
        white-space: pre-wrap !important; 
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
    }
    
    /* Except tables and code which must scroll */
    pre, .table-scroll-wrapper {
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
    
    /* Topbar mobile adjustments */
    .smart-topbar button[onclick="downloadPDF()"] { display: none !important; }
    .smart-topbar { backdrop-filter: blur(16px) !important; -webkit-backdrop-filter: blur(16px) !important; background: rgba(20, 20, 20, 0.7) !important; }
    
    /* FAB adjustments */
    .fab-container {
        bottom: 1rem !important;
        left: 1rem !important;
        right: auto !important;
    }
    .ask-ai-widget {
        right: 1rem !important;
        left: 1rem !important;
        width: calc(100% - 2rem) !important;
    }
}
"""

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css + clean_reset)
