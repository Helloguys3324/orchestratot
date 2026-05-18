import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock

from backend.api.dependencies import get_agent_or_404, get_session_or_404, get_model_or_404

# --- Agent Tests ---

@patch("backend.api.dependencies.agent_manager.get_agent")
def test_get_agent_success(mock_get_agent):
    mock_get_agent.return_value = {"id": "agent_123", "name": "Test Agent"}
    result = get_agent_or_404("agent_123")
    assert result == {"id": "agent_123", "name": "Test Agent"}
    mock_get_agent.assert_called_once_with("agent_123")

@patch("backend.api.dependencies.agent_manager.get_agent")
def test_get_agent_not_found(mock_get_agent):
    mock_get_agent.return_value = None
    with pytest.raises(HTTPException) as exc:
        get_agent_or_404("missing_agent")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Agent not found"
    mock_get_agent.assert_called_once_with("missing_agent")

# --- Session Tests ---

@patch("backend.api.dependencies.session_manager.get_session")
def test_get_session_success(mock_get_session):
    mock_get_session.return_value = {"id": "session_456", "title": "Test Session"}
    result = get_session_or_404("session_456")
    assert result == {"id": "session_456", "title": "Test Session"}
    mock_get_session.assert_called_once_with("session_456")

@patch("backend.api.dependencies.session_manager.get_session")
def test_get_session_not_found(mock_get_session):
    mock_get_session.return_value = None
    with pytest.raises(HTTPException) as exc:
        get_session_or_404("missing_session")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Session not found"
    mock_get_session.assert_called_once_with("missing_session")

# --- Model Tests ---

@patch("backend.api.dependencies.get_model")
def test_get_model_success(mock_get_model):
    mock_get_model.return_value = {"id": "gemini-test", "name": "Gemini Test"}
    result = get_model_or_404("gemini-test")
    assert result == {"id": "gemini-test", "name": "Gemini Test"}
    mock_get_model.assert_called_once_with("gemini-test")

@patch("backend.api.dependencies.get_model")
def test_get_model_not_found(mock_get_model):
    mock_get_model.return_value = None
    with pytest.raises(HTTPException) as exc:
        get_model_or_404("missing_model")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Model not found"
    mock_get_model.assert_called_once_with("missing_model")
