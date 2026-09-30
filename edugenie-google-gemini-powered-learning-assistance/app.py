import html
import json
import os
import re

import streamlit as st
from google import genai
from google.genai import types

# ============================================================
# EDUGENIE - SINGLE FILE STREAMLIT AI LEARNING ASSISTANT
# Requires: streamlit >= 1.39, google-genai
# Run:      streamlit run app.py
# ============================================================

st.set_page_config(
    page_title="EduGenie AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Apply font without breaking Streamlit's icon fonts */
html, body, .stApp, p, label, button, textarea, input, h1, h2, h3, h4, li {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 5% 20%, #dff8ff 0%, transparent 28%),
        radial-gradient(circle at 95% 15%, #eadcff 0%, transparent 30%),
        linear-gradient(135deg, #f8fcff 0%, #f8f5ff 100%);
}

/* Hide Streamlit chrome but KEEP the sidebar toggle usable */
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }
header[data-testid="stHeader"] { background: transparent; }

.block-container {
    max-width: 1150px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* Header */
.edu-header {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(15px);
    border-bottom: 1px solid rgba(120,100,255,0.08);
    padding: 12px 25px;
    border-radius: 0 0 18px 18px;
    margin-bottom: 35px;
}
.edu-header-row { display:flex; justify-content:space-between; align-items:center; }
.logo-box { display:flex; align-items:center; gap:10px; }
.logo-icon {
    width:34px; height:34px;
    background: linear-gradient(135deg,#6655ff,#8d4df5);
    border-radius:10px;
    display:flex; align-items:center; justify-content:center;
    font-size:19px;
    box-shadow: 0 5px 15px rgba(103,85,255,.25);
}
.logo-text { font-size:18px; font-weight:800; color:#17172b; }
.logo-text span { color:#6554f5; }
.online {
    background:white; border:1px solid #e8e8f5; border-radius:30px;
    padding:7px 13px; font-size:11px; color:#666; text-align:center;
}
.green-dot { color:#15b878; }

/* Hero */
.hero { text-align:center; padding:25px 10px 20px; }
.badge {
    display:inline-block; padding:7px 14px; border-radius:30px;
    background:#f0edff; border:1px solid #ddd6ff; color:#6957ed;
    font-size:10px; font-weight:700; margin-bottom:18px;
}
.hero h1 {
    font-size:50px; line-height:1.03; font-weight:800;
    color:#121525; margin:0;
}
.gradient-text {
    background: linear-gradient(90deg,#6253f5,#b247ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    max-width:650px; margin:18px auto 0;
    color:#70748c; font-size:14px; line-height:1.8;
}

/* Containers created with st.container(key=...) get .st-key-<key> */
.st-key-main-card {
    background: rgba(255,255,255,.90);
    border: 1px solid rgba(255,255,255,.9);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 20px 60px rgba(65,45,130,.10);
    margin-top: 15px;
}
.st-key-result-box {
    background: #ffffff;
    border: 1px solid #e7e4ff;
    border-radius: 16px;
    padding: 22px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(70,50,150,.08);
}
.result-title {
    font-weight:800; color:#5f50e8; font-size:15px; margin-bottom:12px;
}

/* Feature cards */
.feature-card {
    background: rgba(255,255,255,.85);
    border: 1px solid rgba(230,228,245,.9);
    border-radius: 16px;
    padding: 20px;
    min-height: 155px;
    box-shadow: 0 10px 30px rgba(50,40,100,.06);
}
.feature-icon { font-size:25px; margin-bottom:10px; }
.feature-title { font-weight:700; color:#16182b; font-size:14px; margin-bottom:8px; }
.feature-text { font-size:11px; color:#777b91; line-height:1.6; }

/* Buttons: full width, secondary = white, primary = purple gradient */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #e4e1f4;
    background: white;
    color: #4d4f63;
    font-weight: 600;
    min-height: 42px;
    transition: all .2s ease;
}
div.stButton > button:hover {
    border-color: #7663ff;
    color: #6655ef;
    box-shadow: 0 5px 15px rgba(102,85,239,.12);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg,#6755f4,#8450ed);
    color: white;
    border: none;
    box-shadow: 0 8px 20px rgba(103,85,244,.25);
}
div.stButton > button[kind="primary"]:hover { color: white; filter: brightness(1.06); }

textarea { border-radius: 12px !important; }

/* Footer */
.footer { text-align:center; color:#85879a; font-size:11px; padding:35px 10px 10px; }
.footer strong { color:#6253ed; }

.score-box {
    text-align:center; background:#f4f1ff; padding:18px;
    border-radius:14px; margin-top:15px;
    font-size:20px; font-weight:800; color:#6252ed;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#f8f7ff,#ffffff);
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="edu-header">
  <div class="edu-header-row">
    <div class="logo-box">
      <div class="logo-icon">🎓</div>
      <div class="logo-text">Edu<span>Genie</span></div>
    </div>
    <div class="online"><span class="green-dot">●</span> AI Assistant Online</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR - API KEY + MODEL
# ============================================================

MODEL_CHOICES = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]


def get_default_api_key() -> str:
    """Look for a key in Streamlit secrets, then the environment."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass  # no secrets.toml present
    return os.environ.get("GEMINI_API_KEY", "")


with st.sidebar:
    st.markdown("## ⚙️ EduGenie Settings")

    default_key = get_default_api_key()
    if default_key:
        st.success("API key loaded from secrets/environment.")

    typed_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your API key here..."
        if not default_key
        else "Optional: override the loaded key",
    )
    api_key = typed_key.strip() or default_key

    model_choice = st.selectbox("Gemini Model", MODEL_CHOICES)
    custom_model = st.text_input(
        "Custom model name (optional)",
        placeholder="e.g. a newer model ID from Google AI Studio",
    )
    model_name = custom_model.strip() or model_choice

    st.markdown("---")
    st.markdown("### 💡 Tip")
    st.info("Your API key is used only for this Streamlit session.")

# ============================================================
# GEMINI HELPERS
# ============================================================


def call_gemini(prompt: str, *, temperature: float, max_tokens: int, json_mode: bool = False):
    """Return (text, error)."""
    if not api_key:
        return None, "Please enter your Gemini API key in the Settings panel."

    try:
        client = genai.Client(api_key=api_key)
        config_kwargs = dict(temperature=temperature, max_output_tokens=max_tokens)
        if json_mode:
            config_kwargs["response_mime_type"] = "application/json"

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )

        text = getattr(response, "text", None)
        if text and text.strip():
            return text.strip(), None

        # Helpful diagnostics when the response is empty
        reason = ""
        try:
            cand = response.candidates[0]
            reason = f" (finish reason: {cand.finish_reason})"
        except Exception:
            pass
        return None, f"Gemini returned an empty response{reason}."

    except Exception as e:
        return None, f"Gemini request failed: {e}"


def ask_gemini(prompt: str):
    # Generous token limit: thinking models spend part of it on reasoning.
    return call_gemini(prompt, temperature=0.7, max_tokens=8192)


def parse_quiz_json(text: str):
    """Extract a list of question dicts from model output."""
    text = re.sub(r"```(?:json)?", "", text).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("["), text.rfind("]")
        if start == -1 or end == -1:
            raise
        data = json.loads(text[start : end + 1])

    if isinstance(data, dict):
        data = data.get("questions", [])
    if not isinstance(data, list):
        raise ValueError("Quiz JSON is not a list.")
    return data


def normalize_question(q):
    """Validate one question and resolve the correct answer to an index."""
    if not isinstance(q, dict):
        return None

    question = str(q.get("question", "")).strip()
    options = q.get("options", [])
    if not question or not isinstance(options, list) or len(options) != 4:
        return None
    options = [str(o).strip() for o in options]

    correct = None
    idx = q.get("answer_index")
    if isinstance(idx, int) and 0 <= idx < 4:
        correct = idx
    else:
        answer = str(q.get("answer", "")).strip().lower()
        for i, opt in enumerate(options):
            if opt.lower() == answer:
                correct = i
                break
    if correct is None:
        return None

    return {
        "question": question,
        "options": options,
        "answer_index": correct,
        "explanation": str(q.get("explanation", "")).strip(),
    }


def generate_quiz(topic: str):
    prompt = f"""
You are EduGenie, an educational AI assistant.

Create exactly 3 multiple-choice questions about:

{topic}

Return ONLY valid JSON in this format:

[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer_index": 0,
    "explanation": "Short explanation"
  }}
]

Rules:
- Exactly 3 questions
- Exactly 4 options per question
- "answer_index" is the 0-based index (0-3) of the single correct option
- Do not include "A)" or "B)" prefixes inside the options
- Questions must be educational
- Keep explanations simple
- Return JSON only
"""
    text, error = call_gemini(prompt, temperature=0.5, max_tokens=8192, json_mode=True)
    if error:
        return None, error

    try:
        raw = parse_quiz_json(text)
    except Exception:
        return None, "Could not read the quiz the model returned. Please try again."

    quiz = [nq for nq in (normalize_question(q) for q in raw) if nq]
    if not quiz:
        return None, "The model returned an invalid quiz. Please try again."
    return quiz, None


# ============================================================
# PROMPT TEMPLATES
# ============================================================

PROMPTS = {
    "Ask Q&A": """
You are EduGenie, a friendly educational AI assistant.

Answer the student's question accurately.

Question:
{user_input}

Requirements:
- Use simple English
- Give a direct answer first
- Explain clearly
- Use bullet points where useful
- Add an example if useful
- Avoid unnecessary complexity
""",
    "Explain Concept": """
You are EduGenie, an expert teacher.

Explain this concept to a college student:

{user_input}

Use this exact structure:

## 📌 Simple Definition

## 💡 Main Idea

## 🔑 Important Points

## 🧠 How It Works

## 📚 Example

## ⚡ Quick Revision

Use simple English and clear bullet points.
""",
    "Summarize": """
You are EduGenie, an educational summarization assistant.

Summarize the following text:

{user_input}

Return:

## 📄 Summary

Give a simple and accurate summary.

## 🔑 Key Points

Give the most important points as bullets.

## ⚡ One-Line Revision

Give one short revision statement.
""",
    "Learning Path": """
You are EduGenie, a personalized learning coach.

Create a learning roadmap for:

{user_input}

Include:

# 🚀 Learning Roadmap

## 🌱 Beginner Level
Important concepts to learn.

## 📘 Intermediate Level
Concepts and skills.

## 🔥 Advanced Level
Advanced concepts.

## 📅 4-Week Study Plan
Week 1
Week 2
Week 3
Week 4

## 🛠 Practice Projects
Give beginner, intermediate and advanced project ideas.

## 📝 Revision Tips
Give practical study tips.

Keep everything student-friendly and achievable.
""",
}

TASKS = [
    ("Ask Q&A", "❓ Ask Q&A"),
    ("Explain Concept", "💡 Explain Concept"),
    ("Practice Quiz", "📝 Practice Quiz"),
    ("Summarize", "📄 Summarize"),
    ("Learning Path", "🚀 Learning Path"),
]

EXAMPLES = {
    "Ask Q&A": [
        "Which is the largest ocean?",
        "What causes gravity?",
        "Why is the sky blue?",
        "How do vaccines work?",
    ],
    "Explain Concept": [
        "Explain Artificial Intelligence",
        "Explain photosynthesis",
        "Explain cloud computing",
        "Explain database normalization",
    ],
    "Practice Quiz": [
        "Python programming",
        "Artificial Intelligence",
        "Computer Networks",
        "Data Structures",
    ],
    "Summarize": [
        "Paste your paragraph here",
        "Paste your lesson here",
        "Paste your article here",
    ],
    "Learning Path": [
        "Learn Python",
        "Learn Data Science",
        "Learn Artificial Intelligence",
        "Learn Web Development",
    ],
}

PLACEHOLDERS = {
    "Ask Q&A": "Ask anything... Example: Which is the largest ocean on Earth and what makes it unique?",
    "Explain Concept": "Enter a concept... Example: Explain Artificial Intelligence in simple words.",
    "Practice Quiz": "Enter a topic... Example: Python programming.",
    "Summarize": "Paste your text here and EduGenie will summarize it.",
    "Learning Path": "Enter a skill... Example: I want to learn Python from beginner to advanced.",
}

# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("task", "Ask Q&A")
st.session_state.setdefault("result", None)
st.session_state.setdefault("quiz", None)
st.session_state.setdefault("quiz_checked", False)


def set_task(name: str):
    """Switch task and clear any previous output."""
    if st.session_state.task != name:
        st.session_state.task = name
        st.session_state.result = None
        st.session_state.quiz = None
        st.session_state.quiz_checked = False


def mark_quiz_checked():
    st.session_state.quiz_checked = True


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">
  <div class="badge">🚀 GEMINI POWERED LEARNING</div>
  <h1>Learn smarter. <span class="gradient-text">Grow faster.</span></h1>
  <p>
    Your personal AI study companion for instant answers, deep conceptual
    explanations, interactive quizzes, summarization, and step-by-step
    learning roadmaps.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# MAIN CARD
# ============================================================

with st.container(key="main-card"):

    # Task buttons (active task highlighted)
    cols = st.columns(len(TASKS))
    for col, (name, label) in zip(cols, TASKS):
        with col:
            st.button(
                label,
                key=f"task_btn_{name}",
                type="primary" if st.session_state.task == name else "secondary",
                on_click=set_task,
                args=(name,),
            )

    task = st.session_state.task

    st.markdown(
        f"""
        <div style="margin-top:18px;margin-bottom:8px;color:#55576c;
                    font-weight:700;font-size:14px;">{html.escape(task)}</div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("TRY ASKING:  •  " + "   •   ".join(EXAMPLES[task]))

    user_input = st.text_area(
        "Your question",
        height=140,
        placeholder=PLACEHOLDERS[task],
        key=f"input_{task}",
    )

    generate = st.button("✨ Generate with EduGenie →", type="primary", key="generate")

    # ---------------- GENERATE ----------------
    if generate:
        if not user_input.strip():
            st.warning("Please enter a question or topic first.")
        else:
            with st.spinner("EduGenie is thinking... ✨"):
                if task == "Practice Quiz":
                    quiz, error = generate_quiz(user_input.strip())
                    if error:
                        st.error(error)
                    else:
                        st.session_state.quiz = quiz
                        st.session_state.quiz_checked = False
                        st.session_state.result = None
                        # Clear old radio selections from a previous quiz
                        for i in range(10):
                            st.session_state.pop(f"quiz_{i}", None)
                else:
                    prompt = PROMPTS[task].format(user_input=user_input.strip())
                    result, error = ask_gemini(prompt)
                    if error:
                        st.error(error)
                    else:
                        st.session_state.result = result
                        st.session_state.quiz = None

    # ---------------- NORMAL RESULT ----------------
    if st.session_state.result:
        with st.container(key="result-box"):
            st.markdown(
                '<div class="result-title">✨ EduGenie Answer</div>',
                unsafe_allow_html=True,
            )
            st.markdown(st.session_state.result)

    # ---------------- QUIZ ----------------
    if st.session_state.quiz:
        quiz = st.session_state.quiz

        with st.container(key="result-box"):
            st.markdown(
                '<div class="result-title">📝 EduGenie Interactive Quiz</div>',
                unsafe_allow_html=True,
            )

            for i, q in enumerate(quiz):
                with st.container(border=True):
                    st.markdown(f"**{i + 1}. {html.escape(q['question'])}**")
                    st.radio(
                        "Choose your answer:",
                        q["options"],
                        index=None,  # nothing preselected
                        key=f"quiz_{i}",
                    )

            st.button(
                "✅ Check My Answers",
                key="check_answers",
                type="primary",
                on_click=mark_quiz_checked,
            )

            if st.session_state.quiz_checked:
                score = 0
                unanswered = 0

                for i, q in enumerate(quiz):
                    selected = st.session_state.get(f"quiz_{i}")
                    correct_text = q["options"][q["answer_index"]]

                    if selected is None:
                        unanswered += 1
                        st.warning(
                            f"Question {i + 1}: Not answered. "
                            f"Correct answer: {correct_text}"
                        )
                    elif selected == correct_text:
                        score += 1
                        st.success(f"Question {i + 1}: Correct! 🎉")
                    else:
                        st.error(
                            f"Question {i + 1}: Incorrect. "
                            f"Correct answer: {correct_text}"
                        )

                    if q["explanation"]:
                        st.info(f"💡 {q['explanation']}")

                st.markdown(
                    f'<div class="score-box">🎯 Your Score: {score} / {len(quiz)}</div>',
                    unsafe_allow_html=True,
                )
                if unanswered:
                    st.caption(f"{unanswered} question(s) left unanswered.")

# ============================================================
# FEATURE CARDS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
    <div class="feature-card">
      <div class="feature-icon">🎯</div>
      <div class="feature-title">Smart Academic Q&amp;A</div>
      <div class="feature-text">
        Receive clear, student-friendly answers with real-world examples
        and bullet-point explanations for your questions.
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
    <div class="feature-card">
      <div class="feature-icon">🧩</div>
      <div class="feature-title">Interactive MCQ Quizzes</div>
      <div class="feature-text">
        Automatically turn any educational topic into a 3-question quiz
        with instant answer verification.
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
    <div class="feature-card">
      <div class="feature-icon">📖</div>
      <div class="feature-title">Personalized Learning Paths</div>
      <div class="feature-text">
        Get comprehensive beginner-to-advanced learning roadmaps with
        weekly schedules and project suggestions.
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
  <strong>EduGenie AI</strong> • Google Gemini Powered Learning Assistant
  <br><br>
  Developed for Educational AI Project
</div>
""",
    unsafe_allow_html=True,
)
