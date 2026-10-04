import re

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Completely strip all ask-ai-btn and ask-ai-widget rules to write fresh clean ones
css = re.sub(r'(?s)/\* =========================================\s*ASK AI WIDGET.*', '', css)

new_css = """
/* =========================================
   ASK AI WIDGET & FAB POSITIONING
   ========================================= */

/* DEFAULT DESKTOP (Question Bank & Quiz) */
/* Bottom-Left to avoid the Progress Widget and FAB Menu on the right */
.ask-ai-btn {
    position: fixed;
    bottom: 2rem;
    left: 2rem;
    right: auto;
    z-index: 9999;
    transition: all 0.3s ease;
}

.ask-ai-widget {
    position: fixed;
    bottom: calc(2rem + 60px) !important;
    left: 2rem !important;
    right: auto !important;
    z-index: 2000;
    width: 400px;
    max-width: calc(100vw - 4rem);
    height: 600px;
    max-height: calc(100vh - 120px);
    resize: both;
    overflow: hidden;
    min-width: 300px;
    min-height: 400px;
}

/* REPORT PAGE DESKTOP */
/* Bottom-Right to avoid overlapping the Sidebar on the left */
body.report-page .ask-ai-btn {
    bottom: 2rem;
    right: 2rem;
    left: auto;
}

body.report-page .ask-ai-widget {
    bottom: calc(2rem + 60px) !important;
    right: 2rem !important;
    left: auto !important;
}

/* MOBILE */
@media (max-width: 768px) {
    /* Mobile Default (Question Bank & Quiz): Stack above Progress Widget on the right */
    .ask-ai-btn {
        bottom: calc(1rem + 50px + 1rem); /* Progress widget is ~50px tall */
        right: 1rem;
        left: auto;
    }
    
    /* Mobile Report Page: Sit in bottom right (Mobile FAB is on the left) */
    body.report-page .ask-ai-btn {
        bottom: 1rem;
        right: 1rem;
        left: auto;
    }
    
    /* Mobile Widget: Full screen width, safe height */
    .ask-ai-widget, body.report-page .ask-ai-widget {
        bottom: calc(1rem + 60px + 50px + 1rem) !important;
        left: 1rem !important;
        right: 1rem !important;
        width: calc(100vw - 2rem) !important;
        max-width: calc(100vw - 2rem) !important;
        max-height: calc(100vh - 160px) !important;
        height: auto !important;
    }
    
    body.report-page .ask-ai-widget {
        bottom: calc(1rem + 60px + 1rem) !important;
    }
}
"""

css += new_css

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
