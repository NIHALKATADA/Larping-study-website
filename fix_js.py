import re

with open('shared/app-utils.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I will replace the broken openModal with the correct one

broken_logic = """window.openModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
        const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        if (scrollbarWidth > 0) {
            document.body.style.paddingRight = scrollbarWidth + 'px';
            const topbar = document.querySelector('.smart-topbar');
            if (topbar) topbar.style.paddingRight = calc(var(--space-4) + px);
            const fab = document.querySelector('.fab-container');
            if (fab && window.innerWidth > 768) fab.style.right = calc(2rem + px);
            const prog = document.getElementById('stickyProgressWidget');
            if (prog && window.innerWidth > 768) prog.style.right = calc(2rem + 48px + 1rem + px);
        }
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};"""

correct_logic = """window.openModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
        const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        if (scrollbarWidth > 0) {
            document.body.style.paddingRight = scrollbarWidth + 'px';
            const topbar = document.querySelector('.smart-topbar');
            if (topbar) topbar.style.paddingRight = `calc(var(--space-4) + ${scrollbarWidth}px)`;
            const fab = document.querySelector('.fab-container');
            if (fab && window.innerWidth > 768) fab.style.right = `calc(2rem + ${scrollbarWidth}px)`;
            const prog = document.getElementById('stickyProgressWidget');
            if (prog && window.innerWidth > 768) prog.style.right = `calc(2rem + 48px + 1rem + ${scrollbarWidth}px)`;
        }
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};"""

js = js.replace(broken_logic, correct_logic)

with open('shared/app-utils.js', 'w', encoding='utf-8') as f:
    f.write(js)
