from fastapi import APIRouter, HTTPException, Request
from backend.state import skills_manager
from backend.skills.errors import SkillValidationError, SkillInstallError, SkillNotFoundError

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("")
async def api_list_skills():
    return skills_manager.list_skills()

@router.get("/marketplace")
async def api_list_marketplace():
    return skills_manager.list_marketplace()

@router.post("")
async def api_create_skill(request: Request):
    data = await request.json()
    try:
        return skills_manager.create_skill(data)
    except SkillValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SkillInstallError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{skill_id}")
async def api_delete_skill(skill_id: str):
    try:
        skills_manager.delete_skill(skill_id)
        return {"status": "ok"}
    except SkillNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SkillInstallError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/install")
async def api_install_skill(request: Request):
    data = await request.json()
    url = data.get("url")
    name = data.get("name")
    if not url:
        raise HTTPException(400, "URL is required")

    try:
        skill = await skills_manager.install_from_url(url, name)
        return skill
    except SkillValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SkillInstallError as e:
        raise HTTPException(status_code=500, detail=str(e))
