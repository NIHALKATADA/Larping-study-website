import glob
import re

html_files = glob.glob('*/comprehensive-report.html', recursive=False)

fab_html = """
    <!-- Mobile FAB Menu for Comprehensive Report -->
    <div class="fab-container mobile-only-fab" style="display: none;">
        <div class="fab-menu" id="fabMenu">
            <button class="fab-item" onclick="document.querySelector('.report-sidebar').classList.add('show-toc'); document.getElementById('fabMenu').classList.remove('open');" title="Table of Contents">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
                <span>TOC</span>
            </button>
            <button class="fab-item" onclick="downloadPDF(); document.getElementById('fabMenu').classList.remove('open');" title="Save as PDF">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                <span>PDF</span>
            </button>
            <button class="fab-item" onclick="window.scrollTo({top: 0, behavior: 'smooth'}); document.getElementById('fabMenu').classList.remove('open');" title="Back to Top">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
                <span>Top</span>
            </button>
        </div>
        <button class="fab-main" id="fabMainBtn" aria-label="Quick Actions" onclick="document.getElementById('fabMenu').classList.toggle('open'); this.classList.toggle('active');">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
        </button>
    </div>
"""

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if we already injected it
    if 'mobile-only-fab' in content:
        continue
        
    # Inject right before the Ask AI button
    content = re.sub(
        r'(<!-- Standalone Ask AI FAB)',
        fab_html + r'\n    \1',
        content
    )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Injected FAB into {html_file}")
