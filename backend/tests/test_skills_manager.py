import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from backend.skills.manager import SkillsManager, BUILTIN_SKILLS, MARKETPLACE_SKILLS
from backend.skills.errors import SkillValidationError, SkillInstallError, SkillNotFoundError

@pytest.fixture
def mock_load_json():
    with patch("backend.skills.manager.load_json") as mock:
        mock.return_value = []
        yield mock

@pytest.fixture
def manager(mock_load_json):
    return SkillsManager()

def test_manager_init(manager, mock_load_json):
    mock_load_json.assert_called_once()
    assert manager._custom_skills == []

def test_list_skills(manager):
    skills = manager.list_skills()
    assert len(skills) == len(BUILTIN_SKILLS)
    assert skills == BUILTIN_SKILLS

def test_list_skills_with_custom(manager):
    manager._custom_skills = [{"id": "custom_1", "name": "Custom 1"}]
    skills = manager.list_skills()
    assert len(skills) == len(BUILTIN_SKILLS) + 1
    assert any(s["id"] == "custom_1" for s in skills)

def test_list_marketplace(manager):
    skills = manager.list_marketplace()
    assert skills == MARKETPLACE_SKILLS

def test_get_skill_builtin(manager):
    builtin_id = BUILTIN_SKILLS[0]["id"]
    skill = manager.get_skill(builtin_id)
    assert skill == BUILTIN_SKILLS[0]

def test_get_skill_custom(manager):
    manager._custom_skills = [{"id": "custom_1", "name": "Custom 1"}]
    skill = manager.get_skill("custom_1")
    assert skill == {"id": "custom_1", "name": "Custom 1"}

def test_get_skill_not_found(manager):
    with pytest.raises(SkillNotFoundError, match="Skill not found"):
        manager.get_skill("non_existent_id")

@patch("backend.skills.manager.uuid.uuid4")
@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
def test_create_skill(mock_save, mock_path, mock_uuid, manager):
    # Setup mock UUID to predict ID
    mock_uuid_instance = MagicMock()
    mock_uuid_instance.hex = "1234567890abcdef"
    mock_uuid.return_value = mock_uuid_instance

    # Mock file operations
    mock_file_path = MagicMock()
    mock_path.__truediv__.return_value = mock_file_path

    data = {
        "name": "My Custom Skill",
        "description": "Does something cool",
        "code": "print('hello')"
    }

    result = manager.create_skill(data)

    # Asserts
    assert result["id"] == "custom_12345678"
    assert result["name"] == "My Custom Skill"
    assert result["builtin"] is False
    assert result["code"] == "print('hello')"
    assert result["file"] == "custom_12345678.py"

    # Verify custom_skills appended
    assert len(manager._custom_skills) == 1
    assert manager._custom_skills[0] == result

    # Verify file written
    mock_file_path.write_text.assert_called_once_with("print('hello')", encoding="utf-8")

    # Verify save called
    mock_save.assert_called_once()

@patch("backend.skills.manager.SkillsManager._save")
def test_create_skill_no_code(mock_save, manager):
    data = {
        "name": "No Code Skill"
    }
    result = manager.create_skill(data)
    assert result["code"] == ""
    assert "file" not in result
    mock_save.assert_called_once()

def test_create_skill_missing_name(manager):
    data = {"description": "No name provided"}
    with pytest.raises(SkillValidationError, match="Skill name is required"):
        manager.create_skill(data)

@patch("backend.skills.manager.uuid.uuid4")
@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
def test_create_skill_write_error(mock_save, mock_path, mock_uuid, manager):
    mock_uuid_instance = MagicMock()
    mock_uuid_instance.hex = "1234567890abcdef"
    mock_uuid.return_value = mock_uuid_instance

    mock_file_path = MagicMock()
    mock_file_path.write_text.side_effect = OSError("Disk full")
    mock_path.__truediv__.return_value = mock_file_path

    data = {
        "name": "Broken Disk Skill",
        "code": "print('fail')"
    }

    with pytest.raises(SkillInstallError, match="Failed to write skill file: Disk full") as exc:
        manager.create_skill(data)
    assert isinstance(exc.value.__cause__, OSError)


@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
def test_delete_skill_exists(mock_save, mock_path, manager):
    manager._custom_skills = [{"id": "custom_1", "file": "custom_1.py"}]

    # Mock file exists and unlink
    mock_file_path = MagicMock()
    mock_file_path.exists.return_value = True
    mock_path.__truediv__.return_value = mock_file_path

    result = manager.delete_skill("custom_1")

    assert result is True
    assert len(manager._custom_skills) == 0
    mock_file_path.unlink.assert_called_once()
    mock_save.assert_called_once()

