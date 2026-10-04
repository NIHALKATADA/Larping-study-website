// ==========================================
// CRITICAL PATH — runs immediately (no defer)
// Theme must apply before first paint to avoid flash
// ==========================================
const utilsPathParts = window.location.pathname.split('/');
const utilsSubjectName = utilsPathParts[utilsPathParts.length - 2] || 'default';
const THEME_KEY = 'global_theme';
const REVIEWED_KEY = utilsSubjectName + '_reviewed';
let hasCelebrated = false;

// Apply theme immediately to avoid FOUC

const safeStorage = {
    getItem: function(key) {
        try { return localStorage.getItem(key); }
        catch (e) { return null; }
    },
    setItem: function(key, value) {
        try { localStorage.setItem(key, value); }
        catch (e) { }
    },
    removeItem: function(key) {
        try { localStorage.removeItem(key); }
        catch (e) { }
    }
};

const savedTheme = safeStorage.getItem(THEME_KEY) || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);

function toggleTheme() {
    const nextTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'paper' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    safeStorage.setItem(THEME_KEY, nextTheme);
}

// Disable native scroll restoration — it fights with our deferred setup
// and causes the page to jump to a stale position after layout completes.
try { if ('scrollRestoration' in history) {
    if (document.getElementById('subjects-grid')) {
        history.scrollRestoration = 'manual';
    } else {
        history.scrollRestoration = 'auto';
    }
} } catch (e) { console.error('History error', e); }
if (document.getElementById('subjects-grid')) {
    window.scrollTo(0, 0);
    // Double safeguard for browsers that process scroll late
    setTimeout(() => window.scrollTo(0, 0), 10);
}

