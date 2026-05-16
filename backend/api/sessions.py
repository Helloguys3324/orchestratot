import asyncio
from fastapi import APIRouter, HTTPException, Request
from backend.state import session_manager

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

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
async def api_create_session(request: Request):
    data = await request.json()
    return session_manager.create_session(data)

@router.delete("/{session_id}")
async def api_delete_session(session_id: str):
    if session_manager.delete_session(session_id):
        return {"status": "ok"}
    raise HTTPException(404, "Session not found")

@router.post("/{session_id}/chat")
async def api_chat(session_id: str, request: Request):
    data = await request.json()
    message = data.get("message", "")
    if not message:
        raise HTTPException(400, "Message is required")

    # Run chat in background so the HTTP response returns immediately
    asyncio.create_task(session_manager.run_chat(session_id, message))
    return {"status": "started"}

@router.post("/{session_id}/clear")
async def api_clear_session(session_id: str):
    if session_manager.clear_messages(session_id):
        return {"status": "ok"}
    raise HTTPException(404, "Session not found")

@router.get("/{session_id}/files")
async def api_session_files(session_id: str):
    return session_manager.get_workspace_files(session_id)
