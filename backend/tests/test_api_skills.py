import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app
from backend.skills.errors import SkillError, SkillValidationError, SkillInstallError, SkillNotFoundError

client = TestClient(app)

@patch("backend.api.skills.skills_manager.create_skill")
def test_create_skill_base_error(mock_create):
    mock_create.side_effect = SkillError("Generic skill error")

    response = client.post("/api/skills", json={"name": ""})

    assert response.status_code == 500
    assert response.json()["detail"] == "Generic skill error"
    mock_create.assert_called_once_with({"name": ""})

@patch("backend.api.skills.skills_manager.create_skill")
def test_create_skill_validation_error(mock_create):
    mock_create.side_effect = SkillValidationError("Invalid skill name")

    response = client.post("/api/skills", json={"name": ""})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid skill name"
    mock_create.assert_called_once_with({"name": ""})

@patch("backend.api.skills.skills_manager.create_skill")
def test_create_skill_install_error(mock_create):
    mock_create.side_effect = SkillInstallError("Disk is full")

    response = client.post("/api/skills", json={"name": "test"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Disk is full"
    mock_create.assert_called_once_with({"name": "test"})

@patch("backend.api.skills.skills_manager.delete_skill")
def test_delete_skill_not_found(mock_delete):
    mock_delete.side_effect = SkillNotFoundError("Skill not found")

    response = client.delete("/api/skills/missing_id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found"
    mock_delete.assert_called_once_with("missing_id")

@patch("backend.api.skills.skills_manager.delete_skill")
def test_delete_skill_install_error(mock_delete):
    mock_delete.side_effect = SkillInstallError("Permission denied")

    response = client.delete("/api/skills/123")

    assert response.status_code == 500
    assert response.json()["detail"] == "Permission denied"
    mock_delete.assert_called_once_with("123")

@patch("backend.api.skills.skills_manager.install_from_url")
def test_install_skill_validation_error(mock_install):
    mock_install.side_effect = SkillValidationError("Invalid URL scheme")

    response = client.post("/api/skills/install", json={"url": "ftp://example.com"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid URL scheme"

@patch("backend.api.skills.skills_manager.install_from_url")
def test_install_skill_install_error(mock_install):
    mock_install.side_effect = SkillInstallError("HTTP Error")

    response = client.post("/api/skills/install", json={"url": "https://example.com"})

    assert response.status_code == 500
    assert response.json()["detail"] == "HTTP Error"

def test_install_skill_missing_url():
    response = client.post("/api/skills/install", json={})
    assert response.status_code == 422

@patch("backend.api.skills.skills_manager.list_skills")
def test_list_skills_validation_error(mock_list):
    mock_list.side_effect = SkillValidationError("test error")
    response = client.get("/api/skills")
    assert response.status_code == 400
    assert response.json()["detail"] == "test error"

@patch("backend.api.skills.skills_manager.list_marketplace")
def test_list_marketplace_validation_error(mock_list):
    mock_list.side_effect = SkillValidationError("test error")
    response = client.get("/api/skills/marketplace")
    assert response.status_code == 400
    assert response.json()["detail"] == "test error"

@patch("backend.api.skills.skills_manager.delete_skill")
def test_delete_skill_success(mock_delete):
    mock_delete.return_value = True
    response = client.delete("/api/skills/123")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_delete.assert_called_once_with("123")

@patch("backend.api.skills.skills_manager.install_from_url")
def test_install_skill_success(mock_install):
    mock_install.return_value = {"id": "custom_123", "name": "Installed Skill"}
    response = client.post("/api/skills/install", json={"url": "https://example.com/skill.py"})
    assert response.status_code == 200
    assert response.json() == {"id": "custom_123", "name": "Installed Skill"}
    mock_install.assert_called_once_with("https://example.com/skill.py", None)

@patch("backend.api.skills.skills_manager.list_skills")
def test_list_skills_success(mock_list):
    mock_list.return_value = [{"id": "code_executor"}]
    response = client.get("/api/skills")
    assert response.status_code == 200
    assert response.json() == [{"id": "code_executor"}]

@patch("backend.api.skills.skills_manager.list_marketplace")
def test_list_marketplace_success(mock_list):
    mock_list.return_value = [{"id": "mp_api_caller"}]
    response = client.get("/api/skills/marketplace")
    assert response.status_code == 200
    assert response.json() == [{"id": "mp_api_caller"}]

@patch("backend.api.skills.skills_manager.create_skill")
def test_create_skill_success(mock_create):
    mock_create.return_value = {"id": "custom_123"}
    response = client.post("/api/skills", json={"name": "test_skill"})
    assert response.status_code == 200
    assert response.json() == {"id": "custom_123"}
    mock_create.assert_called_once_with({"name": "test_skill"})

def test_handle_skill_exceptions_unhandled():
    from backend.api.skills import handle_skill_exceptions
    with pytest.raises(Exception, match="unhandled"):
        with handle_skill_exceptions():
            raise Exception("unhandled")