@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
def test_delete_skill_unlink_error(mock_save, mock_path, manager):
    manager._custom_skills = [{"id": "custom_1", "file": "custom_1.py"}]

    mock_file_path = MagicMock()
    mock_file_path.exists.return_value = True
    mock_file_path.unlink.side_effect = OSError("Permission denied")
    mock_path.__truediv__.return_value = mock_file_path

    with pytest.raises(SkillInstallError, match="Failed to delete skill file: Permission denied") as exc:
        manager.delete_skill("custom_1")
    assert isinstance(exc.value.__cause__, OSError)


@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
def test_delete_skill_file_not_exists(mock_save, mock_path, manager):
    manager._custom_skills = [{"id": "custom_1", "file": "custom_1.py"}]

    # Mock file does NOT exist
    mock_file_path = MagicMock()
    mock_file_path.exists.return_value = False
    mock_path.__truediv__.return_value = mock_file_path

    result = manager.delete_skill("custom_1")

    assert result is True
    assert len(manager._custom_skills) == 0
    mock_file_path.unlink.assert_not_called()
    mock_save.assert_called_once()

def test_delete_skill_not_found(manager):
    manager._custom_skills = [{"id": "custom_1", "file": "custom_1.py"}]
    with pytest.raises(SkillNotFoundError, match="Skill not found"):
        manager.delete_skill("non_existent_id")

    assert len(manager._custom_skills) == 1

@patch("backend.skills.manager.uuid.uuid4")
@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
@patch("backend.skills.manager.httpx.AsyncClient")
def test_install_from_url_success(mock_client_class, mock_save, mock_dir, mock_uuid, manager):
    # Setup mock UUID
    mock_uuid_instance = MagicMock()
    mock_uuid_instance.hex = "abcdef1234567890"
    mock_uuid.return_value = mock_uuid_instance

    # Mock HTTP response
    mock_response = MagicMock()
    mock_response.text = "print('installed')"
    mock_response.raise_for_status.return_value = None

    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client_class.return_value.__aenter__.return_value = mock_client

    # Mock file operations
    mock_file_path = MagicMock()
    mock_dir.__truediv__.return_value = mock_file_path

    result = asyncio.run(manager.install_from_url("http://example.com/skill.py", name="Downloaded Skill"))

    # Asserts
    assert result["id"] == "imported_abcdef12"
    assert result["name"] == "Downloaded Skill"
    assert result["source"] == "http://example.com/skill.py"
    assert result["code"] == "print('installed')"

    mock_client.get.assert_called_once_with("http://example.com/skill.py")
    mock_file_path.write_text.assert_called_once_with("print('installed')", encoding="utf-8")
    mock_save.assert_called_once()
    assert len(manager._custom_skills) == 1

@patch("backend.skills.manager.uuid.uuid4")
@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.httpx.AsyncClient")
def test_install_from_url_write_error(mock_client_class, mock_dir, mock_uuid, manager):
    mock_uuid_instance = MagicMock()
    mock_uuid_instance.hex = "abcdef1234567890"
    mock_uuid.return_value = mock_uuid_instance

    mock_response = MagicMock()
    mock_response.text = "print('installed')"
    mock_response.raise_for_status.return_value = None

    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_file_path = MagicMock()
    mock_file_path.write_text.side_effect = OSError("Read only file system")
    mock_dir.__truediv__.return_value = mock_file_path

    with pytest.raises(SkillInstallError, match="Failed to write skill file: Read only file system") as exc:
        asyncio.run(manager.install_from_url("http://example.com/skill.py", name="Downloaded Skill"))
    assert isinstance(exc.value.__cause__, OSError)

@patch("backend.skills.manager.httpx.AsyncClient")
def test_install_from_url_failure(mock_client_class, manager):
    import httpx

    # Mock HTTP response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason_phrase = "Not Found"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("404 Not Found", request=MagicMock(), response=mock_response)

    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(SkillInstallError, match="HTTP error occurred: 404 Not Found") as exc:
        asyncio.run(manager.install_from_url("http://example.com/404.py"))
    assert isinstance(exc.value.__cause__, httpx.HTTPStatusError)

    assert len(manager._custom_skills) == 0

@patch("backend.skills.manager.httpx.AsyncClient")
def test_install_from_url_request_error(mock_client_class, manager):
    import httpx

    mock_client = MagicMock()
    mock_client.get = AsyncMock(side_effect=httpx.RequestError("Connection failed", request=MagicMock()))
    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(SkillInstallError, match="Request error occurred: Connection failed") as exc:
        asyncio.run(manager.install_from_url("http://example.com/404.py"))
    assert isinstance(exc.value.__cause__, httpx.RequestError)

    assert len(manager._custom_skills) == 0