// Deep linking support for ?open=qID
const urlParams = new URLSearchParams(window.location.search);
const openId = urlParams.get('open');
if (openId) {
    // Wait for skeleton to fade and dom to be ready
    setTimeout(() => {
        const card = document.getElementById(openId);
        if (card) {
            card.open = true;
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }, 500);
}

// ==========================================
// NON-CRITICAL SETUP — deferred until just
// before the CSS page-in animation ends (~300ms).
// This lets the browser paint the first frame
// immediately, then silently wire up all
// interactivity right as the user sees the page.
// ==========================================
const ANIM_DURATION = 280; // ms — matches CSS entry animation duration

function deferUntilAfterAnimation(fn) {
    setTimeout(fn, ANIM_DURATION);
}

// ==========================================
// Progress Bar Update Logic
// ==========================================
function updateProgressBar() {
    const allCheckboxes = document.querySelectorAll('.review-cb');
    if (allCheckboxes.length === 0) return;
    const total = allCheckboxes.length;
    const checked = document.querySelectorAll('.review-cb:checked').length;
    const percentage = (checked / total) * 100;
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    if (progressBar) {
        progressBar.style.width = `${percentage}%`;
        if (total > 0 && checked === total) {
            triggerConfetti();
            showCongratulationModal();
        } else {
            hasCelebrated = false;
        }
    }
    if (progressText) {
        progressText.textContent = `${checked} / ${total}`;
    }
}

function loadReviewState() {
    let reviewed = (() => { try { return JSON.parse(safeStorage.getItem(REVIEWED_KEY) || '{}'); } catch(e) { return {}; } })();
    if (!reviewed || typeof reviewed !== 'object') reviewed = {};
    let hasGhost = false;
    if (reviewed[""]) { delete reviewed[""]; hasGhost = true; }
    if (reviewed["null"]) { delete reviewed["null"]; hasGhost = true; }
    if (hasGhost) safeStorage.setItem(REVIEWED_KEY, JSON.stringify(reviewed));
    document.querySelectorAll('.review-cb').forEach(cb => {
        const cardId = cb.closest('.q-card').id;
        cb.checked = !!reviewed[cardId];
        cb.addEventListener('change', (e) => {
            const currentState = (() => { try { return JSON.parse(safeStorage.getItem(REVIEWED_KEY) || '{}'); } catch(e) { return {}; } })();
            currentState[cardId] = e.target.checked;
            safeStorage.setItem(REVIEWED_KEY, JSON.stringify(currentState));
            updateProgressBar();
        });
    });
    updateProgressBar();
}

// ==========================================
// Toggle All Logic
// ==========================================
function updateToggleButtonState() {
    const toggleAllBtn = document.getElementById('toggleAllBtn');
    if (!toggleAllBtn) return;
    const cards = document.querySelectorAll('.q-card');
    const visibleCards = Array.from(cards).filter(card => card.style.display !== 'none');
    const anyClosed = visibleCards.some(card => !card.hasAttribute('open'));
    toggleAllBtn.textContent = (anyClosed || visibleCards.length === 0) ? 'Reveal All' : 'Collapse All';
}

function toggleAll() {
    const cards = document.querySelectorAll('.q-card');
    const visibleCards = Array.from(cards).filter(card => card.style.display !== 'none');
    const anyClosed = visibleCards.some(card => !card.hasAttribute('open'));
    visibleCards.forEach(card => anyClosed ? card.setAttribute('open', '') : card.removeAttribute('open'));
    updateToggleButtonState();
}

// ==========================================
// Filter / Search Logic
// ==========================================
function applyFilters() {
    const cards = document.querySelectorAll('.q-card');
    const searchInput = document.getElementById('search-box') || document.getElementById('searchInput');
    const filterFeedbackText = document.getElementById('showing-text');
    const noResultsMsg = document.getElementById('no-results');
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const activeUnits = Array.from(document.querySelectorAll('.unit-cb:checked')).map(cb => cb.value);
    const activeBlooms = Array.from(document.querySelectorAll('.bloom-cb:checked')).map(cb => cb.value);
    const activeMarks = Array.from(document.querySelectorAll('.marks-cb:checked')).map(cb => cb.value);
    const importantOnlyCb = document.querySelector('.important-cb');
    const isImportantOnly = importantOnlyCb ? importantOnlyCb.checked : false;
    const reviewedOnlyCb = document.querySelector('.reviewed-filter-cb');
    const isReviewedOnly = reviewedOnlyCb ? reviewedOnlyCb.checked : false;
    let visibleCount = 0;
    const totalCount = cards.length;

    cards.forEach(card => {
        const textContent = card.textContent.toLowerCase();
        const cardUnit = card.getAttribute('data-unit');
        const cardBloom = card.getAttribute('data-bloom');
        const cardMarks = card.getAttribute('data-marks') || (card.querySelector('.marks') ? card.querySelector('.marks').textContent.replace(' Marks', '') : null);
        const cardImportant = card.getAttribute('data-important') === 'true';
        const cardId = card.id;
        const matchesSearch = textContent.includes(searchTerm);
        const matchesUnit = activeUnits.length === 0 || (cardUnit && activeUnits.includes(cardUnit));
        const matchesBloom = activeBlooms.length === 0 || (cardBloom && activeBlooms.includes(cardBloom));
        const matchesMarks = activeMarks.length === 0 || (cardMarks && activeMarks.includes(cardMarks));
        const matchesImportant = !isImportantOnly || cardImportant;
        const cb = card.querySelector('.review-cb');
        const matchesReviewed = !isReviewedOnly || (cb && cb.checked);
        const isVisible = matchesSearch && matchesUnit && matchesBloom && matchesMarks && matchesImportant && matchesReviewed;

        if (isVisible) { card.style.display = ''; visibleCount++; }
        else { card.style.display = 'none'; }

        const tableRow = document.querySelector(`tr[data-target="${cardId}"]`);
        if (tableRow) tableRow.style.display = isVisible ? '' : 'none';
        const navLink = document.querySelector(`.sidebar a[href="#${cardId}"]`);
        if (navLink) navLink.parentElement.style.display = isVisible ? '' : 'none';
    });

    document.querySelectorAll('.nav-group').forEach(group => {
        const visibleLinks = Array.from(group.querySelectorAll('li')).filter(li => li.style.display !== 'none');
        group.style.display = visibleLinks.length === 0 ? 'none' : '';
    });

    const headers = document.querySelectorAll('.segregation-header');
    headers.forEach(header => {
        let hasVisibleCards = false;
        let sibling = header.nextElementSibling;
        while (sibling && !sibling.classList.contains('segregation-header')) {
            if (sibling.classList.contains('q-card') && sibling.style.display !== 'none') { hasVisibleCards = true; break; }
            sibling = sibling.nextElementSibling;
        }
        header.style.display = hasVisibleCards ? '' : 'none';
    });

    if (filterFeedbackText) filterFeedbackText.textContent = `Showing ${visibleCount} of ${totalCount} questions.`;
    if (noResultsMsg) {
        if (visibleCount === 0 && totalCount > 0) {
            noResultsMsg.style.display = 'block';
            if (document.getElementById('quick-ref')) document.getElementById('quick-ref').style.display = 'none';
        } else {
            noResultsMsg.style.display = 'none';
            if (document.getElementById('quick-ref')) document.getElementById('quick-ref').style.display = 'block';
        }
    }
    updateToggleButtonState();
}

// ==========================================
// DEFERRED SETUP — wired up after animation
// ==========================================
deferUntilAfterAnimation(() => {

    try {
        const qCards = document.querySelectorAll('.q-card, .cheat-card');
        if (qCards.length > 0) {
            const cardObserver = new IntersectionObserver((entries, obs) => {
                requestAnimationFrame(() => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            obs.unobserve(entry.target);
                        }
                    });
                });
            }, { threshold: 0.05, rootMargin: '0px 0px 50px 0px' });

            let visibleIndex = 0;
            qCards.forEach((card) => {
                card.classList.add('reveal-on-scroll');
                const rect = card.getBoundingClientRect();
                if (rect.top > 0 && rect.top < window.innerHeight + 100) {
                    const delay = 0.2 + (visibleIndex * 0.08);
                    card.style.transitionDelay = delay + 's';
                    visibleIndex++;
                } else {
                    card.style.transitionDelay = '0.05s';
                }
                cardObserver.observe(card);
            });
        }
    } catch (e) { console.error("Observer Error", e); }
    
    try { loadReviewState(); } catch(e) { console.error("loadReviewState Error", e); }
    try { if (typeof applyFilters === "function") applyFilters(); } catch(e) { console.error("applyFilters Error", e); }

    // Reset button
    const resetProgressBtn = document.getElementById('resetProgressBtn');
    if (resetProgressBtn) {
        resetProgressBtn.addEventListener('click', () => {
            if (confirm("Are you sure you want to reset all your review marks?")) {
                safeStorage.removeItem(REVIEWED_KEY);
                document.querySelectorAll('.review-cb').forEach(cb => { cb.checked = false; });
                updateProgressBar();
            }
        });
    }

    // Toggle all button
    const toggleAllBtn = document.getElementById('toggleAllBtn');
    if (toggleAllBtn) toggleAllBtn.addEventListener('click', toggleAll);

    // Reports use this control; query all elements to stay safe with older
    // report markup that accidentally contained a duplicate id.
    document.querySelectorAll('#themeToggleBtn').forEach(button => {
        button.addEventListener('click', toggleTheme);
    });

    // Card toggle listeners (for collapse/reveal state)
    document.querySelectorAll('.q-card').forEach(card => {
        card.addEventListener('toggle', updateToggleButtonState);
    });

    // Search & filters
    const searchInput = document.getElementById('search-box') || document.getElementById('searchInput');
    if (searchInput) searchInput.addEventListener('input', applyFilters);
    document.querySelectorAll('.filter-toggles input[type="checkbox"], .filter-cb, .reviewed-filter-cb')
        .forEach(cb => cb.addEventListener('change', applyFilters));

    const clearFiltersBtn = document.getElementById('clearFiltersBtn');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            document.querySelectorAll('.filter-toggles input[type="checkbox"], .filter-cb, .reviewed-filter-cb')
                .forEach(cb => cb.checked = false);
            applyFilters();
        });
    }
});

