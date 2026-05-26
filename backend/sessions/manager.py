"""
Session Manager — orchestrates multi-agent chat with smart routing,
file writing workspace, and code execution.
"""
import re
import asyncio
import subprocess
from typing import Optional, Callable
from pathlib import Path
from backend.config import SESSIONS_FILE, BASE_DIR, WORKSPACE_DIR, get_settings
from backend.agents.manager import AgentManager
from backend.models.registry import get_config_list
from backend.llm.provider import call_llm
from backend.base_manager import BaseManager

try:
    import autogen
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False



class SessionManager(BaseManager):
    MAX_HISTORY_MESSAGES = 12

    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self._sessions: dict[str, dict] = {}
        self._message_callback: Optional[Callable] = None
        super().__init__(SESSIONS_FILE)
        self._load()

    def _load(self):
        self._sessions = self._load_dict()

    def _save(self):
        self._save_dict(self._sessions)

    def set_message_callback(self, callback: Callable):
        self._message_callback = callback

    def list_sessions(self) -> list[dict]:
        return list(self._sessions.values())

    def get_session(self, session_id: str) -> Optional[dict]:
        return self._sessions.get(session_id)

    def create_session(self, data: dict) -> dict:
        session_id = self._generate_id()
        session = {
            "id": session_id,
            "name": data.get("name", f"Session {session_id}"),
            "agent_ids": data.get("agent_ids", []),
            "strategy": data.get("strategy", "auto"),
            "max_rounds": data.get("max_rounds", 15),
            "created_at": self._get_now_iso(),
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
        return self._delete_item(self._sessions, session_id)

    async def _emit(self, session_id: str, msg: dict):
        """Send message via WebSocket callback."""
        if self._message_callback:
            await self._message_callback(session_id, msg)

    async def _add_message(self, session: dict, role: str, sender: str, content: str, icon: str, color: str):
        """Helper to create, append, and emit a message."""
        msg = {
            "role": role,
            "sender": sender,
            "content": content,
            "timestamp": self._get_now_iso(),
            "icon": icon,
            "color": color,
        }
        session["messages"].append(msg)
        await self._emit(session["id"], msg)

    async def _sys_msg(self, session, text, icon="\u2139\ufe0f", color="#94A3B8"):
        """Add and emit a system message."""
        await self._add_message(session, "system", "System", text, icon, color)

    async def _error_msg(self, session, text):
        """Add and emit an error system message."""
        await self._sys_msg(session, text, "\u26a0\ufe0f", "#EF4444")

    async def run_chat(self, session_id: str, user_message: str):
        session = self._sessions.get(session_id)
        if not session:
            return

        settings = get_settings()
        from backend.config import _validate_config
        api_key = _validate_config().api_key.get_secret_value()

        session["status"] = "running"
        self._save()

        # Add user message
        await self._add_message(session, "user", "You", user_message, "\U0001f464", "#FFFFFF")

        try:
            if not api_key:
                await self._error_msg(session,
                    "\u274c API key not set! Go to Settings, paste your Google AI Studio key, click Save.")
                return

            await self._run_orchestrated_chat(session, user_message, api_key, settings)
        except Exception as e:
            await self._error_msg(session,
                f"\u274c Error: {type(e).__name__}: {str(e)}")
        finally:
            session["status"] = "idle"
            self._save()

    def _find_agent_by_name(self, name: str, agent_configs: list[dict]) -> Optional[dict]:
        """Find an agent by exact or fuzzy name match."""
        # Exact match
        if exact_match := next((ac for ac in agent_configs if ac["name"] == name), None):
            return exact_match

        # Fuzzy match
        name_lower = name.lower()
        return next(
            (ac for ac in agent_configs if ac["name"].lower() in name_lower or name_lower in ac["name"].lower()),
            None
        )

    async def _run_orchestrated_chat(self, session, user_message, api_key, settings):
        """Smart orchestrated chat: router picks agents, agents write files."""
        agent_configs = [
            agent_data for aid in session["agent_ids"]
            if (agent_data := self.agent_manager.get_agent(aid)) and agent_data.get("enabled", True)
        ]

        if not agent_configs:
            await self._error_msg(session, "No enabled agents.")
            return

        base_url = settings.get("base_url", "https://generativelanguage.googleapis.com/v1beta/openai/")
        # Use Live API for routing (unlimited RPM = free routing decisions)
        router_model = settings.get("router_model", "gemini-3-flash-live")
        workspace = Path(session.get("workspace", WORKSPACE_DIR / session["id"]))
        workspace.mkdir(parents=True, exist_ok=True)

        # Build agent name list for the router
        agent_names = [ac["name"] for ac in agent_configs]

        # Conversation history for context
        conv_history = [{"role": "user", "content": user_message}]
        max_rounds = session.get("max_rounds", 15)

        await self._sys_msg(session,
            f"\U0001f3ad Orchestrator started. Agents: {', '.join(agent_names)}. Workspace: {workspace}",
            "\U0001f3ad", "#8B5CF6")

        for round_num in range(max_rounds):
            # ── Step 1: Router decides who speaks next ──
            next_agent_name = await self._get_router_decision(
                session, agent_names, conv_history, api_key, base_url, router_model
            )
            if next_agent_name is None:
                break

            # Check if done
            if "DONE" in next_agent_name.upper():
                await self._sys_msg(session,
                    f"\u2705 Task complete after {round_num + 1} rounds.",
                    "\u2705", "#10B981")
                break

            # Find the agent
            ac = self._find_agent_by_name(next_agent_name, agent_configs)
            if not ac:
                ac = agent_configs[round_num % len(agent_configs)]

            # Show routing decision
            await self._sys_msg(session,
                f"\U0001f4e2 Router: {ac['icon']} {ac['name']} speaks next (round {round_num + 1}/{max_rounds})",
                "\U0001f4e2", "#6366F1")

            # ── Step 2: Agent responds ──
            content = await self._get_agent_response(
                ac, agent_configs, conv_history, workspace, settings, api_key, base_url
            )

            # ── Step 3: Extract and write files ──
            files_written = await self._extract_and_write_files(session, workspace, content)

            # ── Step 4: Send agent message ──
            await self._add_message(session, "assistant", ac["name"], content, ac["icon"], ac["color"])

            conv_history.append({"role": "assistant", "content": f"[{ac['name']}]: {content}"})

            # Show files written
            if files_written:
                file_list = "\n".join(f"\U0001f4c4 {f}" for f in files_written)
                await self._sys_msg(session,
                    f"\U0001f4be Files written to workspace:\n{file_list}",
                    "\U0001f4be", "#10B981")

            self._save()
            await asyncio.sleep(1.5)  # Rate limit spacing

        # Final summary
        ws_files = [f for f in workspace.rglob("*") if f.is_file()]
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
        if session := self._sessions.get(session_id):
            session["messages"] = []
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

        def _read_content(f: Path) -> str:
            try:
                return f.read_text(encoding="utf-8")[:5000]
            except Exception:
                return "(binary file)"

        return [
            {
                "path": str(f.relative_to(workspace)),
                "full_path": str(f),
                "size": f.stat().st_size,
                "content": _read_content(f),
            }
            for f in workspace.rglob("*")
            if f.is_file()
        ]

    async def _get_router_decision(self, session, agent_names, conv_history, api_key, base_url, router_model):
        """Helper to get the router's decision on the next agent."""
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
        ] + conv_history[-self.MAX_HISTORY_MESSAGES:]

        try:
            next_agent_name = await call_llm(
                api_key, base_url, router_model, router_messages,
                temperature=0.1, max_tokens=50,
            )
            return next_agent_name.strip().strip('"').strip("'")
        except Exception as e:
            await self._error_msg(session,
                f"\u274c Router error: {type(e).__name__}: {str(e)}")
            return None

    async def _get_agent_response(self, ac, agent_configs, conv_history, workspace, settings, api_key, base_url):
        """Helper to get the response from the selected agent."""
        agent_model = ac.get("model") or settings.get("default_model", "gemini-2.5-flash")
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
        ] + conv_history[-self.MAX_HISTORY_MESSAGES:]

        try:
            return await call_llm(
                api_key, base_url, agent_model, agent_messages,
                temperature=ac.get("temperature", 0.7),
                max_tokens=ac.get("max_tokens", 4096),
            )
        except Exception as e:
            return f"\u274c Error: {type(e).__name__}: {str(e)}"
