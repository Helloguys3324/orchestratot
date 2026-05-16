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
  - **Request Example**:
    ```json
    {
      "name": "Custom Data Analyst",
      "icon": "📊",
      "color": "#3B82F6",
      "description": "Analyzes CSV data",
      "system_prompt": "You are a data analyst.",
      "model": "gemini-2.5-flash",
      "temperature": 0.2,
      "max_tokens": 4096,
      "skills": ["file_reader"],
      "enabled": true
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": "a1b2c3d4",
      "name": "Custom Data Analyst",
      "icon": "📊",
      "color": "#3B82F6",
      "description": "Analyzes CSV data",
      "system_prompt": "You are a data analyst.",
      "skills": ["file_reader"],
      "model": "gemini-2.5-flash",
      "temperature": 0.2,
      "max_tokens": 4096,
      "enabled": true,
      "template": "custom"
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
  - **Request Example**:
    ```json
    {
      "name": "Format Code",
      "icon": "✨",
      "description": "Formats Python code using black",
      "category": "custom",
      "code": "def run():\n    return 'Code formatted'"
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": "custom_1a2b3c4d",
      "name": "Format Code",
      "icon": "✨",
      "description": "Formats Python code using black",
      "category": "custom",
      "builtin": false,
      "enabled": true,
      "source": "custom",
      "code": "def run():\n    return 'Code formatted'",
      "file": "custom_1a2b3c4d.py"
    }
    ```
- `DELETE /api/skills/{skill_id}`: Delete a skill.
- `POST /api/skills/install`: Install a skill from a URL.

### Sessions
- `GET /api/sessions`: List all sessions.
- `GET /api/sessions/{session_id}`: Get a specific session.
- `POST /api/sessions`: Create a new session.
  - **Request Example**:
    ```json
    {
      "name": "Data Analysis Task",
      "agent_ids": ["a1b2c3d4", "e5f6g7h8"],
      "strategy": "auto",
      "max_rounds": 15
    }
    ```
  - **Response Example**:
    ```json
    {
      "id": "s1e2s3i4",
      "name": "Data Analysis Task",
      "agent_ids": ["a1b2c3d4", "e5f6g7h8"],
      "strategy": "auto",
      "max_rounds": 15,
      "created_at": "2026-05-16T14:30:00.000000",
      "messages": [],
      "status": "idle",
      "workspace": "workspace/s1e2s3i4"
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
