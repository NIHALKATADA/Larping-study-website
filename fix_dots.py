with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix the offsets
css = css.replace('left: calc(-2rem - 6px);', 'left: calc(-2rem - 9px);')
css = css.replace('left: calc(-1.5rem - 6px);', 'left: calc(-1.5rem - 9px);')

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
