"""
Configuration for AutoGen AI Orchestrator.
"""
import os
import json
from pathlib import Path
from pydantic import BaseModel, SecretStr, field_validator, ValidationError
import re

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

# ─── Load .env ──────────────────────────────────────────
from dotenv import load_dotenv

ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)

# ─── Security ───────────────────────────────────────────
class ConfigModel(BaseModel):
    """Validates configuration and wraps sensitive keys in SecretStr."""
    api_key: SecretStr = SecretStr("")
    default_model: str = "gemini-2.5-flash"
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    max_rounds: int = 15
    temperature: float = 0.7
    max_tokens: int = 4096

    @field_validator('api_key', mode='before')
    def validate_api_key(cls, v):
        if not v:
            return v

        v_str = v.get_secret_value() if isinstance(v, SecretStr) else str(v)
        if v_str and (len(v_str) < 10 or re.search(r'\s', v_str)):
            raise ValueError("API key must be at least 10 characters and contain no whitespace.")
        return v

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

    # Load and typecast overrides from env vars
    env_overrides = {
        "api_key": os.getenv("AUTOGEN_API_KEY"),
        "default_model": os.getenv("AUTOGEN_DEFAULT_MODEL"),
        "base_url": os.getenv("AUTOGEN_BASE_URL"),
        "max_rounds": os.getenv("AUTOGEN_MAX_ROUNDS"),
        "temperature": os.getenv("AUTOGEN_TEMPERATURE"),
        "max_tokens": os.getenv("AUTOGEN_MAX_TOKENS"),
    }

    # Filter out None values to prevent overriding valid settings with empty env vars
    active_overrides = {k: v for k, v in env_overrides.items() if v is not None and v != ""}
    settings.update(active_overrides)

    try:
        model = ConfigModel(**settings)
        validated_settings = model.model_dump(mode="json")
        validated_settings["api_key"] = model.api_key
    except ValidationError as e:
        # If the API key is the cause of validation error, clear it. Otherwise, let it fail loud.
        has_api_key_error = any(err.get('loc') == ('api_key',) for err in e.errors())
        if has_api_key_error:
            # Re-instantiate model without the invalid api_key to validate remaining fields
            safe_settings = settings.copy()
            safe_settings["api_key"] = ""
            model = ConfigModel(**safe_settings)
            validated_settings = model.model_dump(mode="json")
            validated_settings["api_key"] = SecretStr("")

            # If there are other errors initially, raise them
            if len(e.errors()) > 1:
                raise
        else:
            raise

    return validated_settings


def save_settings(settings: dict):
    """Save application settings, scrubbing sensitive data."""
    # Create a copy so we don't modify the runtime state
    safe_settings = dict(settings)
    if "api_key" in safe_settings:
        safe_settings["api_key"] = ""
    save_json(SETTINGS_FILE, safe_settings)
