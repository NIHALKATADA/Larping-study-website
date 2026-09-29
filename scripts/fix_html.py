import re
from pathlib import Path

def fix_file(path):
    print(f"Fixing {path}")
    content = path.read_text(encoding='utf-8')
    
    # 1. Remove duplicate theme toggle
    content = re.sub(r'<button[^>]*id="themeToggleBtn"[^>]*>Mode: Dark</button>', '', content)
    
    # 2. Extract deep dive cards
    deep_dives = []
    # Find cheat cards containing "Deep Dive"
    pattern = r'<div class="cheat-card">\s*<h4>Deep Dive:.*?</ul>\n</div>'
    for m in re.finditer(pattern, content, flags=re.DOTALL):
        deep_dives.append(m.group(0))
        
    # Remove them from the original location
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Now, there's an unclosed div. The original injection did:
    # content.replace('</div>\n</div>', deep_dives + '</div>\n</div>') or something like that.
    # So removing the deep dives might leave `\n</div>\n</div>` correctly, but we need to check if there are unbalanced divs.
    # The instructions say: "Every cheat sheet has an unclosed <div>. The inject_* scripts did a blind content.replace('</div>\n</div>', ...). The "Deep Dive" cards landed at lines ~54–76 of os/cheat-sheet.html, above the cheat-grid sections they were meant to join."
    
    # Let's fix the unbalanced div around the controls section.
    # We can just use BeautifulSoup to prettify and fix, or we can just append the deep dives to the first cheat-grid.
    # First cheat grid is: <div class="cheat-grid"
    
    if deep_dives:
        insertion_point = content.find('<div class="cheat-grid"')
        if insertion_point != -1:
            # find the end of this opening tag
            end_tag = content.find('>', insertion_point) + 1
            content = content[:end_tag] + '\n' + '\n'.join(deep_dives) + content[end_tag:]
    
    # The unclosed div from the blind replace:
    # They did content.replace('</div>\n</div>', cards) instead of cards + '</div>\n</div>'
    # So we are missing a </div></div> at the end of the controls div?
    # Let's check if we can just fix the number of divs.
    
    path.write_text(content, encoding='utf-8')

for p in Path('subjects').rglob('cheat-sheet.html'):
    fix_file(p)
