import re
from config import GEMINI_API_KEY, GEMINI_MODEL, is_gemini_configured


def clean_json_block(text: str) -> str:
    """
    Cleans markdown code fences, e.g. ```json ... ``` or ``` ... ```
    to ensure valid JSON text can be parsed.
    """
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def ask_gemini(prompt: str) -> str:
    """
    Sends a prompt to Google Gemini model and returns the response string.
    Supports both google-genai and google-generativeai SDKs.
    """
    if not is_gemini_configured():
        return (
            "Gemini API key is missing or unconfigured.\n\n"
            "Please open your .env file and set your key:\n"
            "GEMINI_API_KEY=your_actual_api_key_here\n\n"
            "You can obtain a free API key at: https://aistudio.google.com/"
        )

    import os
    model_name = os.getenv("GEMINI_MODEL", GEMINI_MODEL).strip() or "gemini-flash-latest"
    models_to_try = [model_name]
    for fallback in ["gemini-flash-latest", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-flash-lite-latest"]:
        if fallback not in models_to_try:
            models_to_try.append(fallback)

    # 1. Try modern google-genai SDK
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        last_error = None
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=prompt
                )
                text = getattr(response, "text", None)
                if text:
                    return text.strip()
                return "The AI returned an empty response."
            except Exception as model_err:
                err_str = str(model_err)
                last_error = err_str
                # If model is deprecated, not found, or experiencing 503/429 spikes, try next fallback
                if any(k in err_str for k in ["404", "NOT_FOUND", "no longer available", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "high demand"]):
                    continue
                if "API_KEY_INVALID" in err_str or ("400" in err_str and "API key" in err_str):
                    return "Gemini connection error: Invalid API key. Please check your GEMINI_API_KEY in .env."
                return f"Gemini connection error: {err_str}"

        if last_error:
            return f"Gemini connection error: {last_error}"

    except ImportError:
        pass

    # 2. Try legacy google-generativeai SDK fallback
    try:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=GEMINI_API_KEY)
        for m in models_to_try:
            try:
                model = genai_legacy.GenerativeModel(m)
                response = model.generate_content(prompt)
                text = getattr(response, "text", None)
                if text:
                    return text.strip()
                return "The AI returned an empty response."
            except Exception as legacy_err:
                err_str = str(legacy_err)
                if any(k in err_str.lower() for k in ["404", "not_found", "not found", "503", "unavailable", "429", "resource_exhausted", "high demand"]):
                    continue
                return f"Gemini connection error: {err_str}"
    except ImportError:
        return (
            "Gemini SDK is not installed.\n"
            "Please install dependencies with: pip install -r requirements.txt"
        )
    except Exception as e:
        return f"Gemini connection error: {str(e)}"
