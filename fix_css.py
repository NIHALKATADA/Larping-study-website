import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace("url('assets/pre-blurred-glass.webp') center/cover;", "rgba(20, 20, 20, 0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);")
html = html.replace("url('assets/pre-blurred-glass.webp') center/cover", "rgba(20, 20, 20, 0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);")
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()
css = css.replace("url('../assets/pre-blurred-glass.webp') center/cover;", "rgba(20, 20, 20, 0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);")
css = css.replace("url('../assets/pre-blurred-glass.webp') center/cover", "rgba(20, 20, 20, 0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);")
with open('shared/design-system.css', 'w', encoding='utf-8') as f:
    f.write(css)
