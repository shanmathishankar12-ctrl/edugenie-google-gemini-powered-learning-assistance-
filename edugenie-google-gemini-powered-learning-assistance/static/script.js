/**
 * EduGenie AI - Client Application Logic
 * Supports interactive tasks, live quiz grading, and rich text rendering.
 */

// ============================================================
// TASK CONFIGURATION & SAMPLES
// ============================================================

const TASK_CONFIGS = {
    qa: {
        label: "What is your question?",
        placeholder: "Ask anything... Example: Which is the largest ocean on Earth and what makes it unique?",
        buttonText: "Ask EduGenie",
        heading: "EduGenie Answer",
        chips: [
            "Which is the largest ocean?",
            "What causes gravity?",
            "Why is the sky blue?",
            "How do vaccines work?"
        ]
    },
    explain: {
        label: "What concept or topic should EduGenie explain?",
        placeholder: "Enter a topic... Example: The Pythagoras Theorem in geometry.",
        buttonText: "Explain Concept",
        heading: "Concept Explanation",
        chips: [
            "The Pythagoras Theorem",
            "Photosynthesis",
            "Theory of Relativity",
            "Binary Search Algorithm"
        ]
    },
    quiz: {
        label: "Enter a topic or paste a passage for a 3-question MCQ quiz:",
        placeholder: "Enter topic or passage... Example: Solar System and Planetary Orbits",
        buttonText: "Generate 3-MCQ Quiz",
        heading: "Interactive Practice Quiz",
        chips: [
            "The Solar System",
            "Python Programming Basics",
            "World War II History",
            "Human Circulatory System"
        ]
    },
    summary: {
        label: "Paste the educational text or article to summarize:",
        placeholder: "Paste an article, textbook excerpt, or lecture note here...",
        buttonText: "Summarize Content",
        heading: "Summary & Key Points",
        chips: [
            "Renewable energy vs Fossil fuels",
            "How the Internet works",
            "Mitochondria and cellular respiration"
        ]
    },
    learn: {
        label: "What subject, technology, or skill do you want to master?",
        placeholder: "Enter a topic... Example: SQL and Database Administration",
        buttonText: "Create Learning Path",
        heading: "Learning Roadmap & Recommendations",
        chips: [
            "SQL & Database Design",
            "Machine Learning with Python",
            "Full Stack Web Development",
            "Data Structures & Algorithms"
        ]
    }
};

// ============================================================
// DOM ELEMENTS
// ============================================================

let currentTask = "qa";
let currentQuizData = [];
let quizScore = 0;
let questionsAnswered = 0;

const taskButtons = document.querySelectorAll(".task");
const inputTitle = document.getElementById("inputTitle");
const input = document.getElementById("input");
const charCount = document.getElementById("charCount");
const generateBtn = document.getElementById("generate");
const btnText = generateBtn.querySelector(".btn-text");
const chipsList = document.getElementById("chipsList");

const resultBox = document.getElementById("resultBox");
const resultHeading = document.getElementById("resultHeading");
const resultText = document.getElementById("result");
const quizContainer = document.getElementById("quizContainer");
const quizList = document.getElementById("quizList");
const quizScoreBanner = document.getElementById("quizScoreBanner");
const quizScoreText = document.getElementById("quizScoreText");
const retryQuizBtn = document.getElementById("retryQuizBtn");
const copyBtn = document.getElementById("copyBtn");

// ============================================================
// TASK TAB SWITCHING
// ============================================================

function switchTask(taskKey) {
    if (!TASK_CONFIGS[taskKey]) return;
    currentTask = taskKey;

    taskButtons.forEach(btn => {
        btn.classList.toggle("active", btn.dataset.task === taskKey);
    });

    const config = TASK_CONFIGS[taskKey];
    inputTitle.textContent = config.label;
    input.placeholder = config.placeholder;
    btnText.textContent = config.buttonText;

    // Render suggestion chips
    renderChips(config.chips);
    input.focus();
}

taskButtons.forEach(btn => {
    btn.addEventListener("click", () => switchTask(btn.dataset.task));
});

function renderChips(chips) {
    chipsList.innerHTML = "";
    chips.forEach(chipText => {
        const chip = document.createElement("button");
        chip.className = "chip";
        chip.type = "button";
        chip.textContent = chipText;
        chip.addEventListener("click", () => {
            input.value = chipText;
            updateCharCount();
            generateAnswer();
        });
        chipsList.appendChild(chip);
    });
}

// Character counter
function updateCharCount() {
    const len = input.value.length;
    charCount.textContent = `${len.toLocaleString()} / 12,000`;
}
input.addEventListener("input", updateCharCount);

// ============================================================
// TEXT & MARKDOWN FORMATTER
// ============================================================

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function renderFormattedText(rawText) {
    if (!rawText) return "";

    const lines = rawText.split("\n");
    let html = "";
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        if (!line) {
            if (inList) {
                html += "</ul>";
                inList = false;
            }
            continue;
        }

        // Headers
        if (line.startsWith("### ")) {
            if (inList) { html += "</ul>"; inList = false; }
            html += `<h3>${escapeHtml(line.slice(4))}</h3>`;
            continue;
        } else if (line.startsWith("## ")) {
            if (inList) { html += "</ul>"; inList = false; }
            html += `<h2>${escapeHtml(line.slice(3))}</h2>`;
            continue;
        } else if (line.startsWith("# ")) {
            if (inList) { html += "</ul>"; inList = false; }
            html += `<h2>${escapeHtml(line.slice(2))}</h2>`;
            continue;
        }

        // Bullet lists
        if (line.startsWith("- ") || line.startsWith("* ")) {
            if (!inList) {
                html += "<ul>";
                inList = true;
            }
            let itemText = formatInlineMarkdown(escapeHtml(line.slice(2)));
            html += `<li>${itemText}</li>`;
            continue;
        } else {
            if (inList) {
                html += "</ul>";
                inList = false;
            }
        }

        // Paragraphs
        html += `<p>${formatInlineMarkdown(escapeHtml(line))}</p>`;
    }

    if (inList) {
        html += "</ul>";
    }

    return html;
}