// ==========================================
// Print Stylesheet Fix (must be eager)
// ==========================================
window.addEventListener('beforeprint', () => {
    const cards = document.querySelectorAll('.q-card');
    window._cardPrintStates = Array.from(cards).map(c => c.hasAttribute('open'));
    cards.forEach(c => c.setAttribute('open', ''));
});
window.addEventListener('afterprint', () => {
    const cards = document.querySelectorAll('.q-card');
    cards.forEach((c, i) => {
        if (window._cardPrintStates && window._cardPrintStates[i]) c.setAttribute('open', '');
        else c.removeAttribute('open');
    });
    updateToggleButtonState();
});

// ==========================================
// Smart Topbar Scroll (eager — critical UX)
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    let lastScrollY = window.scrollY;
    let rafScheduled = false;
    const topbar = document.querySelector('.smart-topbar');
    if (topbar) {
        window.addEventListener('scroll', () => {
            if (rafScheduled) return;         // at most 1 rAF per frame
            rafScheduled = true;
            requestAnimationFrame(() => {
                rafScheduled = false;
                if (window.scrollY > 100) {
                    topbar.classList.toggle('hidden', window.scrollY > lastScrollY);
                } else {
                    topbar.classList.remove('hidden');
                }
                lastScrollY = window.scrollY;
            });
        }, { passive: true });
    }
});

