// --- STATE MANAGEMENT ---
const state = {
    questions: [],
    currentIndex: 0,
    timerInterval: null
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', async () => {
    await loadQuestions();
    initTimer();
    renderQuestion();
});

async function loadQuestions() {
    try {
        const res = await fetch(`/api/attempt/${CONFIG.attemptId}/questions`);
        state.questions = await res.json();
    } catch (err) {
        alert("Failed to load quiz data.");
    }
}

// --- TIMER LOGIC ---
function initTimer() {
    if (CONFIG.timeRemaining === null) {
        document.getElementById('timer-display').innerText = "Unlimited Time";
        return;
    }

    let secondsLeft = CONFIG.timeRemaining;

    state.timerInterval = setInterval(() => {
        secondsLeft--;
        
        // Format MM:SS
        const m = Math.floor(secondsLeft / 60);
        const s = secondsLeft % 60;
        document.getElementById('timer-display').innerText = 
            `${m}:${s < 10 ? '0' : ''}${s}`;

        if (secondsLeft <= 0) {
            clearInterval(state.timerInterval);
            alert("Time's up! Submitting...");
            submitQuiz();
        }
    }, 1000);
}

// --- RENDERING ENGINE ---
function renderQuestion() {
    const container = document.getElementById('app-root');
    const q = state.questions[state.currentIndex];
    
    // Safety check
    if (!q) return;

    // Generate Options HTML
    const optionsHtml = q.options.map(opt => {
        const isSelected = q.selected_option === opt.id ? 'selected' : '';
        return `<button class="option ${isSelected}" 
                        onclick="handleSelection(${opt.id}, this)">
                    ${opt.text}
                </button>`;
    }).join('');

    // Generate Controls
    const isFirst = state.currentIndex === 0;
    const isLast = state.currentIndex === state.questions.length - 1;

    container.innerHTML = `
        <div class="question-card">
            <h3>Question ${state.currentIndex + 1} of ${state.questions.length}</h3>
            <p style="font-size: 1.2rem;">${q.text}</p>
            <div id="options-list">${optionsHtml}</div>
        </div>
        <div class="controls">
            <button onclick="changeQuestion(-1)" ${isFirst ? 'disabled' : ''}>Previous</button>
            ${isLast 
                ? `<button onclick="submitQuiz()" style="background:#4CAF50; color:white;">Finish Quiz</button>` 
                : `<button onclick="changeQuestion(1)">Next</button>`
            }
        </div>
    `;
}

// --- INTERACTION HANDLERS ---
async function handleSelection(optionId, btnElement) {
    // 1. UI Update (Visual Feedback)
    document.querySelectorAll('.option').forEach(b => b.classList.remove('selected'));
    btnElement.classList.add('selected');
    
    // 2. Local State Update
    const currentQ = state.questions[state.currentIndex];
    currentQ.selected_option = optionId;

    // 3. Backend Sync (Fire and Forget)
    await fetch('/api/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            attempt_id: CONFIG.attemptId,
            question_id: currentQ.id,
            option_id: optionId
        })
    });
}

function changeQuestion(delta) {
    state.currentIndex += delta;
    renderQuestion();
}

async function submitQuiz() {
    clearInterval(state.timerInterval);
    const btn = document.querySelector('button[onclick="submitQuiz()"]');
    if(btn) btn.innerText = "Processing...";

    const res = await fetch(`/api/attempt/${CONFIG.attemptId}/submit`, { method: 'POST' });
    const data = await res.json();
    
    document.getElementById('app-root').innerHTML = `
        <div class="question-card" style="text-align:center;">
            <h1>Quiz Completed!</h1>
            <p style="font-size: 2rem; color: #2196F3;">Score: ${data.score}%</p>
            <a href="/" style="display:inline-block; margin-top:20px;">Return to Gallery</a>
        </div>
    `;
    document.querySelector('.controls').remove();
}