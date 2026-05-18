from typing import Dict, Any
from fastapi import APIRouter
from backend.config import get_settings, save_settings

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("")
async def api_get_settings():
    return get_settings()

@router.post("")
async def api_save_settings(data: Dict[str, Any]):
    save_settings(data)
    return {"status": "ok"}
