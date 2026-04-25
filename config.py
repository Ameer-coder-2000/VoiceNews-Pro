import os

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> None:
        """
        Fallback when python-dotenv is not installed yet.
        The app can still run if environment variables are already available.
        """
        return None


# Try to load from .env.local first for local development
try:
    load_dotenv('.env.local')
except:
    pass
# Fallback to standard .env
load_dotenv()


NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()
NEWS_API_PROVIDER = os.getenv("NEWS_API_PROVIDER", "gnews").strip().lower()
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general").strip().lower()
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "in").strip().lower()
MAX_HEADLINES = int(os.getenv("MAX_HEADLINES", "5"))
LANGUAGE = os.getenv("LANGUAGE", "en").strip().lower()

SUPPORTED_CATEGORIES = [
    "general",
    "world",
    "nation",
    "business",
    "technology",
    "entertainment",
    "sports",
    "science",
    "health",
]
