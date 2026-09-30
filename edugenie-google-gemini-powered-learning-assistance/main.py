"""
EduGenie: Google Gemini Powered Learning Assistant
Main FastAPI Application
"""

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import HOST, PORT, is_gemini_configured
from qna import question_answer
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="EduGenie AI",
    description="A lightweight AI-powered educational assistant that simplifies learning through generative AI.",
    version="1.0.0"
)

# CORS middleware for open integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=15000, description="Input text or prompt")


class UserRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=15000, description="Input text or prompt")
    task: str = Field(..., description="Task type: qa, explain, quiz, summary, or learn")


# ============================================================
# FRONTEND & HEALTH ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the main EduGenie web dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"configured": is_gemini_configured()}
    )


@app.get("/health")
async def health():
    """Health check endpoint to verify service availability."""
    return {
        "status": "online",
        "app": "EduGenie",
        "configured": is_gemini_configured()
    }


# ============================================================
# RESTFUL MODULE ENDPOINTS (Milestone 2 Specification)
# ============================================================

@app.post("/qa")
async def api_qa(payload: TextRequest):
    """Endpoint for Student Q&A."""
    result = question_answer(payload.text)
    return {
        "success": True,
        "type": "text",
        "task": "qa",
        "result": result
    }


@app.post("/explain")
async def api_explain(payload: TextRequest):
    """Endpoint for Structured Concept Explanation."""
    result = explain_topic(payload.text)
    return {
        "success": True,
        "type": "text",
        "task": "explain",
        "result": result
    }


@app.post("/quiz")
async def api_quiz(payload: TextRequest):
    """Endpoint for 3-Question MCQ Quiz Generation."""
    questions = generate_quiz(payload.text)
    return {
        "success": True,
        "type": "quiz",
        "task": "quiz",
        "result": questions
    }


@app.post("/summarize")
async def api_summarize(payload: TextRequest):
    """Endpoint for Text Summarization."""
    result = summarize_text(payload.text)
    return {
        "success": True,
        "type": "text",
        "task": "summarize",
        "result": result
    }


@app.post("/learn/recommendations")
async def api_learn_recommendations(payload: TextRequest):
    """Endpoint for Personalized Learning Paths."""
    result = get_learning_recommendations(payload.text)
    return {
        "success": True,
        "type": "text",
        "task": "learn",
        "result": result
    }


# ============================================================
# UNIFIED GENERATE ROUTE (Frontend & Single-API Support)
# ============================================================

@app.post("/api/generate")
async def api_generate(request: UserRequest):
    """
    Unified router that receives a prompt and task identifier,
    delegating to the appropriate specialized module.
    """
    text = request.text.strip()
    task = request.task.lower().strip()

    if not text:
        return {"success": False, "error": "Please provide non-empty text input."}

    if task in ("qa", "qna", "ask"):
        result = question_answer(text)
        return {"success": True, "type": "text", "task": "qa", "result": result}

    elif task in ("explain", "concept"):
        result = explain_topic(text)
        return {"success": True, "type": "text", "task": "explain", "result": result}

    elif task in ("quiz", "mcq"):
        questions = generate_quiz(text)
        return {"success": True, "type": "quiz", "task": "quiz", "result": questions}

    elif task in ("summary", "summarize"):
        result = summarize_text(text)
        return {"success": True, "type": "text", "task": "summary", "result": result}

    elif task in ("learn", "recommendations", "learning_path"):
        result = get_learning_recommendations(text)
        return {"success": True, "type": "text", "task": "learn", "result": result}

    return {
        "success": False,
        "error": f"Unknown task '{task}'. Valid tasks are: qa, explain, quiz, summary, learn."
    }


# ============================================================
# SERVER RUNNER
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