// ==========================================
// Subject Name & FAB Logic (eager)
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // FAB Toggle
    const fabBtn = document.getElementById('fabMainBtn');
    const fabMenu = document.getElementById('fabMenu');
    if (fabBtn && fabMenu) {
        fabBtn.addEventListener('click', () => {
            fabMenu.classList.toggle('open');
            fabBtn.classList.toggle('active');
        });
    }
});

document.addEventListener('click', (e) => {
    // 1. Handle glass-modals
    if (e.target.classList.contains('glass-modal')) {
        if (typeof closeModal === 'function') {
            closeModal(e.target.id);
        } else {
            e.target.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    // 2. Handle Assistant widget click outside
    const assistant = document.getElementById('assistantModal');
    if (assistant && assistant.style.display === 'flex') {
        const isClickInside = assistant.contains(e.target);
        const isClickOnToggle = e.target.closest('.ask-ai-btn');
        if (!isClickInside && !isClickOnToggle && !window.isAssistantPinned) {
            if (typeof closeAssistant === 'function') closeAssistant();
        }
    }

    // 3. Close glass modal on anchor link click
    if (e.target.tagName === 'A' && e.target.getAttribute('href') && e.target.getAttribute('href').startsWith('#') && e.target.closest('.glass-modal')) {
        const modal = e.target.closest('.glass-modal');
        if (typeof closeModal === 'function') {
            closeModal(modal.id);
        } else {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
});




// ==========================================
// Completion Celebration (Confetti)
// ==========================================
function triggerConfetti() {
    if (hasCelebrated) return;
    hasCelebrated = true;
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#f43f5e', '#8b5cf6'];
    for (let i = 0; i < 150; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `position:fixed;width:${Math.random()*8+6}px;height:${Math.random()*12+8}px;background:${colors[Math.floor(Math.random()*colors.length)]};top:-20px;left:${Math.random()*100}vw;z-index:999999;opacity:1;pointer-events:none;`;
        document.body.appendChild(confetti);
        const dur = (Math.random() * 2 + 2.5) * 1000;
        confetti.animate([
            { transform: 'translate3d(0,0,0) rotate(0deg)', opacity: 1 },
            { transform: `translate3d(${Math.random()*300-150}px,105vh,0) rotate(${Math.random()*1000}deg)`, opacity: 0 }
        ], { duration: dur, easing: 'cubic-bezier(.37,0,.63,1)' });
        setTimeout(() => confetti.remove(), dur);
    }
}
window.triggerConfetti = triggerConfetti;

function showCongratulationModal() {
    if (document.getElementById('congratsModal')) return;
    const isMidterm = window.location.pathname.includes('midterm-important.html');
    const trophy = isMidterm ? '🥈' : '🏆';
    const message = isMidterm
        ? 'You have reviewed all the highly important midterm questions! You are on track for success!'
        : 'You have reviewed every single question in this bank. You are fully prepared for your exam!';
    document.body.insertAdjacentHTML('beforeend', `
    <div id="congratsModal" class="glass-modal active" style="z-index:100000;transition:none;">
        <div class="modal-content" style="text-align:center;max-width:400px;padding:3rem;background:rgba(10,10,12,0.8);backdrop-filter:blur(24px);">
            <div style="font-size:4rem;margin-bottom:1rem;">${trophy}</div>
            <h2 style="margin-bottom:1rem;background:linear-gradient(to right,var(--subject-color),#fff);-webkit-background-clip:text;color:transparent;">Congratulations!</h2>
            <p style="margin-bottom:2rem;color:#a0a0a5;">${message}</p>
            <button class="btn btn-primary" style="width:100%;" onclick="document.getElementById('congratsModal').remove();">Awesome</button>
        </div>
    </div>`);
}

// ==========================================
// Mark All as Reviewed
// ==========================================
window.markAllReviewed = function() {
    const allCb = document.querySelectorAll('.review-cb');
    const checkedCount = document.querySelectorAll('.review-cb:checked').length;
    const isAllMarked = (checkedCount === allCb.length && allCb.length > 0);
    const currentState = (() => { try { return JSON.parse(safeStorage.getItem(REVIEWED_KEY) || '{}'); } catch(e) { return {}; } })();
    allCb.forEach(cb => {
        cb.checked = !isAllMarked;
        const card = cb.closest('.q-card');
        if (card && card.id) currentState[card.id] = !isAllMarked;
    });
    safeStorage.setItem(REVIEWED_KEY, JSON.stringify(currentState));
    updateProgressBar();
    const fabLabel = document.querySelector('button[onclick*="markAllReviewed"] span');
    if (fabLabel) fabLabel.innerText = isAllMarked ? "Mark All" : "Unmark All";
};

// ==========================================
// Flashcards System
// ==========================================
let flashcardQuestions = [];
let currentFcIndex = 0;

window.startFlashcards = function() {
    const visibleCards = Array.from(document.querySelectorAll('.q-card')).filter(c => c.style.display !== 'none');
    if (visibleCards.length === 0) { alert("No questions available for flashcards! Adjust your filters."); return; }
    flashcardQuestions = visibleCards.map(card => ({
        id: card.id,
        q_num: card.querySelector('h3') ? card.querySelector('h3').innerText : 'Unknown',
        badges: card.querySelector('.badges') ? card.querySelector('.badges').innerHTML : '',
        answer: card.querySelector('.answer-content') ? card.querySelector('.answer-content').innerHTML : '<p>No answer available</p>'
    }));
    // Fisher-Yates shuffle
    for (let i = flashcardQuestions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [flashcardQuestions[i], flashcardQuestions[j]] = [flashcardQuestions[j], flashcardQuestions[i]];
    }
    currentFcIndex = 0;
    renderFlashcard();
    openModal('studyModal');
};

function renderFlashcard() {
    if (flashcardQuestions.length === 0) return;
    const q = flashcardQuestions[currentFcIndex];
    document.getElementById('flashcard-inner').classList.remove('flipped');
    setTimeout(() => {
        document.getElementById('fc-question').innerText = q.q_num;
        document.getElementById('fc-badge').innerHTML = q.badges;
        document.getElementById('fc-answer').innerHTML = q.answer;
        const backQ = document.getElementById('fc-back-question');
        if (backQ) backQ.innerText = q.q_num;
    }, 150);
}

window.nextFlashcard = function() { currentFcIndex = (currentFcIndex + 1) % flashcardQuestions.length; renderFlashcard(); };
window.prevFlashcard = function() { currentFcIndex = (currentFcIndex - 1 + flashcardQuestions.length) % flashcardQuestions.length; renderFlashcard(); };
window.shuffleFlashcards = function() {
    for (let i = flashcardQuestions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [flashcardQuestions[i], flashcardQuestions[j]] = [flashcardQuestions[j], flashcardQuestions[i]];
    }
    currentFcIndex = 0;
    renderFlashcard();
};

// ==========================================
// Quiz Mode (legacy modal-based)
// ==========================================
let quizQueue = [];
let currentQuizIndex = 0;
let quizScore = 0;
const QUIZ_LENGTH = 10;

window.startQuiz = function() {
    let pool = Array.from(document.querySelectorAll('.q-card')).filter(c => { const cb = c.querySelector('.review-cb'); return cb && !cb.checked; });
    if (pool.length < QUIZ_LENGTH) {
        pool = pool.concat(Array.from(document.querySelectorAll('.q-card')).filter(c => { const cb = c.querySelector('.review-cb'); return cb && cb.checked; }));
    }
    if (pool.length === 0) { alert("No questions available to quiz!"); return; }
    for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
    quizQueue = pool.slice(0, Math.min(QUIZ_LENGTH, pool.length));
    currentQuizIndex = 0; quizScore = 0;
    document.getElementById('quiz-setup').style.display = 'none';
    document.getElementById('quiz-result').style.display = 'none';
    document.getElementById('quiz-active').style.display = 'flex';
    renderQuizCard();
};

function renderQuizCard() {
    if (currentQuizIndex >= quizQueue.length) {
        document.getElementById('quiz-active').style.display = 'none';
        document.getElementById('quiz-result').style.display = 'block';
        document.getElementById('quiz-final-score').innerText = quizScore;
        document.getElementById('quiz-total-score').innerText = quizQueue.length;
        if (quizScore === quizQueue.length && quizQueue.length > 0) triggerConfetti();
        return;
    }
    const card = quizQueue[currentQuizIndex];
    const h3 = card.querySelector('h3');
    const answer = card.querySelector('.answer-content');
    document.getElementById('quiz-progress-text').innerText = `Question ${currentQuizIndex + 1} of ${quizQueue.length}`;
    document.getElementById('quiz-score-text').innerText = `Score: ${quizScore}`;
    document.getElementById('quiz-question').innerText = h3 ? h3.innerText : 'Question';
    document.getElementById('quiz-answer').innerHTML = answer ? answer.innerHTML : '';
    document.getElementById('quiz-question').style.marginBottom = 'auto';
    document.getElementById('quiz-answer-container').style.display = 'none';
    document.getElementById('quiz-controls-reveal').style.display = 'flex';
    document.getElementById('quiz-controls-grade').style.display = 'none';
}

window.revealQuizAnswer = function() {
    document.getElementById('quiz-question').style.marginBottom = '0';
    document.getElementById('quiz-answer-container').style.display = 'block';
    document.getElementById('quiz-controls-reveal').style.display = 'none';
    document.getElementById('quiz-controls-grade').style.display = 'flex';
};

window.gradeQuiz = function(knewIt) {
    if (knewIt) {
        quizScore++;
        const card = quizQueue[currentQuizIndex];
        const cb = card.querySelector('.review-cb');
        if (cb && !cb.checked) {
            cb.checked = true;
            const s = (() => { try { return JSON.parse(safeStorage.getItem(REVIEWED_KEY) || '{}'); } catch(e) { return {}; } })();
            s[card.id] = true;
            safeStorage.setItem(REVIEWED_KEY, JSON.stringify(s));
            updateProgressBar();
        }
    }
    currentQuizIndex++;
    renderQuizCard();
};

window.clearFilters = function() {
    const searchInput = document.getElementById('search-box') || document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = '';
    }
    document.querySelectorAll('.filter-toggles input[type="checkbox"], .filter-cb, .reviewed-filter-cb')
        .forEach(cb => cb.checked = false);
    
    // Explicitly call applyFilters to update the UI
    if (typeof applyFilters === 'function') {
        applyFilters();
    }
};

// ==========================================
// PDF Download Logic
// ==========================================
window.downloadPDF = function() {
    // 1. Expand all accordions so content is visible in PDF
    document.querySelectorAll('details.q-card').forEach(d => {
        d.setAttribute('open', '');
    });
    
    // 2. Remove entry animations to prevent blank pages if PDF triggers fast
    document.querySelectorAll('.reveal-on-scroll').forEach(el => {
        el.style.transition = 'none';
        el.style.opacity = '1';
        el.style.transform = 'none';
        el.classList.add('visible');
    });

    // 3. Trigger print after layout update
    setTimeout(() => {
        window.print();
    }, 150);
};


// ==========================================
// ==========================================
// Draggable Assistant Widget
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('assistantModal');
    if (!modal) return;
    
    // Add 10px padding as requested
    modal.style.padding = '10px';
    
    let isDragging = false;
    let startX, startY;
    let initialModalLeft, initialModalTop;
    let hasDragged = false; 

    function startDrag(e) {
        if (window.innerWidth <= 768) return; // Disable dragging on mobile
        
        // Allow native resizing: don't drag if clicking the bottom-right corner (15x15px resize handle)
        const rect = modal.getBoundingClientRect();
        const isResizeClick = (e.clientX - rect.left > rect.width - 20) && (e.clientY - rect.top > rect.height - 20);
        if (isResizeClick) return;
        
        // ONLY allow dragging if clicking the modal's 10px padding OR the header
        if (e.target !== modal && !e.target.closest('.modal-header')) return;
        
        // Don't drag if clicking buttons, inputs, or selects inside the header
        if (e.target.closest('button') || e.target.closest('select') || e.target.closest('input')) return;
        
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        let oldTransition = modal.style.transition;
        modal.style.transition = 'none';
        
        let oldTransform = modal.style.transform;
        const modalRect = modal.getBoundingClientRect();
        
        if (!hasDragged && oldTransform !== 'none' && oldTransform !== '') {
            initialModalLeft = modalRect.left;
            initialModalTop = modalRect.top;
            hasDragged = true;
        } else {
            initialModalLeft = modal.offsetLeft;
            initialModalTop = modal.offsetTop;
        }

        modal.style.bottom = 'auto';
        modal.style.right = 'auto';
        modal.style.left = initialModalLeft + 'px';
        modal.style.top = initialModalTop + 'px';
        modal.style.transform = 'none';
        
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
        
        e.preventDefault();
    }

    // Make the modal background and header indicate they are draggable
    modal.style.cursor = 'move';
    const header = modal.querySelector('.modal-header');
    if (header) header.style.cursor = 'move';
    
    // Reset cursor for the inner content wrapper so text selection feels normal
    const body = modal.querySelector('.modal-body');
    if (body) body.style.cursor = 'default';
    
    modal.addEventListener('mousedown', startDrag);

    function onMouseMove(e) {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        
        let newModalLeft = initialModalLeft + dx;
        let newModalTop = initialModalTop + dy;
        
        const mw = modal.offsetWidth || 400;
        const mh = modal.offsetHeight || 600;
        const minX = -mw + 100; 
        const maxX = window.innerWidth - 100; 
        const minY = -mh + 100; 
        const maxY = window.innerHeight - 100; 
        
        newModalLeft = Math.max(minX, Math.min(newModalLeft, maxX));
        newModalTop = Math.max(minY, Math.min(newModalTop, maxY));
        
        modal.style.left = newModalLeft + 'px';
        modal.style.top = newModalTop + 'px';
    }

    function onMouseUp(e) {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }
});

// ==========================================
// Auth UI Initialization
// ==========================================
document.addEventListener('DOMContentLoaded', async () => {
    try {
        if (window.navigator && window.navigator.userAgent.includes('jsdom')) return;
        const path = './auth-ui.js';
        const { initAuthUI } = await import(path);
        initAuthUI();
    } catch (e) {
        console.warn('Failed to load Auth UI. Running in offline/guest mode.', e);
    }
});
document.addEventListener('click', (e) => {
    const fabMenu = document.getElementById('fabMenu');
    const fabBtn = document.getElementById('fabMainBtn');
    if (fabMenu && fabBtn && fabMenu.classList.contains('open')) {
        if (!fabMenu.contains(e.target) && !fabBtn.contains(e.target)) {
            fabMenu.classList.remove('open');
            fabBtn.classList.remove('active');
        }
    }
});

window.openModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
        const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        if (scrollbarWidth > 0) {
            document.body.style.paddingRight = scrollbarWidth + 'px';
            modal.style.paddingRight = scrollbarWidth + 'px';
            const topbar = document.querySelector('.smart-topbar');
            if (topbar) topbar.style.paddingRight = `calc(var(--space-4) + ${scrollbarWidth}px)`;
            const fab = document.querySelector('.fab-container');
            if (fab && window.innerWidth > 768) fab.style.right = `calc(2rem + ${scrollbarWidth}px)`;
            const prog = document.getElementById('stickyProgressWidget');
            if (prog && window.innerWidth > 768) prog.style.right = `calc(2rem + ${scrollbarWidth}px)`;
        }
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};

