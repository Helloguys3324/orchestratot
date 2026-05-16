import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.api.agents import agent_manager

client = TestClient(app)

@patch("backend.api.agents.agent_manager.create_agent")
def test_create_agent_success(mock_create):
    mock_create.return_value = {"id": "123", "name": "Test Agent"}

    response = client.post("/api/agents", json={
        "name": "Test Agent",
        "temperature": 0.5,
        "max_tokens": 100
    })

    assert response.status_code == 200
    assert response.json() == {"id": "123", "name": "Test Agent"}
    mock_create.assert_called_once_with({"name": "Test Agent", "temperature": 0.5, "max_tokens": 100})

def test_create_agent_invalid_temperature():
    response = client.post("/api/agents", json={
        "name": "Test Agent",
        "temperature": "not a number"
    })

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) > 0
    assert errors[0]["loc"] == ["body", "temperature"]

def test_create_agent_invalid_temperature_bounds():
    response = client.post("/api/agents", json={
        "name": "Test Agent",
        "temperature": 2.5
    })

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) > 0
    assert errors[0]["loc"] == ["body", "temperature"]

@patch("backend.api.agents.agent_manager.update_agent")
def test_update_agent_success(mock_update):
    mock_update.return_value = {"id": "123", "name": "Updated Agent"}

    response = client.put("/api/agents/123", json={
        "name": "Updated Agent"
    })

    assert response.status_code == 200
    assert response.json() == {"id": "123", "name": "Updated Agent"}
    mock_update.assert_called_once_with("123", {"name": "Updated Agent"})

def test_update_agent_invalid_max_tokens():
    response = client.put("/api/agents/123", json={
        "max_tokens": 0
    })

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) > 0
    assert errors[0]["loc"] == ["body", "max_tokens"]
