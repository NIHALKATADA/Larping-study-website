with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Add blur to topbar so text scrolling behind it is legible, not a garbled mess
if "backdrop-filter: blur" not in css.split(".smart-topbar {")[1].split("}")[0]:
    css = css.replace(
        'background: rgba(20, 20, 20, 0.6);',
        'background: rgba(20, 20, 20, 0.7);\n    backdrop-filter: blur(16px);\n    -webkit-backdrop-filter: blur(16px);'
    )

new_css = """

/* =========================================
   STRICT MOBILE UI FIXES (Prevent Overflow)
   ========================================= */
@media (max-width: 768px) {
    /* 1. Un-crowd the Topbar by hiding Save as PDF (since it's in the mobile FAB now) */
    .smart-topbar button[onclick="downloadPDF()"] {
        display: none !important;
    }
    
    /* 2. Force document strictly to viewport width */
    html, body {
        width: 100vw !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
        position: relative;
    }
    
    /* 3. Force main content to wrap */
    .report-wrapper, .report-container, .report-main {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }
    
    /* 4. Fix typography bleeding off the edge */
    .report-main * {
        max-width: 100% !important;
        box-sizing: border-box !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* Except tables which should scroll horizontally */
    .report-main table, .report-main table * {
        max-width: none !important;
    }
    .report-main table {
        display: block !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
    }
}
"""

with open('shared/design-system.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
