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

def test_settings_env_override(monkeypatch):
    monkeypatch.setenv("AUTOGEN_MAX_ROUNDS", "42")
    monkeypatch.setenv("AUTOGEN_TEMPERATURE", "0.9")
    monkeypatch.setenv("AUTOGEN_MAX_TOKENS", "2048")

    settings = get_settings()

    assert settings["max_rounds"] == 42
    assert settings["temperature"] == 0.9
    assert settings["max_tokens"] == 2048

def test_api_agents_route():
    response = client.get("/api/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_models_route():
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_models_categories_route():
    response = client.get("/api/models/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_api_get_agent():
    # Retrieve all agents first
    response = client.get("/api/agents")
    assert response.status_code == 200
    agents = response.json()

    if agents:
        agent_id = agents[0]["id"]
        # Fetch the specific agent
        agent_response = client.get(f"/api/agents/{agent_id}")
        assert agent_response.status_code == 200
        agent_data = agent_response.json()
        assert agent_data["id"] == agent_id

def test_api_get_model():
    # Retrieve all models first
    response = client.get("/api/models")
    assert response.status_code == 200
    models = response.json()

    if models:
        model_id = models[0]["id"]
        # Fetch the specific model
        model_response = client.get(f"/api/models/{model_id}")
        assert model_response.status_code == 200
        data = model_response.json()
        assert data["id"] == model_id
        assert "name" in data

def test_api_chat_models_route():
    response = client.get("/api/models/chat")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Ensure every returned chat model has category "text"
    for model in data:
        assert model.get("category") == "text"

def test_api_templates_route():
    response = client.get("/api/templates")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "name" in data[0]
