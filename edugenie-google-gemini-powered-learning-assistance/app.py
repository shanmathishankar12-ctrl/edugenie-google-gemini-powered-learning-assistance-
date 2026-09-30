import streamlit as st
import os
import json
import re
from google import genai
from google.genai import types

# ============================================================
# EDU GENIE - SINGLE FILE STREAMLIT AI LEARNING ASSISTANT
# ============================================================

st.set_page_config(
    page_title="EduGenie AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 5% 20%, #dff8ff 0%, transparent 28%),
        radial-gradient(circle at 95% 15%, #eadcff 0%, transparent 30%),
        linear-gradient(135deg, #f8fcff 0%, #f8f5ff 100%);
}

/* Hide Streamlit default */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main container */
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

.logo-box {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-icon {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg,#6655ff,#8d4df5);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    box-shadow: 0 5px 15px rgba(103,85,255,.25);
}

.logo-text {
    font-size: 18px;
    font-weight: 800;
    color: #17172b;
}

.logo-text span {
    color: #6554f5;
}

.online {
    background: white;
    border: 1px solid #e8e8f5;
    border-radius: 30px;
    padding: 7px 13px;
    font-size: 11px;
    color: #666;
    text-align: center;
}

.green-dot {
    color: #15b878;
}

/* Hero */
.hero {
    text-align: center;
    padding: 25px 10px 20px;
}

.badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 30px;
    background: #f0edff;
    border: 1px solid #ddd6ff;
    color: #6957ed;
    font-size: 10px;
    font-weight: 700;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: 50px;
    line-height: 1.03;
    font-weight: 800;
    color: #121525;
    margin: 0;
}

.gradient-text {
    background: linear-gradient(90deg,#6253f5,#b247ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 650px;
    margin: 18px auto 0;
    color: #70748c;
    font-size: 14px;
    line-height: 1.8;
}

/* Main card */
.main-card {
    background: rgba(255,255,255,.90);
    border: 1px solid rgba(255,255,255,.9);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 20px 60px rgba(65,45,130,.10);
    margin-top: 15px;
}

/* Result */
.result-box {
    background: #ffffff;
    border: 1px solid #e7e4ff;
    border-radius: 16px;
    padding: 22px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(70,50,150,.08);
}

.result-title {
    font-weight: 800;
    color: #5f50e8;
    font-size: 15px;
    margin-bottom: 12px;
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

.feature-icon {
    font-size: 25px;
    margin-bottom: 10px;
}

.feature-title {
    font-weight: 700;
    color: #16182b;
    font-size: 14px;
    margin-bottom: 8px;
}

.feature-text {
    font-size: 11px;
    color: #777b91;
    line-height: 1.6;
}

/* Buttons */
div.stButton > button {
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

.generate-btn button {
    background: linear-gradient(90deg,#6755f4,#8450ed) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 8px 20px rgba(103,85,244,.25);
}

/* Textarea */
textarea {
    border-radius: 12px !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #85879a;
    font-size: 11px;
    padding: 35px 10px 10px;
}

.footer strong {
    color: #6253ed;
}

/* Quiz */
.quiz-card {
    background: #faf9ff;
    border: 1px solid #e8e4ff;
    border-radius: 14px;
    padding: 18px;
    margin: 12px 0;
}

.quiz-question {
    font-weight: 700;
    color: #22243a;
    margin-bottom: 12px;
}

.correct {
    color: #159957;
    font-weight: 700;
}

.wrong {
    color: #d84d5c;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#f8f7ff,#ffffff);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="edu-header">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div class="logo-box">
            <div class="logo-icon">🎓</div>
            <div class="logo-text">Edu<span>Genie</span></div>
        </div>

        <div class="online">
            <span class="green-dot">●</span>
            AI Assistant Online
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR - API KEY
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ EduGenie Settings")

    st.markdown(
        "Enter your **Gemini API key** to activate AI features."
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your API key here..."
    )

    model_name = st.selectbox(
        "Gemini Model",
        [
            "gemini-3.8-flash"
        ]
    )

    st.markdown("---")

    st.markdown("### 💡 Tip")
    st.info(
        "Your API key is used only for this Streamlit session."
    )


# ============================================================
# GEMINI FUNCTION
# ============================================================

def ask_gemini(prompt):

    if not api_key:
        return None, "Please enter your Gemini API key in the Settings panel."

    try:

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2000
            )
        )

        text = getattr(response, "text", None)

        if text:
            return text.strip(), None

        return None, "Gemini returned an empty response."

    except Exception as e:

        return None, str(e)


# ============================================================
# QUIZ JSON FUNCTION
# ============================================================

def generate_quiz(topic):

    if not api_key:
        return None, "Please enter your Gemini API key in the Settings panel."

    prompt = f"""
You are EduGenie, an educational AI assistant.

Create exactly 3 multiple-choice questions about:

{topic}

Return ONLY valid JSON.

Format:

[
  {{
    "question": "Question",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A",
    "explanation": "Short explanation"
  }}
]

Rules:
- Exactly 3 questions
- Exactly 4 options per question
- Only one correct answer
- Questions must be educational
- Keep explanations simple
- Return JSON only
"""

    try:

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=2500,
                response_mime_type="application/json"
            )
        )

        text = getattr(response, "text", "")

        if not text:
            return None, "Gemini returned an empty quiz."

        text = text.strip()

        # Remove accidental markdown
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
        text = text.strip()

        quiz = json.loads(text)

        if not isinstance(quiz, list):
            return None, "Invalid quiz format."

        return quiz, None

    except Exception as e:

        return None, str(e)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="badge">
        🚀 GEMINI POWERED LEARNING
    </div>

    <h1>
        Learn smarter.
        <span class="gradient-text">Grow faster.</span>
    </h1>

    <p>
        Your personal AI study companion for instant answers,
        deep conceptual explanations, interactive quizzes,
        summarization, and step-by-step learning roadmaps.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "task" not in st.session_state:
    st.session_state.task = "Ask Q&A"

if "result" not in st.session_state:
    st.session_state.result = None

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None


# ============================================================
# MAIN CARD
# ============================================================

st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Task buttons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("❓ Ask Q&A", use_container_width=True):
        st.session_state.task = "Ask Q&A"

with col2:
    if st.button("💡 Explain Concept", use_container_width=True):
        st.session_state.task = "Explain Concept"

with col3:
    if st.button("📝 Practice Quiz", use_container_width=True):
        st.session_state.task = "Practice Quiz"

with col4:
    if st.button("📄 Summarize", use_container_width=True):
        st.session_state.task = "Summarize"

with col5:
    if st.button("🚀 Learning Path", use_container_width=True):
        st.session_state.task = "Learning Path"


task = st.session_state.task


# ============================================================
# TASK LABEL
# ============================================================

st.markdown(
    f"""
    <div style="
        margin-top:18px;
        margin-bottom:8px;
        color:#55576c;
        font-weight:700;
        font-size:14px;">
        {task}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXAMPLE SUGGESTIONS
# ============================================================

if task == "Ask Q&A":

    examples = [
        "Which is the largest ocean?",
        "What causes gravity?",
        "Why is the sky blue?",
        "How do vaccines work?"
    ]

elif task == "Explain Concept":

    examples = [
        "Explain Artificial Intelligence",
        "Explain photosynthesis",
        "Explain cloud computing",
        "Explain database normalization"
    ]

elif task == "Practice Quiz":

    examples = [
        "Python programming",
        "Artificial Intelligence",
        "Computer Networks",
        "Data Structures"
    ]

elif task == "Summarize":

    examples = [
        "Paste your paragraph here",
        "Paste your lesson here",
        "Paste your article here"
    ]

else:

    examples = [
        "Learn Python",
        "Learn Data Science",
        "Learn Artificial Intelligence",
        "Learn Web Development"
    ]


st.caption("TRY ASKING:  •  " + "   •   ".join(examples))


# ============================================================
# INPUT
# ============================================================

placeholder = {
    "Ask Q&A":
        "Ask anything... Example: Which is the largest ocean on Earth and what makes it unique?",

    "Explain Concept":
        "Enter a concept... Example: Explain Artificial Intelligence in simple words.",

    "Practice Quiz":
        "Enter a topic... Example: Python programming.",

    "Summarize":
        "Paste your text here and EduGenie will summarize it.",

    "Learning Path":
        "Enter a skill... Example: I want to learn Python from beginner to advanced."
}


user_input = st.text_area(
    "Your question",
    height=140,
    placeholder=placeholder[task],
    label_visibility="visible"
)


# ============================================================
# GENERATE BUTTON
# ============================================================

st.markdown('<div class="generate-btn">', unsafe_allow_html=True)

generate = st.button(
    "✨ Generate with EduGenie →",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# GENERATE
# ============================================================

if generate:

    if not user_input.strip():

        st.warning("Please enter a question or topic first.")

    else:

        with st.spinner("EduGenie is thinking... ✨"):

            # ----------------------------------------
            # Q&A
            # ----------------------------------------

            if task == "Ask Q&A":

                prompt = f"""
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
"""

                result, error = ask_gemini(prompt)

                if error:
                    st.error(error)
                else:
                    st.session_state.result = result
                    st.session_state.quiz_result = None


            # ----------------------------------------
            # EXPLAIN
            # ----------------------------------------

            elif task == "Explain Concept":

                prompt = f"""
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
"""

                result, error = ask_gemini(prompt)

                if error:
                    st.error(error)
                else:
                    st.session_state.result = result
                    st.session_state.quiz_result = None


            # ----------------------------------------
            # SUMMARY
            # ----------------------------------------

            elif task == "Summarize":

                prompt = f"""
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
"""

                result, error = ask_gemini(prompt)

                if error:
                    st.error(error)
                else:
                    st.session_state.result = result
                    st.session_state.quiz_result = None


            # ----------------------------------------
            # LEARNING PATH
            # ----------------------------------------

            elif task == "Learning Path":

                prompt = f"""
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
"""

                result, error = ask_gemini(prompt)

                if error:
                    st.error(error)
                else:
                    st.session_state.result = result
                    st.session_state.quiz_result = None


            # ----------------------------------------
            # QUIZ
            # ----------------------------------------

            elif task == "Practice Quiz":

                quiz, error = generate_quiz(user_input)

                if error:
                    st.error(error)

                else:

                    st.session_state.quiz_result = quiz
                    st.session_state.result = None


# ============================================================
# SHOW NORMAL RESULT
# ============================================================

if st.session_state.result:

    st.markdown(
        '<div class="result-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-title">✨ EduGenie Answer</div>',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state.result)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# SHOW QUIZ
# ============================================================

if st.session_state.quiz_result:

    st.markdown(
        '<div class="result-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-title">📝 EduGenie Interactive Quiz</div>',
        unsafe_allow_html=True
    )

    quiz = st.session_state.quiz_result

    answers = {}

    for index, question in enumerate(quiz):

        st.markdown(
            f"""
            <div class="quiz-card">
                <div class="quiz-question">
                    {index + 1}. {question.get("question", "")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        options = question.get("options", [])

        if len(options) >= 4:

            answers[index] = st.radio(
                "Choose your answer:",
                options,
                key=f"quiz_{index}"
            )

    if st.button(
        "✅ Check My Answers",
        use_container_width=True
    ):

        score = 0

        for index, question in enumerate(quiz):

            correct = question.get("answer", "")
            selected = answers.get(index, "")

            if selected == correct:

                score += 1

                st.success(
                    f"Question {index + 1}: Correct! 🎉"
                )

            else:

                st.error(
                    f"Question {index + 1}: "
                    f"Correct answer: {correct}"
                )

            explanation = question.get("explanation", "")

            if explanation:

                st.info(
                    f"💡 {explanation}"
                )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                background:#f4f1ff;
                padding:18px;
                border-radius:14px;
                margin-top:15px;
                font-size:20px;
                font-weight:800;
                color:#6252ed;">
                🎯 Your Score: {score} / {len(quiz)}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CLOSE MAIN CARD
# ============================================================

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# FEATURE CARDS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">🎯</div>

        <div class="feature-title">
            Smart Academic Q&A
        </div>

        <div class="feature-text">
            Receive clear, student-friendly answers
            with real-world examples and bullet-point
            explanations for your questions.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">🧩</div>

        <div class="feature-title">
            Interactive MCQ Quizzes
        </div>

        <div class="feature-text">
            Automatically turn any educational topic
            into a 3-question quiz with instant
            answer verification.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">📖</div>

        <div class="feature-title">
            Personalized Learning Paths
        </div>

        <div class="feature-text">
            Get comprehensive beginner-to-advanced
            learning roadmaps with weekly schedules
            and project suggestions.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <strong>EduGenie AI</strong>
    • Google Gemini Powered Learning Assistant

    <br><br>

    Developed for Educational AI Project

</div>
""", unsafe_allow_html=True)