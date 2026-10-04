with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Completely eradicate 100vw from the global overflow block
css = css.replace('max-width: 100vw !important;', 'max-width: 100% !important;')
css = css.replace('width: 100vw !important;', 'width: 100% !important;')

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
