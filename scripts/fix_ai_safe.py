new_css = """

/* =========================================
   UX OVERHAUL: NO OVERLAP GRID
   ========================================= */

/* DEFAULT DESKTOP (Question Bank & Quiz) */
/* Bottom-Left to avoid the Progress Widget and FAB Menu on the right */
.ask-ai-btn {
    bottom: 2rem !important;
    left: 2rem !important;
    right: auto !important;
}

.ask-ai-widget {
    bottom: calc(2rem + 60px) !important;
    left: 2rem !important;
    right: auto !important;
}

/* REPORT PAGE DESKTOP */
/* Bottom-Right to avoid overlapping the Sidebar on the left */
body.report-page .ask-ai-btn {
    bottom: 2rem !important;
    right: 2rem !important;
    left: auto !important;
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
        bottom: calc(1rem + 50px + 1rem) !important; /* Progress widget is ~50px tall */
        right: 1rem !important;
        left: auto !important;
    }
    
    /* Mobile Report Page: Sit in bottom right (Mobile FAB is on the left) */
    body.report-page .ask-ai-btn {
        bottom: 1rem !important;
        right: 1rem !important;
        left: auto !important;
    }
    
    /* Mobile Widget: Full screen width, safe height */
    .ask-ai-widget, body.report-page .ask-ai-widget {
        bottom: calc(1rem + 60px + 50px + 1rem) !important;
        left: 1rem !important;
        right: 1rem !important;
        width: calc(100vw - 2rem) !important;
        max-width: calc(100vw - 2rem) !important;
    }
    
    body.report-page .ask-ai-widget {
        bottom: calc(1rem + 60px + 1rem) !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
