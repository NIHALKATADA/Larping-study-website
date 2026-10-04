script = """
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
"""
with open('test.js', 'w') as f: f.write(script)
