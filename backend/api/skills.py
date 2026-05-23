from contextlib import asynccontextmanager
from fastapi import APIRouter, HTTPException
from backend.state import skills_manager
from backend.skills.errors import SkillError, SkillValidationError, SkillInstallError, SkillNotFoundError
from backend.api.schemas import SkillCreateRequest, SkillInstallRequest

router = APIRouter(prefix="/api/skills", tags=["skills"])

@asynccontextmanager
async def async_handle_skill_exceptions():
    try:
        yield
    except SkillValidationError as e:
        raise HTTPException(status_code=400, detail={"error": "SkillValidationError", "message": str(e)})
    except SkillNotFoundError as e:
        raise HTTPException(status_code=404, detail={"error": "SkillNotFoundError", "message": str(e)})
    except SkillInstallError as e:
        raise HTTPException(status_code=500, detail={"error": "SkillInstallError", "message": str(e)})
    except SkillError as e:
        raise HTTPException(status_code=500, detail={"error": "SkillError", "message": str(e)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})

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
