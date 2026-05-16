from fastapi import APIRouter, HTTPException, Request
from backend.state import skills_manager

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
    return skills_manager.create_skill(data)

@router.delete("/{skill_id}")
async def api_delete_skill(skill_id: str):
    if skills_manager.delete_skill(skill_id):
        return {"status": "ok"}
    raise HTTPException(404, "Skill not found")

@router.post("/install")
async def api_install_skill(request: Request):
    data = await request.json()
    url = data.get("url")
    name = data.get("name")
    if not url:
        raise HTTPException(400, "URL is required")
    skill = await skills_manager.install_from_url(url, name)
    return skill
