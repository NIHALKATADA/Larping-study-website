with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace hardcoded white/light colors with theme variables
css = css.replace('color: #f1f5f9;', 'color: var(--text-main);')
css = css.replace('color: #94a3b8;', 'color: var(--text-light);')
css = css.replace('color: #e2e8f0;', 'color: var(--heading-color);')
css = css.replace('color: #cbd5e1;', 'color: var(--text-main);')
css = css.replace('color: #fff;', 'color: var(--heading-color);')
css = css.replace('color: #f8fafc;', 'color: var(--heading-color);')
css = css.replace('background: rgba(0,0,0,0.2) !important;', 'background: var(--card-bg) !important;')

with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Fixed hardcoded colors to support theming.")
