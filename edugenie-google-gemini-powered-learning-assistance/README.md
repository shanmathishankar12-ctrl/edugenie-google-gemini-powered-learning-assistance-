# EduGenie: Google Gemini Powered Learning Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.8%20Flash-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students of all academic levels, EduGenie enables users to:

- ❓ **Ask Questions**: Receive smart, concise, and structured answers with real-world examples.
- 💡 **Understand Complex Concepts**: Break down intricate topics into a beginner-friendly 5-part explanation format.
- 📝 **Generate Interactive Quizzes**: Turn any educational topic into an interactive 3-question MCQ quiz with instant grading and automatic error correction.
- 📄 **Summarize Educational Passages**: Condense long texts into concise executive summaries and key bullet points.
- 🚀 **Personalized Learning Paths**: Receive structured roadmaps from beginner to advanced levels, complete with 4-week study plans, practice projects, revision tips, and curated resource links.

---

## 🏗️ Folder Architecture

```text
EduGenie/
├── main.py                   # FastAPI backend app & routing
├── explanation_module.py     # Concept explanation logic (LaMini-Flan-T5 / Gemini)
├── qna.py                    # Question answering logic
├── quiz_module.py            # 3-question MCQ generator with JSON parsing
├── summary_module.py         # Text summarization and key points extraction
├── learning_path.py          # Structured learning roadmap & recommendation module
├── gemini_client.py          # Unified Gemini AI integration & error handling
├── config.py                 # Configuration loader and .env manager
├── requirements.txt          # Python dependencies
├── .env.example              # Sample environment configuration
├── README.md                 # Complete project documentation
├── templates/
│   └── index.html            # Responsive frontend interface (Jinja2 template)
└── static/
    ├── style.css             # Modern styling, glassmorphism, responsive design
    └── script.js             # Interactive quiz grader, tab switching, and API calls
```

---

## 🎯 Milestones Breakdown

### Milestone 1: Model Selection and Architecture
- **Gemini (Cloud API)**: Advanced reasoning, structured JSON outputs, and fast inference for Q&A, Quizzes, Summaries, and Learning Paths.
- **LaMini-Flan-T5 / Gemini (Hybrid)**: Concept explanation supporting both local instruction-tuned models (`MBZUAI/LaMini-Flan-T5-783M`) and Gemini cloud fallback.

### Milestone 2: Core Functionalities Development
1. **Explanation Module (`explanation_module.py`)**:
   Structured 5-part framework:
   1. Simple Definition
   2. Main Idea
   3. Important Points
   4. Simple Example
   5. Quick Revision
2. **QnA Module (`qna.py`)**:
   Student-friendly explanations with bullet points and examples.
3. **Quiz Module (`quiz_module.py`)**:
   Generates exactly 3 MCQs with 4 options each, correct answer key, and short explanation in valid JSON.
4. **Summary Module (`summary_module.py`)**:
   Converts long passages into `SUMMARY` and `KEY POINTS`.
5. **Learning Path Module (`learning_path.py`)**:
   Produces structured roadmaps: Beginner, Intermediate, Advanced, 4-Week Plan, Practice Projects, and Resources.

### Milestone 3: Frontend Development
- **Web Interface (`templates/index.html`)**: Tab switcher, suggestion chips, character counter, glassmorphism workspace, and responsive layout.
- **Interactive Quiz Engine (`static/script.js`)**: Real-time evaluation—clicking an option reveals whether it's correct (green) or incorrect (red), highlights the true answer, displays an explanation, and tallies your score.

### Milestone 4: Deployment & Testing
- Run locally with Uvicorn.
- End-to-end testing across all 5 learning modes.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Google Gemini API Key**: Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).

### 2. Clone / Open Project
```bash
git clone <repository_url>
cd modest-archimedes
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` (or let the app auto-create it):
```bash
cp .env.example .env
```
Open `.env` and set your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-3.8-flash
USE_LOCAL_LAMINI=False
HOST=127.0.0.1
PORT=8000
```

### 5. Run the Application
```bash
uvicorn main:app --reload
```
or run with python directly:
```bash
python main.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📡 RESTful API Documentation

EduGenie provides dedicated RESTful endpoints as well as a unified generate endpoint:

| Endpoint | Method | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `/health` | `GET` | Health check & config status | *None* |
| `/qa` | `POST` | Ask an academic question | `{"text": "Which is the largest ocean?"}` |
| `/explain` | `POST` | Explain a concept in 5 steps | `{"text": "The Pythagoras Theorem"}` |
| `/quiz` | `POST` | Generate 3-question MCQ quiz | `{"text": "Photosynthesis"}` |
| `/summarize` | `POST` | Summarize educational passage | `{"text": "Article content..."}` |
| `/learn/recommendations` | `POST` | Generate complete learning roadmap | `{"text": "Machine Learning with Python"}` |
| `/api/generate` | `POST` | Unified routing endpoint | `{"text": "...", "task": "qa"}` |

### Sample Quiz Response (`/quiz`)
```json
{
  "success": true,
  "type": "quiz",
  "task": "quiz",
  "result": [
    {
      "question": "What is the primary green pigment involved in photosynthesis?",
      "options": ["Carotenoid", "Chlorophyll", "Anthocyanin", "Hemoglobin"],
      "answer": "Chlorophyll",
      "explanation": "Chlorophyll absorbs light energy (primarily blue and red) to drive the photosynthetic process."
    }
  ]
}
```

---

## 👥 Credits & Metadata

- **Project Name**: EduGenie
- **Author**: Tella Divya Sree
- **Mentor**: Siri
- **Date**: 11/04/2025
- **Technology Stack**: FastAPI, Google Gemini API, Jinja2, HTML5/CSS3/JavaScript
