# ARCHITECTURE_STATE.md

## Genesis Protocol: Zero-State & Initial System Architecture

### 1. High-Level Objective
Build a highly scalable, fault-tolerant Multi-Agent Orchestrator operating in a continuous, zero-human-in-the-loop, multi-week execution pipeline. The system utilizes DAG-based routing, asyncio, and MCP (Model Context Protocol) integration.

### 2. Current Zero-State Repository Structure
The repository is initially structured into the following directories:
- `backend/`: Core orchestrator logic utilizing FastAPI, Uvicorn, and Pydantic v2.
  - `agents/`: Defines agent classes and behaviors.
  - `api/`: FastAPI APIRouter endpoints decoupling application routing logic.
  - `llm/`: Decoupled low-level LLM API integrations (e.g., Gemini Live API and OpenAI compatible endpoints) enforcing strict architectural boundaries.
  - `models/`: Pydantic data models.
  - `sessions/`: Manages orchestration sessions.
  - `skills/`: Agent capabilities.
  - `tests/`: Unit and integration tests for backend modules.
  - `websocket/`: Real-time communication handlers.
  - `state.py`: Global application state and manager instantiations.
- `frontend/`: Web UI components (HTML/CSS/JS).
- `skills_library/`: Reusable skills and MCP tools.
- `data/`: Persistent or temporary data storage.
- `workspace/`: Execution workspace for agents.

### 3. Tech Stack Choices
- **Backend Framework:** FastAPI, Uvicorn (async HTTP server)
- **Data Validation:** Pydantic v2
- **Concurrency:** Asyncio (Python) for non-blocking operations.
- **Environment Management:** `python-dotenv` for configuration loading.
- **Protocol:** MCP (Model Context Protocol) for tool and skill execution.
- **Routing:** DAG-based (Directed Acyclic Graph) task routing.
- **Testing:** `pytest` with heavily type-hinted, asynchronous code.

### 4. Data Flow & System Architecture
1. **Input:** User requests or autonomous triggers initialize a session.
2. **Orchestrator:** A central asynchronous loop manages DAG execution.
3. **Agent Routing:** Tasks are parsed and assigned to specific agents based on capabilities.
4. **Execution:** Agents use skills via MCP, fetching tools and executing them safely.
5. **Memory & State:** `ARCHITECTURE_STATE.md` maintains long-term memory for the continuous loop, alongside structured logs or databases for session memory.
6. **Output/Feedback:** Results are aggregated, validated against constraints, and returned to the user or passed to the next DAG node. Continuous self-healing is triggered on failure.

### 5. Active Interfaces
- **HTTP Server:** `http://localhost:8000` (FastAPI/Uvicorn) entry point via `run.py`.
- **WebSocket:** Real-time updates and streaming between backend and frontend.

### 6. Architectural Constraints & Cognitive Directives
- **Performance:** Optimize algorithmic complexity (prefer O(1)/O(N)), memory management, and execution speed.
- **Verification:** Zero-trust verification. Unit/integration tests via MCP must pass before any code is considered complete.
- **Self-Healing:** Enter a debug loop immediately upon test failure or bug detection. Analyze stack traces and fix.
- **Recursive Meta-Prompting:** All tasks generated must follow the strict 4-part protocol: `[INPUT STATE]`, `[ATOMIC OBJECTIVE]`, `[CONSTRAINTS]`, `[ACCEPTANCE CRITERIA]`.
