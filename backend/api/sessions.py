import asyncio
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.state import session_manager

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

class SessionCreate(BaseModel):
    title: Optional[str] = "New Session"
    agent_ids: Optional[List[str]] = []
    # Any other fields the frontend might send
    model_config = {"extra": "allow"}

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, description="The message content cannot be empty")

@router.get("")
async def api_list_sessions():
    return session_manager.list_sessions()

@router.get("/{session_id}")
async def api_get_session(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session

@router.post("")
async def api_create_session(request: SessionCreate):
    return session_manager.create_session(request.model_dump(exclude_unset=True))

@router.delete("/{session_id}")
async def api_delete_session(session_id: str):
    if session_manager.delete_session(session_id):
        return {"status": "ok"}
    raise HTTPException(404, "Session not found")

@router.post("/{session_id}/chat")
async def api_chat(session_id: str, request: ChatMessage):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    # Run chat in background so the HTTP response returns immediately
    asyncio.create_task(session_manager.run_chat(session_id, request.message))
    return {"status": "started"}

@router.post("/{session_id}/clear")
async def api_clear_session(session_id: str):
    if session_manager.clear_messages(session_id):
        return {"status": "ok"}
    raise HTTPException(404, "Session not found")

@router.get("/{session_id}/files")
async def api_session_files(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session_manager.get_workspace_files(session_id)
