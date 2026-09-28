import re

with open('shared/app-utils.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I will replace the broken section entirely.
# We'll find:
# document.addEventListener('click', (e) => {
#    // 1. Handle glass-modals
# ...
#    }
# });
# And we will replace it with the correct closing brackets AND the new logic at the top.

# Actually, the easiest way to fix it is to restore from the very first unmodified backup if we have one, or just insert the missing brackets before the next block.

# Next block is:
# document.addEventListener('click', (e) => {
#     if (e.target.tagName === 'A' && e.target.getAttribute('href') && ...

js = js.replace('''    }
});
document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href') && e.target.getAttribute('href').startsWith('#') && e.target.closest('.glass-modal')) {''',
'''    }
});
    }
});
document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href') && e.target.getAttribute('href').startsWith('#') && e.target.closest('.glass-modal')) {''')

with open('shared/app-utils.js', 'w', encoding='utf-8') as f:
    f.write(js)
