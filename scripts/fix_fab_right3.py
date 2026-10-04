with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

right_side_fab = """
    /* Restore FAB to the right side, stacked above AI button */
    .fab-container {
        bottom: 120px !important;
        right: 1rem !important;
        left: auto !important;
        align-items: flex-end !important;
    }
    
    .fab-menu {
        right: 0 !important;
        left: auto !important;
        align-items: flex-end !important;
        margin-bottom: 1.5rem !important;
    }
"""

last_brace = css.rfind('}')
if last_brace != -1:
    css = css[:last_brace] + right_side_fab + css[last_brace:]

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