def test_install_from_url_invalid_schema(manager):
    with pytest.raises(SkillValidationError, match="Invalid URL scheme"):
        asyncio.run(manager.install_from_url("file:///etc/passwd"))

    with pytest.raises(SkillValidationError, match="Invalid URL scheme"):
        asyncio.run(manager.install_from_url("ftp://example.com/skill.py"))

def test_install_from_url_invalid_format(manager) -> None:
    with pytest.raises(SkillValidationError, match="Invalid URL format"):
        asyncio.run(manager.install_from_url("http://[::1"))

def test_install_from_url_invalid_hostname(manager):
    with pytest.raises(SkillValidationError, match="Invalid URL hostname"):
        asyncio.run(manager.install_from_url("http://localhost:8080/skill.py"))

    with pytest.raises(SkillValidationError, match="Invalid URL hostname"):
        asyncio.run(manager.install_from_url("https://127.0.0.1/skill.py"))

    with pytest.raises(SkillValidationError, match="Invalid URL hostname"):
        asyncio.run(manager.install_from_url("http://0.0.0.0:5000/skill.py"))

def test_load_oserror():
    with patch("backend.skills.manager.load_json", side_effect=OSError("Read error")):
        with pytest.raises(SkillInstallError, match="Failed to load skills file: Read error"):
            SkillsManager()

def test_save_oserror():
    with patch("backend.skills.manager.load_json", return_value=[]):
        manager = SkillsManager()
        with patch("backend.skills.manager.save_json", side_effect=OSError("Write error")):
            with pytest.raises(SkillInstallError, match="Failed to save skills file: Write error"):
                manager._save()

def test_load_generic_exception() -> None:
    with patch("backend.skills.manager.load_json", side_effect=Exception("Corrupted JSON")):
        with pytest.raises(SkillInstallError, match="Failed to load skills file: Corrupted JSON"):
            SkillsManager()

def test_save_generic_exception() -> None:
    with patch("backend.skills.manager.load_json", return_value=[]):
        manager = SkillsManager()
        with patch("backend.skills.manager.save_json", side_effect=Exception("Serialization error")):
            with pytest.raises(SkillInstallError, match="Failed to save skills file: Serialization error"):
                manager._save()

@patch("backend.skills.manager.uuid.uuid4")
@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
def test_create_skill_write_generic_exception(mock_save, mock_path, mock_uuid, manager) -> None:
    mock_uuid_instance = MagicMock()
    mock_uuid_instance.hex = "1234567890abcdef"
    mock_uuid.return_value = mock_uuid_instance

    mock_file_path = MagicMock()
    mock_file_path.write_text.side_effect = Exception("Generic write error")
    mock_path.__truediv__.return_value = mock_file_path

    data = {
        "name": "Broken Disk Skill",
        "code": "print('fail')"
    }

    with pytest.raises(SkillInstallError, match="Failed to write skill file: Generic write error") as exc:
        manager.create_skill(data)
    assert isinstance(exc.value.__cause__, Exception)

@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.SkillsManager._save")
def test_delete_skill_unlink_generic_exception(mock_save, mock_path, manager) -> None:
    manager._custom_skills = [{"id": "custom_1", "file": "custom_1.py"}]

    mock_file_path = MagicMock()
    mock_file_path.exists.return_value = True
    mock_file_path.unlink.side_effect = Exception("Generic unlink error")
    mock_path.__truediv__.return_value = mock_file_path

    with pytest.raises(SkillInstallError, match="Failed to delete skill file: Generic unlink error") as exc:
        manager.delete_skill("custom_1")
    assert isinstance(exc.value.__cause__, Exception)

@patch("backend.skills.manager.uuid.uuid4")
@patch("backend.skills.manager.CUSTOM_SKILLS_DIR")
@patch("backend.skills.manager.httpx.AsyncClient")
def test_install_from_url_write_generic_exception(mock_client_class, mock_dir, mock_uuid, manager) -> None:
    mock_uuid_instance = MagicMock()
    mock_uuid_instance.hex = "abcdef1234567890"
    mock_uuid.return_value = mock_uuid_instance

    mock_response = MagicMock()
    mock_response.text = "print('installed')"
    mock_response.raise_for_status.return_value = None

    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_file_path = MagicMock()
    mock_file_path.write_text.side_effect = Exception("Generic write error")
    mock_dir.__truediv__.return_value = mock_file_path

    with pytest.raises(SkillInstallError, match="Failed to write skill file: Generic write error") as exc:
        asyncio.run(manager.install_from_url("http://example.com/skill.py", name="Downloaded Skill"))
    assert isinstance(exc.value.__cause__, Exception)
