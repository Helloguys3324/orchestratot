"""
AutoGen AI Orchestrator — Main FastAPI Application.
"""
import sys
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Add parent dir to path so backend package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.state import ws_manager, session_manager
from backend.api import settings, templates, agents, models, skills, sessions

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

# ─── API Routers ─────────────────────────────────────────
app.include_router(settings.router)
app.include_router(templates.router)
app.include_router(agents.router)
app.include_router(models.router)
app.include_router(skills.router)
app.include_router(sessions.router)

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
