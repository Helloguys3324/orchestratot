import pytest
import asyncio
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

def test_connect(manager, mock_websocket):
    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))

    mock_websocket.accept.assert_awaited_once()
    assert session_id in manager.active_connections
    assert mock_websocket in manager.active_connections[session_id]

def test_disconnect(manager, mock_websocket):
    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))

    manager.disconnect(mock_websocket, session_id)

    assert session_id not in manager.active_connections

def test_disconnect_nonexistent(manager, mock_websocket):
    session_id = "test_session_1"

    # Should not raise any error
    manager.disconnect(mock_websocket, session_id)
    assert session_id not in manager.active_connections

def test_send_message_success(manager, mock_websocket):
    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))

    message = {"type": "test_message", "data": "hello"}
    asyncio.run(manager.send_message(session_id, message))

    mock_websocket.send_json.assert_awaited_once_with(message)
    assert session_id in manager.active_connections

def test_send_message_dead_connection(manager, mock_websocket):
    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))

    # Setup the mock to throw an exception
    mock_websocket.send_json.side_effect = Exception("Connection closed")

    message = {"type": "test_message", "data": "hello"}
    asyncio.run(manager.send_message(session_id, message))

    # The dead connection should be removed. Since it's the only one, session should be clean but the code actually just discards it.
    # The implementation in handler doesn't delete the empty session like `disconnect` does.
    assert session_id not in manager.active_connections

def test_broadcast(manager):
    ws1 = MagicMock(spec=WebSocket)
    ws1.accept = AsyncMock()
    ws1.send_json = AsyncMock()

    ws2 = MagicMock(spec=WebSocket)
    ws2.accept = AsyncMock()
    ws2.send_json = AsyncMock()

    session_id1 = "session_1"
    session_id2 = "session_2"

    asyncio.run(manager.connect(ws1, session_id1))
    asyncio.run(manager.connect(ws2, session_id2))

    message = {"type": "broadcast", "data": "hello all"}
    asyncio.run(manager.broadcast(message))

    ws1.send_json.assert_awaited_once_with(message)
    ws2.send_json.assert_awaited_once_with(message)

def test_connect_multiple_websockets_same_session(manager, mock_websocket):
    ws2 = MagicMock(spec=WebSocket)
    ws2.accept = AsyncMock()
    ws2.send_json = AsyncMock()

    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))
    asyncio.run(manager.connect(ws2, session_id))

    assert len(manager.active_connections[session_id]) == 2
    assert mock_websocket in manager.active_connections[session_id]
    assert ws2 in manager.active_connections[session_id]

def test_disconnect_one_of_multiple(manager, mock_websocket):
    ws2 = MagicMock(spec=WebSocket)
    ws2.accept = AsyncMock()
    ws2.send_json = AsyncMock()

    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))
    asyncio.run(manager.connect(ws2, session_id))

    manager.disconnect(mock_websocket, session_id)

    assert session_id in manager.active_connections
    assert len(manager.active_connections[session_id]) == 1
    assert mock_websocket not in manager.active_connections[session_id]
    assert ws2 in manager.active_connections[session_id]

def test_disconnect_not_in_session(manager, mock_websocket):
    ws2 = MagicMock(spec=WebSocket)
    ws2.accept = AsyncMock()
    ws2.send_json = AsyncMock()

    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))

    # Disconnect a websocket that is not in the session
    manager.disconnect(ws2, session_id)

    assert session_id in manager.active_connections
    assert len(manager.active_connections[session_id]) == 1
    assert mock_websocket in manager.active_connections[session_id]

def test_send_message_nonexistent_session(manager):
    session_id = "nonexistent_session"
    message = {"type": "test_message", "data": "hello"}

    # Should not raise an error
    asyncio.run(manager.send_message(session_id, message))
    assert session_id not in manager.active_connections

def test_send_message_partial_failure(manager, mock_websocket):
    ws2 = MagicMock(spec=WebSocket)
    ws2.accept = AsyncMock()
    ws2.send_json = AsyncMock()

    session_id = "test_session_1"
    asyncio.run(manager.connect(mock_websocket, session_id))
    asyncio.run(manager.connect(ws2, session_id))

    # mock_websocket throws exception, ws2 succeeds
    mock_websocket.send_json.side_effect = Exception("Connection closed")

    message = {"type": "test_message", "data": "hello"}
    asyncio.run(manager.send_message(session_id, message))

    # ws2 should have received the message
    ws2.send_json.assert_awaited_once_with(message)

    # mock_websocket should be removed, ws2 should remain
    assert mock_websocket not in manager.active_connections[session_id]
    assert ws2 in manager.active_connections[session_id]
    assert len(manager.active_connections[session_id]) == 1

def test_broadcast_empty(manager):
    message = {"type": "broadcast", "data": "hello all"}

    # Should not raise an error
    asyncio.run(manager.broadcast(message))
    assert len(manager.active_connections) == 0
