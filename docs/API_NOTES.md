# API and Architecture Notes

This document provides a high-level overview of the backend API and the core session orchestration flow in AutoGen AI Factory.

## Backend Architecture

The backend is built with **FastAPI** and uses **asyncio** for non-blocking operations. It serves the frontend UI and provides REST APIs and WebSocket endpoints for communicating with the orchestration logic.

### Key Components

- **Agent Manager (`backend/agents/manager.py`)**: Manages the creation, updating, duplication, and deletion of agents. Agents represent different personas or roles in the system.
- **Skills Manager (`backend/skills/manager.py`)**: Handles the installation and management of tools/skills that agents can use.
- **Session Manager (`backend/sessions/manager.py`)**: The core orchestrator. Manages the chat sessions, agent routing, and file workspace generation.
- **Connection Manager (`backend/websocket/handler.py`)**: Manages real-time WebSocket connections for pushing agent messages to the frontend.

## API Endpoints (`backend/main.py`)

### Settings
- `GET /api/settings`: Fetch current runtime settings.
- `POST /api/settings`: Update settings (the `api_key` field is scrubbed before saving to disk).

### Agents
- `GET /api/agents`: List all agents.
- `GET /api/agents/{agent_id}`: Get a specific agent by ID.
- `POST /api/agents`: Create a new agent.
  **Request Payload Example:**
  ```json
  {
    "name": "Data Analyst",
    "icon": "📊",
    "color": "#3498db",
    "description": "Analyzes raw data and provides insights.",
    "system_prompt": "You are a helpful data analyst.",
    "skills": ["data_analysis"],
    "model": "gemini-2.5-flash",
    "temperature": 0.7,
    "max_tokens": 1024,
    "enabled": true,
    "template": "data_analyst_template"
  }
  ```
  **Response Payload Example:**
  ```json
  {
    "id": "agent_12345678",
    "name": "Data Analyst",
    "icon": "📊",
    "color": "#3498db",
    "description": "Analyzes raw data and provides insights.",
    "system_prompt": "You are a helpful data analyst.",
    "skills": ["data_analysis"],
    "model": "gemini-2.5-flash",
    "temperature": 0.7,
    "max_tokens": 1024,
    "enabled": true,
    "created_at": "2026-05-16T12:00:00Z"
  }
  ```
- `PUT /api/agents/{agent_id}`: Update an existing agent.
- `DELETE /api/agents/{agent_id}`: Delete an agent.
- `POST /api/agents/{agent_id}/duplicate`: Duplicate an agent.

### Models
- `GET /api/models`: List all available models.
- `GET /api/models/categories`: List models grouped by category.
- `GET /api/models/chat`: List models suitable for chat.
- `GET /api/models/{model_id}`: Get details for a specific model.

### Skills
- `GET /api/skills`: List installed skills.
- `GET /api/skills/marketplace`: List skills available for installation.
- `POST /api/skills`: Create a new custom skill.
  **Request Payload Example:**
  ```json
  {
    "name": "Custom Greeter",
    "icon": "👋",
    "description": "Prints a custom greeting message.",
    "category": "custom",
    "code": "def greet(name):\n    return f'Hello, {name}!'"
  }
  ```
  **Response Payload Example:**
  ```json
  {
    "id": "custom_abcdef12",
    "name": "Custom Greeter",
    "icon": "👋",
    "description": "Prints a custom greeting message.",
    "category": "custom",
    "builtin": false,
    "enabled": true,
    "source": "custom",
    "code": "def greet(name):\n    return f'Hello, {name}!'",
    "file": "custom_abcdef12.py"
  }
  ```
- `DELETE /api/skills/{skill_id}`: Delete a skill.
- `POST /api/skills/install`: Install a skill from a URL.

### Sessions
- `GET /api/sessions`: List all sessions.
- `GET /api/sessions/{session_id}`: Get a specific session.
- `POST /api/sessions`: Create a new session.
  **Request Payload Example:**
  ```json
  {
    "title": "Data Processing Project",
    "agent_ids": ["agent_12345678", "agent_87654321"]
  }
  ```
  **Response Payload Example:**
  ```json
  {
    "id": "session_abcdef12",
    "title": "Data Processing Project",
    "created_at": "2026-05-16T12:05:00Z",
    "agent_ids": ["agent_12345678", "agent_87654321"],
    "messages": []
  }
  ```
- `DELETE /api/sessions/{session_id}`: Delete a session.
- `POST /api/sessions/{session_id}/chat`: Start an orchestrated chat based on a user message. This runs asynchronously.
- `POST /api/sessions/{session_id}/clear`: Clear the message history for a session.
- `GET /api/sessions/{session_id}/files`: List all files written in the session's workspace.

### WebSocket
- `WS /ws/{session_id}`: Establish a WebSocket connection to stream real-time updates and agent messages for a session.

## Session Orchestration Flow

When a user sends a message via `POST /api/sessions/{session_id}/chat`, the Session Manager (`SessionManager._run_orchestrated_chat`) executes the following flow:

1. **Initialization**: It gathers all enabled agents assigned to the session and initializes the session's workspace directory (`workspace/{session_id}`).
2. **Routing (LLM-driven)**: A router model (`gemini-3-flash-live`) acts as the orchestrator. It receives the conversation history and the list of available agents. Its prompt instructs it to pick the *most relevant* agent to respond next or reply with `DONE` if the task is complete.
3. **Agent Execution**:
    - The selected agent's system prompt is assembled, including instructions on how to write files to the workspace (using `<<<FILE: path>>>...<<<END_FILE>>>` blocks).
    - The LLM is called using the specific agent's configured model, temperature, and system prompt.
4. **File Extraction**: The system parses the agent's response, securely extracts any file blocks (preventing path traversal), and writes them to the workspace.
5. **Message Emission**: The agent's response is appended to the session history and emitted via WebSocket to the connected frontend clients.
6. **Loop**: Steps 2-5 repeat until the router outputs `DONE` or the maximum number of rounds (`max_rounds`, default 15) is reached.

## Security and Dependencies

- `python-multipart` should be kept at version `>= 0.0.28` to mitigate vulnerabilities including CVE-2026-24486, CVE-2026-40347, and CVE-2026-42561.
- `fastapi` and `starlette` are upgraded to `>= 0.136.1` and `>= 1.0.1` respectively, to fix starlette vulnerabilities such as CVE-2025-54121, CVE-2025-62727, and PYSEC-2026-161.
- `pyautogen` is constrained to `>= 0.2.36,<0.4.0` due to massive breaking API changes in AutoGen 0.4.x+. Because 0.2.x and 0.3.x still rely on the `diskcache` dependency, `CVE-2025-69872` remains unmitigated. A complete application rewrite is required before we can upgrade to `pyautogen>=0.4.0` and safely remove `diskcache`.
- `uvicorn[standard]` is upgraded to `>= 0.47.0` to fix security vulnerabilities in older versions.
- `aiofiles` is upgraded to `>= 25.1.0` to fix security vulnerabilities in older versions.
- `websockets` is upgraded to `>= 14.1` to fix security vulnerabilities in older versions.
