import os
import json
import pytest
from pydantic import SecretStr, ValidationError
from backend.config import get_settings, save_settings, ENV_FILE, ConfigModel

from backend.config import SETTINGS_FILE, save_json

@pytest.fixture(autouse=True)
def setup_teardown_settings(tmp_path, monkeypatch):
    import backend.config

    # Create temporary paths for tests
    temp_env_file = tmp_path / ".env"
    temp_settings_file = tmp_path / "settings.json"

    # Store original values
    orig_env_file = backend.config.ENV_FILE
    orig_settings_file = backend.config.SETTINGS_FILE

    # Override configuration paths dynamically
    backend.config.ENV_FILE = temp_env_file
    backend.config.SETTINGS_FILE = temp_settings_file

    # Override environment variable so child processes also see the temp file
    monkeypatch.setenv("AUTOGEN_ENV_FILE", str(temp_env_file))

    # Ensure AUTOGEN_API_KEY is unset in the environment initially
    if "AUTOGEN_API_KEY" in os.environ:
        monkeypatch.delenv("AUTOGEN_API_KEY", raising=False)

    yield

    # Restore original paths
    backend.config.ENV_FILE = orig_env_file
    backend.config.SETTINGS_FILE = orig_settings_file

def test_secret_str_prevents_json_dump():
    secret = SecretStr("my-super-secret-key")
    with pytest.raises(TypeError):
        json.dumps({"key": secret})

def test_config_model_validation(monkeypatch):
    monkeypatch.delenv('AUTOGEN_TEMPERATURE', raising=False)
    # Valid
    model = ConfigModel(api_key="valid-api-key-123")
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

    assert settings["api_key"] == "**********"

def test_get_settings_invalid_key_fallback(monkeypatch):
    monkeypatch.setenv("AUTOGEN_API_KEY", "short")
    settings = get_settings()

    # It should catch ValidationError and default to empty SecretStr
    assert settings["api_key"] == ""

def test_save_settings_writes_to_env():
    test_settings = {"api_key": SecretStr("key-to-scrub"), "max_rounds": 25}
    save_settings(test_settings)

    import backend.config
    if backend.config.ENV_FILE.exists():
        content = backend.config.ENV_FILE.read_text(encoding="utf-8")
        assert "AUTOGEN_API_KEY" in content
        assert "AUTOGEN_MAX_ROUNDS" in content
    else:
        pytest.fail("ENV_FILE was not created")

def test_save_settings_partial_update():
    # Make sure we start fresh for this test
    import backend.config
    if backend.config.ENV_FILE.exists():
        backend.config.ENV_FILE.unlink()

    test_settings = {"max_rounds": 30}
    save_settings(test_settings)

    if backend.config.ENV_FILE.exists():
        content = backend.config.ENV_FILE.read_text(encoding="utf-8")
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

    import backend.config
    # Make sure ENV_FILE doesn't have these to prove migration works
    if backend.config.ENV_FILE.exists():
        content = backend.config.ENV_FILE.read_text(encoding="utf-8")
        if "AUTOGEN_MAX_ROUNDS" in content:
            backend.config.ENV_FILE.unlink()

    # get_settings should read it, migrate to .env, and clear JSON
    settings = get_settings()

    assert settings["temperature"] == 0.3
    assert settings["max_rounds"] == 42

    # verify .env has it
    if backend.config.ENV_FILE.exists():
        content = backend.config.ENV_FILE.read_text(encoding="utf-8")
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
    assert settings["api_key"] == ""

    # verify JSON is cleared securely even after error
    assert load_json(SETTINGS_FILE) == {}

def test_save_settings_clear_api_key():
    import backend.config
    # Make sure we start fresh
    if backend.config.ENV_FILE.exists():
        backend.config.ENV_FILE.unlink()

    # Save a valid key
    save_settings({"api_key": "valid-key-12345"})

    content = backend.config.ENV_FILE.read_text(encoding="utf-8")
    assert "valid-key-12345" in content

    # Clear it
    save_settings({"api_key": ""})

    if backend.config.ENV_FILE.exists():
        content = backend.config.ENV_FILE.read_text(encoding="utf-8")
        assert "valid-key-12345" not in content
        assert "AUTOGEN_API_KEY=''" not in content and "AUTOGEN_API_KEY=" not in content

