from fastapi import APIRouter
from backend.state import skills_manager
from backend.api.schemas import SkillCreateRequest, SkillInstallRequest

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("")
async def api_list_skills():
    return skills_manager.list_skills()

@router.get("/marketplace")
async def api_list_marketplace():
    return skills_manager.list_marketplace()

@router.post("")
async def api_create_skill(request: SkillCreateRequest):
    return skills_manager.create_skill(request.model_dump(exclude_unset=True))

@router.delete("/{skill_id}")
async def api_delete_skill(skill_id: str):
    skills_manager.delete_skill(skill_id)
    return {"status": "ok"}

@router.post("/install")
async def api_install_skill(request: SkillInstallRequest):
    skill = await skills_manager.install_from_url(request.url, request.name)
    return skill
