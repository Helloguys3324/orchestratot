import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from backend.main import app

client = TestClient(app)

@pytest.fixture
def mock_session_manager():
    with patch("backend.api.sessions.session_manager") as mock:
        yield mock

def test_api_list_sessions(mock_session_manager):
    mock_session_manager.list_sessions.return_value = [{"id": "s1"}, {"id": "s2"}]
    response = client.get("/api/sessions")
    assert response.status_code == 200
    assert response.json() == [{"id": "s1"}, {"id": "s2"}]
    mock_session_manager.list_sessions.assert_called_once()

def test_api_get_session_exists(mock_session_manager):
    mock_session_manager.get_session.return_value = {"id": "s1", "title": "Test"}
    response = client.get("/api/sessions/s1")
    assert response.status_code == 200
    assert response.json() == {"id": "s1", "title": "Test"}
    mock_session_manager.get_session.assert_called_once_with("s1")

def test_api_get_session_not_found(mock_session_manager):
    mock_session_manager.get_session.return_value = None
    response = client.get("/api/sessions/s1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}

def test_api_create_session(mock_session_manager):
    mock_session_manager.create_session.return_value = {"id": "s1", "title": "New"}
    response = client.post("/api/sessions", json={"title": "New"})
    assert response.status_code == 200
    assert response.json() == {"id": "s1", "title": "New"}
    mock_session_manager.create_session.assert_called_once_with({"title": "New"})

def test_api_delete_session_success(mock_session_manager):
    mock_session_manager.delete_session.return_value = True
    response = client.delete("/api/sessions/s1")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_session_manager.delete_session.assert_called_once_with("s1")

def test_api_delete_session_not_found(mock_session_manager):
    mock_session_manager.delete_session.return_value = False
    response = client.delete("/api/sessions/s1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}

def test_api_chat_success(mock_session_manager):
    mock_session_manager.get_session.return_value = {"id": "s1"}

    # Needs to mock asyncio.create_task to avoid actually running chat
    with patch("backend.api.sessions.asyncio.create_task") as mock_create_task:
        response = client.post("/api/sessions/s1/chat", json={"message": "hello"})
        assert response.status_code == 200
        assert response.json() == {"status": "started"}
        mock_create_task.assert_called_once()
        # Verify get_session was called to check existence
        mock_session_manager.get_session.assert_called_once_with("s1")

def test_api_chat_session_not_found(mock_session_manager):
    mock_session_manager.get_session.return_value = None
    response = client.post("/api/sessions/s1/chat", json={"message": "hello"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}

def test_api_chat_empty_message(mock_session_manager):
    response = client.post("/api/sessions/s1/chat", json={"message": ""})
    assert response.status_code == 422 # Pydantic validation error

def test_api_chat_missing_message(mock_session_manager):
    response = client.post("/api/sessions/s1/chat", json={})
    assert response.status_code == 422

def test_api_clear_session_success(mock_session_manager):
    mock_session_manager.clear_messages.return_value = True
    response = client.post("/api/sessions/s1/clear")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_session_manager.clear_messages.assert_called_once_with("s1")

def test_api_clear_session_not_found(mock_session_manager):
    mock_session_manager.clear_messages.return_value = False
    response = client.post("/api/sessions/s1/clear")
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}

def test_api_session_files_success(mock_session_manager):
    mock_session_manager.get_session.return_value = {"id": "s1"}
    mock_session_manager.get_workspace_files.return_value = [{"name": "file.txt"}]
    response = client.get("/api/sessions/s1/files")
    assert response.status_code == 200
    assert response.json() == [{"name": "file.txt"}]
    mock_session_manager.get_session.assert_called_once_with("s1")
    mock_session_manager.get_workspace_files.assert_called_once_with("s1")

def test_api_session_files_not_found(mock_session_manager):
    mock_session_manager.get_session.return_value = None
    response = client.get("/api/sessions/s1/files")
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}
