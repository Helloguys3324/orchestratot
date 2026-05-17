from fastapi import HTTPException
from backend.state import agent_manager, session_manager
from backend.models.registry import get_model

def get_agent_or_404(agent_id: str) -> dict:
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

def get_session_or_404(session_id: str) -> dict:
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

def get_model_or_404(model_id: str) -> dict:
    model = get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
