# ARCHITECTURE_STATE.md

## Genesis Protocol: Current System Architecture

### 1. High-Level Objective
Build a highly scalable, fault-tolerant Multi-Agent Orchestrator operating in a continuous, zero-human-in-the-loop, multi-week execution pipeline. The system utilizes DAG-based routing, asyncio, and MCP (Model Context Protocol) integration.

### 2. Current Repository Structure
The repository is structured into the following directories:
- `.github/`: CI/CD workflows, automation scripts, and task queues for AI Factory.
- `backend/`: Core orchestrator logic utilizing FastAPI, Uvicorn, and Pydantic v2.
  - `agents/`: Defines agent classes and behaviors.
  - `api/`: FastAPI APIRouter endpoints decoupling application routing logic, utilizing FastAPI's `Depends()` injection for reusable API dependencies.
  - `llm/`: Decoupled low-level LLM API integrations (e.g., Gemini Live API and OpenAI compatible endpoints) enforcing strict architectural boundaries.
  - `models/`: Pydantic data models.
  - `sessions/`: Manages orchestration sessions.
  - `skills/`: Agent capabilities.
  - `tests/`: Unit and integration tests for backend modules.
  - `websocket/`: Real-time communication handlers.
  - `state.py`: Global application state and manager instantiations.
- `docs/`: Architectural Decision Records (ADRs) and architectural state documentation.
- `frontend/`: Web UI components (HTML/CSS/JS) with shared UI utilities and Node.js testing.
- `skills_library/`: Reusable skills and MCP tools.
- `tests/`: Unit tests for `skills_library` and other non-backend modules.
- `data/`: Persistent or temporary data storage.
- `workspace/`: Execution workspace for agents.

### 3. Tech Stack Choices
- **Backend Framework:** FastAPI, Uvicorn (async HTTP server)
- **Data Validation:** Pydantic v2 (includes SecretStr for config security and request models)
- **Concurrency:** Asyncio (Python) for non-blocking operations.
- **Environment Management:** `pydantic-settings` for configuration loading, robust parsing, and environment variable overlay prioritization over JSON fallbacks, including bypassing invalid empty variables.
- **Protocol:** MCP (Model Context Protocol) for tool and skill execution.
- **Routing:** DAG-based (Directed Acyclic Graph) task routing.
- **Testing:** `pytest` (backend) and Node.js built-in `node:test` (frontend, leveraging conditional CommonJS exports to expose vanilla JS objects, achieving complete line coverage, and simulating DOM manipulation via `global.document` mocking without external libraries) with heavily type-hinted, asynchronous code. For config models, validate dynamically via `model_fields.keys()` rather than `model_dump()` to prevent environment-dependent crashes. For Node.js modules that conditionally attach event listeners upon evaluation, test setups must clear `require.cache` and re-require the module after establishing global DOM mocks to ensure proper listener attachment.
- **Dependency Management:** Proactive vulnerability mitigation (e.g., upgrading packages to avoid insecure transitive dependencies like `diskcache`) and explicit local vulnerability scanning utilizing `pip-audit`, which requires core backend dependencies to be installed first to ensure accurate evaluation of transitive dependencies.

### 4. Data Flow & System Architecture
1. **Input:** User requests or autonomous triggers initialize a session.
2. **Orchestrator:** A central asynchronous loop manages DAG execution.
3. **Agent Routing:** Tasks are parsed and assigned to specific agents based on capabilities.
4. **Execution:** Agents use skills via MCP, fetching tools and executing them safely. Managers (e.g., `SessionManager`) isolate real-time WebSocket communication from core logic by utilizing injected `_message_callback` functions to emit events (e.g., `_add_message`), decoupling them from direct FastAPI WebSocket routing. Localized helper functions (e.g., `_error_msg`) are utilized for standardized event formatting.
5. **Memory & State:** `ARCHITECTURE_STATE.md` maintains long-term memory for the continuous loop, alongside structured logs or databases for session memory.
6. **Output/Feedback:** Results are aggregated, validated against constraints, and returned to the user or passed to the next DAG node. Continuous self-healing is triggered on failure.

### 5. Active Interfaces
- **HTTP Server:** `http://localhost:8000` (FastAPI/Uvicorn) entry point via `run.py`.
- **WebSocket:** Real-time updates and streaming between backend and frontend.

### 6. Architectural Constraints & Cognitive Directives
- **Performance:** Optimize algorithmic complexity (prefer O(1)/O(N)), memory management, and execution speed.
- **Verification:** Zero-trust verification. Unit/integration tests via MCP must pass before any code is considered complete. Furthermore, strict frontend visual validation is required for any UI modifications to confirm layout stability and absence of console errors before changes can be submitted.
- **Self-Healing:** Enter a debug loop immediately upon test failure or bug detection. Analyze stack traces and fix.
- **Recursive Meta-Prompting:** All tasks generated must follow the strict 4-part protocol: `[INPUT STATE]`, `[ATOMIC OBJECTIVE]`, `[CONSTRAINTS]`, `[ACCEPTANCE CRITERIA]`.
- **Error Handling & Validation:** Enforce explicit typed domain exceptions. When catching low-level exceptions like `OSError` or `json.JSONDecodeError`, explicitly re-raise them as specific domain errors (e.g., `SkillInstallError`) instead of generic `Exception`, chaining `from e` to preserve original tracebacks, and mapping to precise HTTP status codes. Use standard synchronous `@contextmanager` from `contextlib` to wrap asynchronous FastAPI route handlers for centralized HTTP status mapping, eliminating duplicate `try...except` blocks. Use shared base request models to reduce duplication in API contracts. Use Pydantic `BaseModel` for inbound request payload validation, and `pydantic-settings` for config management with empty env var filtering via `os.environ.pop`, dynamic `ValidationError` fallback using explicit defaults via `init_kwargs`, and persisting only explicitly provided keys during runtime `.env` updates to avoid cluttering with defaults.
- **Documentation:** API payloads must be documented in `docs/API_NOTES.md`.
- **Emergency Stop:** The `AUTOPILOT_STOP` file acts as an emergency stop signal; automation must immediately halt and the file must not be removed.
