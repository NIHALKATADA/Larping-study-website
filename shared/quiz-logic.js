let totalScore = 0;
let totalQs = 0;

document.addEventListener("DOMContentLoaded", () => {
    const allCards = Array.from(document.querySelectorAll('.quiz-card'));
    
    // Shuffle
    for (let i = allCards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [allCards[i], allCards[j]] = [allCards[j], allCards[i]];
    }
    
    const selectedCards = allCards.slice(0, 10);
    totalQs = selectedCards.length;
    
    const container = document.getElementById('quiz-list');
    if (!container) return;
    
    container.innerHTML = ''; 
    
    selectedCards.forEach((card, index) => {
        card.style.display = 'block';
        const numSpan = card.querySelector('.q-number');
        if (numSpan) numSpan.innerText = `Q${index + 1}.`;
        container.appendChild(card);
    });
    
    const scoreDisplay = document.getElementById('final-score-display');
    if (scoreDisplay) scoreDisplay.innerText = `Score: 0 / ${totalQs}`;
    
    const finalScoreContainer = document.getElementById('final-score-container');
    if (finalScoreContainer) finalScoreContainer.style.display = 'block';
});

function selectOption(el) {
    const siblings = el.parentElement.querySelectorAll('.mcq-option');
    siblings.forEach(s => s.classList.remove('selected'));
    el.classList.add('selected');
}

function verifyAnswer(btn) {
    const card = btn.closest('.quiz-card');
    if (card.classList.contains('verified')) return;
    const type = card.getAttribute('data-type');
    const correctStr = card.getAttribute('data-correct').toLowerCase().trim();
    let userStr = "";
    if (type === 'mcq') {
        const selected = card.querySelector('.selected');
        if (!selected) { alert("Please select an option!"); return; }
        userStr = selected.innerText.toLowerCase().trim();
    } else if (type === 'code') {
        userStr = card.querySelector('.code-input').value.toLowerCase().trim();
    } else {
        userStr = card.querySelector('.short-answer-input').value.toLowerCase().trim();
    }
    if (!userStr) { alert("Please provide an answer!"); return; }
    card.classList.add('verified');
    card.querySelector('.action-buttons').style.display = 'none';
    const feedback = card.querySelector('.feedback-box');
    feedback.style.display = 'block';
    const isCorrect = userStr === correctStr || (type !== 'mcq' && correctStr.includes(userStr) && userStr.length > 3);
    if (isCorrect) {
        feedback.classList.add('correct');
        feedback.querySelector('.feedback-title').innerText = "✅ Correct!";
        totalScore++;
    } else {
        feedback.classList.add('incorrect');
        feedback.querySelector('.feedback-title').innerText = `❌ Incorrect. The expected answer was: ${card.getAttribute('data-correct')}`;
        const overBtn = feedback.querySelector('.override-btn');
        if(overBtn) overBtn.style.display = 'inline-block';
    }
    const scoreDisplay = document.getElementById('final-score-display');
    if (scoreDisplay) scoreDisplay.innerText = `Score: ${totalScore} / ${totalQs}`;
}

function revealAnswer(btn) {
    const card = btn.closest('.quiz-card');
    if (card.classList.contains('verified')) return;
    card.classList.add('verified');
    card.querySelector('.action-buttons').style.display = 'none';
    const feedback = card.querySelector('.feedback-box');
    feedback.style.display = 'block';
    feedback.classList.add('incorrect');
    feedback.querySelector('.feedback-title').innerText = `👀 Revealed Answer: ${card.getAttribute('data-correct')}`;
}

function overrideCorrect(btn) {
    const feedback = btn.closest('.feedback-box');
    if (feedback.classList.contains('overridden')) return;
    feedback.classList.remove('incorrect');
    feedback.classList.add('correct');
    feedback.classList.add('overridden');
    feedback.querySelector('.feedback-title').innerText = "✅ Correct! (Overridden)";
    btn.style.display = 'none';
    totalScore++;
    const scoreDisplay = document.getElementById('final-score-display');
    if (scoreDisplay) scoreDisplay.innerText = `Score: ${totalScore} / ${totalQs}`;
}
