"""
Configuration for AutoGen AI Orchestrator.
"""
import os
import json
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SKILLS_DIR = BASE_DIR / "skills_library"
CUSTOM_SKILLS_DIR = BASE_DIR / "custom_skills"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
SKILLS_DIR.mkdir(exist_ok=True)
CUSTOM_SKILLS_DIR.mkdir(exist_ok=True)

# ─── Data files ──────────────────────────────────────────
AGENTS_FILE = DATA_DIR / "agents.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
SKILLS_FILE = DATA_DIR / "skills.json"
SETTINGS_FILE = DATA_DIR / "settings.json"

# ─── Default settings ───────────────────────────────────
DEFAULT_SETTINGS = {
    "api_key": "",
    "default_model": "gemini-2.5-flash",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "max_rounds": 15,
    "temperature": 0.7,
    "max_tokens": 4096,
}


def load_json(filepath: Path, default=None):
    """Load JSON data from a file, returning default if not found."""
    if default is None:
        default = []
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(filepath: Path, data):
    """Save data to a JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_settings() -> dict:
    """Get application settings."""
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    # Merge with defaults for any missing keys
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value
    env_overrides = {
        "api_key": os.getenv("AUTOGEN_API_KEY"),
        "default_model": os.getenv("AUTOGEN_DEFAULT_MODEL"),
        "base_url": os.getenv("AUTOGEN_BASE_URL"),
    }
    for key, value in env_overrides.items():
        if value:
            settings[key] = value
    return settings


def save_settings(settings: dict):
    """Save application settings."""
    save_json(SETTINGS_FILE, settings)
