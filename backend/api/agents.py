from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.state import agent_manager

router = APIRouter(prefix="/api/agents", tags=["agents"])

class AgentBaseRequest(BaseModel):
    name: str | None = None
    icon: str | None = None
    color: str | None = None
    description: str | None = None
    system_prompt: str | None = None
    skills: list[str] | None = None
    model: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, ge=1)
    enabled: bool | None = None

class AgentCreateRequest(AgentBaseRequest):
    template: str | None = None

class AgentUpdateRequest(AgentBaseRequest):
    pass

@router.get("")
async def api_list_agents():
    return agent_manager.list_agents()

@router.get("/{agent_id}")
async def api_get_agent(agent_id: str):
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent

@router.post("")
async def api_create_agent(request: AgentCreateRequest):
    data = request.model_dump(exclude_unset=True)
    return agent_manager.create_agent(data)

@router.put("/{agent_id}")
async def api_update_agent(agent_id: str, request: AgentUpdateRequest):
    data = request.model_dump(exclude_unset=True)
    agent = agent_manager.update_agent(agent_id, data)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent

@router.delete("/{agent_id}")
async def api_delete_agent(agent_id: str):
    if agent_manager.delete_agent(agent_id):
        return {"status": "ok"}
    raise HTTPException(404, "Agent not found")

@router.post("/{agent_id}/duplicate")
async def api_duplicate_agent(agent_id: str):
    agent = agent_manager.duplicate_agent(agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent
