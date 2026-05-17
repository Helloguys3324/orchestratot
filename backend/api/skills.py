from contextlib import contextmanager
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from backend.state import skills_manager
from backend.skills.errors import SkillValidationError, SkillInstallError, SkillNotFoundError

router = APIRouter(prefix="/api/skills", tags=["skills"])

@contextmanager
def handle_skill_exceptions():
    try:
        yield
    except SkillValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SkillNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SkillInstallError as e:
        raise HTTPException(status_code=500, detail=str(e))

class SkillCreateRequest(BaseModel):
    name: str | None = None
    icon: str | None = None
    description: str | None = None
    category: str | None = None
    code: str | None = None

class SkillInstallRequest(BaseModel):
    url: str
    name: Optional[str] = None

@router.get("")
async def api_list_skills():
    return skills_manager.list_skills()

@router.get("/marketplace")
async def api_list_marketplace():
    return skills_manager.list_marketplace()

@router.post("")
async def api_create_skill(request: SkillCreateRequest):
    data = request.model_dump(exclude_unset=True)
    with handle_skill_exceptions():
        return skills_manager.create_skill(data)

@router.delete("/{skill_id}")
async def api_delete_skill(skill_id: str):
    with handle_skill_exceptions():
        skills_manager.delete_skill(skill_id)
        return {"status": "ok"}

@router.post("/install")
async def api_install_skill(request: SkillInstallRequest):
    with handle_skill_exceptions():
        skill = await skills_manager.install_from_url(request.url, request.name)
        return skill
