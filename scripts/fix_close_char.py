import glob

html_files = glob.glob('**/*-report.html', recursive=True)

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '? Close' in content:
        content = content.replace('? Close', '? Close')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
