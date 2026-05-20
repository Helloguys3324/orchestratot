from typing import List, Optional
from pydantic import BaseModel, Field

# --- Sessions ---
class SessionCreateRequest(BaseModel):
    title: Optional[str] = "New Session"
    agent_ids: Optional[List[str]] = []
    # Any other fields the frontend might send
    model_config = {"extra": "allow"}

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The message content cannot be empty")

# --- Skills ---
class SkillCreateRequest(BaseModel):
    name: str | None = None
    icon: str | None = None
    description: str | None = None
    category: str | None = None
    code: str | None = None

class SkillInstallRequest(BaseModel):
    url: str
    name: Optional[str] = None

# --- Agents ---
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
