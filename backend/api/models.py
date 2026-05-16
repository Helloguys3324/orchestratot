from fastapi import APIRouter, HTTPException
from backend.models.registry import list_models, list_models_by_category, get_model, get_chat_models

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
async def api_get_model(model_id: str):
    model = get_model(model_id)
    if not model:
        raise HTTPException(404, "Model not found")
    return model
