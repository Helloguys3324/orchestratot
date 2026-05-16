import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import WebSocket
from backend.websocket.handler import ConnectionManager

@pytest.fixture
def manager():
    return ConnectionManager()

@pytest.fixture
def mock_websocket():
    ws = MagicMock(spec=WebSocket)
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    return ws

@pytest.mark.asyncio
async def test_connect(manager, mock_websocket):
    session_id = "test_session_1"
    await manager.connect(mock_websocket, session_id)

    mock_websocket.accept.assert_awaited_once()
    assert session_id in manager.active_connections
    assert mock_websocket in manager.active_connections[session_id]

@pytest.mark.asyncio
async def test_disconnect(manager, mock_websocket):
    session_id = "test_session_1"
    await manager.connect(mock_websocket, session_id)

    manager.disconnect(mock_websocket, session_id)

    assert session_id not in manager.active_connections

@pytest.mark.asyncio
async def test_disconnect_nonexistent(manager, mock_websocket):
    session_id = "test_session_1"

    # Should not raise any error
    manager.disconnect(mock_websocket, session_id)
    assert session_id not in manager.active_connections

@pytest.mark.asyncio
async def test_send_message_success(manager, mock_websocket):
    session_id = "test_session_1"
    await manager.connect(mock_websocket, session_id)

    message = {"type": "test_message", "data": "hello"}
    await manager.send_message(session_id, message)

    mock_websocket.send_json.assert_awaited_once_with(message)
    assert session_id in manager.active_connections

@pytest.mark.asyncio
async def test_send_message_dead_connection(manager, mock_websocket):
    session_id = "test_session_1"
    await manager.connect(mock_websocket, session_id)

    # Setup the mock to throw an exception
    mock_websocket.send_json.side_effect = Exception("Connection closed")

    message = {"type": "test_message", "data": "hello"}
    await manager.send_message(session_id, message)

    # The connection should have been removed
    assert mock_websocket not in manager.active_connections[session_id]

@pytest.mark.asyncio
async def test_broadcast(manager):
    ws1 = MagicMock(spec=WebSocket)
    ws1.accept = AsyncMock()
    ws1.send_json = AsyncMock()

    ws2 = MagicMock(spec=WebSocket)
    ws2.accept = AsyncMock()
    ws2.send_json = AsyncMock()

    session_id1 = "session_1"
    session_id2 = "session_2"

    await manager.connect(ws1, session_id1)
    await manager.connect(ws2, session_id2)

    message = {"type": "broadcast", "data": "hello all"}
    await manager.broadcast(message)

    ws1.send_json.assert_awaited_once_with(message)
    ws2.send_json.assert_awaited_once_with(message)
