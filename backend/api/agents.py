from fastapi import APIRouter, Depends
from backend.state import agent_manager
from backend.api.dependencies import get_agent_or_404
from backend.api.schemas import AgentCreateRequest, AgentUpdateRequest

router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.get("")
async def api_list_agents():
    return agent_manager.list_agents()

@router.get("/{agent_id}")
async def api_get_agent(agent: dict = Depends(get_agent_or_404)):
    return agent

@router.post("")
async def api_create_agent(request: AgentCreateRequest):
    return agent_manager.create_agent(request.model_dump(exclude_unset=True))

@router.put("/{agent_id}")
async def api_update_agent(agent_id: str, request: AgentUpdateRequest, agent: dict = Depends(get_agent_or_404)):
    return agent_manager.update_agent(agent_id, request.model_dump(exclude_unset=True))

@router.delete("/{agent_id}")
async def api_delete_agent(agent_id: str, agent: dict = Depends(get_agent_or_404)):
    agent_manager.delete_agent(agent_id)
    return {"status": "ok"}

@router.post("/{agent_id}/duplicate")
async def api_duplicate_agent(agent_id: str, agent: dict = Depends(get_agent_or_404)):
    return agent_manager.duplicate_agent(agent_id)
