import os
import json
import pytest
from pydantic import SecretStr, ValidationError
from backend.config import get_settings, save_settings, ENV_FILE, ConfigModel

from backend.config import SETTINGS_FILE, save_json

@pytest.fixture(autouse=True)
def setup_teardown_settings():
    original_env = None
    if ENV_FILE.exists():
        original_env = ENV_FILE.read_text(encoding="utf-8")

    original_json = None
    if SETTINGS_FILE.exists():
        original_json = SETTINGS_FILE.read_text(encoding="utf-8")

    orig_env_var = os.environ.get("AUTOGEN_API_KEY")
    if "AUTOGEN_API_KEY" in os.environ:
        del os.environ["AUTOGEN_API_KEY"]

    yield

    if original_env is not None:
        ENV_FILE.write_text(original_env, encoding="utf-8")
    else:
        if ENV_FILE.exists():
            ENV_FILE.unlink()

    if original_json is not None:
        SETTINGS_FILE.write_text(original_json, encoding="utf-8")
    else:
        if SETTINGS_FILE.exists():
            SETTINGS_FILE.unlink()

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

def test_legacy_json_migration():
    from backend.config import SETTINGS_FILE, save_json, load_json

    # Create a legacy JSON file with some settings
    test_settings = {"temperature": 0.3, "max_rounds": 42}
    save_json(SETTINGS_FILE, test_settings)

    # Make sure ENV_FILE doesn't have these to prove migration works
    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        if "AUTOGEN_MAX_ROUNDS" in content:
            ENV_FILE.unlink()

    # get_settings should read it, migrate to .env, and clear JSON
    settings = get_settings()

    assert settings["temperature"] == 0.3
    assert settings["max_rounds"] == 42

    # verify .env has it
    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        assert "AUTOGEN_TEMPERATURE='0.3'" in content or "AUTOGEN_TEMPERATURE=0.3" in content
        assert "AUTOGEN_MAX_ROUNDS='42'" in content or "AUTOGEN_MAX_ROUNDS=42" in content
    else:
        pytest.fail("ENV_FILE was not created during migration")

    # verify JSON is cleared securely
    assert load_json(SETTINGS_FILE) == {}

def test_legacy_json_migration_invalid_data():
    from backend.config import SETTINGS_FILE, save_json, load_json

    # Create a legacy JSON file with invalid settings
    test_settings = {"api_key": "short"}
    save_json(SETTINGS_FILE, test_settings)

    # get_settings should read it, fail to migrate due to ValidationError, but still clear JSON and not crash
    settings = get_settings()

    # Default should be returned or an empty SecretStr for api_key
    assert settings["api_key"].get_secret_value() == ""

    # verify JSON is cleared securely even after error
    assert load_json(SETTINGS_FILE) == {}

def test_save_settings_clear_api_key():
    # Make sure we start fresh
    if ENV_FILE.exists():
        ENV_FILE.unlink()

    # Save a valid key
    save_settings({"api_key": "valid-key-12345"})

    content = ENV_FILE.read_text(encoding="utf-8")
    assert "valid-key-12345" in content

    # Clear it
    save_settings({"api_key": ""})

    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        assert "valid-key-12345" not in content
        assert "AUTOGEN_API_KEY=''" not in content and "AUTOGEN_API_KEY=" not in content

def test_save_settings_ignores_unrelated_invalid_env_vars(monkeypatch):
    # Setup an unrelated invalid env var
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "invalid_int")

    # saving a different, valid setting should succeed and not crash
    # due to the invalid max_rounds environment variable.
    save_settings({"temperature": 0.8})

    # Verify the partial update was written
    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        assert "AUTOGEN_TEMPERATURE='0.8'" in content or "AUTOGEN_TEMPERATURE=0.8" in content
    else:
        pytest.fail("ENV_FILE was not created")

def test_config_model_boundaries():
    # Valid bounds
    model = ConfigModel(temperature=0.0, max_rounds=1, max_tokens=1)
    assert model.temperature == 0.0

    # Invalid: temperature too low
    with pytest.raises(ValidationError):
        ConfigModel(temperature=-0.1)

    # Invalid: temperature too high
    with pytest.raises(ValidationError):
        ConfigModel(temperature=2.1)

    # Invalid: max_rounds too low
    with pytest.raises(ValidationError):
        ConfigModel(max_rounds=0)

    # Invalid: max_rounds too high
    with pytest.raises(ValidationError):
        ConfigModel(max_rounds=101)

    # Invalid: max_tokens too low
    with pytest.raises(ValidationError):
        ConfigModel(max_tokens=0)

    # Invalid: max_tokens too high
    with pytest.raises(ValidationError):
        ConfigModel(max_tokens=128001)

def test_get_settings_out_of_bounds_fallback(monkeypatch):
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "5.0")
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "1000")
    monkeypatch.setenv("AUTOGEN_MAX_TOKENS", "-10")

    settings = get_settings()

    assert settings["temperature"] == 0.7  # Default from model
    assert settings["max_rounds"] == 15  # Default from model
    assert settings["max_tokens"] == 4096  # Default from model

def test_path_configuration_env_vars():
    import subprocess
    import sys

    # Run python in a subprocess with mocked env vars to verify parsing
    env = os.environ.copy()
    env["AUTOGEN_DATA_DIR"] = "/tmp/mock_data"
    env["AUTOGEN_SKILLS_DIR"] = "/tmp/mock_skills"
    env["AUTOGEN_CUSTOM_SKILLS_DIR"] = "/tmp/mock_custom_skills"

    code = (
        "import sys\n"
        "from backend.config import DATA_DIR, SKILLS_DIR, CUSTOM_SKILLS_DIR\n"
        "sys.stdout.write(str(DATA_DIR) + '|' + str(SKILLS_DIR) + '|' + str(CUSTOM_SKILLS_DIR))\n"
    )

    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert result.returncode == 0

    paths = result.stdout.split('|')
    assert paths[0] == "/tmp/mock_data"
    assert paths[1] == "/tmp/mock_skills"
    assert paths[2] == "/tmp/mock_custom_skills"
