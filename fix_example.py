with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('background: rgba(255, 255, 255, 0.03);', 'background: var(--card-bg);')
css = css.replace('border-left: 4px solid rgba(255,255,255,0.2);', 'border-left: 4px solid var(--text-light);')

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Fixed example box styling.")
