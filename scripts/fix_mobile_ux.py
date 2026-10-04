import re

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Force body to have overflow-x hidden on mobile to prevent table scrolling from breaking the entire layout
css += """

/* Mobile UX Overhaul */
@media (max-width: 768px) {
    html, body {
        overflow-x: hidden !important;
        width: 100vw;
        position: relative;
    }
    
    .report-main {
        max-width: 100vw !important;
        overflow-x: hidden;
    }
    
    /* Make tables strictly scroll internally, never break layout */
    .report-main table {
        display: block;
        max-width: 100%;
        overflow-x: auto;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
    }
    
    /* Turn TOC into a Floating Action Button on the left */
    .mobile-toc-toggle {
        position: fixed !important;
        bottom: 1rem !important;
        left: 1rem !important;
        width: 56px !important;
        height: 56px !important;
        border-radius: 50% !important;
        background: var(--primary-teal, #10b981) !important;
        color: white !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        z-index: 10000 !important;
    }
    
    /* Swap text for an icon */
    .mobile-toc-toggle {
        font-size: 0 !important; /* Hide the text */
    }
    .mobile-toc-toggle::after {
        content: "?";
        font-size: 1.5rem !important;
        display: block !important;
    }

    /* Transform the sidebar into a full-screen modal when opened via the FAB */
    .report-sidebar.show-toc {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        max-height: 100vh !important;
        z-index: 9998 !important;
        background: rgba(10, 10, 15, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        padding: 4rem 1.5rem 6rem 1.5rem !important;
        display: block !important;
        border-radius: 0 !important;
        margin: 0 !important;
        border-right: none !important;
    }
    
    /* Add a visual title for the full-screen TOC */
    .report-sidebar.show-toc::before {
        content: "Table of Contents";
        display: block;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 1rem;
    }
    
    /* Close TOC when clicking a link inside it */
    .report-sidebar.show-toc li a {
        font-size: 1.1rem !important;
        padding: 1rem 0 !important;
    }
}
"""

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update build_reports.py to add onclick to sidebar links to close the TOC modal on mobile
