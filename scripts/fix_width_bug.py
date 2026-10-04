with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix the deadly width: 100% on report-main in desktop mode
css = css.replace('.report-main {\n    width: 100% !important;\n    max-width: 100% !important;\n    box-sizing: border-box !important;\n    min-width: 0 !important;\n}', 
                  '.report-main {\n    max-width: 100% !important;\n    box-sizing: border-box !important;\n    min-width: 0 !important;\n}')

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
