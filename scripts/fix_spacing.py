with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix overlap spacing by adding an extra rem
css = css.replace(
    'bottom: calc(2rem + 70px + 60px); /* Stack above quiz progress and fab */',
    'bottom: calc(2rem + 70px + 60px + 1rem); /* Stack above quiz progress and fab */'
)

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
