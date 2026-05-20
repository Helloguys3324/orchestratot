import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from backend.websocket.handler import ConnectionManager

@pytest.fixture
def manager():
    return ConnectionManager()

@pytest.mark.anyio
async def test_connect(manager):
    ws = AsyncMock()
    await manager.connect(ws, "session1")
    assert "session1" in manager.active_connections
    assert ws in manager.active_connections["session1"]
    ws.accept.assert_awaited_once()

@pytest.mark.anyio
async def test_disconnect(manager):
    ws = AsyncMock()
    await manager.connect(ws, "session1")
    manager.disconnect(ws, "session1")
    assert "session1" not in manager.active_connections

@pytest.mark.anyio
async def test_send_message(manager):
    ws = AsyncMock()
    await manager.connect(ws, "session1")
    await manager.send_message("session1", {"type": "test"})
    ws.send_json.assert_awaited_once_with({"type": "test"})

@pytest.mark.anyio
async def test_send_message_dead_socket(manager):
    ws = AsyncMock()
    ws.send_json.side_effect = Exception("Connection closed")
    await manager.connect(ws, "session1")

    await manager.send_message("session1", {"type": "test"})
    assert "session1" not in manager.active_connections

@pytest.mark.anyio
async def test_broadcast(manager):
    ws1 = AsyncMock()
    ws2 = AsyncMock()
    await manager.connect(ws1, "session1")
    await manager.connect(ws2, "session2")

    await manager.broadcast({"type": "test"})
    ws1.send_json.assert_awaited_once_with({"type": "test"})
    ws2.send_json.assert_awaited_once_with({"type": "test"})