def test_save_settings_ignores_unrelated_invalid_env_vars(monkeypatch):
    import backend.config
    # Setup an unrelated invalid env var
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "invalid_int")

    # saving a different, valid setting should succeed and not crash
    # due to the invalid max_rounds environment variable.
    save_settings({"temperature": 0.8})

    # Verify the partial update was written
    if backend.config.ENV_FILE.exists():
        content = backend.config.ENV_FILE.read_text(encoding="utf-8")
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
    assert settings["router_model"] == "gemini-3-flash-live"
    assert settings["default_model"] == "gemini-2.5-flash"

def test_path_configuration_env_vars():
    import subprocess
    import sys

    # Run python in a subprocess with mocked env vars to verify parsing
    env = os.environ.copy()
    env["AUTOGEN_DATA_DIR"] = "/tmp/mock_data"
    env["AUTOGEN_SKILLS_DIR"] = "/tmp/mock_skills"
    env["AUTOGEN_CUSTOM_SKILLS_DIR"] = "/tmp/mock_custom_skills"
    env["AUTOGEN_WORKSPACE_DIR"] = "/tmp/mock_workspace"

    code = (
        "import sys\n"
        "from backend.config import DATA_DIR, SKILLS_DIR, CUSTOM_SKILLS_DIR, WORKSPACE_DIR\n"
        "sys.stdout.write(str(DATA_DIR) + '|' + str(SKILLS_DIR) + '|' + str(CUSTOM_SKILLS_DIR) + '|' + str(WORKSPACE_DIR))\n"
    )

    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert result.returncode == 0

    paths = result.stdout.split('|')
    assert paths[0] == "/tmp/mock_data"
    assert paths[1] == "/tmp/mock_skills"
    assert paths[2] == "/tmp/mock_custom_skills"
    assert paths[3] == "/tmp/mock_workspace"

def test_path_configuration_dotenv_subprocess(tmp_path):
    import subprocess
    import sys

    mock_env = tmp_path / ".env"
    mock_env.write_text("AUTOGEN_DATA_DIR=/tmp/dotenv_data\nAUTOGEN_SKILLS_DIR=/tmp/dotenv_skills\nAUTOGEN_CUSTOM_SKILLS_DIR=/tmp/dotenv_custom_skills\nAUTOGEN_WORKSPACE_DIR=/tmp/dotenv_workspace\n")

    code = (
        "import sys, os\n"
        "from pathlib import Path\n"
        "import backend.config\n"
        "backend.config.ENV_FILE = Path('" + str(mock_env) + "')\n"
        "from dotenv import load_dotenv\n"
        "load_dotenv(dotenv_path=backend.config.ENV_FILE)\n"
        "backend.config.DATA_DIR = backend.config._get_path_env('AUTOGEN_DATA_DIR', 'data')\n"
        "backend.config.SKILLS_DIR = backend.config._get_path_env('AUTOGEN_SKILLS_DIR', 'skills_library')\n"
        "backend.config.CUSTOM_SKILLS_DIR = backend.config._get_path_env('AUTOGEN_CUSTOM_SKILLS_DIR', 'custom_skills')\n" \
        "backend.config.WORKSPACE_DIR = backend.config._get_path_env('AUTOGEN_WORKSPACE_DIR', 'workspace')\n"
        "sys.stdout.write(str(backend.config.DATA_DIR) + '|' + str(backend.config.SKILLS_DIR) + '|' + str(backend.config.CUSTOM_SKILLS_DIR) + '|' + str(backend.config.WORKSPACE_DIR))\n"
    )

    env = os.environ.copy()
    if "AUTOGEN_DATA_DIR" in env: del env["AUTOGEN_DATA_DIR"]
    if "AUTOGEN_SKILLS_DIR" in env: del env["AUTOGEN_SKILLS_DIR"]
    if "AUTOGEN_CUSTOM_SKILLS_DIR" in env: del env["AUTOGEN_CUSTOM_SKILLS_DIR"]
    if "AUTOGEN_WORKSPACE_DIR" in env: del env["AUTOGEN_WORKSPACE_DIR"]

    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert result.returncode == 0

    paths = result.stdout.split('|')
    assert paths[0] == "/tmp/dotenv_data"
    assert paths[1] == "/tmp/dotenv_skills"
    assert paths[2] == "/tmp/dotenv_custom_skills"
    assert paths[3] == "/tmp/dotenv_workspace"