window.closeModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        modal.style.paddingRight = '';
        const topbar = document.querySelector('.smart-topbar');
        if (topbar) topbar.style.paddingRight = '';
        const fab = document.querySelector('.fab-container');
        if (fab) fab.style.right = '';
        const prog = document.getElementById('stickyProgressWidget');
        if (prog) prog.style.right = '';
    }
};


// SVG Lightbox Logic with Smooth Overlay
document.addEventListener('DOMContentLoaded', () => {
    // Create overlay container
    const overlay = document.createElement('div');
    overlay.id = 'svg-overlay';
    document.body.appendChild(overlay);

    const closeOverlay = () => {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            overlay.innerHTML = '';
        }, 300); // Wait for transition
    };

    overlay.addEventListener('click', closeOverlay);

    const svgs = document.querySelectorAll('.report-main svg');
    svgs.forEach(svg => {
        const w = svg.getAttribute('width');
        const h = svg.getAttribute('height');
        // Skip small UI icons
        if (w === "16" || w === "18" || w === "20" || w === "24" || h === "16" || h === "18" || h === "20" || h === "24") {
            return;
        }
        
        svg.addEventListener('click', (e) => {
            e.stopPropagation();
            const clone = svg.cloneNode(true);
            
            // Remove any inline styles that might restrict the clone
            clone.style.maxHeight = '80vh';
            clone.style.maxWidth = '700px'; // Sensible limit so it doesn't stretch massively
            clone.style.width = '100%';
            clone.style.height = 'auto';
            
            overlay.innerHTML = '';
            overlay.appendChild(clone);
            
            // Trigger reflow for animation
            void overlay.offsetWidth;
            
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay.classList.contains('active')) {
            closeOverlay();
        }
    });
});

