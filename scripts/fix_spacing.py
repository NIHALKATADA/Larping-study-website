with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I will append new spacing optimizations for mobile.
mobile_spacing = """
    /* -------------------------------------
       SPACE OPTIMIZATION (MOBILE)
       ------------------------------------- */
    .report-main .unit-section {
        margin-bottom: 2.5rem !important;
    }
    
    .report-main .unit-section h3.unit-heading {
        font-size: 1.8rem !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.75rem !important;
    }
    
    .report-main .article-card {
        margin-bottom: 2rem !important;
    }
    
    .report-main .article-card h4 {
        font-size: 1.3rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    .presenter-transition {
        margin: 1rem 0 1.5rem 0.5rem !important;
        padding-left: 0.75rem !important;
        font-size: 0.95rem !important;
    }
    
    .report-main p, .report-main ul, .report-main div {
        margin-bottom: 0.75rem !important;
        font-size: 1rem !important; /* Slightly smaller for density */
    }
    
    .report-main li {
        margin-bottom: 0.5rem !important;
    }
    
    .report-main table {
        margin: 1rem 0 !important;
        font-size: 0.9rem !important;
    }
    
    .report-main th, .report-main td {
        padding: 0.75rem !important;
    }
    
    /* Ensure the FABs don't feel too floating */
    .fab-container {
        bottom: 0.75rem !important;
        left: 0.75rem !important;
    }
    .ask-ai-widget {
        right: 0.75rem !important;
        left: 0.75rem !important;
        width: calc(100% - 1.5rem) !important;
    }
}
"""

# The CSS file already ends with a closing brace for the @media block.
# I will insert this right before the last closing brace.
import re
last_brace_index = css.rfind('}')
if last_brace_index != -1:
    new_css = css[:last_brace_index] + mobile_spacing + css[last_brace_index+1:]
else:
    new_css = css + mobile_spacing

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(new_css)
