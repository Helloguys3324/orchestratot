from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_and_get_tasks():
    task_data = {"title": "Test Task", "description": "Description", "status": "todo"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_invalid_task_creation():
    # Invalid status
    task_data = {"title": "Task", "description": "Desc", "status": "invalid_status"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 422
    
    # Missing title (assuming title is required)
    task_data = {"description": "Desc"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 422