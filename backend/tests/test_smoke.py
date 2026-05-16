import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.config import get_settings, DEFAULT_SETTINGS

client = TestClient(app)

def test_app_import():
    assert app is not None
    assert app.title == "AutoGen AI Orchestrator"

def test_settings_loading():
    settings = get_settings()
    assert isinstance(settings, dict)
    for key in DEFAULT_SETTINGS:
        assert key in settings

def test_api_settings_route():
    response = client.get("/api/settings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "default_model" in data
