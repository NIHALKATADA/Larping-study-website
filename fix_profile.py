import re

with open('profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''    <!-- Non-blocking external fonts (combines profile and design-system fonts) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
    
    <!-- Prevent FOUC while asynchronously fetching design-system.css to strip its blocking @import -->
    <style id="fouc-shield">html { visibility: hidden !important; }</style>
    <script>
        fetch('shared/design-system.css')
            .then(res => res.text())
            .then(css => {
                const style = document.createElement('style');
                style.textContent = css.replace(/@import\\s+url\\([^)]+\\);/g, '');
                document.head.appendChild(style);
                document.getElementById('fouc-shield').remove();
            })
            .catch(() => {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = 'shared/design-system.css';
                document.head.appendChild(link);
                document.getElementById('fouc-shield').remove();
            });
    </script>
    <noscript>
        <style>html { visibility: visible !important; }</style>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="shared/design-system.css">
    </noscript>'''

target = '''    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;700&family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="shared/design-system.css">'''

content = content.replace(target, replacement)

with open('profile.html', 'w', encoding='utf-8') as f:
    f.write(content)
