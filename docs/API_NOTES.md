# API & Architecture Notes

This document provides a high-level overview of the backend API endpoints and the session message flow, based on the FastAPI application defined in `backend/main.py`.

## Core API Endpoints

The backend exposes several sets of RESTful endpoints to manage the orchestration platform's resources:

### Settings API
- `GET /api/settings` - Retrieve current application settings.
- `POST /api/settings` - Update application settings.

### Templates API
- `GET /api/templates` - List available agent templates.

### Agents API
- `GET /api/agents` - List all configured agents.
- `GET /api/agents/{agent_id}` - Retrieve a specific agent.
- `POST /api/agents` - Create a new agent.
- `PUT /api/agents/{agent_id}` - Update an existing agent.
- `DELETE /api/agents/{agent_id}` - Delete an agent.
- `POST /api/agents/{agent_id}/duplicate` - Duplicate an existing agent.

### Models API
- `GET /api/models` - List all available models.
- `GET /api/models/categories` - List models grouped by category.
- `GET /api/models/chat` - List models that support chat capabilities.
- `GET /api/models/{model_id}` - Retrieve details for a specific model.

### Skills API
- `GET /api/skills` - List installed skills.
- `GET /api/skills/marketplace` - List available skills from the marketplace.
- `POST /api/skills` - Create a new custom skill.
- `DELETE /api/skills/{skill_id}` - Delete an installed skill.
- `POST /api/skills/install` - Install a skill from a provided URL.

### Sessions API
- `GET /api/sessions` - List all sessions.
- `GET /api/sessions/{session_id}` - Retrieve a specific session.
- `POST /api/sessions` - Create a new session.
- `DELETE /api/sessions/{session_id}` - Delete a session.
- `POST /api/sessions/{session_id}/chat` - Submit a message to the session.
- `POST /api/sessions/{session_id}/clear` - Clear all messages in a session.
- `GET /api/sessions/{session_id}/files` - Retrieve workspace files associated with a session.

### WebSocket
- `WS /ws/{session_id}` - Establish a WebSocket connection for real-time updates for a specific session. Clients can send a `ping` text message to receive a `{"type": "pong"}` response to maintain connection.

## Session Message Flow

The platform uses a combination of REST APIs and WebSockets to handle real-time chat interactions asynchronously:

1. **User Input:** A user submits a message via the `POST /api/sessions/{session_id}/chat` endpoint.
2. **Background Execution:** The `api_chat` endpoint validates the input message and immediately returns a `{"status": "started"}` response to the client. The actual chat processing logic (`session_manager.run_chat(session_id, message)`) is delegated to an `asyncio` background task.
3. **Agent Updates & WebSocket Streaming:** While the background task processes the message and the agent executes its logic, real-time updates are pushed to the client via the active WebSocket connection at `WS /ws/{session_id}`. This allows the frontend to stream responses and display execution states without blocking the main thread or keeping long HTTP requests open.
