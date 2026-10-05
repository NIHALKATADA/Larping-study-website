import glob

for file in glob.glob('*/comprehensive-report.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('?v=5.0', '?v=5.1')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
