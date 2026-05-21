"""
Configuration for AutoGen AI Orchestrator.
"""
import os
import json
from pathlib import Path
from typing import Type, Tuple
from pydantic import SecretStr, field_validator, ValidationError, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from pydantic_core import PydanticUndefined
import re

# ─── Paths ───────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Load .env ──────────────────────────────────────────
from dotenv import load_dotenv

ENV_FILE = Path(os.environ.get("AUTOGEN_ENV_FILE", BASE_DIR / ".env"))
load_dotenv(dotenv_path=ENV_FILE)

def _get_path_env(key: str, default_subpath: str) -> Path:
    val = os.environ.get(key)
    return Path(val) if val else BASE_DIR / default_subpath

# Since we can't initialize ConfigModel here without causing cyclical/missing dependency
# at import time when tests run (as ConfigModel relies on ENV_FILE which is not fully
# defined in scope sometimes during tests execution), we'll parse paths manually but
# with the exact same logic as ConfigModel.


DATA_DIR = _get_path_env("AUTOGEN_DATA_DIR", "data")
SKILLS_DIR = _get_path_env("AUTOGEN_SKILLS_DIR", "skills_library")
CUSTOM_SKILLS_DIR = _get_path_env("AUTOGEN_CUSTOM_SKILLS_DIR", "custom_skills")
WORKSPACE_DIR = _get_path_env("AUTOGEN_WORKSPACE_DIR", "workspace")

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
    default_model: str = Field(default="gemini-2.5-flash", json_schema_extra={"env_ignore_empty": False})
    router_model: str = Field(default="gemini-3-flash-live", json_schema_extra={"env_ignore_empty": False})
    base_url: str = Field(default="https://generativelanguage.googleapis.com/v1beta/openai/", json_schema_extra={"env_ignore_empty": False})
    max_rounds: int = Field(default=15, ge=1, le=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=128000)

    # Path configuration
    data_dir: Path = Field(default_factory=lambda: BASE_DIR / "data", json_schema_extra={"env_ignore_empty": False})
    skills_dir: Path = Field(default_factory=lambda: BASE_DIR / "skills_library", json_schema_extra={"env_ignore_empty": False})
    custom_skills_dir: Path = Field(default_factory=lambda: BASE_DIR / "custom_skills", json_schema_extra={"env_ignore_empty": False})
    workspace_dir: Path = Field(default_factory=lambda: BASE_DIR / "workspace", json_schema_extra={"env_ignore_empty": False})


    @field_validator('data_dir', 'skills_dir', 'custom_skills_dir', 'workspace_dir', mode='before')
    def validate_paths(cls, v, info):
        if not v or str(v).strip() == "" or str(v) == ".":
            factory = cls.model_fields[info.field_name].default_factory
            if factory:
                return factory()
        return v

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
        from pydantic_settings import DotEnvSettingsSource
        # Ensure we dynamically reload DotEnvSettingsSource based on the current ENV_FILE path (important for tests)
        return init_settings, env_settings, DotEnvSettingsSource(settings_cls, env_file=str(ENV_FILE)), file_secret_settings

    @field_validator('default_model', 'router_model', 'base_url', 'max_rounds', 'temperature', 'max_tokens', mode='before')
    def validate_empty_strings(cls, v, info):
        if v == "" or (isinstance(v, str) and not v.strip()):
            field_info = cls.model_fields[info.field_name]
            if field_info.default_factory is not None:
                return field_info.default_factory()
            elif getattr(field_info, 'get_default', None) and field_info.get_default() is not None and field_info.get_default() is not PydanticUndefined:
                return field_info.get_default()
        return v

    @field_validator('base_url', mode='before')
    def validate_base_url(cls, v):
        import urllib.parse
        if v is None or v == "":
            return v
        if not isinstance(v, str):
            raise ValueError("URL must be a string")
        try:
            parsed = urllib.parse.urlparse(v)
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

        UPDATABLE_FIELDS = set(ConfigModel.model_fields.keys())

        # We must provide the default values to override invalid entries in the .env file
        defaults = {}
        for k in invalid_keys:
            if isinstance(k, str) and k in UPDATABLE_FIELDS:
                if k == "api_key":
                    defaults[k] = ""
                else:
                    field_info = ConfigModel.model_fields[k]
                    # Handle both default values and default factories
                    if field_info.default_factory is not None:
                        defaults[k] = field_info.default_factory()
                    elif getattr(field_info, 'get_default', None) and field_info.get_default() is not None and field_info.get_default() is not PydanticUndefined:
                        defaults[k] = field_info.get_default()

        # Explicit settings take precedence
        merged = {**defaults, **input_kwargs}
        kwargs = {k: merged[k] for k in UPDATABLE_FIELDS if k in merged}

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

    # Override settings output to match the original globals for now,
    # as tests and UI might expect standard path layouts.
    validated_settings["data_dir"] = str(model.data_dir)
    validated_settings["skills_dir"] = str(model.skills_dir)
    validated_settings["custom_skills_dir"] = str(model.custom_skills_dir)
    validated_settings["workspace_dir"] = str(model.workspace_dir)

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
