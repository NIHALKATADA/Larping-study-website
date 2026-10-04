with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
css = re.split(r'/\*\s*W3Schools style layout for Comprehensive Report\s*\*/', css)[0]
css = re.split(r'/\*\s*Revert previous sidebar/flowchart.*?\*/', css, flags=re.DOTALL)[0]

new_css = """
/* Single Column Clean Layout with Sidebar */
.report-container {
    display: flex;
    flex-direction: row;
    max-width: 1500px;
    margin: 0 auto;
    padding: var(--space-4);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #f1f5f9;
    line-height: 1.7;
    position: relative;
    gap: 4rem;
}

/* Sidebar Navigation */
.report-sidebar {
    width: 300px;
    flex-shrink: 0;
    position: sticky;
    top: 80px;
    max-height: calc(100vh - 100px);
    overflow-y: auto;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    padding-right: var(--space-4);
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

/* Main Content - Centered to balance empty space */
.report-main {
    flex: 1;
    min-width: 0;
    max-width: 900px;
    padding-bottom: 150px;
    column-count: 1 !important;
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
    .report-main {
        padding-left: var(--space-4);
        padding-right: var(--space-4);
    }
}

@media (max-width: 768px) {
    .report-container {
        flex-direction: column;
        padding: var(--space-4);
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
        background: rgba(0,0,0,0.2);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    
    .report-sidebar.show-toc {
        display: block !important;
    }

    .report-main {
        padding-left: 0;
        padding-right: 0;
    }
}
"""

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css.strip() + '\n' + new_css)
print("Updated CSS cleanly.")
