with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
css = re.split(r'/\*\s*Single Column Clean Layout with Sidebar\s*\*/', css)[0]

new_css = """
/* Single Column Clean Layout with Sidebar */
.report-container {
    display: flex;
    flex-direction: row;
    width: 100%;
    max-width: 100%;
    margin: 0;
    padding: var(--space-4) var(--space-8);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #f1f5f9;
    line-height: 1.7;
    gap: 4rem;
}

/* Sticky Sidebar Navigation */
.report-sidebar {
    width: 300px;
    flex-shrink: 0;
    position: sticky;
    top: 80px;
    max-height: calc(100vh - 100px);
    overflow-y: auto;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    padding-right: var(--space-4);
    background: transparent !important; /* Seamless with page background */
    display: block !important;
}

.report-sidebar h3 {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-bottom: var(--space-4);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.report-sidebar ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.report-sidebar li a {
    display: block;
    padding: var(--space-2) var(--space-3);
    color: #94a3b8;
    text-decoration: none;
    border-radius: 6px;
    transition: all 0.2s;
    font-size: 0.95rem;
    margin-bottom: 2px;
}

.report-sidebar li a:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--subject-color, #fff);
}

.report-sidebar li.unit-link a {
    font-weight: 600;
    margin-top: var(--space-4);
    color: #e2e8f0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    border-radius: 0;
    padding-left: 0;
}

.report-sidebar li.sub-link a {
    padding-left: var(--space-4);
    font-size: 0.85rem;
}

/* Main Content takes remaining space, with comfortable reading width */
.report-main {
    flex: 1;
    min-width: 0;
    padding-bottom: 150px;
}

/* Limit the width of the actual text for readability */
.report-main > div, .report-main > h2, .report-main > h3, .report-main .unit-section {
    max-width: 900px;
}

/* Clean, open sections instead of boxed cards */
.report-main .unit-section {
    margin-bottom: 5rem;
}

.report-main .unit-section h3.unit-heading {
    font-size: 2.2rem;
    color: var(--subject-color, #fff);
    border-bottom: 2px solid rgba(255,255,255,0.1);
    padding-bottom: var(--space-3);
    margin-bottom: 3rem;
    margin-top: 0;
    font-weight: 700;
}

/* Remove all boxed backgrounds */
.report-main .article-card {
    margin-bottom: 3.5rem;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    width: 100%;
}

.report-main .article-card h4 {
    font-size: 1.5rem;
    color: #f8fafc;
    margin-top: 0;
    margin-bottom: 1.25rem;
    font-weight: 600;
}

/* Content Typography */
.report-main p, .report-main ul, .report-main div {
    font-size: 1.1rem;
    color: #cbd5e1;
    margin-bottom: 1rem;
}

.report-main strong {
    color: #fff;
    font-weight: 600;
}

/* High contrast examples and tips */
.report-main .example {
    margin-top: 1.5rem;
    background: rgba(255, 255, 255, 0.03);
    padding: 1.25rem;
    border-radius: 8px;
    border-left: 4px solid rgba(255,255,255,0.2);
    font-size: 1rem;
    color: #e2e8f0;
}

.report-main .article-card .pro-tip,
.report-main .article-card .exam-trap,
.report-main .article-card .examiner-trap {
    margin-top: 1.5rem;
    padding: 1.25rem;
    border-radius: 8px;
    font-size: 1rem;
    display: block;
}

.report-main .article-card .exam-trap,
.report-main .article-card .examiner-trap {
    background: rgba(239, 68, 68, 0.08);
    border-left: 4px solid #ef4444;
    color: #fca5a5;
}

.report-main .article-card .pro-tip {
    background: rgba(16, 185, 129, 0.08);
    border-left: 4px solid #10b981;
    color: #6ee7b7;
}

/* Mobile Adjustments */
.mobile-toc-toggle {
    display: none;
    width: 100%;
    background: rgba(255,255,255,0.05);
    color: #f1f5f9;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 1rem;
    font-weight: bold;
    text-align: center;
    border-radius: 8px;
    margin-bottom: 2rem;
    cursor: pointer;
}

@media (max-width: 1024px) {
    .report-container {
        padding: var(--space-4);
        gap: 2rem;
    }
}

@media (max-width: 768px) {
    .report-container {
        flex-direction: column;
    }
    
    .mobile-toc-toggle {
        display: block;
    }

    .report-sidebar {
        width: 100%;
        position: static;
        height: auto;
        border-right: none;
        padding-right: 0;
        display: none !important;
        background: rgba(0,0,0,0.2) !important;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    
    .report-sidebar.show-toc {
        display: block !important;
    }
}
"""

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css.strip() + '\n' + new_css)
print("Updated CSS to fix sidebar alignment and theme seamlessness.")
