"""
Session Manager — orchestrates multi-agent chat with smart routing,
file writing workspace, and code execution.
"""
import uuid
import re
import asyncio
import subprocess
from datetime import datetime
from typing import Optional, Callable
from pathlib import Path
from backend.config import SESSIONS_FILE, BASE_DIR, load_json, save_json, get_settings
from backend.agents.manager import AgentManager
from backend.models.registry import get_config_list

try:
    import autogen
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False

WORKSPACE_DIR = BASE_DIR / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)


class SessionManager:
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self._sessions: dict[str, dict] = {}
        self._message_callback: Optional[Callable] = None
        self._load()

    def _load(self):
        sessions_list = load_json(SESSIONS_FILE, [])
        self._sessions = {s["id"]: s for s in sessions_list}

    def _save(self):
        save_json(SESSIONS_FILE, list(self._sessions.values()))

    def set_message_callback(self, callback: Callable):
        self._message_callback = callback

    def list_sessions(self) -> list[dict]:
        return list(self._sessions.values())

    def get_session(self, session_id: str) -> Optional[dict]:
        return self._sessions.get(session_id)

    def create_session(self, data: dict) -> dict:
        session_id = str(uuid.uuid4())[:8]
        session = {
            "id": session_id,
            "name": data.get("name", f"Session {session_id}"),
            "agent_ids": data.get("agent_ids", []),
            "strategy": data.get("strategy", "auto"),
            "max_rounds": data.get("max_rounds", 15),
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "status": "idle",
            "workspace": str(WORKSPACE_DIR / session_id),
        }
        # Create workspace directory
        Path(session["workspace"]).mkdir(parents=True, exist_ok=True)
        self._sessions[session_id] = session
        self._save()
        return session

    def delete_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            self._save()
            return True
        return False

    async def _emit(self, session_id: str, msg: dict):
        """Send message via WebSocket callback."""
        if self._message_callback:
            await self._message_callback(session_id, msg)

    async def _sys_msg(self, session, text, icon="\u2139\ufe0f", color="#94A3B8"):
        """Add and emit a system message."""
        msg = {
            "role": "system", "sender": "System",
            "content": text,
            "timestamp": datetime.now().isoformat(),
            "icon": icon, "color": color,
        }
        session["messages"].append(msg)
        await self._emit(session["id"], msg)

    async def run_chat(self, session_id: str, user_message: str):
        session = self._sessions.get(session_id)
        if not session:
            return

        settings = get_settings()
        api_key = settings.get("api_key", "")

        session["status"] = "running"
        self._save()

        # Add user message
        user_msg = {
            "role": "user", "sender": "You",
            "content": user_message,
            "timestamp": datetime.now().isoformat(),
            "icon": "\U0001f464", "color": "#FFFFFF",
        }
        session["messages"].append(user_msg)
        await self._emit(session_id, user_msg)

        if not api_key:
            await self._sys_msg(session,
                "\u274c API key not set! Go to Settings, paste your Google AI Studio key, click Save.",
                "\u26a0\ufe0f", "#EF4444")
            session["status"] = "idle"
            self._save()
            return

        try:
            await self._run_orchestrated_chat(session, user_message, api_key, settings)
        except Exception as e:
            await self._sys_msg(session,
                f"\u274c Error: {type(e).__name__}: {str(e)}",
                "\u26a0\ufe0f", "#EF4444")

        session["status"] = "idle"
        self._save()

    async def _call_llm(self, api_key, base_url, model, messages, temperature=0.7, max_tokens=4096):
        """Async call to Gemini. Auto-routes to Live API for live models."""
        from backend.models.registry import get_model as get_model_info
        model_info = get_model_info(model)
        
        # Use Live API for live models (unlimited rate limits!)
        if model_info and model_info.get("live_api"):
            return await self._call_live_api(api_key, model, messages, temperature)
        
        # Standard OpenAI-compatible API
        import openai
        client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _call_live_api(self, api_key, model, messages, temperature=0.7):
        """Call Gemini via the Live API (WebSocket) — unlimited RPM/RPD."""
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        # Extract system prompt and build conversation text
        system_text = ""
        conversation = ""
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            elif msg["role"] == "user":
                conversation += f"User: {msg['content']}\n\n"
            elif msg["role"] == "assistant":
                conversation += f"Assistant: {msg['content']}\n\n"

        config = types.LiveConnectConfig(
            response_modalities=[types.Modality.TEXT],
            system_instruction=types.Content(
                parts=[types.Part(text=system_text)]
            ) if system_text else None,
            temperature=temperature,
        )

        full_response = ""
        try:
            async with client.aio.live.connect(
                model="gemini-3-flash-live",
                config=config,
            ) as session:
                await session.send(input=conversation.strip(), end_of_turn=True)
                async for response in session.receive():
                    if response.server_content:
                        model_turn = response.server_content.model_turn
                        if model_turn:
                            for part in model_turn.parts:
                                if part.text:
                                    full_response += part.text
                        # Check if turn is complete
                        if response.server_content.turn_complete:
                            break
        except Exception as e:
            return f"Live API error: {type(e).__name__}: {str(e)}"

        return full_response or "(empty response)"

    async def _run_orchestrated_chat(self, session, user_message, api_key, settings):
        """Smart orchestrated chat: router picks agents, agents write files."""
        agent_configs = []
        for aid in session["agent_ids"]:
            agent_data = self.agent_manager.get_agent(aid)
            if agent_data and agent_data.get("enabled", True):
                agent_configs.append(agent_data)

        if not agent_configs:
            await self._sys_msg(session, "No enabled agents.", "\u26a0\ufe0f", "#EF4444")
            return

        base_url = settings.get("base_url", "https://generativelanguage.googleapis.com/v1beta/openai/")
        # Use Live API for routing (unlimited RPM = free routing decisions)
        router_model = "gemini-3-flash-live"
        workspace = Path(session.get("workspace", WORKSPACE_DIR / session["id"]))
        workspace.mkdir(parents=True, exist_ok=True)

        # Build agent name list for the router
        agent_names = [ac["name"] for ac in agent_configs]
        agent_map = {ac["name"]: ac for ac in agent_configs}

        # Conversation history for context
        conv_history = [{"role": "user", "content": user_message}]
        max_rounds = session.get("max_rounds", 15)

        await self._sys_msg(session,
            f"\U0001f3ad Orchestrator started. Agents: {', '.join(agent_names)}. Workspace: {workspace}",
            "\U0001f3ad", "#8B5CF6")

        for round_num in range(max_rounds):
            # ── Step 1: Router decides who speaks next ──
            router_prompt = (
                "You are a team orchestrator. Based on the conversation so far, "
                "decide which team member should respond NEXT.\n\n"
                f"Team members: {', '.join(agent_names)}\n\n"
                "Rules:\n"
                "- Pick the MOST relevant agent for the current stage of work\n"
                "- If the task is done, respond with exactly: DONE\n"
                "- Respond with ONLY the agent name (exactly as listed) or DONE\n"
                "- No explanation, just the name\n"
            )
            router_messages = [
                {"role": "system", "content": router_prompt},
            ] + conv_history[-12:]

            try:
                next_agent_name = await self._call_llm(
                    api_key, base_url, router_model, router_messages,
                    temperature=0.1, max_tokens=50,
                )
                next_agent_name = next_agent_name.strip().strip('"').strip("'")
            except Exception as e:
                await self._sys_msg(session,
                    f"\u274c Router error: {type(e).__name__}: {str(e)}",
                    "\u26a0\ufe0f", "#EF4444")
                break

            # Check if done
            if "DONE" in next_agent_name.upper():
                await self._sys_msg(session,
                    f"\u2705 Task complete after {round_num + 1} rounds.",
                    "\u2705", "#10B981")
                break

            # Find the agent
            ac = agent_map.get(next_agent_name)
            if not ac:
                # Fuzzy match
                for name in agent_names:
                    if name.lower() in next_agent_name.lower() or next_agent_name.lower() in name.lower():
                        ac = agent_map[name]
                        break
                if not ac:
                    ac = agent_configs[round_num % len(agent_configs)]

            # Show routing decision
            await self._sys_msg(session,
                f"\U0001f4e2 Router: {ac['icon']} {ac['name']} speaks next (round {round_num + 1}/{max_rounds})",
                "\U0001f4e2", "#6366F1")

            # ── Step 2: Agent responds ──
            agent_model = ac.get("model", "gemini-2.5-flash")
            file_instructions = (
                "\n\n--- FILE WRITING ---\n"
                "You can write files to the project workspace.\n"
                f"Workspace path: {workspace}\n"
                "To create/write a file, use this exact format:\n"
                "<<<FILE: relative/path/to/file.ext>>>\n"
                "file content here\n"
                "<<<END_FILE>>>\n"
                "You can write multiple files in one response.\n"
                "--- END FILE WRITING ---\n"
            )
            agent_system = ac["system_prompt"] + file_instructions
            other_agents = [a["name"] for a in agent_configs if a["id"] != ac["id"]]
            if other_agents:
                agent_system += f"\nTeam members: {', '.join(other_agents)}. Collaborate with them."

            agent_messages = [
                {"role": "system", "content": agent_system},
            ] + conv_history[-12:]

            try:
                content = await self._call_llm(
                    api_key, base_url, agent_model, agent_messages,
                    temperature=ac.get("temperature", 0.7),
                    max_tokens=ac.get("max_tokens", 4096),
                )
            except Exception as e:
                content = f"\u274c Error: {type(e).__name__}: {str(e)}"

            # ── Step 3: Extract and write files ──
            files_written = await self._extract_and_write_files(session, workspace, content)

            # ── Step 4: Send agent message ──
            msg = {
                "role": "assistant",
                "sender": ac["name"],
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "icon": ac["icon"],
                "color": ac["color"],
            }
            session["messages"].append(msg)
            await self._emit(session["id"], msg)

            conv_history.append({"role": "assistant", "content": f"[{ac['name']}]: {content}"})

            # Show files written
            if files_written:
                file_list = "\n".join([f"\U0001f4c4 {f}" for f in files_written])
                await self._sys_msg(session,
                    f"\U0001f4be Files written to workspace:\n{file_list}",
                    "\U0001f4be", "#10B981")

            self._save()
            await asyncio.sleep(1.5)  # Rate limit spacing

        # Final summary
        ws_files = list(workspace.rglob("*"))
        ws_files = [f for f in ws_files if f.is_file()]
        if ws_files:
            file_list = "\n".join([f"  \U0001f4c4 {f.relative_to(workspace)}" for f in ws_files[:20]])
            await self._sys_msg(session,
                f"\U0001f4c2 Project workspace ({len(ws_files)} files):\n{file_list}\n\nPath: {workspace}",
                "\U0001f4c2", "#06B6D4")

    async def _extract_and_write_files(self, session, workspace: Path, content: str) -> list[str]:
        """Extract <<<FILE: path>>> ... <<<END_FILE>>> blocks and write them."""
        pattern = r'<<<FILE:\s*(.+?)>>>\n([\s\S]*?)<<<END_FILE>>>'
        matches = re.findall(pattern, content)
        written = []

        for filepath, file_content in matches:
            filepath = filepath.strip()
            # Security: prevent path traversal
            if ".." in filepath or filepath.startswith("/") or filepath.startswith("\\"):
                continue

            target = workspace / filepath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(file_content.strip(), encoding="utf-8")
            written.append(filepath)

        return written

    def clear_messages(self, session_id: str) -> bool:
        if session_id in self._sessions:
            self._sessions[session_id]["messages"] = []
            self._save()
            return True
        return False

    def get_workspace_files(self, session_id: str) -> list[dict]:
        session = self._sessions.get(session_id)
        if not session:
            return []
        workspace = Path(session.get("workspace", ""))
        if not workspace.exists():
            return []
        files = []
        for f in workspace.rglob("*"):
            if f.is_file():
                try:
                    content = f.read_text(encoding="utf-8")
                except Exception:
                    content = "(binary file)"
                files.append({
                    "path": str(f.relative_to(workspace)),
                    "full_path": str(f),
                    "size": f.stat().st_size,
                    "content": content[:5000],
                })
        return files