function formatInlineMarkdown(text) {
    // Bold **text**
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // Inline `code`
    text = text.replace(/`([^`]+)`/g, "<code>$1</code>");
    return text;
}

// ============================================================
// INTERACTIVE QUIZ LOGIC ("Corrects answer if chosen wrong")
// ============================================================

function renderQuiz(questions) {
    currentQuizData = questions;
    quizScore = 0;
    questionsAnswered = 0;

    quizList.innerHTML = "";
    quizScoreBanner.style.display = "none";

    questions.forEach((q, qIndex) => {
        const card = document.createElement("div");
        card.className = "quiz-card";
        card.id = `quizCard-${qIndex}`;

        const questionRow = document.createElement("div");
        questionRow.className = "quiz-question-row";

        const qTitle = document.createElement("div");
        qTitle.className = "quiz-question";
        qTitle.textContent = `${qIndex + 1}. ${q.question}`;

        const badge = document.createElement("span");
        badge.className = "quiz-badge";
        badge.textContent = `Q ${qIndex + 1} of ${questions.length}`;

        questionRow.appendChild(qTitle);
        questionRow.appendChild(badge);
        card.appendChild(questionRow);

        const optionsGrid = document.createElement("div");
        optionsGrid.className = "options-grid";

        q.options.forEach((optText, optIndex) => {
            const optBtn = document.createElement("button");
            optBtn.className = "option-btn";
            optBtn.type = "button";
            optBtn.dataset.qIndex = qIndex;
            optBtn.dataset.optText = optText;

            const letter = String.fromCharCode(65 + optIndex);
            optBtn.innerHTML = `<span><strong>${letter}.</strong> ${escapeHtml(optText)}</span><span class="opt-indicator"></span>`;

            optBtn.addEventListener("click", () => handleOptionSelection(qIndex, optText, optBtn, card));
            optionsGrid.appendChild(optBtn);
        });

        card.appendChild(optionsGrid);

        // Feedback container (hidden until answered)
        const feedback = document.createElement("div");
        feedback.className = "quiz-feedback";
        feedback.id = `quizFeedback-${qIndex}`;
        card.appendChild(feedback);

        quizList.appendChild(card);
    });

    resultText.style.display = "none";
    quizContainer.style.display = "flex";
}

function handleOptionSelection(qIndex, selectedOption, clickedBtn, card) {
    const questionObj = currentQuizData[qIndex];
    if (!questionObj) return;

    // Check if question already answered
    const feedback = card.querySelector(".quiz-feedback");
    if (feedback.classList.contains("show")) return;

    const allOptionBtns = card.querySelectorAll(".option-btn");
    allOptionBtns.forEach(btn => btn.classList.add("locked"));

    const correctAnswer = (questionObj.answer || "").trim();
    const isCorrect = (selectedOption.trim().toLowerCase() === correctAnswer.toLowerCase());

    const indicator = clickedBtn.querySelector(".opt-indicator");

    if (isCorrect) {
        // Highlight correct in green
        clickedBtn.classList.add("selected-correct");
        indicator.textContent = "✓";
        quizScore += 1;

        feedback.className = "quiz-feedback is-correct show";
        feedback.innerHTML = `
            <strong>🎉 Excellent! That is correct.</strong>
            ${escapeHtml(questionObj.explanation || "")}
        `;
    } else {
        // Highlight chosen wrong in red
        clickedBtn.classList.add("selected-wrong");
        indicator.textContent = "✗";

        // Spec Requirement: "It corrects the answer if chosen wrong"
        // Find and highlight the correct option in green
        allOptionBtns.forEach(btn => {
            if (btn.dataset.optText.trim().toLowerCase() === correctAnswer.toLowerCase()) {
                btn.classList.add("reveal-correct");
                const rightIndicator = btn.querySelector(".opt-indicator");
                if (rightIndicator) rightIndicator.textContent = "✓";
            }
        });

        feedback.className = "quiz-feedback is-wrong show";
        feedback.innerHTML = `
            <strong>❌ Not quite. The correct answer is: "${escapeHtml(correctAnswer)}"</strong>
            ${escapeHtml(questionObj.explanation || "")}
        `;
    }

    questionsAnswered += 1;

    // Check if full quiz is completed
    if (questionsAnswered === currentQuizData.length) {
        showFinalQuizScore();
    }
}

function showFinalQuizScore() {
    quizScoreBanner.style.display = "flex";
    const total = currentQuizData.length;
    const percentage = Math.round((quizScore / total) * 100);

    let message = "";
    if (percentage === 100) message = "🌟 Outstanding! Perfect score!";
    else if (percentage >= 66) message = "👏 Great job! Almost there!";
    else message = "💡 Good effort! Review the explanations and try again.";

    quizScoreText.textContent = `Your Score: ${quizScore} / ${total} (${percentage}%) — ${message}`;
}

retryQuizBtn.addEventListener("click", () => {
    if (currentQuizData.length > 0) {
        renderQuiz(currentQuizData);
    }
});

// ============================================================
// GENERATE ACTION (Fetch from Backend)
// ============================================================

async function generateAnswer() {
    const text = input.value.trim();

    if (!text) {
        resultBox.classList.add("show");
        resultHeading.textContent = "Notice";
        resultText.style.display = "block";
        quizContainer.style.display = "none";
        resultText.innerHTML = `<p style="color:#b45309;">⚠️ Please enter a question, topic, or passage above to proceed.</p>`;
        return;
    }

    // Set Loading State
    generateBtn.disabled = true;
    btnText.textContent = "EduGenie is thinking...";
    resultBox.classList.add("show");
    resultHeading.textContent = TASK_CONFIGS[currentTask].heading;

    if (currentTask === "quiz") {
        resultText.style.display = "block";
        quizContainer.style.display = "none";
        resultText.innerHTML = `<p>⏳ Generating 3 multiple-choice questions with answer keys...</p>`;
    } else {
        resultText.style.display = "block";
        quizContainer.style.display = "none";
        resultText.innerHTML = `<p>⏳ Consulting EduGenie AI...</p>`;
    }

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                task: currentTask
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned error code ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || "Generation request failed.");
        }

        if (data.type === "quiz" && Array.isArray(data.result)) {
            renderQuiz(data.result);
        } else {
            resultText.style.display = "block";
            quizContainer.style.display = "none";
            resultText.innerHTML = renderFormattedText(data.result);
        }

    } catch (error) {
        resultText.style.display = "block";
        quizContainer.style.display = "none";
        resultText.innerHTML = `
            <div style="padding:16px; border-radius:12px; background:#fff1f2; border:1px solid #fecdd3; color:#9f1239;">
                <strong>⚠️ Something went wrong</strong>
                <p style="margin-top:6px;">${escapeHtml(error.message)}</p>
                <p style="margin-top:8px; font-size:12.5px; color:#475569;">
                    Ensure your <code>.env</code> file has a valid <code>GEMINI_API_KEY</code> and the server is running.
                </p>
            </div>
        `;
    } finally {
        generateBtn.disabled = false;
        btnText.textContent = TASK_CONFIGS[currentTask].buttonText;
    }
}

generateBtn.addEventListener("click", generateAnswer);

// Ctrl + Enter shortcut
input.addEventListener("keydown", event => {
    if (event.ctrlKey && event.key === "Enter") {
        event.preventDefault();
        generateAnswer();
    }
});

// ============================================================
// COPY TO CLIPBOARD
// ============================================================

copyBtn.addEventListener("click", async () => {
    let contentToCopy = "";

    if (currentTask === "quiz" && currentQuizData.length > 0) {
        contentToCopy = currentQuizData.map((q, i) => {
            const opts = q.options.map((o, idx) => `  ${String.fromCharCode(65 + idx)}. ${o}`).join("\n");
            return `Question ${i + 1}: ${q.question}\n${opts}\nAnswer: ${q.answer}\nExplanation: ${q.explanation}\n`;
        }).join("\n");
    } else {
        contentToCopy = resultText.innerText;
    }

    if (!contentToCopy) return;

    try {
        await navigator.clipboard.writeText(contentToCopy);
        const originalText = copyBtn.textContent;
        copyBtn.textContent = "✓ Copied!";
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    } catch (err) {
        console.error("Clipboard copy failed:", err);
    }
});

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    switchTask("qa");
    updateCharCount();
});
