import glob

html_files = glob.glob('*/comprehensive-report.html', recursive=False)
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<div class="fab-container mobile-only-fab" style="display: none;">', '<div class="fab-container mobile-only-fab">')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