def test_path_configuration_empty_env_vars() -> None:
    import subprocess
    import sys
    import os

    env = os.environ.copy()
    env["AUTOGEN_DATA_DIR"] = ""
    env["AUTOGEN_SKILLS_DIR"] = ""
    env["AUTOGEN_CUSTOM_SKILLS_DIR"] = ""
    env["AUTOGEN_WORKSPACE_DIR"] = ""

    code = (
        "import sys\n"
        "from backend.config import DATA_DIR, SKILLS_DIR, CUSTOM_SKILLS_DIR, WORKSPACE_DIR, BASE_DIR\n"
        "sys.stdout.write(str(DATA_DIR) + '|' + str(SKILLS_DIR) + '|' + str(CUSTOM_SKILLS_DIR) + '|' + str(WORKSPACE_DIR))\n"
    )

    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert result.returncode == 0

    paths = result.stdout.split('|')

    # Note: BASE_DIR in the subprocess will be the absolute path to backend
    from backend.config import BASE_DIR
    assert paths[0] == str(BASE_DIR / "data")
    assert paths[1] == str(BASE_DIR / "skills_library")
    assert paths[2] == str(BASE_DIR / "custom_skills")
    assert paths[3] == str(BASE_DIR / "workspace")

def test_config_model_base_url_validation() -> None:
    # Valid URL
    model = ConfigModel(base_url="https://api.example.com/v1/")
    assert model.base_url == "https://api.example.com/v1/"

    # Invalid URL format (missing scheme/netloc)
    with pytest.raises(ValidationError):
        ConfigModel(base_url="invalid_url")

    # Invalid URL format (missing scheme)
    with pytest.raises(ValidationError):
        ConfigModel(base_url="api.example.com/v1/")

    # Invalid type
    with pytest.raises(ValidationError):
        ConfigModel(base_url=123)

    # Invalid type (bytes)
    with pytest.raises(ValidationError):
        ConfigModel(base_url=b"https://api.example.com/v1/")

def test_validate_config_merging_logic(monkeypatch):
    """Test that _validate_config properly merges and filters env vars, defaults, and kwargs."""
    from backend.config import _validate_config, ConfigModel

    # Simulate an invalid env var for temperature and an unrelated bad env var
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "invalid_float")
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "50")

    # Pass explicit input kwargs that should override
    model = _validate_config({"temperature": 0.5})

    # 50 from env
    assert model.max_rounds == 50
    # 0.5 from input_kwargs (overrides invalid env and default)
    assert model.temperature == 0.5

def test_validate_config_ignores_unrelated_kwargs():
    """Test that _validate_config filters out keys not in UPDATABLE_FIELDS."""
    from backend.config import _validate_config

    # Pass arbitrary extra keys
    model = _validate_config({"temperature": 0.8, "some_unknown_field": 123})

    assert model.temperature == 0.8
    assert not hasattr(model, "some_unknown_field")

def test_get_path_env_populated(monkeypatch):
    from backend.config import _get_path_env, BASE_DIR
    monkeypatch.setenv("AUTOGEN_DATA_DIR", "/tmp/populated_data")
    from pathlib import Path; assert _get_path_env("AUTOGEN_DATA_DIR", "data") == Path("/tmp/populated_data")

def test_get_path_env_empty_string(monkeypatch):
    from backend.config import _get_path_env, BASE_DIR
    monkeypatch.setenv("AUTOGEN_DATA_DIR", "")
    assert _get_path_env("AUTOGEN_DATA_DIR", "data") == BASE_DIR / "data"

def test_get_path_env_unset(monkeypatch):
    from backend.config import _get_path_env, BASE_DIR
    monkeypatch.delenv("AUTOGEN_DATA_DIR", raising=False)
    assert _get_path_env("AUTOGEN_DATA_DIR", "data") == BASE_DIR / "data"

def test_autogen_env_file_location(tmp_path):
    import subprocess
    import sys
    import os

    mock_env = tmp_path / "custom.env"
    mock_env.write_text("AUTOGEN_TEMPERATURE=0.99\n", encoding="utf-8")

    env = os.environ.copy()
    env["AUTOGEN_ENV_FILE"] = str(mock_env)
    env["PYTHONPATH"] = "."
    if "AUTOGEN_TEMPERATURE" in env:
        del env["AUTOGEN_TEMPERATURE"]

    code = (
        "import sys\n"
        "from backend.config import ENV_FILE, get_settings\n"
        "sys.stdout.write(str(ENV_FILE) + '|' + str(get_settings()['temperature']))\n"
    )

    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert result.returncode == 0

    parts = result.stdout.split('|')
    assert parts[0] == str(mock_env)
    assert parts[1] == "0.99"

