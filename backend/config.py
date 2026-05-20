"""
Configuration for AutoGen AI Orchestrator.
"""
import os
import json
from pathlib import Path
from typing import Type, Tuple
from pydantic import SecretStr, field_validator, ValidationError, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
import re

# ─── Paths ───────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Load .env ──────────────────────────────────────────
from dotenv import load_dotenv

ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)

DATA_DIR = Path(os.getenv("AUTOGEN_DATA_DIR") or BASE_DIR / "data")
SKILLS_DIR = Path(os.getenv("AUTOGEN_SKILLS_DIR") or BASE_DIR / "skills_library")
CUSTOM_SKILLS_DIR = Path(os.getenv("AUTOGEN_CUSTOM_SKILLS_DIR") or BASE_DIR / "custom_skills")
WORKSPACE_DIR = Path(os.getenv("AUTOGEN_WORKSPACE_DIR") or BASE_DIR / "workspace")

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
SKILLS_DIR.mkdir(parents=True, exist_ok=True)
CUSTOM_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

# ─── Data files ──────────────────────────────────────────
AGENTS_FILE = DATA_DIR / "agents.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
SKILLS_FILE = DATA_DIR / "skills.json"
SETTINGS_FILE = DATA_DIR / "settings.json"

# ─── Security ───────────────────────────────────────────
class ConfigModel(BaseSettings):
    """Validates configuration and wraps sensitive keys in SecretStr."""
    api_key: SecretStr = SecretStr("")
    default_model: str = "gemini-2.5-flash"
    router_model: str = "gemini-3-flash-live"
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    max_rounds: int = Field(default=15, ge=1, le=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=128000)

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
        # Priority: init_settings > env_settings > dotenv_settings
        return init_settings, env_settings, dotenv_settings, file_secret_settings

    @field_validator('base_url', mode='before')
    def validate_base_url(cls, v):
        import urllib.parse
        if v is None or v == "":
            return v
        try:
            parsed = urllib.parse.urlparse(v)
            if hasattr(parsed.scheme, "decode"):
                raise ValueError("URL must be a string")
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL format. Must include scheme and netloc.")
        except (ValueError, AttributeError, TypeError) as e:
            raise ValueError(f"Invalid base_url: {e}")
        return v

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


def _validate_config(input_kwargs: dict = None) -> ConfigModel:
    """Helper to instantiate ConfigModel with fallback for invalid env vars."""
    if input_kwargs is None:
        input_kwargs = {}

    try:
        model = ConfigModel(**input_kwargs)
    except ValidationError as e:
        invalid_keys = [err.get('loc')[0] for err in e.errors() if err.get('loc')]
        # Temporarily remove invalid keys from os.environ to prevent re-reading invalid env vars
        old_envs = {
            f"AUTOGEN_{k.upper()}": os.environ.pop(f"AUTOGEN_{k.upper()}", None)
            for k in invalid_keys if isinstance(k, str)
        }

        # We must provide the default values in kwargs to override invalid entries in the .env file
        kwargs = {
            k: ("" if k == "api_key" else default_val)
            for k in invalid_keys if isinstance(k, str) and k in ConfigModel.model_fields
            if k == "api_key" or (default_val := ConfigModel.model_fields[k].get_default()) is not None
        }

        # Explicit settings take precedence
        kwargs.update(input_kwargs)

        try:
            # Initialize with kwargs (defaults + explicit overrides)
            model = ConfigModel(**kwargs)
        except ValidationError as final_e:
            # Re-raise if explicitly provided values are themselves invalid
            raise final_e
        finally:
            # Restore the environment variables
            for env_key, val in old_envs.items():
                if val is not None:
                    os.environ[env_key] = val

    return model


def get_settings() -> dict:
    """Get application settings."""
    # Migrate legacy JSON config to .env if needed
    legacy_settings = load_json(SETTINGS_FILE, {})
    if legacy_settings:
        try:
            save_settings(legacy_settings)
        except ValidationError:
            pass
        finally:
            save_json(SETTINGS_FILE, {})

    model = _validate_config()

    validated_settings = model.model_dump(mode="json")
    validated_settings["api_key"] = model.api_key
    return validated_settings


def save_settings(settings: dict):
    """Save application settings to .env."""
    from dotenv import set_key, unset_key
    if not ENV_FILE.exists():
        ENV_FILE.touch()

    # Filter out masked api_key from incoming data
    filtered_settings = {k: v for k, v in settings.items() if not (k == "api_key" and v == "**********")}

    # Validate before saving (handles unrelated invalid env vars gracefully)
    model = _validate_config(filtered_settings)
    validated_settings = model.model_dump(mode="json")
    validated_settings["api_key"] = model.api_key

    # Only save keys that were actually provided in the settings payload
    keys_to_save = [k for k in settings.keys() if k in validated_settings]

    for k in keys_to_save:
        v = validated_settings[k]

        if isinstance(v, SecretStr):
            str_v = v.get_secret_value()
        else:
            str_v = str(v)

        env_key = f"AUTOGEN_{k.upper()}"
        if str_v == "":
            unset_key(str(ENV_FILE), env_key)
            os.environ.pop(env_key, None)
        else:
            set_key(str(ENV_FILE), env_key, str_v)
            os.environ[env_key] = str_v

    save_json(SETTINGS_FILE, {})
