import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app
from backend.skills.errors import SkillValidationError, SkillInstallError, SkillNotFoundError

client = TestClient(app)

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
