from fastapi import HTTPException
from backend.state import agent_manager, session_manager
from backend.models.registry import get_model

from typing import Callable, Any

def _get_item_or_404(getter: Callable[[str], Any], item_id: str, item_name: str) -> dict:
    item = getter(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"{item_name} not found")
    return item

def get_agent_or_404(agent_id: str) -> dict:
    return _get_item_or_404(agent_manager.get_agent, agent_id, "Agent")

def get_session_or_404(session_id: str) -> dict:
    return _get_item_or_404(session_manager.get_session, session_id, "Session")

def get_model_or_404(model_id: str) -> dict:
    return _get_item_or_404(get_model, model_id, "Model")