// ScrollSpy for Table of Contents
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.report-sidebar');
    if (!sidebar) return;

    const links = Array.from(sidebar.querySelectorAll('a[href^="#"]'));
    if (links.length === 0) return;

    const sections = links.map(link => {
        const id = link.getAttribute('href').substring(1);
        const target = document.getElementById(id);
        return target ? { link, target } : null;
    }).filter(Boolean);

    let lastActive = null;

    function updateScrollSpy() {
        const scrollPosition = window.scrollY + 200; // offset for topbar and breathing room
        
        let current = null;
        for (let i = sections.length - 1; i >= 0; i--) {
            if (sections[i].target.offsetTop <= scrollPosition) {
                current = sections[i];
                break;
            }
        }

        if (!current && sections.length > 0) {
            current = sections[0];
        }

        if (current && current.link !== lastActive) {
            links.forEach(l => l.classList.remove('active'));
            current.link.classList.add('active');
            lastActive = current.link;

            // Scroll the sidebar itself if the active item is out of view
            const sidebarRect = sidebar.getBoundingClientRect();
            const linkRect = current.link.getBoundingClientRect();
            
            // Only auto-scroll if it's out of bounds
            if (linkRect.top < sidebarRect.top || linkRect.bottom > sidebarRect.bottom) {
                sidebar.scrollTo({
                    top: current.link.offsetTop - sidebar.offsetHeight / 2,
                    behavior: 'smooth'
                });
            }
        }
    }

    // Use requestAnimationFrame for smooth, non-blocking scroll spy
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateScrollSpy();
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
    
    // Initial trigger
    setTimeout(updateScrollSpy, 100);
});