def test_config_model_default_paths():
    from backend.config import ConfigModel, BASE_DIR
    model = ConfigModel()
    assert model.data_dir == BASE_DIR / "data"
    assert model.skills_dir == BASE_DIR / "skills_library"
    assert model.custom_skills_dir == BASE_DIR / "custom_skills"
    assert model.workspace_dir == BASE_DIR / "workspace"

def test_config_model_custom_paths():
    from backend.config import ConfigModel
    from pathlib import Path
    custom_data = Path("/tmp/data")
    custom_skills = Path("/tmp/skills")
    custom_custom_skills = Path("/tmp/custom_skills")
    custom_workspace = Path("/tmp/workspace")

    model = ConfigModel(
        data_dir=custom_data,
        skills_dir=custom_skills,
        custom_skills_dir=custom_custom_skills,
        workspace_dir=custom_workspace
    )

    assert model.data_dir == custom_data
    assert model.skills_dir == custom_skills
    assert model.custom_skills_dir == custom_custom_skills
    assert model.workspace_dir == custom_workspace

def test_config_model_empty_path_fallback():
    from backend.config import ConfigModel, BASE_DIR
    model = ConfigModel(data_dir="", skills_dir=" ", workspace_dir=".", custom_skills_dir=None)
    assert model.data_dir == BASE_DIR / "data"
    assert model.skills_dir == BASE_DIR / "skills_library"
    assert model.workspace_dir == BASE_DIR / "workspace"
    assert model.custom_skills_dir == BASE_DIR / "custom_skills"

def test_validate_config_with_undefined_fallback(monkeypatch):
    from pydantic_core import PydanticUndefined
    from backend.config import _validate_config, ConfigModel
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "invalid_float")
    monkeypatch.setenv("AUTOGEN_API_KEY", "invalid key")

    config = _validate_config()
    assert config.temperature == 0.7
    assert config.api_key.get_secret_value() == ""

def test_empty_string_fallbacks_for_models_and_base_url():
    from backend.config import ConfigModel, _validate_config
    model = _validate_config({"default_model": "", "router_model": "    ", "base_url": ""})
    assert model.default_model == "gemini-2.5-flash"
    assert model.router_model == "gemini-3-flash-live"
    assert model.base_url == "https://generativelanguage.googleapis.com/v1beta/openai/"

def test_empty_string_fallbacks_from_env_vars(monkeypatch):
    from backend.config import ConfigModel, _validate_config
    monkeypatch.setenv("AUTOGEN_DEFAULT_MODEL", "")
    monkeypatch.setenv("AUTOGEN_ROUTER_MODEL", "    ")
    monkeypatch.setenv("AUTOGEN_BASE_URL", "")

    model = _validate_config()
    assert model.default_model == "gemini-2.5-flash"
    assert model.router_model == "gemini-3-flash-live"
    assert model.base_url == "https://generativelanguage.googleapis.com/v1beta/openai/"

def test_empty_string_fallbacks_for_numeric_fields():
    from backend.config import ConfigModel, _validate_config
    model = _validate_config({"temperature": "", "max_rounds": "", "max_tokens": ""})
    assert model.temperature == 0.7
    assert model.max_rounds == 15
    assert model.max_tokens == 4096


def test_config_model_base_url_none_bypass() -> None:
    # Explicitly test that passing None (if it somehow bypassed the early return)
    # or other types like int/bytes are caught by the explicit isinstance check.
    # We can test by bypassing the validator entirely, or since None is returned by the early check,
    # we can test bytes/ints which do hit the isinstance check.
    with pytest.raises(ValidationError, match="URL must be a string"):
        ConfigModel(base_url=123)

    with pytest.raises(ValidationError, match="URL must be a string"):
        ConfigModel(base_url=b"https://api.example.com/v1/")

