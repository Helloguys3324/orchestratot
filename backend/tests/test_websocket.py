import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
import pytest
from fastapi import WebSocket

from backend.websocket.handler import ConnectionManager


def test_connection_manager_init():
    manager = ConnectionManager()
    assert manager.active_connections == {}


def test_connect():
    manager = ConnectionManager()
    mock_websocket = AsyncMock(spec=WebSocket)

    async def run_test():
        await manager.connect(mock_websocket, "session_1")

    asyncio.run(run_test())

    mock_websocket.accept.assert_called_once()
    assert "session_1" in manager.active_connections
    assert mock_websocket in manager.active_connections["session_1"]

    # Connect another socket to same session
    mock_websocket_2 = AsyncMock(spec=WebSocket)
    async def run_test_2():
        await manager.connect(mock_websocket_2, "session_1")

    asyncio.run(run_test_2())
    assert len(manager.active_connections["session_1"]) == 2


def test_disconnect():
    manager = ConnectionManager()
    mock_websocket = AsyncMock(spec=WebSocket)

    # Setup initial connection manually for test
    manager.active_connections["session_1"] = {mock_websocket}

    manager.disconnect(mock_websocket, "session_1")

    # Disconnecting the last socket should remove the session
    assert "session_1" not in manager.active_connections

    # Disconnecting when session not present should not raise error
    manager.disconnect(mock_websocket, "session_nonexistent")

    # Disconnect one of multiple
    mock_websocket_1 = AsyncMock(spec=WebSocket)
    mock_websocket_2 = AsyncMock(spec=WebSocket)
    manager.active_connections["session_2"] = {mock_websocket_1, mock_websocket_2}

    manager.disconnect(mock_websocket_1, "session_2")
    assert "session_2" in manager.active_connections
    assert len(manager.active_connections["session_2"]) == 1
    assert mock_websocket_2 in manager.active_connections["session_2"]


def test_send_message():
    manager = ConnectionManager()
    mock_websocket = AsyncMock(spec=WebSocket)
    manager.active_connections["session_1"] = {mock_websocket}

    message = {"type": "test", "data": "hello"}

    async def run_test():
        await manager.send_message("session_1", message)

    asyncio.run(run_test())

    mock_websocket.send_json.assert_called_once_with(message)

    # Send message to nonexistent session should silently pass
    async def run_test_nonexistent():
        await manager.send_message("session_nonexistent", message)

    asyncio.run(run_test_nonexistent())


def test_send_message_dead_connection():
    manager = ConnectionManager()
    mock_ws_good = AsyncMock(spec=WebSocket)
    mock_ws_dead = AsyncMock(spec=WebSocket)

    # Make the dead websocket raise an exception on send_json
    mock_ws_dead.send_json.side_effect = Exception("Connection closed")

    manager.active_connections["session_1"] = {mock_ws_good, mock_ws_dead}

    message = {"type": "test", "data": "hello"}

    async def run_test():
        await manager.send_message("session_1", message)

    asyncio.run(run_test())

    mock_ws_good.send_json.assert_called_once_with(message)
    mock_ws_dead.send_json.assert_called_once_with(message)

    # Dead websocket should have been removed
    assert len(manager.active_connections["session_1"]) == 1
    assert mock_ws_good in manager.active_connections["session_1"]
    assert mock_ws_dead not in manager.active_connections["session_1"]


def test_broadcast():
    manager = ConnectionManager()
    mock_ws_1 = AsyncMock(spec=WebSocket)
    mock_ws_2 = AsyncMock(spec=WebSocket)

    manager.active_connections["session_1"] = {mock_ws_1}
    manager.active_connections["session_2"] = {mock_ws_2}

    message = {"type": "broadcast", "data": "hello all"}

    async def run_test():
        await manager.broadcast(message)

    asyncio.run(run_test())

    mock_ws_1.send_json.assert_called_once_with(message)
    mock_ws_2.send_json.assert_called_once_with(message)
