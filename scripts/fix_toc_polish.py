import glob

css_path = 'shared/design-system.css'
css = open(css_path, encoding='utf-8').read()
block = """

/* Mobile TOC overlay: solid background (overrides earlier transparent rule) */
@media (max-width: 768px) {
    body.report-page aside.report-sidebar.show-toc {
        background: #0a0a0f !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch;
    }
}
"""
if 'Mobile TOC overlay: solid background' not in css:
    css = css.rstrip() + block
    open(css_path, 'w', encoding='utf-8').write(css)

for p in glob.glob('*/comprehensive-report.html'):
    s = open(p, encoding='utf-8').read()
    s = s.replace("closeBtn.innerHTML = '? Close';", "closeBtn.innerHTML = '&#10005; Close';")
    s = s.replace('design-system.css?v=4.8', 'design-system.css?v=4.9')
    open(p, 'w', encoding='utf-8').write(s)
    print('patched', p)
