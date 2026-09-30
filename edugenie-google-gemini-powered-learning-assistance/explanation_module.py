"""
Explanation Module for EduGenie
Delivers structured concept explanations using a 5-step pedagogical framework:
1. Simple Definition
2. Main Idea
3. Important Points
4. Simple Example
5. Quick Revision

Supports both:
- Cloud-based Gemini API (default & high reasoning)
- Optional local LaMini-Flan-T5-783M model (via Hugging Face transformers)
"""

import logging
from config import USE_LOCAL_LAMINI
from gemini_client import ask_gemini

logger = logging.getLogger(__name__)

# Cached local pipeline
_lamini_pipeline = None


def _get_lamini_pipeline():
    """Lazily load the local LaMini-Flan-T5 model pipeline if requested."""
    global _lamini_pipeline
    if _lamini_pipeline is not None:
        return _lamini_pipeline

    try:
        from transformers import pipeline
        logger.info("Loading local model MBZUAI/LaMini-Flan-T5-783M...")
        _lamini_pipeline = pipeline(
            "text2text-generation",
            model="MBZUAI/LaMini-Flan-T5-783M",
            max_length=512
        )
        return _lamini_pipeline
    except Exception as e:
        logger.warning("Failed to load local LaMini model (%s). Falling back to Gemini.", e)
        return None


def explain_topic(text: str) -> str:
    """
    Explains an educational topic to a beginner student using a structured 5-part format.
    """
    cleaned_input = text.strip()
    if not cleaned_input:
        return "Please provide a topic to explain."

    prompt = f"""You are EduGenie, an expert and patient educational teacher.

Explain this topic to a student who is learning it for the very first time.

Topic:
{cleaned_input}

Use this exact structure:

1. Simple Definition
2. Main Idea
3. Important Points
4. Simple Example
5. Quick Revision

Use easy, relatable English and make it captivating and memorable.
"""

    if USE_LOCAL_LAMINI:
        pipeline = _get_lamini_pipeline()
        if pipeline:
            try:
                response = pipeline(prompt)
                return response[0]["generated_text"].strip()
            except Exception as e:
                logger.error("Local inference error: %s. Falling back to Gemini.", e)

    return ask_gemini(prompt)
