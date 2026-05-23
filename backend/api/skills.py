from contextlib import asynccontextmanager
from fastapi import APIRouter, HTTPException
from backend.state import skills_manager
from backend.skills.errors import SkillError, SkillValidationError, SkillNotFoundError
from backend.api.schemas import SkillCreateRequest, SkillInstallRequest

router = APIRouter(prefix="/api/skills", tags=["skills"])

@asynccontextmanager
async def async_handle_skill_exceptions():
    try:
        yield
    except HTTPException:
        raise
    except Exception as e:
        status_codes = {
            SkillValidationError: 400,
            SkillNotFoundError: 404,
        }
        status_code = next((code for exc_type, code in status_codes.items() if isinstance(e, exc_type)), 500)
        error_type = type(e).__name__ if isinstance(e, SkillError) else "InternalServerError"
        raise HTTPException(status_code=status_code, detail={"error": error_type, "message": str(e)})

@router.get("")
async def api_list_skills():
    async with async_handle_skill_exceptions():
        return skills_manager.list_skills()

@router.get("/marketplace")
async def api_list_marketplace():
    async with async_handle_skill_exceptions():
        return skills_manager.list_marketplace()

@router.post("")
async def api_create_skill(request: SkillCreateRequest):
    data = request.model_dump(exclude_unset=True)
    async with async_handle_skill_exceptions():
        return skills_manager.create_skill(data)

@router.delete("/{skill_id}")
async def api_delete_skill(skill_id: str):
    async with async_handle_skill_exceptions():
        skills_manager.delete_skill(skill_id)
        return {"status": "ok"}

@router.post("/install")
async def api_install_skill(request: SkillInstallRequest):
    async with async_handle_skill_exceptions():
        skill = await skills_manager.install_from_url(request.url, request.name)
        return skill
