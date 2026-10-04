with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Remove overflow-x: hidden from the mobile blocks
css = css.replace('overflow-x: hidden !important;', '/* overflow removed to allow pinch-to-zoom panning */')
css = css.replace('overflow-x: hidden;', '/* overflow removed */')

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
