with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

# 1. Hide the mobile-toc-toggle globally
css = css.replace('.mobile-toc-toggle {\n        display: block;', 
                  '.mobile-toc-toggle {\n        display: none !important;')

# 2. Add padding-bottom to report-main on mobile so text doesn't hide behind FABs
css = css.replace('.report-main {\n        padding-left: 1.25rem !important;\n        padding-right: 1.25rem !important;\n    }',
                  '.report-main {\n        padding-left: 1.25rem !important;\n        padding-right: 1.25rem !important;\n        padding-bottom: 150px !important;\n    }')

# 3. Fix the FAB menu opening off-screen because of the left-alignment
# We need to append the fab-menu override to the mobile overrides block.
# I will find the end of the file and append it inside the @media (max-width: 768px) block.
# Wait, the last block in the file IS the @media (max-width: 768px) block.
fab_fix = """
    /* Fix FAB menu opening direction since container is on the left */
    .fab-menu {
        left: 0 !important;
        right: auto !important;
        align-items: flex-start !important;
    }
"""

last_brace = css.rfind('}')
if last_brace != -1:
    css = css[:last_brace] + fab_fix + css[last_brace:]

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
