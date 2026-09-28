// ==========================================
// CRITICAL PATH — runs immediately (no defer)
// Theme must apply before first paint to avoid flash
// ==========================================
const pathParts = window.location.pathname.split('/');
const subjectName = pathParts[pathParts.length - 2] || 'default';
const THEME_KEY = 'global_theme';
const REVIEWED_KEY = subjectName + '_reviewed';
let hasCelebrated = false;

// Apply theme immediately to avoid FOUC
const savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);

// Disable native scroll restoration — it fights with our deferred setup
// and causes the page to jump to a stale position after layout completes.
if ('scrollRestoration' in history) {
    if (document.getElementById('subjects-grid')) {
        history.scrollRestoration = 'manual';
    } else {
        history.scrollRestoration = 'auto';
    }
}
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
    // Wait for animation to nearly complete, then use requestIdleCallback
    // for zero-jank setup during the browser's free time.
    setTimeout(() => {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(fn, { timeout: 500 });
        } else {
            fn(); // Safari fallback
        }
    }, ANIM_DURATION);
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
    let reviewed = JSON.parse(localStorage.getItem(REVIEWED_KEY) || '{}');
    let hasGhost = false;
    if (reviewed[""]) { delete reviewed[""]; hasGhost = true; }
    if (reviewed["null"]) { delete reviewed["null"]; hasGhost = true; }
    if (hasGhost) localStorage.setItem(REVIEWED_KEY, JSON.stringify(reviewed));
    document.querySelectorAll('.review-cb').forEach(cb => {
        const cardId = cb.closest('.q-card').id;
        cb.checked = !!reviewed[cardId];
        cb.addEventListener('change', (e) => {
            const currentState = JSON.parse(localStorage.getItem(REVIEWED_KEY) || '{}');
            currentState[cardId] = e.target.checked;
            localStorage.setItem(REVIEWED_KEY, JSON.stringify(currentState));
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
    const filterFeedbackText = document.getElementById('filter-feedback-text');
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

    // Add staggered entrance animations to cards (q-cards and cheat-cards)
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
            // Stagger only initially visible elements above the fold
            if (rect.top > 0 && rect.top < window.innerHeight + 100) {
                // Wait for skeleton to start fading (~0.2s from now) + stagger
                const delay = 0.2 + (visibleIndex * 0.08);
                card.style.transitionDelay = delay + 's';
                visibleIndex++;
            } else {
                card.style.transitionDelay = '0.05s';
            }
            cardObserver.observe(card);
        });
    }
    // Review state & progress bar
    loadReviewState();
    if (typeof applyFilters === "function") applyFilters();

    // Reset button
    const resetProgressBtn = document.getElementById('resetProgressBtn');
    if (resetProgressBtn) {
        resetProgressBtn.addEventListener('click', () => {
            if (confirm("Are you sure you want to reset all your review marks?")) {
                localStorage.removeItem(REVIEWED_KEY);
                document.querySelectorAll('.review-cb').forEach(cb => { cb.checked = false; });
                updateProgressBar();
            }
        });
    }

    // Toggle all button
    const toggleAllBtn = document.getElementById('toggleAllBtn');
    if (toggleAllBtn) toggleAllBtn.addEventListener('click', toggleAll);

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
        document.addEventListener('click', (e) => {
    // 1. Handle glass-modals
    if (e.target.classList.contains('glass-modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
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
});
    }
});
document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href') && e.target.getAttribute('href').startsWith('#') && e.target.closest('.glass-modal')) {
        e.target.closest('.glass-modal').classList.remove('active');
        document.body.style.overflow = '';
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
    const currentState = JSON.parse(localStorage.getItem(REVIEWED_KEY) || '{}');
    allCb.forEach(cb => {
        cb.checked = !isAllMarked;
        const card = cb.closest('.q-card');
        if (card && card.id) currentState[card.id] = !isAllMarked;
    });
    localStorage.setItem(REVIEWED_KEY, JSON.stringify(currentState));
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
            const s = JSON.parse(localStorage.getItem(REVIEWED_KEY) || '{}');
            s[card.id] = true;
            localStorage.setItem(REVIEWED_KEY, JSON.stringify(s));
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
// Draggable Assistant Widget & Button
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('assistantModal');
    const fab = document.querySelector('.ask-ai-btn');
    if (!modal) return;
    
    const header = modal.querySelector('.modal-header');
    
    let isDragging = false;
    let startX, startY;
    let initialModalLeft, initialModalTop;
    let initialFabLeft, initialFabTop;
    let dragTarget = null;
    let hasDragged = false; // Flag to indicate if we've switched to absolute positioning
    let fabOffsetY = 0; // Relative offset to keep them perfectly locked // 'header' or 'fab'

    function startDrag(e, targetType) {
        if (window.innerWidth <= 768) return; // Disable dragging on mobile devices
        if (e.target.closest('button:not(.ask-ai-btn)') || e.target.closest('label') || e.target.closest('input')) return;
        
        isDragging = true;
        dragTarget = targetType;
        startX = e.clientX;
        startY = e.clientY;
        
        let oldTransform = modal.style.transform;
        modal.style.transform = 'none';
        let modalRect = modal.getBoundingClientRect();
        if (modal.style.display === 'none') {
            // Modal is hidden, temporarily show it to get its true size/position
            modal.style.visibility = 'hidden';
            modal.style.display = 'flex';
            modalRect = modal.getBoundingClientRect();
            modal.style.display = 'none';
            modal.style.visibility = 'visible';
        }
        modal.style.transform = oldTransform;
        
        initialModalLeft = modalRect.left;
        initialModalTop = modalRect.top;
        
        // If it's still 0 (e.g. initial load), use computed style or defaults
        if (initialModalLeft === 0 && initialModalTop === 0 && fab) {
            const fRect = fab.getBoundingClientRect();
            initialModalLeft = fRect.left;
            initialModalTop = fRect.top - 620; // approximate height + padding
        }
        
        if (fab) {
            const fabRect = fab.getBoundingClientRect();
            initialFabLeft = fabRect.left;
            initialFabTop = fabRect.top;
        }

        // Convert bottom/right constraints to left/top so they can be dragged freely
        modal.style.bottom = 'auto';
        modal.style.right = 'auto';
        modal.style.left = initialModalLeft + 'px';
        modal.style.top = initialModalTop + 'px';
        modal.style.transform = 'none';
        
        if (fab) {
            fab.style.bottom = 'auto';
            fab.style.right = 'auto';
            fab.style.left = initialFabLeft + 'px';
            fab.style.top = initialFabTop + 'px';
        }
        
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
        
        if (targetType === 'fab') {
            // Prevent the click from opening/closing immediately if it was a drag
            e.stopPropagation();
        } else {
            e.preventDefault();
        }
    }

    if (header) {
        header.style.cursor = 'move';
        header.addEventListener('mousedown', (e) => startDrag(e, 'header'));
    }
    
    if (fab) {
        // We use a small threshold to distinguish drag from click
        let isFabClick = true;
        fab.style.cursor = 'move';
        fab.addEventListener('mousedown', (e) => {
            isFabClick = true;
            startDrag(e, 'fab');
        });
        
        // Wrap openAssistant to prevent it if we dragged
        const oldOnclick = fab.onclick;
        fab.onclick = (e) => {
            if (!isFabClick) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
            if (oldOnclick) oldOnclick.call(fab, e);
        };
    }

    function onMouseMove(e) {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        
        // If moved more than 3px, it's a drag, not a click
        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
            if (fab && dragTarget === 'fab') fab.isFabClick = false; // We use a local closure variable but fab.isFabClick is safer?
            // Actually, we just need to set the outer scoped isFabClick
            if (fab) fab.isFabClick = false; // We'll just check this inside onclick if we can. 
            // Wait, I can't easily modify the closure var from here. Let's just set a property on the element.
        }

        modal.style.left = (initialModalLeft + dx) + 'px';
        modal.style.top = (initialModalTop + dy) + 'px';
        
        if (fab) {
            fab.style.left = (initialFabLeft + dx) + 'px';
            fab.style.top = (initialFabTop + dy) + 'px';
            if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
                fab.setAttribute('data-dragged', 'true');
            }
        }
    }

    function onMouseUp(e) {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        
        if (fab) {
            setTimeout(() => {
                fab.removeAttribute('data-dragged');
            }, 50);
        }
    }
});

