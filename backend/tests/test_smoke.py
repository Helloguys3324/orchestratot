import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.config import get_settings, ConfigModel

client = TestClient(app)

def test_app_import():
    assert app is not None
    assert app.title == "AutoGen AI Orchestrator"

def test_settings_loading():
    settings = get_settings()
    assert isinstance(settings, dict)
    for key in ConfigModel().model_dump().keys():
        assert key in settings

def test_api_settings_route():
    response = client.get("/api/settings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_api_settings_route_default_model_restored():
    response = client.get("/api/settings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "default_model" in data

def test_agent_retrieval(monkeypatch):
    # Mock save to avoid disk writes
    import backend.state
    monkeypatch.setattr(backend.state.agent_manager, "_save", lambda: None)

    # Create an agent
    create_response = client.post("/api/agents", json={"name": "Smoke Test Agent"})
    assert create_response.status_code == 200
    agent_data = create_response.json()
    assert "id" in agent_data
    agent_id = agent_data["id"]

    # Retrieve the agent
    get_response = client.get(f"/api/agents/{agent_id}")
    assert get_response.status_code == 200
    retrieved_data = get_response.json()
    assert retrieved_data["name"] == "Smoke Test Agent"

def test_model_registry_fetching():
    # Fetch all models
    list_response = client.get("/api/models")
    assert list_response.status_code == 200
    models_list = list_response.json()
    assert isinstance(models_list, list)
    assert len(models_list) > 0

    # Fetch specific model by dynamically retrieved ID
    first_model_id = models_list[0]["id"]
    model_response = client.get(f"/api/models/{first_model_id}")
    assert model_response.status_code == 200
    model_data = model_response.json()
    assert model_data["id"] == first_model_id

    # Fetch chat models
    chat_response = client.get("/api/models/chat")
    assert chat_response.status_code == 200
    chat_models = chat_response.json()
    assert isinstance(chat_models, list)
    if len(chat_models) > 0:
        assert chat_models[0].get("category") == "text"

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
