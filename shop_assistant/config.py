"""Constants and secret names. SDD §3.9. Ticket #1."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CHANNEL = "status_dokon"
STALE_DAYS = 60            # FR-16
MAX_RESULTS = 5            # FR-18
FETCH_LIMIT = 500          # FR-1
CATEGORIES = ["kiyim", "poyabzal", "aksessuar", "boshqa"]   # SDD §2.2
HISTORY_TURNS = 10         # FR-17
EXTRACT_BATCH = 10         # NFR-3
EMBED_BATCH = 128          # NFR-3

MODEL = "gemma4:31b"            # Ollama, tool calling (SDD §1.1)
MAX_ITERATIONS = 8
MAX_TOKENS = 1024
EMBED_MODEL = "bge-m3"           # Ollama, multilingual embeddings, 1024-d
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SESSION_DIR = ROOT / "session"
POSTS_PATH = DATA_DIR / "posts.jsonl"
PRODUCTS_PATH = DATA_DIR / "products.jsonl"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.npy"
EMBEDDINGS_IDS_PATH = DATA_DIR / "embeddings_ids.json"
FAQ_PATH = DATA_DIR / "faq.jsonl"
FAQ_EMBEDDINGS_PATH = DATA_DIR / "faq_embeddings.npy"
STATE_PATH = DATA_DIR / "state.json"
LOG_PATH = DATA_DIR / "log.jsonl"

# Secrets — read lazily so importing config never fails without .env (NFR-6).
ENV_KEYS = ("TG_API_ID", "TG_API_HASH", "TG_BOT_TOKEN", "TG_OWNER_ID")

# The Anthropic SDK talks to Ollama's Anthropic-compatible endpoint; no real key needed.
os.environ.setdefault("ANTHROPIC_BASE_URL", OLLAMA_URL)
os.environ.setdefault("ANTHROPIC_API_KEY", "ollama")


def secret(name: str) -> str:
    """Return env var `name` or raise a clear error naming the missing key."""
    if name not in ENV_KEYS:
        raise KeyError(f"{name} is not a known secret; see ENV_KEYS")
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is not set — add it to .env")
    return value