def test_config_model_base_url_whitespace_fallback(monkeypatch):
    """Test that passing whitespace to base_url explicitly falls back to default via chaining validators."""
    from backend.config import ConfigModel
    # Setting the env var directly as whitespace
    monkeypatch.setenv("AUTOGEN_BASE_URL", "   ")
    model = ConfigModel()
    assert model.base_url == "https://generativelanguage.googleapis.com/v1beta/openai/"
    monkeypatch.delenv("AUTOGEN_BASE_URL", raising=False)

def test_config_model_env_var_parsing(monkeypatch):
    """Test that environment variables are correctly parsed by ConfigModel."""
    from backend.config import ConfigModel
    monkeypatch.setenv("AUTOGEN_DEFAULT_MODEL", "gpt-4")
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "1.2")
    monkeypatch.setenv("AUTOGEN_MAX_TOKENS", "1024")
    model = ConfigModel()
    assert model.default_model == "gpt-4"
    assert model.temperature == 1.2
    assert model.max_tokens == 1024
    monkeypatch.delenv("AUTOGEN_DEFAULT_MODEL", raising=False)
    monkeypatch.delenv("AUTOGEN_TEMPERATURE", raising=False)
    monkeypatch.delenv("AUTOGEN_MAX_TOKENS", raising=False)

def test_empty_string_fallbacks_for_numeric_fields_whitespace(monkeypatch):
    from backend.config import _validate_config
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "   ")
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "   ")
    monkeypatch.setenv("AUTOGEN_MAX_TOKENS", "   ")
    model = _validate_config()
    assert model.temperature == 0.7
    assert model.max_rounds == 15
    assert model.max_tokens == 4096

    model2 = _validate_config({"temperature": "   ", "max_rounds": "   ", "max_tokens": "   "})
    assert model2.temperature == 0.7
    assert model2.max_rounds == 15
    assert model2.max_tokens == 4096

def test_get_path_env_whitespace(monkeypatch):
    from backend.config import _get_path_env, BASE_DIR
    monkeypatch.setenv("AUTOGEN_DATA_DIR", "   ")
    assert _get_path_env("AUTOGEN_DATA_DIR", "data") == BASE_DIR / "data"

def test_get_path_env_relative(monkeypatch):
    from backend.config import _get_path_env, BASE_DIR
    monkeypatch.setenv("AUTOGEN_DATA_DIR", "relative_dir")
    from pathlib import Path
    assert _get_path_env("AUTOGEN_DATA_DIR", "data") == (BASE_DIR / "relative_dir").resolve()

def test_config_model_relative_paths():
    from backend.config import ConfigModel, BASE_DIR
    from pathlib import Path

    model = ConfigModel(
        data_dir="relative_data",
        skills_dir=Path("relative_skills"),
        custom_skills_dir="relative_custom",
        workspace_dir="relative_workspace"
    )

    assert model.data_dir == (BASE_DIR / "relative_data").resolve()
    assert model.skills_dir == (BASE_DIR / "relative_skills").resolve()
    assert model.custom_skills_dir == (BASE_DIR / "relative_custom").resolve()
    assert model.workspace_dir == (BASE_DIR / "relative_workspace").resolve()

def test_config_model_validate_paths_get_default():
    # To hit line 74: field_info.get_default() logic where default_factory is None
    # We will create a dummy model inheriting from ConfigModel or similar
    from pydantic import Field
    from backend.config import ConfigModel, BASE_DIR
    from pydantic_settings import BaseSettings

    # We can just check the default fallback explicitly if we modify the kwargs
    model = ConfigModel(data_dir="")
    assert model.data_dir == BASE_DIR / "data"

def test_config_model_base_url_none():
    from backend.config import ConfigModel
    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        ConfigModel(base_url=None)

def test_validate_config_default_factory(monkeypatch):
    from backend.config import _validate_config, BASE_DIR
    from pydantic import ValidationError
    import pytest

    # We can just explicitly monkeypatch environ with bad data so _validate_config handles it
    monkeypatch.setenv("AUTOGEN_DATA_DIR", ".") # invalid value
    config = _validate_config()
    assert config.data_dir == BASE_DIR / "data"

def test_validate_empty_strings_default_factory():
    from backend.config import ConfigModel

    # We create an instance to hit lines in validate_empty_strings. Since default_model
    # uses default and not default_factory, it won't hit line 118, but it tests the logic.
    model = ConfigModel(default_model="")
    assert model.default_model == "gemini-2.5-flash"
