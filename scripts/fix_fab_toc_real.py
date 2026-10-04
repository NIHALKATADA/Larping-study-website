with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Protect the TOC modal
css = css.replace('.report-sidebar { display: none !important; }', 
                  '.report-sidebar:not(.show-toc) { display: none !important; }')

# 2. Add z-index to TOC modal
css = css.replace('height: 100vh !important;\n    }', 
                  'height: 100vh !important;\n        z-index: 999999 !important;\n    }')

# 3. Force the FAB menu to definitely be visible
fab_super_fix = """
    /* Guarantee FAB Menu Visibility */
    .fab-menu.open {
        opacity: 1 !important;
        pointer-events: auto !important;
        transform: translateY(0) scale(1) !important;
        visibility: visible !important;
        display: flex !important;
        z-index: 99999 !important;
    }
"""

last_brace = css.rfind('}')
if last_brace != -1:
    css = css[:last_brace] + fab_super_fix + css[last_brace:]

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
