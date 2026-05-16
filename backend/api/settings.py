from fastapi import APIRouter, Request
from backend.config import get_settings, save_settings

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("")
async def api_get_settings():
    return get_settings()

@router.post("")
async def api_save_settings(request: Request):
    data = await request.json()
    settings = get_settings()
    settings.update(data)
    save_settings(settings)
    return {"status": "ok"}
