import os
import json
import pytest
from pydantic import SecretStr, ValidationError
from backend.config import get_settings, save_settings, SETTINGS_FILE, DEFAULT_SETTINGS, ConfigModel

@pytest.fixture(autouse=True)
def setup_teardown_settings():
    original_data = None
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            original_data = json.load(f)

    orig_env = os.environ.get("AUTOGEN_API_KEY")
    if "AUTOGEN_API_KEY" in os.environ:
        del os.environ["AUTOGEN_API_KEY"]

    yield

    if original_data is not None:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(original_data, f, indent=2, ensure_ascii=False)
    else:
        if SETTINGS_FILE.exists():
            SETTINGS_FILE.unlink()

    if orig_env is not None:
        os.environ["AUTOGEN_API_KEY"] = orig_env
    elif "AUTOGEN_API_KEY" in os.environ:
        del os.environ["AUTOGEN_API_KEY"]

def test_secret_str_prevents_json_dump():
    secret = SecretStr("my-super-secret-key")
    with pytest.raises(TypeError):
        json.dumps({"key": secret})

def test_config_model_validation():
    # Valid
    model = ConfigModel(**DEFAULT_SETTINGS | {"api_key": "valid-api-key-123"})
    assert model.api_key.get_secret_value() == "valid-api-key-123"

    # Invalid: too short
    with pytest.raises(ValidationError):
        ConfigModel(**DEFAULT_SETTINGS | {"api_key": "short"})

    # Invalid: whitespace
    with pytest.raises(ValidationError):
        ConfigModel(**DEFAULT_SETTINGS | {"api_key": "has space in it"})

def test_get_settings_masks_api_key():
    test_settings = DEFAULT_SETTINGS.copy()
    test_settings["api_key"] = "test-key-from-file"

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(test_settings, f)

    settings = get_settings()

    assert isinstance(settings["api_key"], SecretStr)
    assert settings["api_key"].get_secret_value() == "test-key-from-file"

def test_get_settings_invalid_key_fallback():
    test_settings = DEFAULT_SETTINGS.copy()
    test_settings["api_key"] = "short"

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(test_settings, f)

    settings = get_settings()
    # It should catch ValidationError and default to empty SecretStr
    assert isinstance(settings["api_key"], SecretStr)
    assert settings["api_key"].get_secret_value() == ""

def test_save_settings_scrubs_api_key():
    test_settings = DEFAULT_SETTINGS.copy()
    test_settings["api_key"] = SecretStr("key-to-scrub")

    save_settings(test_settings)

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["api_key"] == ""

def test_get_settings_ignores_empty_env_vars(monkeypatch):
    test_settings = DEFAULT_SETTINGS.copy()
    test_settings["max_rounds"] = 25
    test_settings["temperature"] = 0.5

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(test_settings, f)

    # Simulate an empty environment variable being set
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "")

    settings = get_settings()

    # The empty env var should be ignored, preserving the value from the file
    assert settings["max_rounds"] == 25
    assert settings["temperature"] == 0.5

def test_get_settings_typecasts_env_vars(monkeypatch):
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "50")
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "0.9")

    settings = get_settings()

    assert settings["max_rounds"] == 50
    assert settings["temperature"] == 0.9
