from fastapi import APIRouter
from backend.agents.templates import list_templates

router = APIRouter(prefix="/api/templates", tags=["templates"])

@router.get("")
async def api_list_templates():
    return list_templates()
