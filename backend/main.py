"""
AutoGen AI Orchestrator — Main FastAPI Application.
"""
import sys
import asyncio
import json
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Add parent dir to path so backend package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.config import get_settings, save_settings
from backend.agents.manager import AgentManager
from backend.agents.templates import list_templates
from backend.models.registry import list_models, list_models_by_category, get_model, get_chat_models
from backend.skills.manager import SkillsManager
from backend.sessions.manager import SessionManager
from backend.websocket.handler import ConnectionManager

# ─── Globals ─────────────────────────────────────────────
agent_manager = AgentManager()
skills_manager = SkillsManager()
session_manager = SessionManager(agent_manager)
ws_manager = ConnectionManager()


async def on_agent_message(session_id: str, message: dict):
    """Callback fired when an agent sends a message."""
    await ws_manager.send_message(session_id, {
        "type": "agent_message",
        "data": message,
    })


session_manager.set_message_callback(on_agent_message)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="AutoGen AI Orchestrator", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files

async def get_request_json(request: Request) -> dict:
    """Safely parse JSON from a request, raising 400 if the body is empty or invalid."""
    try:
        return await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid or empty JSON body")


# Serve frontend static files
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


# ─── Frontend ────────────────────────────────────────────
@app.get("/")
async def serve_frontend():
    index = frontend_dir / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "Frontend not found. Place index.html in frontend/"}


# ─── Settings API ────────────────────────────────────────
@app.get("/api/settings")
async def api_get_settings():
    return get_settings()


@app.post("/api/settings")
async def api_save_settings(request: Request):
    data = await get_request_json(request)
    settings = get_settings()
    settings.update(data)
    save_settings(settings)
    return {"status": "ok"}


# ─── Templates API ───────────────────────────────────────
@app.get("/api/templates")
async def api_list_templates():
    return list_templates()


# ─── Agents API ──────────────────────────────────────────
@app.get("/api/agents")
async def api_list_agents():
    return agent_manager.list_agents()


@app.get("/api/agents/{agent_id}")
async def api_get_agent(agent_id: str):
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent


@app.post("/api/agents")
async def api_create_agent(request: Request):
    data = await get_request_json(request)
    return agent_manager.create_agent(data)


@app.put("/api/agents/{agent_id}")
async def api_update_agent(agent_id: str, request: Request):
    data = await get_request_json(request)
    agent = agent_manager.update_agent(agent_id, data)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent


@app.delete("/api/agents/{agent_id}")
async def api_delete_agent(agent_id: str):
    if agent_manager.delete_agent(agent_id):
        return {"status": "ok"}
    raise HTTPException(404, "Agent not found")


@app.post("/api/agents/{agent_id}/duplicate")
async def api_duplicate_agent(agent_id: str):
    agent = agent_manager.duplicate_agent(agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent


# ─── Models API ──────────────────────────────────────────
@app.get("/api/models")
async def api_list_models():
    return list_models()


@app.get("/api/models/categories")
async def api_list_models_by_category():
    return list_models_by_category()


@app.get("/api/models/chat")
async def api_list_chat_models():
    return get_chat_models()


@app.get("/api/models/{model_id}")
async def api_get_model(model_id: str):
    model = get_model(model_id)
    if not model:
        raise HTTPException(404, "Model not found")
    return model


# ─── Skills API ──────────────────────────────────────────
@app.get("/api/skills")
async def api_list_skills():
    return skills_manager.list_skills()


@app.get("/api/skills/marketplace")
async def api_list_marketplace():
    return skills_manager.list_marketplace()


@app.post("/api/skills")
async def api_create_skill(request: Request):
    data = await get_request_json(request)
    return skills_manager.create_skill(data)


@app.delete("/api/skills/{skill_id}")
async def api_delete_skill(skill_id: str):
    if skills_manager.delete_skill(skill_id):
        return {"status": "ok"}
    raise HTTPException(404, "Skill not found")


@app.post("/api/skills/install")
async def api_install_skill(request: Request):
    data = await get_request_json(request)
    url = data.get("url")
    name = data.get("name")
    if not url:
        raise HTTPException(400, "URL is required")
    skill = await skills_manager.install_from_url(url, name)
    return skill


# ─── Sessions API ────────────────────────────────────────
@app.get("/api/sessions")
async def api_list_sessions():
    return session_manager.list_sessions()


@app.get("/api/sessions/{session_id}")
async def api_get_session(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session


@app.post("/api/sessions")
async def api_create_session(request: Request):
    data = await get_request_json(request)
    return session_manager.create_session(data)


@app.delete("/api/sessions/{session_id}")
async def api_delete_session(session_id: str):
    if session_manager.delete_session(session_id):
        return {"status": "ok"}
    raise HTTPException(404, "Session not found")


@app.post("/api/sessions/{session_id}/chat")
async def api_chat(session_id: str, request: Request):
    data = await get_request_json(request)
    message = data.get("message", "")
    if not message:
        raise HTTPException(400, "Message is required")

    # Run chat in background so the HTTP response returns immediately
    asyncio.create_task(session_manager.run_chat(session_id, message))
    return {"status": "started"}


@app.post("/api/sessions/{session_id}/clear")
async def api_clear_session(session_id: str):
    if session_manager.clear_messages(session_id):
        return {"status": "ok"}
    raise HTTPException(404, "Session not found")


@app.get("/api/sessions/{session_id}/files")
async def api_session_files(session_id: str):
    return session_manager.get_workspace_files(session_id)


# ─── WebSocket ───────────────────────────────────────────
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await ws_manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Clients can send pings or commands
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, session_id)
