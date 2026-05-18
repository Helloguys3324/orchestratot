import os
import json
import pytest
from pydantic import SecretStr, ValidationError
from backend.config import get_settings, save_settings, ENV_FILE, ConfigModel

@pytest.fixture(autouse=True)
def setup_teardown_settings():
    original_env = None
    if ENV_FILE.exists():
        original_env = ENV_FILE.read_text(encoding="utf-8")

    orig_env_var = os.environ.get("AUTOGEN_API_KEY")
    if "AUTOGEN_API_KEY" in os.environ:
        del os.environ["AUTOGEN_API_KEY"]

    yield

    if original_env is not None:
        ENV_FILE.write_text(original_env, encoding="utf-8")
    else:
        if ENV_FILE.exists():
            ENV_FILE.unlink()

    if orig_env_var is not None:
        os.environ["AUTOGEN_API_KEY"] = orig_env_var
    elif "AUTOGEN_API_KEY" in os.environ:
        del os.environ["AUTOGEN_API_KEY"]

def test_secret_str_prevents_json_dump():
    secret = SecretStr("my-super-secret-key")
    with pytest.raises(TypeError):
        json.dumps({"key": secret})

def test_config_model_validation():
    # Valid
    model = ConfigModel(**{"api_key": "valid-api-key-123"})
    assert model.api_key.get_secret_value() == "valid-api-key-123"

    # Invalid: too short
    with pytest.raises(ValidationError):
        ConfigModel(**{"api_key": "short"})

    # Invalid: whitespace
    with pytest.raises(ValidationError):
        ConfigModel(**{"api_key": "has space in it"})

def test_get_settings_masks_api_key(monkeypatch):
    monkeypatch.setenv("AUTOGEN_API_KEY", "test-key-from-env")
    settings = get_settings()

    assert isinstance(settings["api_key"], SecretStr)
    assert settings["api_key"].get_secret_value() == "test-key-from-env"

def test_get_settings_invalid_key_fallback(monkeypatch):
    monkeypatch.setenv("AUTOGEN_API_KEY", "short")
    settings = get_settings()

    # It should catch ValidationError and default to empty SecretStr
    assert isinstance(settings["api_key"], SecretStr)
    assert settings["api_key"].get_secret_value() == ""

def test_save_settings_writes_to_env():
    test_settings = {"api_key": SecretStr("key-to-scrub"), "max_rounds": 25}
    save_settings(test_settings)

    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        assert "AUTOGEN_API_KEY" in content
        assert "AUTOGEN_MAX_ROUNDS" in content
    else:
        pytest.fail("ENV_FILE was not created")

def test_save_settings_partial_update():
    # Make sure we start fresh for this test
    if ENV_FILE.exists():
        ENV_FILE.unlink()

    test_settings = {"max_rounds": 30}
    save_settings(test_settings)

    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        assert "AUTOGEN_MAX_ROUNDS" in content
        assert "AUTOGEN_TEMPERATURE" not in content
    else:
        pytest.fail("ENV_FILE was not created")

def test_get_settings_ignores_empty_env_vars(monkeypatch):
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "")
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "0.5")

    settings = get_settings()

    assert settings["max_rounds"] == 15  # Default from model
    assert settings["temperature"] == 0.5

def test_get_settings_typecasts_env_vars(monkeypatch):
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "50")
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "0.9")

    settings = get_settings()

    assert settings["max_rounds"] == 50
    assert settings["temperature"] == 0.9

def test_get_settings_all_invalid_fallback(monkeypatch):
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "invalid_float")
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "invalid_int")

    settings = get_settings()

    assert settings["temperature"] == 0.7  # Default from model
    assert settings["max_rounds"] == 15  # Default from model

def test_save_settings_validation():
    # Valid settings, should pass
    save_settings({"temperature": 0.5, "max_rounds": 20})

    # Validation error with invalid setting
    with pytest.raises(ValidationError):
        save_settings({"temperature": "invalid_float"})

    # Should safely ignore placeholder api_key
    save_settings({"api_key": "**********", "temperature": 0.6})
