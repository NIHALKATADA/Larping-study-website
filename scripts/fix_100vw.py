with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace any lingering 100vw with 100% in the god mode block
css = css.replace('width: 100vw !important;', 'width: 100% !important;')
css = css.replace('max-width: 100vw !important;', 'max-width: 100% !important;')

# Replace in glow-bg too just in case
css = css.replace('width: 100vw;', 'width: 100%;')

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
