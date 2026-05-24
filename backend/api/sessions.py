import asyncio
from fastapi import APIRouter, Depends
from backend.state import session_manager
from backend.api.dependencies import get_session_or_404
from backend.api.schemas import SessionCreateRequest, ChatMessageRequest

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

@router.get("")
async def api_list_sessions():
    return session_manager.list_sessions()

@router.get("/{session_id}")
async def api_get_session(session: dict = Depends(get_session_or_404)):
    return session

@router.post("")
async def api_create_session(request: SessionCreateRequest):
    return session_manager.create_session(request.model_dump(exclude_unset=True))

@router.delete("/{session_id}")
async def api_delete_session(session_id: str, session: dict = Depends(get_session_or_404)):
    session_manager.delete_session(session_id)
    return {"status": "ok"}

@router.post("/{session_id}/chat")
async def api_chat(session_id: str, request: ChatMessageRequest, session: dict = Depends(get_session_or_404)):
    # Run chat in background so the HTTP response returns immediately
    asyncio.create_task(session_manager.run_chat(session_id, request.message))
    return {"status": "started"}

@router.post("/{session_id}/clear")
async def api_clear_session(session_id: str, session: dict = Depends(get_session_or_404)):
    session_manager.clear_messages(session_id)
    return {"status": "ok"}

@router.get("/{session_id}/files")
async def api_session_files(session_id: str, session: dict = Depends(get_session_or_404)):
    return session_manager.get_workspace_files(session_id)
