with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the problematic 100vw
css = css.replace('width: 100vw !important;', 'width: 100% !important;')
css = css.replace('max-width: 100vw !important;', 'max-width: 100% !important;')

# Add padding and white-space normal overrides
new_css = """
@media (max-width: 768px) {
    /* Critical padding to prevent edge-hugging and text cutoff */
    .report-container {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Ensure text forces wrapping and ignores any rogue nowrap */
    .report-main p, .report-main ul, .report-main li, .report-main h4 {
        white-space: normal !important;
        word-break: break-word !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
