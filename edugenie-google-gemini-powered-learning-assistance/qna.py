"""
QnA Module for EduGenie
Handles question-answering tasks for academic queries and general knowledge.
Powered by Google Gemini with a student-friendly prompt structure.
"""

from gemini_client import ask_gemini


def question_answer(text: str) -> str:
    """
    Answers a student's question accurately with clear structure,
    bullet points, and simple language.
    """
    cleaned_input = text.strip()
    if not cleaned_input:
        return "Please provide a valid question."

    prompt = f"""You are EduGenie, a friendly and knowledgeable AI learning assistant for students.

Answer the student's question accurately, engagingly, and helpfully.

Rules:
- Use simple, student-friendly English.
- Explain concepts clearly without unnecessary jargon.
- Give concrete examples whenever helpful.
- Structure the answer cleanly using headings and bullet points.
- Highlight key takeaways at the end.

Student question:
{cleaned_input}
"""
    return ask_gemini(prompt)
