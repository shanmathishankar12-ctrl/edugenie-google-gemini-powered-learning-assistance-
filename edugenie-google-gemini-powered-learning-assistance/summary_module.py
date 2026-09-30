"""
Summary Module for EduGenie
Summarizes long educational texts into concise summaries and clear key points.
Ideal for quick student revision and note-taking.
"""

from gemini_client import ask_gemini


def summarize_text(text: str) -> str:
    """
    Summarizes educational content and highlights crucial key points.
    """
    cleaned_input = text.strip()
    if not cleaned_input:
        return "Please provide content to summarize."

    prompt = f"""You are EduGenie, an expert educational summarizer.

Summarize the following educational content clearly and concisely for a student.

Content:
{cleaned_input}

Return your response using this exact structure:

SUMMARY
- A short, coherent, easy-to-understand summary paragraph explaining the core theme.

KEY POINTS
- Important point 1
- Important point 2
- Important point 3
- Important point 4

Use simple, student-friendly English that makes revision effortless.
"""
    return ask_gemini(prompt)
