import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from backend.sessions.manager import SessionManager

@pytest.fixture
def session_manager():
    return SessionManager(agent_manager=None)

@pytest.mark.asyncio
async def test_handle_task_done(session_manager):
    session = {"id": "test_session", "messages": []}
    session_manager._sys_msg = AsyncMock()
    result = await session_manager._handle_task_done(session, "DONE", 5)
    assert result is True
    session_manager._sys_msg.assert_called_once_with(session, "✅ Task complete after 6 rounds.", "✅", "#10B981")

@pytest.mark.asyncio
async def test_handle_task_not_done(session_manager):
    session = {"id": "test_session", "messages": []}
    session_manager._sys_msg = AsyncMock()
    result = await session_manager._handle_task_done(session, "Agent_1", 5)
    assert result is False
    session_manager._sys_msg.assert_not_called()

@pytest.mark.asyncio
async def test_send_final_summary(session_manager, tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "file1.txt").write_text("hello")
    (workspace / "file2.txt").write_text("world")

    session = {"id": "test_session", "messages": []}
    session_manager._sys_msg = AsyncMock()

    await session_manager._send_final_summary(session, workspace)

    session_manager._sys_msg.assert_called_once()
    args, kwargs = session_manager._sys_msg.call_args
    assert "Project workspace (2 files):" in args[1]
    assert "file1.txt" in args[1]
    assert "file2.txt" in args[1]
