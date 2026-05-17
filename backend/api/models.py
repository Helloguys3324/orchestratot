from fastapi import APIRouter, Depends
from backend.models.registry import list_models, list_models_by_category, get_model, get_chat_models
from backend.api.dependencies import get_model_or_404

router = APIRouter(prefix="/api/models", tags=["models"])

@router.get("")
async def api_list_models():
    return list_models()

@router.get("/categories")
async def api_list_models_by_category():
    return list_models_by_category()

@router.get("/chat")
async def api_list_chat_models():
    return get_chat_models()

@router.get("/{model_id}")
async def api_get_model(model: dict = Depends(get_model_or_404)):
    return model
