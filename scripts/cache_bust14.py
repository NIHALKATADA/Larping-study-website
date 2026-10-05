import glob
for file in glob.glob('*/comprehensive-report.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('?v=5.3', '?v=5.4')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
