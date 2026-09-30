import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Auto-create .env if missing
if not ENV_FILE.exists():
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write("# Google Gemini API Key\n")
        f.write("GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n")
        f.write("GEMINI_MODEL=gemini-3.8-flash\n")
        f.write("USE_LOCAL_LAMINI=False\n")
        f.write("HOST=127.0.0.1\n")
        f.write("PORT=8000\n")

load_dotenv(dotenv_path=ENV_FILE)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
USE_LOCAL_LAMINI = os.getenv("USE_LOCAL_LAMINI", "False").strip().lower() in ("true", "1", "yes")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

PLACEHOLDER_KEYS = {
    "",
    "YOUR_GEMINI_API_KEY_HERE",
    "your_actual_api_key_here",
}

def is_gemini_configured() -> bool:
    """Check if a valid Gemini API key is configured."""
    return bool(GEMINI_API_KEY and GEMINI_API_KEY not in PLACEHOLDER_KEYS)
