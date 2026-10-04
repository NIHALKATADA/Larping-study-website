import glob

html_files = glob.glob('**/*-report.html', recursive=True)

script_to_add = """
<script>
    // Close the TOC modal on mobile when a link is clicked
    document.querySelectorAll('.report-sidebar a').forEach(link => {
        link.addEventListener('click', () => {
            document.querySelector('.report-sidebar').classList.remove('show-toc');
        });
    });
    
    // Also add a close button at the top of the sidebar for mobile
    const sidebar = document.querySelector('.report-sidebar');
    if (sidebar && !document.getElementById('mobileCloseTocBtn')) {
        const closeBtn = document.createElement('button');
        closeBtn.id = 'mobileCloseTocBtn';
        closeBtn.innerHTML = '? Close';
        closeBtn.style.cssText = 'display: none; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 8px; margin-bottom: 1rem; width: 100%; font-weight: bold; cursor: pointer;';
        closeBtn.onclick = () => sidebar.classList.remove('show-toc');
        sidebar.insertBefore(closeBtn, sidebar.firstChild);
    }
</script>
"""

css_to_add = """
    /* Show close button only when TOC is open on mobile */
    .report-sidebar.show-toc #mobileCloseTocBtn {
        display: block !important;
    }
"""

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'mobileCloseTocBtn' not in content:
        content = content.replace('</body>', script_to_add + '\n</body>')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

with open('shared/design-system.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'mobileCloseTocBtn' not in css:
    last_brace = css.rfind('}')
    css = css[:last_brace] + css_to_add + css[last_brace:]
    with open('shared/design-system.css', 'w', encoding='utf-8') as f:
        f.write(css)

