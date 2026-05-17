"""
Configuration for AutoGen AI Orchestrator.
"""
import os
import json
from pathlib import Path
from typing import Type, Tuple
from pydantic import SecretStr, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
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
class ConfigModel(BaseSettings):
    """Validates configuration and wraps sensitive keys in SecretStr."""
    api_key: SecretStr = SecretStr("")
    default_model: str = "gemini-2.5-flash"
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    max_rounds: int = 15
    temperature: float = 0.7
    max_tokens: int = 4096

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_prefix="AUTOGEN_",
        env_ignore_empty=True,
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        # Priority: env_settings > dotenv_settings > init_settings
        return env_settings, dotenv_settings, init_settings, file_secret_settings

    @field_validator('api_key', mode='before')
    def validate_api_key(cls, v):
        if not v:
            return v

        v_str = v.get_secret_value() if isinstance(v, SecretStr) else str(v)
        if v_str and (len(v_str) < 10 or re.search(r'\s', v_str)):
            raise ValueError("API key must be at least 10 characters and contain no whitespace.")
        return v

def load_json(filepath: Path, default=None):
    """Load JSON data from a file, returning default if not found."""
    if default is None:
        default = {}
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
    try:
        model = ConfigModel()
    except ValidationError as e:
        # If the API key is the cause of validation error, clear it. Otherwise, let it fail loud.
        has_api_key_error = any(err.get('loc') == ('api_key',) for err in e.errors())
        if has_api_key_error:
            # Temporarily set it to empty string in os.environ to override any invalid value in .env
            old_env = os.environ.get("AUTOGEN_API_KEY")
            os.environ["AUTOGEN_API_KEY"] = ""
            try:
                model = ConfigModel()
            finally:
                if old_env is not None:
                    os.environ["AUTOGEN_API_KEY"] = old_env
                else:
                    del os.environ["AUTOGEN_API_KEY"]

            if len(e.errors()) > 1:
                raise
        else:
            raise

    validated_settings = model.model_dump(mode="json")
    validated_settings["api_key"] = model.api_key
    return validated_settings


def save_settings(settings: dict):
    """Save application settings to .env."""
    from dotenv import set_key
    if not ENV_FILE.exists():
        ENV_FILE.touch()

    for k, v in settings.items():
        if k == "api_key" and not v:
            continue

        if isinstance(v, SecretStr):
            str_v = v.get_secret_value()
        else:
            str_v = str(v)

        set_key(str(ENV_FILE), f"AUTOGEN_{k.upper()}", str_v)
        os.environ[f"AUTOGEN_{k.upper()}"] = str_v

    save_json(SETTINGS_FILE, {})