// OVERRIDE ALL CLICK OUTSIDE LOGIC
document.addEventListener('click', (e) => {
    // 1. Handle glass-modals
    if (e.target.classList.contains('glass-modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
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
}, true); // Use capture to intercept early

// ==========================================
// Draggable Assistant Widget & Button
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('assistantModal');
    const fab = document.querySelector('.ask-ai-btn');
    if (!modal) return;
    
    const header = modal.querySelector('.modal-header');
    
    let isDragging = false;
    let startX, startY;
    let initialModalLeft, initialModalTop;
    let initialFabLeft, initialFabTop;
    let dragTarget = null;
    let hasDragged = false; // Flag to indicate if we've switched to absolute positioning
    let fabOffsetY = 0; // Relative offset to keep them perfectly locked

    function startDrag(e, targetType) {
        if (window.innerWidth <= 768) return; // Disable dragging on mobile devices
        if (e.target.closest('button:not(.ask-ai-btn)') || e.target.closest('label') || e.target.closest('input')) return;
        
        isDragging = true;
        dragTarget = targetType;
        startX = e.clientX;
        startY = e.clientY;
        
        // Prevent CSS transitions from animating the transform to 'none', which breaks measurements
        let oldTransition = modal.style.transition;
        let oldFabTransition = fab ? fab.style.transition : '';
        modal.style.transition = 'none';
        if (fab) fab.style.transition = 'none';
        
        let oldTransform = modal.style.transform;
        let oldFabTransform = fab ? fab.style.transform : '';
        modal.style.transform = 'none';
        if (fab) fab.style.transform = 'none'; 
        
        // Force reflow so the instant snap takes effect
        void modal.offsetWidth;
        if (fab) void fab.offsetWidth;
        
        let modalRect = modal.getBoundingClientRect();
        if (modal.style.display === 'none') {
            modal.style.visibility = 'hidden';
            modal.style.display = 'flex';
            modalRect = modal.getBoundingClientRect();
            modal.style.display = 'none';
            modal.style.visibility = 'visible';
        }
        
        initialModalLeft = modalRect.left;
        initialModalTop = modalRect.top;
        
        if (fab) {
            const fabRect = fab.getBoundingClientRect();
            initialFabLeft = fabRect.left;
            initialFabTop = fabRect.top;
        }
        
        modal.style.transform = oldTransform;
        if (fab) fab.style.transform = oldFabTransform;
        
        // Restore transitions
        modal.style.transition = oldTransition;
        if (fab) fab.style.transition = oldFabTransition;

        // If it's the first drag, compute their relative offset
        if (!hasDragged && fab) {
            fabOffsetY = initialFabTop - initialModalTop;
            hasDragged = true;
        }

        modal.style.bottom = 'auto';
        modal.style.right = 'auto';
        modal.style.left = initialModalLeft + 'px';
        modal.style.top = initialModalTop + 'px';
        
        if (fab) {
            fab.style.bottom = 'auto';
            fab.style.right = 'auto';
            fab.style.left = initialFabLeft + 'px';
            fab.style.top = initialFabTop + 'px';
        }
        
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
        
        if (targetType === 'fab') {
            e.stopPropagation();
        } else {
            e.preventDefault();
        }
    }

    if (header) {
        header.style.cursor = 'move';
        header.addEventListener('mousedown', (e) => startDrag(e, 'header'));
    }
    
    if (fab) {
        let isFabClick = true;
        fab.style.cursor = 'move';
        fab.addEventListener('mousedown', (e) => {
            isFabClick = true;
            startDrag(e, 'fab');
        });
        
        const oldOnclick = fab.onclick;
        fab.onclick = (e) => {
            if (!isFabClick || fab.getAttribute('data-dragged') === 'true') {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
            if (oldOnclick) oldOnclick.call(fab, e);
        };
    }

    function onMouseMove(e) {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        
        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
            if (fab && dragTarget === 'fab') {
                fab.setAttribute('data-dragged', 'true');
            }
        }

        let newModalLeft = initialModalLeft + dx;
        let newModalTop = initialModalTop + dy;
        
        // Enforce relaxed window bounds (allow partial off-screen dragging but never lose it)
        const mw = modal.offsetWidth || 400;
        const mh = modal.offsetHeight || 600;
        const minX = -mw + 100; // keep at least 100px visible on the left
        const maxX = window.innerWidth - 100; // keep at least 100px visible on the right
        const minY = -mh + 100; // keep at least 100px visible on the top
        const maxY = window.innerHeight - 100; // keep at least 100px visible on the bottom
        
        newModalLeft = Math.max(minX, Math.min(newModalLeft, maxX));
        newModalTop = Math.max(minY, Math.min(newModalTop, maxY));
        
        modal.style.left = newModalLeft + 'px';
        modal.style.top = newModalTop + 'px';
        
        if (fab) {
            // Force the FAB to stay mathematically locked to the modal
            fab.style.left = newModalLeft + 'px';
            fab.style.top = (newModalTop + fabOffsetY) + 'px';
        }
    }

    function onMouseUp(e) {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        
        if (fab) {
            setTimeout(() => {
                fab.removeAttribute('data-dragged');
            }, 50);
        }
    }
});
