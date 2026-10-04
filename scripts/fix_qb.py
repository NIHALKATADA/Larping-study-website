with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the dangerous global wildcard wrap that breaks the banner h1
import re
css = css.replace('p, h1, h2, h3, h4, h5, h6, li, span, div, .article-card *, .unit-heading {', 
                 '.report-main p, .report-main h2, .report-main h3, .report-main h4, .report-main h5, .report-main h6, .report-main li, .report-main span, .article-card *, .unit-heading, .q-card * {')

# Find the mobile override block for .layout-wrapper
# We want to make sure we don't break the question bank's margin top
css = css.replace('.layout-wrapper, .report-wrapper, .report-container, .report-main {', 
                  '.report-wrapper, .report-container, .report-main {')

# Adjust the AI button spacing on mobile so it clears the progress widget completely
css = css.replace('bottom: calc(1rem + 50px + 1rem) !important; /* Progress widget is ~50px tall */', 
                  'bottom: calc(1rem + 75px + 1rem) !important;')
                  
# Wait, I didn't add the AI button calc logic in the last script. Let me just append an override.

fix_qb = """
/* =========================================
   QUESTION BANK RESTORATION & FAB CLEARANCE
   ========================================= */
@media (max-width: 768px) {
    /* Protect the banner background clip */
    header.banner h1 {
        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
    }
    
    /* Ensure the layout wrapper behaves correctly on Question Bank */
    body:not(.report-page) .layout-wrapper {
        display: flex !important;
        flex-direction: column !important;
        padding: 1rem !important; /* Restore padding */
        margin: 0 auto !important; /* Restore centering */
    }
    
    /* Ensure AI button properly clears the Progress Widget on Question Bank */
    body:not(.report-page) .ask-ai-btn {
        bottom: 95px !important; /* Push it up above the 70px tall progress widget */
    }
    
    /* Ensure the progress widget sits flush in the corner */
    #stickyProgressWidget {
        bottom: 1rem !important;
        right: 1rem !important;
    }
}
"""

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css + fix_qb)
