import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app

client = TestClient(app)

@patch("backend.agents.manager.AgentManager._save")
def test_api_agents_crud(mock_save):
    # 1. Create with empty dict should be ok because FastAPI json={} parses to {}
    response = client.post("/api/agents", json={})
    assert response.status_code == 200
    agent = response.json()
    assert "id" in agent
    agent_id = agent["id"]

    # 2. Get
    response = client.get(f"/api/agents/{agent_id}")
    assert response.status_code == 200

    # 3. Update
    response = client.put(f"/api/agents/{agent_id}", json={"name": "Updated Agent"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Agent"

    # 4. Delete
    response = client.delete(f"/api/agents/{agent_id}")
    assert response.status_code == 200

    # 5. Get after delete should 404
    response = client.get(f"/api/agents/{agent_id}")
    assert response.status_code == 404

def test_api_agents_empty_body():
    # Should return 400 for empty content instead of 500
    response = client.post("/api/agents", content="")
    assert response.status_code == 400
    assert "Invalid or empty JSON body" in response.text

def test_api_agents_invalid_json():
    # Should return 400 for invalid json instead of 500
    response = client.post("/api/agents", content="{invalid json")
    assert response.status_code == 400
    assert "Invalid or empty JSON body" in response.text
